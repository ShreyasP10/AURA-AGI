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

    def listen_vad(
        lang="en",
        silence_ms=1500,
        max_s=25,
        min_voiced_s=0.4,
        energy_threshold=400,
    ):
        """Record until silence (energy VAD), then transcribe. Best accuracy, offline.

        Stops after `silence_ms` of quiet once `min_voiced_s` of speech heard;
        hard-caps at `max_s`. Returns transcribed text (may be "").
        """
        import audioop
        import time as _time

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
        chunk_s = 512 / 16000
        need_silent = max(1, int(silence_ms / 1000 / chunk_s))
        max_chunks = max(1, int(max_s / chunk_s))
        frames: list = []
        silent = 0
        voiced = 0
        print("Whisper listening... (speak now)")
        try:
            for _ in range(max_chunks):
                try:
                    data = stream.read(512, exception_on_overflow=False)
                except Exception:
                    continue
                frames.append(data)
                try:
                    energy = audioop.rms(data, 2)
                except Exception:
                    energy = energy_threshold + 1
                if energy >= energy_threshold:
                    voiced += 1
                    silent = 0
                else:
                    silent += 1
                if voiced * chunk_s >= min_voiced_s and silent >= need_silent:
                    break
        finally:
            try:
                stream.stop_stream()
                stream.close()
            except Exception:
                pass
            try:
                pa.terminate()
            except Exception:
                pass
        if not frames or voiced * chunk_s < min_voiced_s:
            return ""
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            wf = wave.open(f.name, "wb")
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(16000)
            wf.writeframes(b"".join(frames))
            wf.close()
            try:
                return transcribe_file(f.name, lang)
            finally:
                try:
                    os.remove(f.name)
                except Exception:
                    pass
except ImportError:

    def transcribe_file(*a, **k):
        return "[install faster-whisper: pip install faster-whisper]"

    def listen_offline(*a, **k):
        return "[install faster-whisper]"

    def listen_vad(*a, **k):
        return "[install faster-whisper]"


if __name__ == "__main__":
    print(listen_offline())
