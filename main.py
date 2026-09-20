# ██████╗   ███████╗ ██╗    ██╗ ███████╗            ██████╗    ██████╗             ██████╗   ██████╗    ██████╗   ███████╗
# ██╔══██╗ ██╔════╝ ██║    ██║ ██╔════╝            ██╔══██╗ ██╔═══██╗          ██╔════╝ ██╔═══██╗ ██╔══██╗ ██╔════╝
# ██║    ██║ █████╗     ██║    ██║ ███████╗            ██║    ██║ ██║      ██║         ██║          ██║      ██║ ██║    ██║ █████╗
# ██║    ██║ ██╔══╝    ╚██╗  ██╔╝ ╚════██║           ██║    ██║ ██║      ██║         ██║          ██║      ██║ ██║    ██║ ██╔══╝
# ██████╔╝ ███████╗  ╚████╔╝  ███████║            ██████╔╝╚██████╔╝          ╚██████╗ ╚██████╔╝  ██████╔╝ ███████╗
# ╚═════╝  ╚══════╝    ╚═══╝     ╚══════╝            ╚═════╝    ╚═════╝             ╚═════╝   ╚═════╝    ╚═════╝   ╚══════╝

#  Made With 💓 By - Shreyas Pawar (AURA-AGI)
#  YouTube Channel: https://www.youtube.com/@AURA-Team

(
    """"""
    """"""
    """"""
    """"""
    """"""
    """"""
    """"""
    """"""
    """"""
    """""

      - Support: https://buymeacoffee.com/AURA-Team
      - Patreon: https://patreon.com/AURA-Team

"""
    """"""
    """"""
    """"""
    """"""
    """"""
    """"""
    """"""
    """"""
    """"""
    ""
)

#  For any questions or concerns, reach out to us via our social media handles.
#  Our top choice for contact is Telegram: https://t.me/AURA-Team
#  You can also find us on other platforms listed above. We're here to help!

#  - YouTube Channel: https://www.youtube.com/@AURA-Team
#  - Telegram Group: https://t.me/AURA-Team
#  - Discord Server: https://discord.gg/ehwfVtsAts
#  - Instagram:
#    - Personal: https://www.instagram.com/Shreyas.shades_/
#    - Channel: https://www.instagram.com/AURA-Team_/

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""

    - Support: https://buymeacoffee.com/AURA-Team
    - Patreon: https://patreon.com/AURA-Team

""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
#  ------------------------------------------------------------------------------
#  Dive into the world of coding with AURA Team - where passion meets programming!
#  Make sure to hit that Subscribe button to stay tuned for exciting content!

#  Pro Tip: For optimal performance and a seamless experience, we recommend using
#  the default library versions demonstrated in this demo. Your coding journey just
#  got even better! Happy coding!
#  ----------------------------------------------------------------------------

from IMPORTS import (
    os,
    concurrent,
    speak,
    openrouter,
    deepInfra_TEXT,
    Hugging_Face_TEXT,
    deepInfra_VISION,
    decohere_ai,
    jenna_reader,
    chrome_latest_url,
    camera_vision,
    INSTRUCTIONS,
    BISECTORS,
    system_theme,
    taskbar,
    listener,
    history_manager,
)
import queue as _queue
import threading as _threading
import time as _time

# Realtime TTS: ordered queue + single playback worker (no overlap garble, preserves order)
_tts_queue: _queue.Queue = _queue.Queue()
_stop_tts = _threading.Event()


def _tts_worker():
    while True:
        try:
            _txt = _tts_queue.get()
            _stop_tts.clear()
            try:
                if not _stop_tts.is_set():
                    try:
                        listener.stop_recording()
                    except Exception:
                        pass
                    speak(_txt)
            except Exception as _e:
                print(f"TTS worker fail: {_e}")
            finally:
                try:
                    # only restart mic if queue is empty, so we don't start/stop rapidly
                    if _tts_queue.empty():
                        listener.start_recording()
                except Exception:
                    pass
                _tts_queue.task_done()
        except Exception:
            pass


