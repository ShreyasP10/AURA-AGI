import concurrent.futures
_INTENT_EXECUTOR = concurrent.futures.ThreadPoolExecutor(max_workers=3, thread_name_prefix="aura-intent")
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
    _lazy_groq,
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
                    except Exception as e:
                        print(f"[error {__file__}] {type(e).__name__}: {e}")
                    speak(_txt)
            except Exception as _e:
                print(f"TTS worker fail: {_e}")
            finally:
                try:
                    # only restart mic if queue is empty, so we don't start/stop rapidly
                    if _tts_queue.empty():
                        listener.start_recording()
                except Exception as e:
                    print(f"[error {__file__}] {type(e).__name__}: {e}")
                _tts_queue.task_done()
        except Exception as e:
            print(f"[error {__file__}] {type(e).__name__}: {e}")


_threading.Thread(target=_tts_worker, daemon=True).start()


def _speak_fast(text: str):
    """Non-blocking ordered speak; drops unspeakable/code-only chunks instantly."""
    if os.environ.get("AURA_VOICE", "1") == "0":
        return  # text-only mode: no TTS delay at all
    if not text or not text.strip():
        return
    try:
        _tts_queue.put_nowait(text.strip())
    except Exception as e:
        print(f"[error {__file__}] {type(e).__name__}: {e}")


def _stop_speaking():
    """Say 'stop' -> clear pending speech + halt current playback immediately."""
    _stop_tts.set()
    try:
        listener.stop_recording()
    except Exception as e:
        print(f"[error {__file__}] {type(e).__name__}: {e}")
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
    except Exception as e:
        print(f"[error {__file__}] {type(e).__name__}: {e}")
    try:
        import pygame

        try:
            pygame.mixer.music.stop()
        except Exception as e:
            print(f"[error {__file__}] {type(e).__name__}: {e}")
        try:
            pygame.mixer.quit()
        except Exception as e:
            print(f"[error {__file__}] {type(e).__name__}: {e}")
    except Exception as e:
        print(f"[error {__file__}] {type(e).__name__}: {e}")

_STOP_WORDS = (
    "stop",
    "stop speaking",
    "quiet",
    "enough",
    "cancel",
    "shut up",
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
                _Panel(_Markdown(text), title="[bold magenta]AURA[/bold magenta]", border_style="cyan", expand=False)
            )
            return
        except BaseException:
            pass
    print(f"\n\033[92mAURA >> {text}\033[0m\n")


def _ui_print_sys(text: str):
    if _USE_RICH and _console:
        try:
            _console.print(text)
            return
        except BaseException:
            pass
    print(text)


