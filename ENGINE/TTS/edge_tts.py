import os
import re
import subprocess
import threading
import uuid
from playsound import playsound

_tts_gen_lock = threading.Lock()


def _sanitize_for_tts(text: str) -> str:
    """Strip markdown/code/LaTeX/ASCII-art that makes edge-tts return NoAudioReceived."""
    t = text or ""
    # remove code fences
    t = re.sub(r"```.*?```", " ", t, flags=re.DOTALL)
    t = t.replace("```", " ")
    # latex \(...\) \[...\]
    t = re.sub(r"\\\(.*?\\\)", " ", t)
    t = re.sub(r"\\\[.*?\\\]", " ", t)
    # markdown bold/italic/headers/links
    t = re.sub(r"\*\*(.*?)\*\*", r"\1", t)
    t = re.sub(r"__(.*?)__", r"\1", t)
    t = re.sub(r"^#{1,6}\s*", "", t, flags=re.MULTILINE)
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    # ascii-art / code symbols-only lines
    lines = []
    for ln in t.splitlines():
        s = ln.strip()
        if not s:
            continue
        # skip lines with no alphanumeric (e.g. /\_/\ ( o.o ))
        if not re.search(r"[A-Za-z0-9]", s):
            continue
        # skip lines that are mostly symbols
        alnum = len(re.findall(r"[A-Za-z0-9]", s))
        if alnum < max(2, len(s) // 4):
            continue
        lines.append(s)
    t = " ".join(lines) if lines else ""
    if not t:
        return ""
    # musical notes / control chars from streamed deltas
    t = t.replace("♪", " ").replace("◙", " ").replace("`", " ")
    t = re.sub(r"\s+", " ", t).strip()
    return t[:500]  # edge-tts per-call cap to avoid throttle


def speak(
    text: str,
    voice: str = "en-US-JennyNeural",
    subtitle_file: str = "Subtitles_File.srt",
) -> None:
    """
    Function to convert text to speech using Edge TTS.

    Args:
        text (str): The text to be spoken.
        voice (str): The voice to use for speech synthesis. Defaults to "en-US-JennyNeural".
        subtitle_file (str): The path to the subtitle file. Defaults to "Subtitles_File.srt".

    Notes:
        This function utilizes the Edge TTS command line tool to convert text to speech.
        Users can choose from a variety of available voices for different accents and tones.
        Uncomment the corresponding line in the function to select the preferred voice.

    Available voices:
        - en-US-JennyNeural: Clear and professional-sounding American female voice
        - en-SG-LunaNeural: Friendly and approachable Singaporean female voice
        - en-AU-NatashaNeural: Warm and friendly Australian female voice
        - en-CA-ClaraNeural: Crisp and articulate Canadian female voice
        - en-CA-LiamNeural: Confident and professional Canadian male voice (currently selected)
    """

    if not text or not text.strip():
        print("edge_tts: empty text, skipping TTS")
        return
    text = _sanitize_for_tts(text)
    if not text or not re.search(r"[A-Za-z0-9]", text):
        print("edge_tts: unspeakable text (code/art only), skipping TTS")
        return
    # sanitize quotes for shell (use list args, no shell)
    safe_text = text.replace("\n", " ")

    unique_id = uuid.uuid4().hex
    mp3_file = f"{voice}_{unique_id}.mp3"
    subtitle_file = f"Subtitles_File_{unique_id}.srt"
    
    # Serialize generation: concurrent edge-tts calls get throttled -> NoAudioReceived
    with _tts_gen_lock:
        ret = 1
        for attempt in range(2):
            try:
                proc = subprocess.run(
                    ["edge-tts", "--voice", voice, "--text", safe_text,
                     "--write-media", mp3_file, "--write-subtitles", subtitle_file],
                    capture_output=True, text=True, timeout=60,
                )
                ret = proc.returncode
                if ret == 0 and os.path.exists(mp3_file):
                    break
                # quiet the noisy edge-tts traceback, show one line
                err = (proc.stderr or "").strip().splitlines()
                err_tail = err[-1] if err else "unknown error"
                print(f"edge_tts attempt {attempt+1} failed: {err_tail[:200]}")
            except subprocess.TimeoutExpired:
                print(f"edge_tts attempt {attempt+1} timeout")
                ret = 1
            except FileNotFoundError:
                print("edge_tts CLI not found: pip install edge-tts")
                return
            import time as _t
            if attempt == 0:
                _t.sleep(1.0)
    if ret != 0 or not os.path.exists(mp3_file):
        print(f"edge_tts failed, file missing: {mp3_file}")
        if os.path.exists(subtitle_file):
            try:
                os.remove(subtitle_file)
            except Exception:
                pass
        return

    # Use a global lock so sentences don't talk over each other
    if not hasattr(speak, "playback_lock"):
        speak.playback_lock = threading.Lock()
        
    with speak.playback_lock:
        try:
            playsound(mp3_file)
        except Exception:
            # Silently fallback to pygame if playsound fails
            try:
                os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
                import pygame
    
                pygame.mixer.init()
                pygame.mixer.music.load(mp3_file)
                pygame.mixer.music.play()
                import time
    
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                pygame.mixer.quit()
            except Exception as e2:
                print(f"pygame fallback also failed: {e2}")
        try:
            if os.path.exists(subtitle_file):
                os.remove(subtitle_file)
            if os.path.exists(mp3_file):
                os.remove(mp3_file)
        except Exception:
            pass


if __name__ == "__main__":
    speak(
        "Thank you for watching! I hope you found this video informative and helpful. If you did, please give it a thumbs up and consider subscribing to my channel for more videos like this"
    )
