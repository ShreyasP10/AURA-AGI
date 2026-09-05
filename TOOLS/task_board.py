"""
12. Task Board — Kanban like Notes App
Syntax: !high / !medium / !low, @YYYY-MM-DD, #tag
Stored in ~/.aura/tasks.json
"""
import json, os, re, pathlib
from datetime import datetime

TASK_PATH=os.path.expanduser("~/.aura/tasks.json")
os.makedirs(os.path.dirname(TASK_PATH), exist_ok=True)

def parse_task(raw: str):
    prio=re.search(r"!(high|medium|low)", raw, re.I)
    due=re.search(r"@(\d{4}-\d{2}-\d{2})", raw)
    tags=re.findall(r"#(\w+)", raw)
    text=re.sub(r"!(high|medium|low)|@\d{4}-\d{2}-\d{2}|#\w+", "", raw).strip()
    return {"text":text or raw, "priority":(prio.group(1).lower() if prio else "none"), "due":(due.group(1) if due else None), "tags":tags, "done":False, "star":False, "ts":datetime.now().isoformat()}

def add_task(raw: str):
    tasks=load_tasks()
    tasks.append(parse_task(raw))
    save_tasks(tasks)
    return tasks[-1]

def load_tasks():
    if not os.path.exists(TASK_PATH): return []
    try: return json.load(open(TASK_PATH))
    except: return []

def save_tasks(tasks):
    # auto-sort high->low
    order={"high":0,"medium":1,"low":2,"none":3}
    tasks.sort(key=lambda x: order.get(x.get("priority","none"),3))
    json.dump(tasks, open(TASK_PATH,"w"), indent=2)

def list_tasks(filter_tag=None, search=None):
    tasks=load_tasks()
    if filter_tag: tasks=[t for t in tasks if filter_tag in t.get("tags",[])]
    if search: tasks=[t for t in tasks if search.lower() in t["text"].lower()]
    return tasks

def toggle_done(idx: int):
    tasks=load_tasks()
    if 0<=idx<len(tasks): tasks[idx]["done"]=not tasks[idx]["done"]; save_tasks(tasks)
    return tasks

if __name__=="__main__":
    print(add_task("Finish AURA docs !high @2026-09-10 #work"))
    print(list_tasks())
