"""
2. Offline Whisper — faster-whisper (no internet, local)
pip install faster-whisper
Uses small model quantized, 4x faster than openai whisper
"""

import os
import tempfile

try:
    from faster_whisper import WhisperModel

    _model = None

    def get_model(size="small"):
        global _model
        if _model is None:
            # download on first use: small, base, tiny
            _model = WhisperModel(size, device="cpu", compute_type="int8")
        return _model

    def transcribe_file(path: str, lang="en"):
        m = get_model()
        segs, _ = m.transcribe(path, language=lang, beam_size=5)
        return " ".join([s.text for s in segs]).strip()

    def listen_offline(duration=5, lang="en"):
        import pyaudio
        import wave

        pa = pyaudio.PyAudio()
        stream = pa.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=512,
        )
        print(f"Whisper offline listening {duration}s...")
        frames = []
        for _ in range(int(16000 / 512 * duration)):
            frames.append(stream.read(512))
        stream.stop_stream()
        stream.close()
        pa.terminate()
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            wf = wave.open(f.name, "wb")
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(16000)
            wf.writeframes(b"".join(frames))
            wf.close()
            text = transcribe_file(f.name, lang)
            os.remove(f.name)
            return text
except ImportError:

    def transcribe_file(*a, **k):
        return "[install faster-whisper: pip install faster-whisper]"

    def listen_offline(*a, **k):
        return "[install faster-whisper]"


if __name__ == "__main__":
    print(listen_offline())