_threading.Thread(target=_tts_worker, daemon=True).start()


def _speak_fast(text: str):
    """Non-blocking ordered speak; drops unspeakable/code-only chunks instantly."""
    if os.environ.get("AURA_VOICE", "1") == "0":
        return  # text-only mode: no TTS delay at all
    if not text or not text.strip():
        return
    try:
        _tts_queue.put_nowait(text.strip())
    except Exception:
        pass


def _stop_speaking():
    """Say 'stop' -> clear pending speech + halt current playback immediately."""
    _stop_tts.set()
    try:
        listener.stop_recording()
    except Exception:
        pass
    try:
        while not _tts_queue.empty():
            try:
                _tts_queue.get_nowait()
                # Balanced: each drained item had exactly one put(), and the
                # worker's in-flight item gets its own task_done() in finally.
                # Without this, unfinished_tasks inflates and any future join() hangs.
                try:
                    _tts_queue.task_done()
                except ValueError:
                    pass  # counter already balanced; never crash stop
            except Exception:
                break
    except Exception:
        pass
    try:
        import pygame

        try:
            pygame.mixer.music.stop()
        except Exception:
            pass
        try:
            pygame.mixer.quit()
        except Exception:
            pass
    except Exception:
        pass


_STOP_WORDS = (
    "aura stop",
    "aura stop speaking",
    "aura quiet",
    "aura enough",
    "aura cancel",
    "aura shut up",
)

# Instant replies: skip Groq round-trip (~1s) for common greetings
_FAST_REPLIES = {
    "hello": "Hello! How can I help you today?",
    "hi": "Hi there! How can I help?",
    "hey": "Hey! What can I do for you?",
    "how are you": "I'm doing great! How can I help you today?",
    "thank you": "You're welcome!",
    "thanks": "You're welcome!",
    "bye": "Goodbye! Talk soon.",
}
_AURA_FAST = os.environ.get("AURA_FAST", "1") == "1"  # 1=realtime mode


# --- 12 new features (1-12) imports (isolated so one broken file doesn't disable all) ---
def _optional_import(importer, fallback):
    try:
        return importer()
    except Exception as _e:
        print(f"Feature import warning: {_e}")
        return fallback


def _fallback(*a, **k):
    print("Feature not available")
    return ""


open_app = _optional_import(
    lambda: __import__(
        "TOOLS.SYSTEM_SETTINGS.app_launcher", fromlist=["open_app"]
    ).open_app,
    _fallback,
)
find_and_summarize = _optional_import(
    lambda: __import__(
        "TOOLS.file_finder", fromlist=["find_and_summarize"]
    ).find_and_summarize,
    _fallback,
)
try:
    from TOOLS.task_board import add_task, list_tasks
except Exception as _e:
    print(f"Feature import warning: {_e}")
    add_task = list_tasks = _fallback
try:
    from BRAIN.TOOLS.emotion import detect_emotion, adapt_prompt
except Exception as _e:
    print(f"Feature import warning: {_e}")

    def detect_emotion(t):
        return "neutral"

    def adapt_prompt(b, e):
        return b


try:
    from PLAYGROUND.CAMERA.ocr_live import ocr_vision_live
except Exception as _e:
    print(f"Feature import warning: {_e}")
    ocr_vision_live = _fallback
try:
    from PLAYGROUND.WEBSITE_ASSISTANT.screen_see import see_screen
except Exception as _e:
    print(f"Feature import warning: {_e}")
    see_screen = _fallback

emo = "neutral"

# Opencode-style terminal UI (rich) + hybrid voice+type
try:
    from rich.console import Console as _Console
    from rich.panel import Panel as _Panel
    from rich.markdown import Markdown as _Markdown
    from rich.prompt import Prompt as _Prompt

    _console = _Console()
    _USE_RICH = True
except ImportError:
    _console = None
    _USE_RICH = False


