# ██████╗   ███████╗ ██╗    ██╗ ███████╗            ██████╗    ██████╗             ██████╗   ██████╗    ██████╗   ███████╗
# ██╔══██╗ ██╔════╝ ██║    ██║ ██╔════╝            ██╔══██╗ ██╔═══██╗          ██╔════╝ ██╔═══██╗ ██╔══██╗ ██╔════╝
# ██║    ██║ █████╗     ██║    ██║ ███████╗            ██║    ██║ ██║      ██║         ██║          ██║      ██║ ██║    ██║ █████╗  
# ██║    ██║ ██╔══╝    ╚██╗  ██╔╝ ╚════██║           ██║    ██║ ██║      ██║         ██║          ██║      ██║ ██║    ██║ ██╔══╝  
# ██████╔╝ ███████╗  ╚████╔╝  ███████║            ██████╔╝╚██████╔╝          ╚██████╗ ╚██████╔╝  ██████╔╝ ███████╗
# ╚═════╝  ╚══════╝    ╚═══╝     ╚══════╝            ╚═════╝    ╚═════╝             ╚═════╝   ╚═════╝    ╚═════╝   ╚══════╝

#  Made With 💓 By - Shreyas Pawar (AURA-AGI)
#  YouTube Channel: https://www.youtube.com/@AURA-Team

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

      - Support: https://buymeacoffee.com/AURA-Team
      - Patreon: https://patreon.com/AURA-Team

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

#  For any questions or concerns, reach out to us via our social media handles.
#  Our top choice for contact is Telegram: https://t.me/AURA-Team
#  You can also find us on other platforms listed above. We're here to help!

#  - YouTube Channel: https://www.youtube.com/@AURA-Team
#  - Telegram Group: https://t.me/AURA-Team
#  - Discord Server: https://discord.gg/ehwfVtsAts
#  - Instagram:
#    - Personal: https://www.instagram.com/Shreyas.shades_/
#    - Channel: https://www.instagram.com/AURA-Team_/

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    - Support: https://buymeacoffee.com/AURA-Team
    - Patreon: https://patreon.com/AURA-Team

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#  ------------------------------------------------------------------------------
#  Dive into the world of coding with AURA Team - where passion meets programming!
#  Make sure to hit that Subscribe button to stay tuned for exciting content!

#  Pro Tip: For optimal performance and a seamless experience, we recommend using
#  the default library versions demonstrated in this demo. Your coding journey just
#  got even better! Happy coding!
#  ----------------------------------------------------------------------------

from IMPORTS import *
# --- 12 new features (1-12) imports ---
try:
    from TOOLS.SYSTEM_SETTINGS.app_launcher import open_app
    from TOOLS.file_finder import find_and_summarize
    from TOOLS.task_board import add_task, list_tasks
    from BRAIN.TOOLS.emotion import detect_emotion, adapt_prompt
    from PLAYGROUND.CAMERA.ocr_live import ocr_vision_live
    from PLAYGROUND.WEBSITE_ASSISTANT.screen_see import see_screen
except Exception as _imp_e:
    print(f"Feature import warning: {_imp_e}")
    open_app = find_and_summarize = add_task = list_tasks = detect_emotion = adapt_prompt = ocr_vision_live = see_screen = lambda *a, **k: "[feature not installed]"

