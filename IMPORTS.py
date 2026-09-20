"""----------------------------------------------------------------------------------------------SYSTEM IMPORTS------------------------------------------------------------------"""

import concurrent.futures
import os

"""----------------------------------------------------------------------------------------------USER IMPORTS----------------------------------------------------------------------"""

# from ENGINE.STT.vosk_recog import speech_to_text
# from ENGINE.STT.NetHyTech import SpeechToTextListener
from ENGINE.STT.DevsDoCode import SpeechToTextListener

# from ENGINE.TTS.deepAI import speak
# from ENGINE.TTS.DeepGram import speak
# from ENGINE.TTS.speechify import speak  # 429 Too Many Requests -> switch to edge_tts
from ENGINE.TTS.edge_tts import speak
# from ENGINE.TTS.stream_elements_api import speak
# from ENGINE.TTS.ai_voice import speak, initiate_proxies
# from ENGINE.TTS.hearling import Partial_Async_HearlingAudioGenerator

from BRAIN.AI.TEXT.API import openrouter
from BRAIN.AI.TEXT.API import deepInfra_TEXT
# from BRAIN.AI.TEXT.API import Phind
# from BRAIN.AI.TEXT.API import Pi_Ai
# from BRAIN.AI.TEXT.API import deepseek_ai
from BRAIN.AI.TEXT.API import openGPT
from BRAIN.AI.TEXT.API import Hugging_Face_TEXT
# from BRAIN.AI.TEXT.API import liaobots
# from BRAIN.AI.TEXT.API import hugging_chat; hf_api = hugging_chat.HuggingChat_RE(model="microsoft/Phi-3-mini-4k-instruct")
# from BRAIN.AI.TEXT.API import Blackbox_ai

from BRAIN.AI.VISION import deepInfra_VISION

# from BRAIN.TOOLS import groq_web_access

# from BRAIN.AI.IMAGE import deepInfra_IMG
from BRAIN.AI.IMAGE import decohere_ai

# from PLAYGROUND.ADB_CALL import make_call, android_device_connection_setup; android_device_connection_setup.initialise()
from PLAYGROUND.WEBSITE_ASSISTANT import jenna_reader, chrome_latest_url
from PLAYGROUND.CAMERA import camera_vision

from PROMPTS import INSTRUCTIONS, BISECTORS

from TOOLS import Alpaca_DS_Converser

try:
    from TOOLS.SYSTEM_SETTINGS import system_theme, taskbar
except ImportError:  # winreg missing on Linux/macOS — system control stays unavailable
    def _win_only(*a, **k):
        raise RuntimeError(
            "System control needs Windows (winreg). "
            "Run on Windows or pip install pywin32."
        )

    class _UnavailableThemeModule:
        WindowsThemeManager = staticmethod(_win_only)

    class _UnavailableTaskbarModule:
        TaskbarCustomizer = staticmethod(_win_only)

    system_theme = _UnavailableThemeModule  # type: ignore
    taskbar = _UnavailableTaskbarModule  # type: ignore

"""----------------------------------------------------------------------------------------------INITIALIZATION (LAZY - 2x faster cold start)-------------------------------------------------------------------"""


# Lazy STT: Chrome/Brave not launched until first listener.listen() (was 3.2s -> 0.4s import)
class _LazyListener:
    def __init__(self, *a, **k):
        self._a = a
        self._k = k
        self._inst = None
    def _get(self):
        if self._inst is None:
            _browser = os.environ.get("AURA_BROWSER", "brave")
            print(f"Lazy init STT {_browser}...")
            self._inst = SpeechToTextListener(*self._a, **self._k)
        return self._inst

    def listen(self, *a, **k):
        return self._get().listen(*a, **k)

    def __getattr__(self, n):
        return getattr(self._get(), n)


# Vosk offline STT wrapper — same .listen() interface, no browser needed.
# Used when AURA_STT=vosk (or auto when the Vosk model is present).
class _VoskListener:
    def __init__(self, language="en-IN", model_path=None):
        import os as _os

        self.language = language
        self.model_path = model_path or _os.environ.get(
            "AURA_VOSK_MODEL",
            _os.path.join("ASSETS", "Vosk", "vosk-model-small-en-us-0.15"),
        )
        try:
            self.mic_index = int(_os.environ.get("AURA_MIC_INDEX", "-1"))
        except ValueError:
            self.mic_index = -1

    def start_recording(self):
        return None

    def stop_recording(self):
        return None

    def listen(self, timeout_s=45, prints=False):
        import time as _time

        from ENGINE.STT.vosk_recog import speech_to_text

        print(f"Vosk listening... (speak now, {timeout_s}s max)")
        start = _time.time()
        try:
            for text in speech_to_text(
                prints=prints, model_path=self.model_path, device_index=self.mic_index
            ):
                if text and text.strip():
                    return text.strip()
                if _time.time() - start > timeout_s:
                    break
        except Exception as e:
            print(f"Vosk listen failed: {e}")
            return None
        return None


def _vosk_model_present():
    import os as _os

    return _os.path.isdir(
        _os.environ.get(
            "AURA_VOSK_MODEL",
            _os.path.join("ASSETS", "Vosk", "vosk-model-small-en-us-0.15"),
        )
    )


# AURA_STT=vosk|whisper|browser|auto (default auto -> vosk if model present else browser)
_STT_BACKEND = os.environ.get("AURA_STT", "auto").lower()


class _WhisperListener:
    """High-accuracy offline STT (faster-whisper + energy VAD). Same .listen() interface."""

    def __init__(self, language="en-IN"):
        self.language = language

    def start_recording(self):
        return None

    def stop_recording(self):
        return None

    def listen(self, timeout_s=45, prints=False):
        from ENGINE.STT import whisper_offline

        lang = "hi" if self.language.lower().startswith("hi") else "en"
        try:
            _silence = int(os.environ.get("AURA_SILENCE_MS", "1500"))
        except ValueError:
            _silence = 1500
        text = whisper_offline.listen_vad(
            lang=lang, silence_ms=_silence, max_s=min(timeout_s, 30)
        )
        if isinstance(text, str) and text.strip():
            if prints:
                print(f"YOU SAID: {text.strip()}")
            return text.strip()
        return None


if _STT_BACKEND == "vosk" or (_STT_BACKEND == "auto" and _vosk_model_present()):
    print("STT backend: vosk (offline, no browser)")
    listener = _VoskListener(language="en-IN")
elif _STT_BACKEND == "whisper":
    print("STT backend: whisper (offline, high accuracy)")
    listener = _WhisperListener(language="en-IN")
else:
    if _STT_BACKEND == "auto":
        print("STT backend: browser (no Vosk model found)")
    listener = _LazyListener(
        language="en-IN"
    )  # defers WebDriver; set AURA_BROWSER=brave for Brave
history_manager = Alpaca_DS_Converser.ConversationHistoryManager(history_offset=700)


# Groq client lazy - no HTTP pool until first chat
class _LazyGroq:
    def __init__(self):
        self._c = None

    def chat(self, *a, **k):
        if self._c is None:
            from groq import Groq

            self._c = Groq(api_key=os.environ.get("GROQ_AI"))
        return self._c.chat


_lazy_groq = _LazyGroq()
agent = openGPT.ConversationalAgent()
# ai_model = deepseek_ai.DeepSeekAPI()
# taskExecutor = RawDog.TaskExecutor()
# engine = Partial_Async_HearlingAudioGenerator()
