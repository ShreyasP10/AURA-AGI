"""
11. File Finder — aura find my resume / aura find <filename>
Searches user directory with Groq summarizer
"""

import os
import pathlib
import fnmatch
from dotenv import load_dotenv

load_dotenv()
try:
    from groq import Groq

    _g = Groq(api_key=os.environ.get("GROQ_AI")) if os.environ.get("GROQ_AI") else None
except Exception:
    _g = None


def find_files(query: str, root=None, max_results=10):
    root = root or os.path.expanduser("~")
    # extract filename from "find my resume" -> resume
    q = query.lower().replace("find", "").replace("my", "").strip() or query
    matches = []
    for dirpath, _, files in os.walk(root):
        if dirpath.count(os.sep) - root.count(os.sep) > 4:
            continue  # limit depth 4
        # skip hidden/system
        if any(x.startswith(".") for x in pathlib.Path(dirpath).parts[-1:]):
            continue
        for f in files:
            if fnmatch.fnmatch(f.lower(), f"*{q.lower()}*"):
                matches.append(os.path.join(dirpath, f))
                if len(matches) >= max_results:
                    break
        if len(matches) >= max_results:
            break
        # limit depth for speed: skip long walks after 5000 files
        if len(matches) > 100:
            break
    return matches[:max_results]


def find_and_summarize(query: str):
    files = find_files(query)
    if not files:
        return f"No files found for '{query}'"
    if _g:
        try:
            prompt = (
                f"User query: find {query}\nFound files:\n"
                + "\n".join(files[:5])
                + "\nSummarize in one line."
            )
            r = _g.chat.completions.create(
                model=os.environ.get("GROQ_MODEL", "llama-3.1-8b-instant"),
                messages=[{"role": "user", "content": prompt}],
                max_tokens=60,
            )
            summary = r.choices[0].message.content
            return summary + "\n\n" + "\n".join(files)
        except Exception as e:
            return "\n".join(files) + f"\n(Groq fail {e})"
    return "\n".join(files)


if __name__ == "__main__":
    print(find_and_summarize("resume"))