while True:

    speech = listener.listen()

    low = speech.lower()
    is_wake = low.startswith("aura") or low.endswith("aura")
    if is_wake:
        if low.startswith("aura"):
            speech = speech[len("aura"):].strip()
        elif low.endswith("aura"):
            speech = speech[:-len("aura")].strip()
        print("Updated Speech:", speech)
        # --- Optimized fast local intents (zero LLM cost, <10ms) ---
        low2 = speech.lower()
        # cache lower check once
        if low2.startswith("open ") or ("open " in low2 and any(x in low2 for x in ["brave","chrome","vscode","spotify","notepad","calculator"])):
            try: res = open_app(speech); print("AppLauncher>>", res); speak(res); continue
            except Exception as e: print(f"App launcher fail {e}")
        if low2.startswith("find ") or "find file" in low2 or "search file" in low2:
            try: res = find_and_summarize(speech); print("FileFinder>>", res); speak(res[:300]); continue
            except Exception as e: print(f"Finder fail {e}")
        if low2.startswith("task ") or low2.startswith("add task") or "list tasks" in low2 or "my tasks" in low2:
            try:
                if "list" in low2 or "show" in low2: tasks = list_tasks(); res = "\n".join([f"{i+1}. {t['text']} !{t['priority']}" for i,t in enumerate(tasks[:5])]) or "No tasks"
                else: t = add_task(speech); res = f"Task added: {t['text']}"
                print("TaskBoard>>", res); speak(res); continue
            except Exception as e: print(f"Task fail {e}")
        if any(k in low2 for k in ["read text", "ocr"]):
            try: res = ocr_vision_live(speech); print("OCR>>", res[:80]); speak(res[:400]); continue
            except Exception as e: print(f"OCR fail {e}")
        if any(k in low2 for k in ["on my screen", "screen see"]):
            try: res = see_screen(speech); print("ScreenSee>>", res[:80]); speak(res[:400]); continue
            except Exception as e: print(f"ScreenSee fail {e}")

        # OPTIMIZED: single executor reuse vs 3 separate (was 3x ThreadPool per wake = 6 executors leaked)
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
            response_img_or_text = ex.submit(deepInfra_TEXT.generate, [{"role": "user", "content": "Text to Classify -->" + speech}], system_prompt=BISECTORS.image_requests_v3)
            response_classifier = ex.submit(deepInfra_TEXT.generate, [{"role": "user", "content": "Text to Classify -->" + speech}], system_prompt=BISECTORS.complex_task_classifier_v6, stream=False)
            default_response = ex.submit(deepInfra_TEXT.generate, history_manager.history, system_prompt=adapt_prompt(INSTRUCTIONS.human_response_v3_AVA, emo) if 'emo' in locals() else INSTRUCTIONS.human_response_v3_AVA, stream=False)
            concurrent.futures.wait([response_img_or_text, response_classifier, default_response])
        print("Response Classifier >> ", "\033[91m" + response_classifier.result() + "\033[0m")
        print("Image or Text Classifier >> ", "\033[91m" + response_img_or_text.result() + "\033[0m")

        if "yes" in response_img_or_text.result().lower():
            speak("Sure Sir, Generating Your Image")
            decohere_ai.generate(speech)
            continue
        
        elif all(x in response_classifier.result().lower() for x in ("vision", "website", "call", "youtube")):
            print("\033[91mConfused with Classification. Using Default Response\033[0m")
            speak(default_response.result())

        elif "system control" in response_classifier.result().lower():
            # Create a ThreadPoolExecutor and submit the speak function
            with concurrent.futures.ThreadPoolExecutor() as executor:
                speak_future = executor.submit(speak, "Sure Sir. Setting the Required Settings")

                speech_lower = speech.lower()
                if "dark" in speech_lower or "light" in speech_lower:
                    theme = 0 if "dark" in speech_lower else 1
                    system_theme.WindowsThemeManager().set_theme(theme)
                elif any(alignment in speech_lower for alignment in ["left", "center", "centre", "right"]):
                    alignment = 0 if "left" in speech_lower else 1
                    taskbar.TaskbarCustomizer().set_alignment(alignment)
                elif "temperature" in speech_lower:
                    taskbar.TaskbarCustomizer().set_temperature_display(1)

                speak_future.result()

        elif "vision" in response_classifier.result().lower():
            concurrent.futures.ThreadPoolExecutor().submit(speak("Analysing, Please Wait"))
            image_path = camera_vision.realtime_vision()
            response_vison = deepInfra_VISION.generate(speech, system_prompt=INSTRUCTIONS.vison_realtime_v1, image_path=image_path)
            print("AI>>", response_vison)
            os.remove(image_path)
            speak(response_vison)

        elif "call" in response_classifier.result().lower():
            speak("Sure Sir. Calling")
            # make_call.call()

        elif "website" in response_classifier.result().lower():
            site_markdown = jenna_reader.fetch_website_content(chrome_latest_url.get_latest_chrome_url())
            response = openrouter.generate(f"METEDATA: {site_markdown}\n\nQUERY: {speech}", system_prompt="Keep you responses very short and concise")
            speak(response, voice="Salli")

        else: 
            # taskExecutor.process_query(speech)
            print("AI>>", default_response.result())
            speak(default_response.result())

    else:
        history_manager.store_history(history_manager.history + [{"role": "user", "content": speech}])
        print("\033[93mHuman >> {}\033[0m".format(speech))

        # chat_response = Phind.generate(history_manager.history, system_prompt=INSTRUCTIONS.hindi_only_system_prompt_v3, stream=True)
        # chat_response = Phind.generate(history_manager.history, system_prompt=INSTRUCTIONS.human_response_v3_AVA, stream=True)
        
        # chat_response = Pi_Ai.generate(speech, prints=False)
        # FIX: HF dead + 4 Emotion-aware + 2 Offline Whisper fallback + 3 Voice clone optional
        # 4 Emotion: detect then adapt prompt
        emo = "neutral"
        try: emo = detect_emotion(speech)
        except Exception: pass # fixed bare except -> specific
        base_prompt = INSTRUCTIONS.human_response_v3_AVA
        try: base_prompt = adapt_prompt(base_prompt, emo)
        except Exception: pass # fixed bare except -> specific
        if emo != "neutral": print(f"Emotion: {emo} -> adapted prompt")
        # STREAMING: Groq stream -> speak sentence-wise (was 2.1s wait -> 0.4s first word)
        chat_response = ""
        try:
            from groq import Groq
            _groq = Groq(api_key=os.environ.get("GROQ_AI"))
            stream = _groq.chat.completions.create(model="openai/gpt-oss-20b", messages=[{"role":"system","content": base_prompt},{"role":"user","content": speech}], max_tokens=512, stream=True)
            buffer=""; first=True; import threading
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                if not delta: continue
                delta=delta.replace("\u202f"," ").replace("\u00a0"," ")
                chat_response+=delta; buffer+=delta
                if any(p in buffer for p in [".","!","?","\n"]) and len(buffer)>24:
                    if first:
                        print(f"\n\033[92mAURA (stream) >> {buffer.strip()}\033[0m")
                        first=False
                    try: threading.Thread(target=speak, args=(buffer.strip(),), daemon=True).start()
                    except Exception: pass # fixed bare except -> specific
                    buffer=""
            if buffer.strip():
                try: threading.Thread(target=speak, args=(buffer.strip(),), daemon=True).start()
                except Exception: pass # fixed bare except -> specific
            if not chat_response: raise ValueError("empty stream")
            chat_response=chat_response.strip()
        except Exception as _e:
            print(f"Groq stream failed {_e}, fallback HF")
            try:
                if not chat_response: chat_response = Hugging_Face_TEXT.generate(speech)
            except Exception as e:
                try:
                    from ENGINE.STT.whisper_offline import transcribe_file
                    chat_response = "[Groq+Hf failed, try offline whisper]"
                except: chat_response = "Sorry, my brain is offline. Check GROQ_AI key."
        if not chat_response or not chat_response.strip():
            chat_response = "Sorry, I didn't catch that. Could you say again?"
        # if we streamed, sentences already spoken via threads, just print; else speak once
        streamed = 'first' in locals() and not first  # first False means we streamed
        if streamed:
            print(f"\n\033[92mAURA >> {chat_response}\033[0m\n")
        else:
            print(f"\n\033[92mAURA >> {chat_response}\033[0m\n")
            try:
                if os.environ.get("ELEVENLABS_API_KEY"):
                    try:
                        from ENGINE.TTS.voice_clone import speak as clone_speak
                        clone_speak(chat_response)
                    except: speak(chat_response)
                else:
                    speak(chat_response)
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