def _get_input_hybrid() -> str | None:
    """Each turn: type directly, or press Enter empty / type '/voice' for mic. Voice timeout falls back to typing."""
    _mode = os.environ.get("AURA_TEXT_MODE", "0")
    _prompt = "YOU"
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
        _ui_print_sys("[bold yellow]🎙️ Listening...[/bold yellow] [dim](speak now, 45s max, Ctrl+C for typing)[/dim]")
        speech = listener.listen(timeout_s=45)
        if speech and speech.strip():
            _ui_print_sys(f"[bold green]YOU SAID:[/bold green] {speech.strip()}")
            return speech.strip()
        _ui_print_sys("[dim]No speech heard — type instead.[/dim]")
    except KeyboardInterrupt:
        _ui_print_sys("[dim]Mic cancelled — type instead.[/dim]")
    except Exception as e:
        _ui_print_sys(f"[bold red]STT failed ({type(e).__name__})[/bold red] [dim]Type instead.[/dim]")
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
    # Never clear the user's scrollback unannounced (destroys prior errors);
    # opt in explicitly with AURA_CLEAR=1.
    if os.environ.get("AURA_CLEAR", "0") == "1":
        import os as _os

        _os.system("cls" if _os.name == "nt" else "clear")
    _console.print(
        _Panel.fit(
            "[bold cyan]AURA-AGI Autonomous Assistant[/bold cyan]\n"
            "[dim]Type your message, or press Enter to use the microphone.\n"
            "Type [bold red]/quit[/bold red] to exit. Say or type [bold red]stop[/bold red] to halt speech.[/dim]",
            title="[bold green]System Ready[/bold green]",
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
        _ui_print_sys("[bold magenta]Goodbye![/bold magenta]")
        break

    low = speech.lower().strip()
    # STOP: interrupt immediately, no LLM call — works with/without wakeword
    if low in _STOP_WORDS:
        _stop_speaking()
        _ui_print_sys("[bold red]🛑 Stopped.[/bold red]")
        continue
    is_wake = low.startswith("aura") or low.endswith("aura")
    if is_wake:
        if low.startswith("aura"):
            speech = speech[len("aura") :].strip()
        elif low.endswith("aura"):
            speech = speech[: -len("aura")].strip()
        _ui_print_sys(f"[dim]Parsed intent: {speech}[/dim]")
        # stop after wake strip too: "aura stop speaking"
        if speech.lower().strip() in _STOP_WORDS:
            _stop_speaking()
            _ui_print_sys("[bold red]🛑 Stopped.[/bold red]")
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
                except Exception as e:
                    print(f"[error {__file__}] {type(e).__name__}: {e}")
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
                _ui_print_sys(f"[bold blue]AppLauncher ⚡[/bold blue] {res}")
                _speak_fast(res)
                continue
            except Exception as e:
                print(f"App launcher fail {e}")
        if low2.startswith("find ") or "find file" in low2 or "search file" in low2:
            try:
                res = find_and_summarize(speech)
                _ui_print_sys(f"[bold blue]FileFinder ⚡[/bold blue] {res}")
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
                                f"{i + 1}. {t.get('text', '')} !{t.get('priority', 'none')}"
                                for i, t in enumerate(tasks[:5])
                            ]
                        )
                        or "No tasks"
                    )
                else:
                    t = add_task(speech)
                    res = f"Task added: {t.get('text', '')}"
                _ui_print_sys(f"[bold blue]TaskBoard ⚡[/bold blue] {res}")
                _speak_fast(res)
                continue
            except Exception as e:
                print(f"Task fail {e}")
        if any(k in low2 for k in ["read text", "ocr"]):
            try:
                res = ocr_vision_live(speech)
                _ui_print_sys(f"[bold blue]OCR ⚡[/bold blue] {res[:80]}")
                _speak_fast(res[:400])
                continue
            except Exception as e:
                print(f"OCR fail {e}")
        if any(k in low2 for k in ["on my screen", "screen see"]):
            try:
                res = see_screen(speech)
                _ui_print_sys(f"[bold blue]ScreenSee ⚡[/bold blue] {res[:80]}")
                _speak_fast(res[:400])
                continue
            except Exception as e:
                print(f"ScreenSee fail {e}")

        _classifier_prompt = getattr(BISECTORS, "complex_task_classifier_v6", BISECTORS.complex_task_classifier_v5)
        # Injection guard applied consistently
        _safe_speech = (
            f"<<BEGIN_CLASSIFICATION_INPUT>>\n{speech[:500]}\n<<END_CLASSIFICATION_INPUT>>\n"
            "Classify ONLY the text between the tags above."
        )

        # Submit 3 parallel LLM calls using the shared executor
        f_img   = _INTENT_EXECUTOR.submit(deepInfra_TEXT.generate,
                      [{"role": "user", "content": _safe_speech}],
                      system_prompt=BISECTORS.image_requests_v3,
                      stream=False)
        f_cls   = _INTENT_EXECUTOR.submit(deepInfra_TEXT.generate,
                      [{"role": "user", "content": _safe_speech}],
                      system_prompt=_classifier_prompt, stream=False)
        f_def   = _INTENT_EXECUTOR.submit(deepInfra_TEXT.generate,
                      list(history_manager.history) + [{"role": "user", "content": speech}],
                      system_prompt=adapt_prompt(INSTRUCTIONS.human_response_v3_AVA, emo),
                      stream=False)
        concurrent.futures.wait([f_img, f_cls, f_def], timeout=20)

        # Normalise results safely (prevent unhandled future exceptions from crashing the loop)
        def _safe_res(fut, default=""):
            try:
                return fut.result(timeout=0) if fut.done() else default
            except Exception as e:
                print(f"[intent future] {e}")
                return default

        _img_text = (_safe_res(f_img) or "").strip().lower()
        _cls_res  = (_safe_res(f_cls) or "").lower()
        _def_res  =  _safe_res(f_def, "Sorry, I could not think of a reply.")

        # FIX 1: exact-match image detection (not substring)
        _is_image_req = _img_text in ("yes", "response: yes") or _img_text.endswith("response: yes")

        if _is_image_req:
            _speak_fast("Sure Sir, Generating Your Image.")
            try:
                ok, msg = decohere_ai.generate(speech)
                _ui_print_sys(f"[bold blue]ImageGen ⚡[/bold blue] {ok} - {msg}")
                reply_msg = "Image ready." if ok else f"Image failed: {msg}"
                _speak_fast(reply_msg)
                history_manager.update_file(speech, reply_msg)
            except Exception as e:
                _speak_fast("Image generation failed.")
                print(f"[image] {e}")

        # FIX 2: sum() instead of all() for confused-classifier fallback
        elif sum(1 for x in ("vision","website","call","youtube") if x in _cls_res) >= 3:
            print("Ambiguous classification — using default response")
            _ui_print_ai(_def_res)
            _speak_fast(_def_res)
            history_manager.update_file(speech, _def_res)

        elif "system control" in _cls_res:
            _speak_fast("Sure, applying the setting now.")
            try:
                sl = speech.lower()
                if "dark" in sl or "light" in sl:
                    system_theme.WindowsThemeManager().set_theme(0 if "dark" in sl else 1)
                elif any(a in sl for a in ("left","center","centre","right")):
                    taskbar.TaskbarCustomizer().set_alignment(0 if "left" in sl else 1)
                elif "temperature" in sl:
                    taskbar.TaskbarCustomizer().set_temperature_display(1)
                else:
                    print("[system] no matching action")
                history_manager.update_file(speech, "Applied system setting.")
            except Exception as e:
                print(f"[system] {e}")

        elif "vision" in _cls_res:
            _speak_fast("Analysing, please wait.")
            image_path = None
            try:
                image_path = camera_vision.realtime_vision()
                resp = deepInfra_VISION.generate(
                    speech, system_prompt=INSTRUCTIONS.vison_realtime_v1, image_path=image_path
                )
                _ui_print_ai(resp)
                _speak_fast(resp)
                history_manager.update_file(speech, resp)
            except Exception as e:
                print(f"[vision] {e}")
                _speak_fast("Vision failed. Check camera.")
            finally:
                if image_path:
                    try:
                        os.remove(image_path)
                    except OSError:
                        pass

        elif "call" in _cls_res:
            _speak_fast("Sure. Calling.")
            # make_call.call()

        elif "website" in _cls_res:
            try:
                site_md = jenna_reader.fetch_website_content(chrome_latest_url.get_latest_chrome_url())
                resp = openrouter.generate(
                    f"METADATA: {site_md[:6000]}\n\nQUERY: {speech}",
                    system_prompt="Keep responses very short and concise.",
                )
                _ui_print_ai(resp)
                _speak_fast(resp)
                history_manager.update_file(speech, resp)
            except Exception as e:
                print(f"[website] {e}")
                _speak_fast("Website summarization failed.")

        else:
            _ui_print_ai(_def_res)
            _speak_fast(_def_res)
            history_manager.update_file(speech, _def_res)

    else:
        history_manager.store_history(
            history_manager.history + [{"role": "user", "content": speech}]
        )
        

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
            except Exception as e:
                print(f"[error {__file__}] {type(e).__name__}: {e}")  # fixed bare except -> specific
        base_prompt = INSTRUCTIONS.human_response_v3_AVA
        try:
            base_prompt = adapt_prompt(base_prompt, emo)
        except Exception as e:
            print(f"[error {__file__}] {type(e).__name__}: {e}")  # fixed bare except -> specific
        if emo != "neutral":
            print(f"Emotion: {emo} -> adapted prompt")
        # STREAMING: Groq stream -> speak sentence-wise (was 2.1s wait -> 0.4s first word)
        # REALTIME: max_tokens 150 (voice, was 512) + voice-brevity prompt + flush on ,;: too + time flush
        chat_response = ""
        first = True
        _voice_prompt = (
            base_prompt
            + " Reply in 1-2 short sentences for voice. No markdown, no code, no emoji."
            if _AURA_FAST
            else base_prompt
        )
        try:
            _groq = _lazy_groq.get_client()
            _groq_model = os.environ.get("GROQ_MODEL", "llama-3.1-8b-instant")
            stream = _groq.chat.completions.create(
                model=_groq_model,
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
                        _ui_print_sys(f"[bold cyan]AURA (stream) >>[/bold cyan] {buffer.strip()}")
                        first = False
                    try:
                        _speak_fast(buffer.strip())
                    except Exception as e:
                        print(f"[error {__file__}] {type(e).__name__}: {e}")  # fixed bare except -> specific
                    buffer = ""
                    _last_flush = _time.time()
            if buffer.strip():
                try:
                    _speak_fast(buffer.strip())
                except Exception as e:
                    print(f"[error {__file__}] {type(e).__name__}: {e}")  # fixed bare except -> specific
            if not chat_response:
                raise ValueError("empty stream")
            chat_response = chat_response.strip()
        except Exception as _e:
            print(f"Groq stream failed {_e}, falling back to OpenRouter...")
            first = True  # reset flag so fallback response is voiced
            chat_response = ""
            try:
                chat_response = openrouter.generate(history_manager.history + [{"role": "user", "content": speech}], system_prompt=_voice_prompt, stream=False)
            except Exception as _e2:
                print(f"OpenRouter failed {_e2}, falling back to DeepInfra...")
                try:
                    chat_response = deepInfra_TEXT.generate(history_manager.history + [{"role": "user", "content": speech}], system_prompt=_voice_prompt, stream=False)
                except Exception as _e3:
                    print(f"DeepInfra failed {_e3}, falling back to HuggingFace...")
                    try:
                        chat_response = Hugging_Face_TEXT.generate(speech)
                    except Exception as _e4:
                        print(f"HuggingFace failed {_e4}")
                        chat_response = "Sorry, my brain is offline. All API providers failed."
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
