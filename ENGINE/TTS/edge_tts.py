import os
from playsound import playsound

def speak(text: str, voice: str = 'en-US-JennyNeural', subtitle_file: str = 'Subtitles_File.srt') -> None:
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
    # sanitize quotes for shell
    safe_text = text.replace('"', "'").replace("\n", " ")
    mp3_file = f"{voice}.mp3"
    # Build the edge-tts command string, including voice, text, and output media
    command = f'edge-tts --voice "{voice}" --text "{safe_text}" --write-media "{mp3_file}" --write-subtitles {subtitle_file}'

    # Execute the edge-tts command using the system shell
    ret = os.system(command)
    if ret != 0 or not os.path.exists(mp3_file):
        print(f"edge_tts failed (code {ret}), file missing: {mp3_file}")
        if os.path.exists(subtitle_file):
            try: os.remove(subtitle_file)
            except: pass
        return
    try:
        playsound(mp3_file)
    except Exception as e:
        print(f"playsound failed: {e} - trying pygame fallback")
        try:
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
    except:
        pass

if __name__ == "__main__": 
    speak("Thank you for watching! I hope you found this video informative and helpful. If you did, please give it a thumbs up and consider subscribing to my channel for more videos like this")
