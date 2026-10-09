from typing import Dict, Generator
import pyaudio
from vosk import Model, KaldiRecognizer
import ast

# Model load takes seconds (all the LOG lines) — cache per path so turns start instantly.
_model_cache: Dict[str, Model] = {}


def get_cached_model(model_path: str) -> Model:
    if model_path not in _model_cache:
        _model_cache[model_path] = Model(model_path)
    return _model_cache[model_path]


def speech_to_text(
    prints: bool = True,
    model_path: str = r"ASSETS\Vosk\vosk-model-small-en-us-0.15",
    device_index: int = -1,
) -> Generator[str, None, None]:
    """
    Asynchronously transcribes continuous speech into text using the Vosk library and PyAudio.

    This function initializes a Vosk speech-to-text model and a PyAudio stream, and continuously listens to the
    user's speech using the microphone. It yields the transcribed text in lowercase as it becomes available.

    Args:
        prints (bool): If True, prints the transcription results.
        model_path (str): The path to the Vosk model file.

    Yields:
        str: The transcribed text in lowercase.

    Note:
        The function uses the Vosk library for speech recognition and the PyAudio library for audio input.
        Both libraries must be installed for this function to work properly.

    Example Usage:
        >>> for speech in speech_to_text():
        ...     print(speech)
    """
    # Initialize Vosk model (cached after first turn)
    model = get_cached_model(model_path)
    recognizer = KaldiRecognizer(model, 16000)
    print("Model Initialized....")

    # Initialize PyAudio (explicit device_index wins, else AURA_MIC_INDEX env, else default)
    audio = pyaudio.PyAudio()
    import os

    mic_index = device_index
    if mic_index is None or mic_index < 0:
        try:
            mic_index = int(os.environ.get("AURA_MIC_INDEX", "-1"))
        except ValueError:
            mic_index = -1

    _open_kwargs = dict(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=8192,
    )
    if mic_index is not None and mic_index >= 0:
        _open_kwargs["input_device_index"] = mic_index
    stream = audio.open(**_open_kwargs)
    stream.start_stream()

    try:
        while True:
            data = stream.read(8192, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                try:
                    result_dict = ast.literal_eval(result)
                except Exception:
                    continue
                if "text" in result_dict:
                    if prints:
                        print("\rTranscript: " + result_dict["text"])
                    yield result_dict["text"].lower()
            else:
                if prints:
                    try:
                        print(
                            "\rSpeaking: " + recognizer.PartialResult().split('"')[-2],
                            end="",
                            flush=True,
                        )
                    except Exception as e:
                        print(f"[error {__file__}] {type(e).__name__}: {e}")
    finally:
        try:
            stream.stop_stream()
            stream.close()
            audio.terminate()
        except Exception as e:
            print(f"[error {__file__}] {type(e).__name__}: {e}")


if __name__ == "__main__":
    for speech in speech_to_text():
        if "stop" in speech:
            print(
                "Speech: ", speech
            )  # The actual printing is handled within the function now
            print("Broken....")
            break
