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
    return t[:2000]  # edge-tts per-call cap to avoid throttle


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

    def _synth_in_process() -> bool:
        """In-process edge-tts (no CLI spawn ~1s overhead). Returns True on audio saved."""
        import asyncio

        async def _run():
            import edge_tts as _et

            comm = _et.Communicate(safe_text, voice)
            subs: list[str] = []
            async for chunk in comm.stream():
                if chunk["type"] == "audio":
                    with open(mp3_file, "ab") as f:
                        f.write(chunk["data"])
                elif chunk["type"] == "WordBoundary":
                    subs.append(f"{chunk.get('start',0)} --> {chunk.get('end',0)}\n{chunk.get('text','')}\n\n")
            if subs:
                with open(subtitle_file, "w", encoding="utf-8") as f:
                    f.writelines(f"{i}\n{s}" for i, s in enumerate(subs, 1))
            return os.path.exists(mp3_file) and os.path.getsize(mp3_file) > 0

        try:
            if os.path.exists(mp3_file):
                os.remove(mp3_file)
        except Exception:
            pass
        try:
            return asyncio.run(_run())
        except Exception as e:
            print(f"edge_tts in-process failed: {type(e).__name__}: {str(e)[:150]}")
            return False

    def _synth_cli() -> bool:
        try:
            proc = subprocess.run(
                ["edge-tts", "--voice", voice, "--text", safe_text,
                 "--write-media", mp3_file, "--write-subtitles", subtitle_file],
                capture_output=True, text=True, timeout=60,
            )
            if proc.returncode == 0 and os.path.exists(mp3_file):
                return True
            err = (proc.stderr or "").strip().splitlines()
            print(f"edge_tts CLI failed: {(err[-1] if err else 'unknown')[:200]}")
            return False
        except subprocess.TimeoutExpired:
            print("edge_tts CLI timeout")
            return False
        except FileNotFoundError:
            print("edge_tts CLI not found: pip install edge-tts")
            return False

    # Serialize generation: concurrent calls get throttled -> NoAudioReceived
    ok = False
    with _tts_gen_lock:
        for attempt in range(2):
            ok = _synth_in_process() or _synth_cli()
            if ok:
                break
            import time as _t
            if attempt == 0:
                _t.sleep(1.0)
    if not ok or not os.path.exists(mp3_file):
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