def _ui_print_ai(text: str):
    if _USE_RICH and _console:
        try:
            _console.print(
                _Panel(_Markdown(text), title="AURA", border_style="cyan", expand=False)
            )
            return
        except BaseException:
            pass
    print(f"\n\033[92mAURA >> {text}\033[0m\n")


def _ui_print_sys(text: str):
    if _USE_RICH and _console:
        try:
            _console.print(f"[dim]{text}[/dim]")
            return
        except BaseException:
            pass
    print(text)


def _get_input_hybrid() -> str | None:
    """Each turn: type directly, or press Enter empty / type '/voice' for mic. Voice timeout falls back to typing."""
    _mode = os.environ.get("AURA_TEXT_MODE", "0")
    _prompt = "YOU (type, Enter=voice, /voice=mic, /quit=exit)"
    if _mode == "1":
        try:
            if _USE_RICH and _console:
                return (
                    _Prompt.ask(f"\n[bold green]{_prompt}[/bold green]").strip()
                    or "aura hello"
                )
            return input(f"\n{_prompt}: ").strip() or "aura hello"
        except (EOFError, KeyboardInterrupt):
            return None
    # hybrid: typed line wins; empty or /voice -> mic with timeout
    try:
        if _USE_RICH and _console:
            typed = _Prompt.ask(
                f"\n[bold green]{_prompt}[/bold green]", default=""
            ).strip()
        else:
            typed = input(f"\n{_prompt} [Enter=voice]: ").strip()
    except (EOFError, KeyboardInterrupt):
        return None
    if typed.lower() in ("/quit", "/exit", "quit()", "exit()"):
        return None
    if typed and typed != "/voice":
        return typed
    # voice path
    try:
        _ui_print_sys("🎤 Listening... (speak now, 45s max, Ctrl+C for typing)")
        speech = listener.listen(timeout_s=45)
        if speech and speech.strip():
            _ui_print_sys(f"YOU SAID: {speech.strip()}")
            return speech.strip()
        _ui_print_sys("No speech heard — type instead.")
    except KeyboardInterrupt:
        _ui_print_sys("Mic cancelled — type instead.")
    except Exception as e:
        _ui_print_sys(f"STT failed ({type(e).__name__}: {str(e)[:200]}). Type instead.")
    try:
        if _USE_RICH and _console:
            return (
                _Prompt.ask("[bold green]YOU (type)[/bold green]").strip()
                or "aura hello"
            )
        return input("YOU (type 'aura hello'): ").strip() or "aura hello"
    except (EOFError, KeyboardInterrupt):
        return None


if _USE_RICH and _console:
    _console.print(
        _Panel.fit(
            "AURA-AGI — voice + text. Type, or Enter for mic. `stop` halts speech.",
            title="AURA ready",
            border_style="green",
        )
    )
else:
    print(
        "AURA ready. Type, or Enter for mic. AURA_BROWSER=brave|chrome, AURA_HEADLESS=0 headed, AURA_TEXT_MODE=1 keyboard-only."
    )
