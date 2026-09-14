"""
3. Voice Clone — ElevenLabs (clone your voice)
pip install elevenlabs
.env: ELEVENLABS_API_KEY=sk_...
1. Go to elevenlabs.io -> Voice Lab -> Add Voice -> Instant Voice Clone (upload 1min sample)
2. Copy voice_id -> set VOICE_ID in .env or pass to speak()
"""

import os
from dotenv import load_dotenv

load_dotenv()
try:
    from elevenlabs.client import ElevenLabs
    from elevenlabs import play as eleven_play

    def speak(text: str, voice_id: str = None):
        key = os.environ.get("ELEVENLABS_API_KEY")
        if not key:
            return "[set ELEVENLABS_API_KEY in .env]"
        vid = (
            voice_id or os.environ.get("ELEVENLABS_VOICE_ID") or "21m00Tcm4TlvDq8ikWAM"
        )  # Rachel default
        client = ElevenLabs(api_key=key)
        audio = client.text_to_speech.convert(
            voice_id=vid, text=text, model_id="eleven_multilingual_v2"
        )
        # play via pygame or eleven_play
        try:
            eleven_play(audio)
        except Exception:
            import tempfile

            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                for chunk in audio:
                    f.write(chunk)
                fname = f.name
            from playsound import playsound

            playsound(fname)
            os.remove(fname)
        return True
except ImportError:

    def speak(text, voice_id=None):
        return "[pip install elevenlabs]"


if __name__ == "__main__":
    speak("Hello, I am AURA, now with your cloned voice!")
