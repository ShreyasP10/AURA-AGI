import cv2


def realtime_vision(image_path: str = "ASSETS/captured_image.png") -> str:
    """
    Capture and save a real-time image from the default camera.

    Args:
        image_path (str): The path where the captured image will be saved.
                        Defaults to "captured_image.png".

    Returns:
        str: The path where the captured image is saved.
    """

    print("\033[92m" + "Turned on Realtime Vision. Capturing Image.\033[0m")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError(
            "Camera not available (index 0). Check permission / close other apps."
        )
    ret, frame = cap.read()
    cap.release()  # Release the camera resource
    cv2.destroyAllWindows()  # Close OpenCV windows
    if not ret or frame is None:
        raise RuntimeError("Failed to capture frame from camera.")
    import os

    os.makedirs(os.path.dirname(image_path) or ".", exist_ok=True)
    cv2.imwrite(image_path, frame)
    print("\033[92m" + "Image captured.....\033[0m")
    return image_path


if __name__ == "__main__":
    realtime_vision()
