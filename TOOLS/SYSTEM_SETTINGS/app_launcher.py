"""
10. App Launcher — aura open <app>
Supports brave, chrome, vscode, spotify, notepad, explorer
"""
from functools import lru_cache
import subprocess, os, shutil
APPS={
    "brave": r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "vscode": r"C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "spotify": r"C:\Users\%USERNAME%\AppData\Roaming\Spotify\Spotify.exe",
    "notepad": "notepad.exe",
    "explorer": "explorer.exe",
    "calc": "calc.exe",
}
@lru_cache(maxsize=32)
def open_app(name: str):
    name=name.lower().strip()
    # fuzzy match
    for k, path in APPS.items():
        if k in name or name in k:
            full=os.path.expandvars(path)
            if os.path.exists(full) or shutil.which(full):
                subprocess.Popen([full] if os.path.exists(full) else [name], shell=True)
                return f"Opening {k}"
            else:
                try: subprocess.Popen([name], shell=True); return f"Opening {name} via PATH"
                except Exception as e: return f"Failed to open {k}: {e}"
    # fallback try directly
    try:
        subprocess.Popen([name], shell=True)
        return f"Opening {name}"
    except Exception as e:
        return f"App not found: {name} ({e})"

if __name__=="__main__":
    print(open_app("brave"))