while True:
    speech = _get_input_hybrid()
    if speech is None:
        _ui_print_sys("Bye!")
        break

    low = speech.lower().strip()
    # STOP: interrupt immediately, no LLM call — works with/without wakeword
    if low in _STOP_WORDS:
        _stop_speaking()
        print("Stopped.")
        continue
    is_wake = low.startswith("aura") or low.endswith("aura")
    if is_wake:
        if low.startswith("aura"):
            speech = speech[len("aura") :].strip()
        elif low.endswith("aura"):
            speech = speech[: -len("aura")].strip()
        print("Updated Speech:", speech)
        # stop after wake strip too: "aura stop speaking"
        if speech.lower().strip() in _STOP_WORDS:
            _stop_speaking()
            print("Stopped.")
            continue
        # --- Optimized fast local intents (zero LLM cost, <10ms) ---
        low2 = speech.lower()
        if _AURA_FAST:
            _fast = _FAST_REPLIES.get(low2.strip())
            if _fast:
                _ui_print_ai(_fast)
                _speak_fast(_fast)
                try:
                    history_manager.update_file(speech, _fast)
                except Exception:
                    pass
                continue
        # cache lower check once
        if low2.startswith("open ") or (
            "open " in low2
            and any(
                x in low2
                for x in [
                    "brave",
                    "chrome",
                    "vscode",
                    "spotify",
                    "notepad",
                    "calculator",
                ]
            )
        ):
            try:
                res = open_app(speech)
                print("AppLauncher>>", res)
                _speak_fast(res)
                continue
            except Exception as e:
                print(f"App launcher fail {e}")
        if low2.startswith("find ") or "find file" in low2 or "search file" in low2:
            try:
                res = find_and_summarize(speech)
                print("FileFinder>>", res)
                _speak_fast(res[:300])
                continue
            except Exception as e:
                print(f"Finder fail {e}")
        if (
            low2.startswith("task ")
            or low2.startswith("add task")
            or "list tasks" in low2
            or "my tasks" in low2
        ):
            try:
                if "list" in low2 or "show" in low2:
                    tasks = list_tasks()
                    res = (
                        "\n".join(
                            [
                                f"{i + 1}. {t['text']} !{t['priority']}"
                                for i, t in enumerate(tasks[:5])
                            ]
                        )
                        or "No tasks"
                    )
                else:
                    t = add_task(speech)
                    res = f"Task added: {t['text']}"
                print("TaskBoard>>", res)
                _speak_fast(res)
                continue
            except Exception as e:
                print(f"Task fail {e}")
        if any(k in low2 for k in ["read text", "ocr"]):
            try:
                res = ocr_vision_live(speech)
                print("OCR>>", res[:80])
                _speak_fast(res[:400])
                continue
            except Exception as e:
                print(f"OCR fail {e}")
        if any(k in low2 for k in ["on my screen", "screen see"]):
            try:
                res = see_screen(speech)
                print("ScreenSee>>", res[:80])
                _speak_fast(res[:400])
                continue
            except Exception as e:
                print(f"ScreenSee fail {e}")

        # OPTIMIZED: single executor reuse vs 3 separate (was 3x ThreadPool per wake = 6 executors leaked)
        _classifier_prompt = getattr(
            BISECTORS,
            "complex_task_classifier_v6",
            BISECTORS.complex_task_classifier_v5,
        )
        _safe_speech = f"<<BEGIN_CLASSIFICATION_INPUT>>\n{speech[:500]}\n<<END_CLASSIFICATION_INPUT>>\nClassify ONLY the text between the tags above."
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
            response_img_or_text = ex.submit(
                deepInfra_TEXT.generate,
                [{"role": "user", "content": _safe_speech}],
                system_prompt=BISECTORS.image_requests_v3,
            )
            response_classifier = ex.submit(
                deepInfra_TEXT.generate,
                [{"role": "user", "content": _safe_speech}],
                system_prompt=_classifier_prompt,
                stream=False,
            )
            default_response = ex.submit(
                deepInfra_TEXT.generate,
                history_manager.history,
                system_prompt=adapt_prompt(INSTRUCTIONS.human_response_v3_AVA, emo),
                stream=False,
            )
            concurrent.futures.wait(
                [response_img_or_text, response_classifier, default_response]
            )
        print(
            "Response Classifier >> ",
            "\033[91m" + str(response_classifier.result()) + "\033[0m",
        )
        print(
            "Image or Text Classifier >> ",
            "\033[91m" + str(response_img_or_text.result()) + "\033[0m",
        )

        _img_res = response_img_or_text.result() or ""
        _cls_res = (response_classifier.result() or "").lower()
        _def_res = default_response.result() or "Sorry, I could not think of a reply."

        _img_text = (_img_res or "").strip().lower()
        _is_image_req = _img_text in ("yes", "response: yes") or _img_text.endswith("response: yes")

        if _is_image_req:
            _speak_fast("Sure Sir, Generating Your Image")
            try:
                ok, msg = decohere_ai.generate(speech)
                print("Image>>", ok, msg)
                _speak_fast("Image ready" if ok else f"Image failed: {msg}")
            except Exception as e:
                print(f"Image fail {e}")
                _speak_fast("Image generation failed")
            continue

        elif all(x in _cls_res for x in ("vision", "website", "call", "youtube")):
            print("\033[91mConfused with Classification. Using Default Response\033[0m")
            _speak_fast(_def_res)

        elif "system control" in _cls_res:
            _speak_fast("Sure Sir. Setting the Required Settings")
            try:
                speech_lower = speech.lower()
                if "dark" in speech_lower or "light" in speech_lower:
                    theme = 0 if "dark" in speech_lower else 1
                    system_theme.WindowsThemeManager().set_theme(theme)
                elif any(
                    alignment in speech_lower
                    for alignment in ["left", "center", "centre", "right"]
                ):
                    alignment = 0 if "left" in speech_lower else 1
                    taskbar.TaskbarCustomizer().set_alignment(alignment)
                elif "temperature" in speech_lower:
                    taskbar.TaskbarCustomizer().set_temperature_display(1)
                else:
                    print("System control: no matching action")
            except Exception as e:
                print(f"System control fail (Windows only?): {e}")

        elif "vision" in _cls_res:
            _speak_fast("Analysing, Please Wait")
            image_path = None
            try:
                image_path = camera_vision.realtime_vision()
                response_vision = deepInfra_VISION.generate(
                    speech,
                    system_prompt=INSTRUCTIONS.vison_realtime_v1,
                    image_path=image_path,
                )
                print("AI>>", response_vision)
                _speak_fast(response_vision)
            except Exception as e:
                print(f"Vision fail {e}")
                _speak_fast("Vision failed. Check camera.")
            finally:
                try:
                    if image_path and os.path.exists(image_path):
                        os.remove(image_path)
                except Exception:
                    pass

        elif "call" in _cls_res:
            _speak_fast("Sure Sir. Calling")
            # make_call.call()

        elif "website" in _cls_res:
            try:
                site_markdown = jenna_reader.fetch_website_content(
                    chrome_latest_url.get_latest_chrome_url()
                )
                response = openrouter.generate(
                    f"METEDATA: {site_markdown}\n\nQUERY: {speech}",
                    system_prompt="Keep you responses very short and concise",
                )
                _speak_fast(response)
            except Exception as e:
                print(f"Website fail {e}")
                _speak_fast("Website summarization failed.")

        else:
            # taskExecutor.process_query(speech)
            print("AI>>", _def_res)
            _speak_fast(_def_res)

    else:
        history_manager.store_history(
            history_manager.history + [{"role": "user", "content": speech}]
        )
        print("\033[93mHuman >> {}\033[0m".format(speech))

        # chat_response = Phind.generate(history_manager.history, system_prompt=INSTRUCTIONS.hindi_only_system_prompt_v3, stream=True)
        # chat_response = Phind.generate(history_manager.history, system_prompt=INSTRUCTIONS.human_response_v3_AVA, stream=True)

        # chat_response = Pi_Ai.generate(speech, prints=False)
        # FIX: HF dead + 4 Emotion-aware + 2 Offline Whisper fallback + 3 Voice clone optional
        # REALTIME: instant cache + skip emotion for short inputs + short max_tokens + early flush
        _low_stripped = speech.lower().strip(" .!?")
        if _AURA_FAST and _low_stripped in _FAST_REPLIES:
            chat_response = _FAST_REPLIES[_low_stripped]
            _ui_print_ai(chat_response)
            _speak_fast(chat_response)
            history_manager.update_file(speech, chat_response)
            continue
        # 4 Emotion: detect then adapt prompt (skip Groq call for <15 chars to save ~0.5s)
        emo = "neutral"
        if len(speech) >= 15:
            try:
                emo = detect_emotion(speech)
            except Exception:
                pass  # fixed bare except -> specific
        base_prompt = INSTRUCTIONS.human_response_v3_AVA
        try:
            base_prompt = adapt_prompt(base_prompt, emo)
        except Exception:
            pass  # fixed bare except -> specific
        if emo != "neutral":
            print(f"Emotion: {emo} -> adapted prompt")
        # STREAMING: Groq stream -> speak sentence-wise (was 2.1s wait -> 0.4s first word)
        # REALTIME: max_tokens 150 (voice, was 512) + voice-brevity prompt + flush on ,;: too + time flush
        chat_response = ""
        first = True
        try:
            from groq import Groq

            _groq = Groq(api_key=os.environ.get("GROQ_AI"))
            _voice_prompt = (
                base_prompt
                + " Reply in 1-2 short sentences for voice. No markdown, no code, no emoji."
                if _AURA_FAST
                else base_prompt
            )
            stream = _groq.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {"role": "system", "content": _voice_prompt},
                    {"role": "user", "content": speech},
                ],
                max_tokens=150 if _AURA_FAST else 512,
                stream=True,
            )
            buffer = ""
            _last_flush = _time.time()

            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                if not delta:
                    continue
                delta = delta.replace("\u202f", " ").replace("\u00a0", " ")
                chat_response += delta
                buffer += delta
                _words = len(buffer.split())
                _hit_punct = any(
                    p in buffer for p in [".", "!", "?", "\n", ",", ";", ":"]
                )
                _timed_out = (_time.time() - _last_flush) > 0.8 and _words >= 5
                if (
                    (_hit_punct and len(buffer.strip()) > 12)
                    or _words >= 10
                    or _timed_out
                ) and len(buffer.strip()) > 3:
                    if first:
                        _ui_print_sys(f"AURA (stream) >> {buffer.strip()}")
                        first = False
                    try:
                        _speak_fast(buffer.strip())
                    except Exception:
                        pass  # fixed bare except -> specific
                    buffer = ""
                    _last_flush = _time.time()
            if buffer.strip():
                try:
                    _speak_fast(buffer.strip())
                except Exception:
                    pass  # fixed bare except -> specific
            if not chat_response:
                raise ValueError("empty stream")
            chat_response = chat_response.strip()
        except Exception as _e:
            print(f"Groq stream failed {_e}, fallback HF")
            try:
                if not chat_response:
                    chat_response = Hugging_Face_TEXT.generate(speech)
            except Exception:
                try:
                    chat_response = "[Groq+Hf failed, try offline whisper]"
                except Exception:
                    chat_response = "Sorry, my brain is offline. Check GROQ_AI key."
        if not chat_response or not chat_response.strip():
            chat_response = "Sorry, I didn't catch that. Could you say again?"
        # if we streamed, sentences already spoken via queue, just render panel; else speak once
        streamed = not first  # first False means we streamed
        _ui_print_ai(chat_response)
        if not streamed:
            try:
                if os.environ.get("ELEVENLABS_API_KEY"):
                    try:
                        from ENGINE.TTS.voice_clone import speak as clone_speak

                        clone_speak(chat_response)
                    except Exception:
                        _speak_fast(chat_response)
                else:
                    _speak_fast(chat_response)
            except Exception as _tts_e:
                print(f"TTS failed: {_tts_e}, continuing...")
        history_manager.update_file(speech, chat_response)

        # engine.speak(chat_response, voice="hi-IN-Wavenet-D")

    # ai_response = Phind.generate(speech, stream=False)
    # ai_response = openrouter.generate(speech, stream=False)
    # ai_response = hf_api.generate(speech, stream=False)
    # ai_response = liaobots.generate(speech)
    # ai_response = groq_web_access.generate(speech)
    # ai_response = openrouter.generate(speech)
    # ai_response = deepInfra_TEXT.generate(speech)
    # sources, ai_response = Blackbox_ai.generate(speech, system_prompt="Keep your Responses very short and concise", web_access=True, stream=False)

    # print("AI >>", ai_response.replace("@web_search", ""))
    # speak(ai_response)

    # if 'call' in speech:
    #     speak("Sure Sir. Calling")
    #     make_call.call()

    # speak("Sure sir, generating images for you")
    # images_link = deepInfra_IMG.generate(speech)
    # print(images_link)
