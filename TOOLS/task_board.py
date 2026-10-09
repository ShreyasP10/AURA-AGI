"""
12. Task Board — Kanban like Notes App
Syntax: !high / !medium / !low, @YYYY-MM-DD, #tag
Stored in ~/.aura/tasks.json
"""

import json
import os
import re
from datetime import datetime

TASK_PATH = os.path.expanduser("~/.aura/tasks.json")
os.makedirs(os.path.dirname(TASK_PATH), exist_ok=True)


def parse_task(raw: str):
    prio = re.search(r"!(high|medium|low)", raw, re.I)
    due = re.search(r"@(\d{4}-\d{2}-\d{2})", raw)
    tags = re.findall(r"#(\w+)", raw)
    text = re.sub(r"!(high|medium|low)|@\d{4}-\d{2}-\d{2}|#\w+", "", raw).strip()
    return {
        "text": text or raw,
        "priority": (prio.group(1).lower() if prio else "none"),
        "due": (due.group(1) if due else None),
        "tags": tags,
        "done": False,
        "star": False,
        "ts": datetime.now().isoformat(),
    }


def add_task(raw: str):
    tasks = load_tasks()
    tasks.append(parse_task(raw))
    save_tasks(tasks)
    return tasks[-1]


def load_tasks():
    if not os.path.exists(TASK_PATH):
        return []
    try:
        with open(TASK_PATH) as _f:
            return json.load(_f)
    except Exception:
        return []


def save_tasks(tasks):
    # auto-sort high->low
    order = {"high": 0, "medium": 1, "low": 2, "none": 3}
    tasks.sort(key=lambda x: order.get(x.get("priority", "none"), 3))
    # Atomic write: crash mid-save no longer truncates the task file
    import os as _os
    import tempfile as _tf

    _dir = _os.path.dirname(TASK_PATH) or "."
    _fd, _tmp = _tf.mkstemp(dir=_dir, suffix=".tmp")
    try:
        with _os.fdopen(_fd, "w") as _f:
            json.dump(tasks, _f, indent=2)
        _os.replace(_tmp, TASK_PATH)
    except Exception:
        try:
            _os.remove(_tmp)
        except Exception as e:
            print(f"[error {__file__}] {type(e).__name__}: {e}")
        raise


def list_tasks(filter_tag=None, search=None):
    tasks = load_tasks()
    if filter_tag:
        tasks = [t for t in tasks if filter_tag in t.get("tags", [])]
    if search:
        tasks = [t for t in tasks if search.lower() in t["text"].lower()]
    return tasks


def toggle_done(idx: int):
    tasks = load_tasks()
    if 0 <= idx < len(tasks):
        tasks[idx]["done"] = not tasks[idx]["done"]
        save_tasks(tasks)
    return tasks


if __name__ == "__main__":
    print(add_task("Finish AURA docs !high @2026-09-10 #work"))
    print(list_tasks())
