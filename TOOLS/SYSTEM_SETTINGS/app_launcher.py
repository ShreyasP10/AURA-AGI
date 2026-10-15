"""
10. App Launcher — aura open <app>
Supports brave, chrome, vscode, spotify, notepad, explorer
"""

import subprocess
import os
import shutil

APPS = {
    "brave": r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "vscode": r"C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "spotify": r"C:\Users\%USERNAME%\AppData\Roaming\Spotify\Spotify.exe",
    "notepad": "notepad.exe",
    "explorer": "explorer.exe",
    "calc": "calc.exe",
}


def open_app(name: str):
    name = name.lower().strip()
    # Allowlist: only known app keys or bare executable names (no shell -> no injection
    # via voice input like "aura open x; rm -rf").
    # fuzzy match
    for k, path in APPS.items():
        if k in name or name in k:
            full = os.path.expandvars(path)
            if os.path.exists(full) or shutil.which(full):
                subprocess.Popen(
                    [full] if os.path.exists(full) else [k], shell=False
                )
                return f"Opening {k}"
            else:
                return f"Failed to open {k}: not installed"
    # fallback: bare executable name only (letters, digits, dot, dash, underscore)
    import re as _re

    m = _re.search(r"([a-z0-9][a-z0-9._-]*\.?(?:exe)?)", name)
    if m:
        try:
            subprocess.Popen([m.group(1)], shell=False)
            return f"Opening {m.group(1)}"
        except Exception as e:
            return f"App not found: {m.group(1)} ({e})"
    return f"App not found: {name}"


if __name__ == "__main__":
    print(open_app("brave"))
