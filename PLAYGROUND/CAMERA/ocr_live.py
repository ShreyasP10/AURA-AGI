"""
5. Live OCR — read text from camera/paper via vision
pip install pytesseract pillow
Requires Tesseract installed: https://github.com/UB-Mannheim/tesseract/wiki
+ fallback to deepInfra_VISION for cloud OCR
"""
import os

try:
    import cv2  # noqa: F401
except ImportError:
    cv2 = None

try:
    import pytesseract
    from PIL import Image

    def _resize(img, max_w=1200):
        w, h = img.size
        if w > max_w:
            r = max_w / w
            img = img.resize((max_w, int(h * r)))
        return img

    def ocr_pytesseract(image_path: str) -> str:
        return pytesseract.image_to_string(_resize(Image.open(image_path)))

    _OCR_AVAILABLE = True
except ImportError:

    def _resize(img, max_w=1200):
        return img

    def ocr_pytesseract(p):  # type: ignore
        return "[pip install pytesseract pillow]"

    _OCR_AVAILABLE = False


def ocr_vision_live(prompt="Read all text in this image accurately"):
    from PLAYGROUND.CAMERA import camera_vision
    from BRAIN.AI.VISION import deepInfra_VISION
    path = camera_vision.realtime_vision()
    try:
        # try local first, fallback to vision
        local = ocr_pytesseract(path)
        if local.strip() and len(local) > 10 and "[pip install" not in local:
            os.remove(path)
            return f"[Local OCR]\n{local}"
        text = deepInfra_VISION.generate(prompt, image_path=path)
        os.remove(path)
        return text
    except Exception as e:
        if os.path.exists(path):
            os.remove(path)
        return f"OCR failed: {e}"


if __name__ == "__main__":
    print(ocr_vision_live())
