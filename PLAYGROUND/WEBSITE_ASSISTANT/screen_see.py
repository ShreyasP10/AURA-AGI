"""
7. Screen See — capture screen + vision answer "what's on my screen?"
pip install mss pillow opencv-python
"""

import os

try:
    import mss
    import mss.tools
    from PIL import Image

    def capture_screen(path="ASSETS/screen_capture.png"):
        with mss.mss() as sct:
            mon = sct.monitors[1]
            shot = sct.grab(mon)
            img = Image.frombytes("RGB", shot.size, shot.bgra, "raw", "BGRX")
            # optimize: resize to 1024w + JPEG 70% (3x smaller, 2x faster upload to Vision)
            if img.width > 1024:
                r = 1024 / img.width
                img = img.resize((1024, int(img.height * r)))
            img.save(path, "JPEG", quality=70, optimize=True)
            return path
except ImportError:

    def capture_screen(p="ASSETS/screen_capture.png"):
        # fallback via pyautogui
        try:
            import pyautogui

            pyautogui.screenshot(p)
            return p
        except Exception:
            return "[pip install mss]"


def see_screen(prompt="Describe what's on my screen and answer the user query"):
    from BRAIN.AI.VISION import deepInfra_VISION

    path = capture_screen()
    if "pip install" in path:
        return path
    try:
        ans = deepInfra_VISION.generate(prompt, image_path=path)
        os.remove(path)
        return ans
    except Exception as e:
        if os.path.exists(path):
            os.remove(path)
        return f"Screen see failed: {e}"


if __name__ == "__main__":
    print(see_screen("Summarize my screen"))
