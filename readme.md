<div align="center">
  <img src="https://img.shields.io/badge/AURA--AGI-v1.0-red?style=for-the-badge&logo=huggingface&logoColor=white" alt="AURA-AGI Badge">
  <br/>
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=flat-square" alt="Platform">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/Version-1.0.0-blue?style=flat-square" alt="Version">
  <!-- <p>
    <a href="https://github.com/ShreyasP10/AURA-AGI/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/ShreyasP10/AURA-AGI?style=social"></a>
    <a href="https://github.com/ShreyasP10/AURA-AGI/network/members"><img alt="GitHub forks" src="https://img.shields.io/github/forks/ShreyasP10/AURA-AGI?style=social"></a>
    <a href="https://github.com/ShreyasP10/AURA-AGI/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/ShreyasP10/AURA-AGI?style=social"></a>
  </p> -->
</div>

# AURA-AGI — Autonomous Unified Responsive Assistant
### *Your everyday voice buddy that actually listens — say “aura” and it handles the rest.*

> **AURA-AGI** is a feature-rich desktop voice assistant built in **Python** that combines **Speech-to-Text**, **LLM routing**, **Vision**, **Image generation** and **System control** — all wrapped in a modular, provider-agnostic architecture with hotword, interruptible TTS and persistent memory.

---

## Table of Contents
- [Features](#features)
- [Supported Intents & Commands](#supported-intents--commands)
- [Screenshots](#screenshots)
- [System at a Glance](#system-at-a-glance)
- [Repo Layout / Project Structure](#repo-layout--project-structure)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [How It Works](#how-it-works)
- [Data & Memory](#data--memory)
- [Troubleshooting](#troubleshooting)
- [What's New](#whats-new)
- [Roadmap](#roadmap)
- [Documentation Index](#documentation-index)
- [Contributing](#contributing)
- [License](#license)
- [Authors](#authors)

---

## Features

### 🎙️ Wakeword & Speech
Your voice is the command line. AURA listens continuously and respects `aura` as wakeword. Every turn also accepts typing — press Enter empty or `/voice` for mic, `/quit` to exit.

| Feature | Description |
|---------|-------------|
| **`aura` wakeword** | Prefix or suffix: `aura what is capital` or `what is capital aura` → routed; otherwise continuous chat |
| **`stop` to interrupt** | Say/type `stop`, `stop speaking`, `quiet`, `enough`, `cancel` → clears TTS queue + halts playback instantly, no LLM call |
| **Brave-first Selenium STT** | `ENGINE/STT/DevsDoCode.py` Brave (default, `AURA_BROWSER=brave`) with Chrome auto-fallback, isolated profile, `?silence=` (default 3000ms, `AURA_SILENCE_MS=800-8000`), 45s listen timeout + driver restart |
| **Offline STT** | Vosk `vosk_recog.py` (no browser/mic-server needed) + `whisper_offline.py` (`faster-whisper`) fallback |
| **Hotword Detection** | `TOOLS/AUDIO/Hotword_Detection.py` `pvporcupine` (jarvis model → mapped to AURA) with activation sound |
| **Interruptible Playback** | Ordered TTS queue + single playback worker + `pygame.mixer.stop()` on `stop` |

### 🧠 LLM Router — Your Intent, Best Brain
One utterance → 3 parallel classifications → best provider.

| Feature | Description |
|---------|-------------|
| **Parallel Classification** | 3x LLM fan-out with `BISECTORS.image_requests_v3` + `complex_task_classifier_v6` (with `v5` fallback) + emotion-adapted `INSTRUCTIONS.human_response_v3_AVA` |
| **Provider Zoo (16 adapters)** | `BRAIN/AI/TEXT/API/` — Groq, OpenRouter, DeepInfra, HuggingFace, Pi, Liaobots, Phind, etc. |
| **Realtime chat** | Groq `openai/gpt-oss-20b` streaming with early flush (punctuation/10 words/0.8s), 150-token voice cap, instant replies for greetings, emotion skipped for short inputs (`AURA_FAST=1`) |
| **Local LLM** | `BRAIN/AI/TEXT/LOCAL/llama_CPP.py` — fully offline via `llama.cpp` |
| **Streaming** | `BRAIN/AI/TEXT/STREAM/` sentence-level generators feeding the ordered TTS queue |

### 🖼️ Vision & Image — See & Create
| Feature | Description |
|---------|-------------|
| **Real-time Vision** | `PLAYGROUND/CAMERA/camera_vision.py` `cv2.VideoCapture(0)` → `BRAIN/AI/VISION/deepInfra_VISION.py` LLaVA 1.5 `vision_realtime_v1` |
| **Image Generation** | `BRAIN/AI/IMAGE/decohere_ai.py` → `turbo.decohere.ai` (steps/seed/enhance, safety filter) |

### 🌐 Web & Automation — Act, Don’t Just Answer
| Feature | Description |
|---------|-------------|
| **Website Assistant** | `PLAYGROUND/WEBSITE_ASSISTANT/jenna_reader.py` + Brave-first history (`chrome_latest_url.py` tries Chrome → Brave) → `openrouter` summarization |
| **Web Search** | `TOOLS/Web_Results.py`, `BRAIN/TOOLS/groq_web_access.py` tool-call `get_web_info` |
| **Code Execution** | `TOOLS/RawDog.py` `webscout.AIutel.RawDog` (opt-in, `confirm_script=False`) |
| **System Control** | `TOOLS/SYSTEM_SETTINGS/system_theme.py` + `taskbar.py` — dark/light, taskbar align/temperature via registry |

### 🔊 TTS — Voices That Stay With You
Drawing toolbar equivalent for voice: pick your voice, color your reply.

| Feature | Description |
|---------|-------------|
| **Voices** | `edge_tts` default (`en-US-JennyNeural`): markdown/art sanitizer, serialized in-process synthesis with CLI fallback, unique files per utterance; DeepGram, ElevenLabs, Speechify, StreamElements, `STREAMING/` queue variants available |
| **Voice on/off** | `AURA_VOICE=1` speaks (default), `AURA_VOICE=0` text-only with zero TTS wait |
| **Sticky Notes Analogy** | Persistent `conversation_history.json` = your sticky notes that never fall off |

### 💾 Memory & Playground
| Feature | Description |
|---------|-------------|
| **Conversation Manager** | `TOOLS/Alpaca_DS_Converser.py` word-window `history_offset=700` → `ASSETS/conversation_history.json` |
| **Everyday tools** | App launcher (`aura open chrome`), file finder (`aura find resume`), task board (`aura add task ... !high #tag`), live OCR, screen-see, alarms/timers via NL time parser |
| **Playground** | ADB calls `PLAYGROUND/ADB_CALL/`, CLAP audio classifier `CLAP_NN/`, gesture control, proxy `ProxyAPI.py` |

---

## Supported Intents & Commands

| Intent | Example Utterance | Route | Output |
|--------|-------------------|-------|--------|
| **Image** | `aura generate image of futuristic city` | `BISECTORS.image_requests_v3` → `decohere_ai` | `ASSETS/image.jpg` + `Sure Sir, Generating...` |
| **System Control** | `aura set dark theme` / `move taskbar left` | `system control` → `system_theme`/`taskbar` | Registry flip + toast `TOOLS/SYSTEM_SETTINGS/Alarms.py` |
| **Vision** | `aura what is in my hand` | `vision` → `camera_vision` + `deepInfra_VISION` | `You are holding a pen` |
| **Website** | `aura summarize this website` | `website` → `jenna_reader` + `openrouter` | Short spoken summary (Brave history first) |
| **Call** | `aura call mum` | `call` → `PLAYGROUND/ADB_CALL/make_call.py` (stub) | `Sure Sir. Calling` |
| **Open / Find / Tasks** | `aura open vscode` / `aura find resume` / `aura list tasks` | fast local intents, zero LLM | Spoken result |
| **Stop** | `stop` / `aura stop` | immediate, no LLM | Playback halted |
| **Chat** | `aura hello` / `hello` (no wakeword) | `default` `human_response_v3_AVA` / Groq stream + `Hugging_Face_TEXT` fallback | AVA persona + history persist |

---

## Screenshots

> Real interaction, not mockups — Screenshots coming soon.

| 🎙️ Everyday Chat | 👀 See & Understand | ⚙️ Do Things |
|---|---|---|
| `aura what is capital` → instant answer | `aura what is in my hand` → “You are holding a pen” | `aura set dark theme` → flips Windows in a blink |
| *Talk naturally, no rigid commands* | *Your camera becomes its eyes* | *Your voice becomes the control center* |

---

## System at a Glance
*System at a Glance* — AURA’s flow: **Capture → Buffer → Classify → Dispatch → Speak → Persist**.

```
Mic ──▶ DevsDoCode STT (Selenium) ──▶ main.py:48 listener.listen()
                                         │
                    ┌────────────────────┼────────────────────┐
                    │ wakeword "aura"?   │  no wakeword       │
                    ▼                    │  ▼                 │
  ┌─────────────────────────────────┐    │  Hugging_Face_TEXT ──▶ TTS ──▶ history_manager.update_file()
  │ 3x deepInfra_TEXT parallel      │    │
  │  BISECTORS + INSTRUCTIONS       │    │
  └────────┬────────────────────────┘    │
           ▼                             │
  ┌────────────────┐  yes  ┌──────────────┴─┐
  │ image_requests │──────▶│ decohere_ai    │
  │ system control │──────▶│ system_theme/  │
  │ vision         │──────▶│ camera_vision + deepInfra_VISION │
  │ website        │──────▶│ jenna_reader + openrouter        │
  │ default        │──────▶│ deepInfra_TEXT (human_response_v3_AVA) │
           └────────────────┘
                              ▼
                     Interrupted_Playsound (pygame) ◀── HotwordDetector (pvporcupine)
                              │
                     ASSETS/conversation_history.json (local, 700-word window)
```

All data lives locally in `ASSETS/` + `~/.aura/` equivalent, isolated per user — no cloud lock-in unless you opt for cloud LLMs.

---

## Repo Layout / Project Structure

> **Fixed structure** — `__pycache__/` and `ASSETS/conversation_history.json` now ignored via `.gitignore`, `SETTING.py` → `SETTING.md` (doc), `WEB-3D/` added, 12 new features integrated.

| Path | What it is |
|------|------------|
| `main.py` | Entry loop, wakeword `aura` dispatch `main.py:50` + 12 intents (app/finder/task/ocr/screen) |
| `IMPORTS.py` | Central aggregator — **lazy** `_LazyListener` (Chrome defers) + `edge_tts` |
| `PROMPTS/` | `BISECTORS.py` classifiers, `INSTRUCTIONS.py` AVA persona (emotion-adapted), `SYSTEM.py` |
| `BRAIN/AI/TEXT/API/` | 16 LLM adapters (fixed `Hugging_Face_TEXT.py` → `api.huggingface.co`) |
| `BRAIN/AI/TEXT/LOCAL/` | `llama_CPP.py` offline |
| `BRAIN/AI/VISION/` | `deepInfra_VISION.py` LLaVA |
| `BRAIN/AI/IMAGE/` | `decohere_ai.py` |
| `BRAIN/TOOLS/` | `groq_web_access.py`, `emotion.py` (4) |
| `ENGINE/STT/` | `DevsDoCode.py` (lazy, 2s silence `src/index.html`), `vosk_recog.py`, `whisper_offline.py` (2), `src/index.html` |
| `ENGINE/TTS/` | `edge_tts.py` (empty-guard + pygame fallback), `voice_clone.py` (3), `DeepGram.py` + `STREAMING/` |
| `TOOLS/AUDIO/` | `Hotword_Detection.py` (dual 1.9.5/4.x + `.ppn`), `custom_wakeword.md` (1), `Interrupted_Playsound.py` |
| `TOOLS/` | `Alpaca_DS_Converser.py` (700w window), `file_finder.py` (11), `task_board.py` (12), `RawDog.py` |
| `TOOLS/SYSTEM_SETTINGS/` | `system_theme.py`, `taskbar.py`, `app_launcher.py` (10), `SETTING.md` (doc) |
| `PLAYGROUND/` | `CAMERA/` (`camera_vision.py`, `ocr_live.py` (5), `gesture_control.py` (6)), `WEBSITE_ASSISTANT/` (`jenna_reader.py`, `screen_see.py` (7)), `ADB_CALL/`, `CLAP_NN/` |
| `WEB-3D/` | **New** 3D site `index.html`, `app.js` (whisper fallback + ring visualizer), `style.css`, `skins.js` (8), `party.js` (9) |
| `ASSETS/` | `SOUNDS/`, `Vosk/` *(ignored)*, `porcupine/` `aura*.ppn` *(ignored)*, `conversation_history.json` *(ignored)* |
| `.gitignore` | `__pycache__/`, `*.pyc`, `.env`, `Vosk/`, `*.ppn`, `conversation_history.json` |

<details>
<summary>Full tree (click to expand)</summary>

```
AURA-AGI/
├── .env / .env.example  # real keys not committed
├── .gitignore           # fixed: ignores __pycache__, Vosk, .ppn, history
├── main.py              # lazy STT + 12 intents + streaming Groq 0.4s
├── IMPORTS.py           # _LazyListener + _LazyGroq
├── requirements.txt
├── readme.md            # this file (combined Notes+CropIQ+LifeLensIQ)
├── LICENCE / CODE_OF_CONDUCT.md
├── ASSETS/
│   ├── SOUNDS/activation_sound.wav
│   ├── Vosk/  (ignored - download from vosk releases)
│   ├── porcupine/aura_windows.ppn (ignored - custom wakeword)
│   └── conversation_history.json (ignored - local memory)
├── BRAIN/
│   ├── AI/TEXT/API/            # 16 adapters + fixed HF host
│   ├── AI/TEXT/LOCAL/llama_CPP.py
│   ├── AI/TEXT/STREAM/
│   ├── AI/VISION/deepInfra_VISION.py
│   ├── AI/IMAGE/decohere_ai.py
│   └── TOOLS/emotion.py + groq_web_access.py
├── ENGINE/
│   ├── STT/ DevsDoCode.py, vosk_recog.py, whisper_offline.py, src/index.html (2s silence)
│   └── TTS/ edge_tts.py, voice_clone.py, DeepGram.py + STREAMING/
├── PROMPTS/ BISECTORS.py, INSTRUCTIONS.py
├── TOOLS/ Alpaca_DS_Converser.py, file_finder.py, task_board.py, AUDIO/, SYSTEM_SETTINGS/
├── PLAYGROUND/ CAMERA/ocr_live.py, gesture_control.py, WEBSITE_ASSISTANT/screen_see.py
└── WEB-3D/ index.html, app.js, style.css, skins.js, party.js  # audio-reactive ring + Whisper fallback
```
</details>

---

## Tech Stack

| Category | Technology | Version | Purpose |
|----------|------------|---------|---------|
| **Frontend / Runtime** | Python | 3.10+ (3.13 tested) | Core language |
| **Speech** | Selenium / Vosk / PyAudio | 4.45 / 0.3.45 / 0.2.14 | STT streaming + offline + mic |
| **Wakeword** | pvporcupine | 4.0.3 (or 1.9.5) | Hotword detection |
| **Audio** | pygame / playsound / opencv | 2.6.1 / 1.2.2 / 4.13 | Playback + vision |
| **LLM** | huggingface_hub / groq / webscout | 1.30 / 1.7 / 2026.6.14 | Inference + adapters |
| **TTS** | edge-tts / requests | 7.2.8 / 2.32 | Speech synthesis |
| **Util** | python-dotenv / googlesearch-python | 1.2.1 / 1.3 | Env + web search |
| **Build** | pip / venv | — | Dependency mgmt |

---

## Getting Started: Step-by-Step Guide (0 to 100)

Whether you are a seasoned developer or completely new to Python, this guide will take you from absolute zero to running AURA-AGI on your machine.

### Step 1: System Requirements & Prerequisites
Before you begin, ensure you have the following installed:
1. **Python 3.10 or higher**: Download it from [python.org](https://www.python.org/downloads/). 
   * **Important (Windows)**: During installation, make sure to check the box that says **"Add Python to PATH"**.
2. **Git**: Download and install from [git-scm.com](https://git-scm.com/downloads).
3. **Brave Browser (Recommended)** or **Google Chrome**: AURA uses Selenium for local speech-to-text, which works best with these browsers.
4. **A Working Microphone**: Make sure your default system microphone is active and not muted.

### Step 2: Download the Project
Open your terminal (Command Prompt, PowerShell, or macOS/Linux Terminal) and run:
```bash
git clone https://github.com/ShreyasP10/AURA-AGI.git
cd AURA-AGI
```

### Step 3: Set Up a Virtual Environment (Recommended)
It is highly recommended to install AURA's dependencies in an isolated environment so it doesn't conflict with other Python projects on your PC.
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Step 4: Install Dependencies
With your virtual environment active (you should see `(.venv)` in your terminal prompt), install the required Python packages:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
*(Note for Python 3.13 users: if Pygame fails to build, install the binary explicitly: `pip install -r requirements.txt --only-binary pygame`)*

### Step 5: Configure API Keys
AURA-AGI uses third-party AI models (Groq, OpenRouter) to think and process language. You need to provide API keys for these services.
1. Copy the `.env.example` file to create a new `.env` file:
   * **Windows (PowerShell)**: `Copy-Item .env.example .env`
   * **macOS/Linux**: `cp .env.example .env`
2. Open the `.env` file in any text editor (like Notepad or VS Code).
3. Get your free API keys and paste them into the file:
   * **GROQ_AI**: Get it for free at [console.groq.com](https://console.groq.com/)
   * **OPENROUTER**: Get it for free at [openrouter.ai/keys](https://openrouter.ai/keys)
   * **HUGGING_FACE_READ**: Get it for free at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

### Step 6: (Optional) Download Vosk for Offline Voice Recognition
If you want AURA to recognize your voice completely offline without using the browser fallback:
1. Download the Vosk small English model from [here](https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip).
2. Extract the downloaded `.zip` file.
3. Rename the extracted folder to `vosk-model-small-en-us-0.15` and place it inside the `ASSETS/Vosk/` directory in your AURA-AGI folder.

### Step 7: Run AURA-AGI
You are now ready to start the assistant! In your terminal, simply run:
```bash
# For Windows
$env:PYTHONIOENCODING="utf-8"
$env:AURA_BROWSER="brave"  # Or "chrome" if you prefer
python main.py

# For macOS/Linux
PYTHONIOENCODING="utf-8" AURA_BROWSER="brave" python3 main.py
```

### Step 8: How to Interact
* **Voice**: Just say **"aura"** followed by your command (e.g., *"Aura, what is the capital of France?"*).
* **Keyboard**: Press `Enter` to manually trigger the microphone, or type your query directly into the terminal and press `Enter`.
* **Stop**: If Aura is speaking and you want it to stop, just say or type **"stop"**, **"quiet"**, or **"cancel"**.
* **Exit**: Type `/quit` or press `Ctrl+C` to exit the application.

---

## Configuration

*Configure Keys* — AURA’s `.env` (must-have first):

| Key | Provider | Where to get | Free tier | Required? |
|-----|----------|--------------|-----------|-----------|
| `GROQ_AI` | Groq `openai/gpt-oss-20b` chat + emotion + file-finder | `console.groq.com` → `gsk_...` | **Generous free** | Recommended |
| `OPENROUTER` | OpenRouter website summarizer | `openrouter.ai/keys` → `sk-or-v1-...` (`:free` models) | $5 credit | For website summary |
| `HUGGING_FACE_READ` | HF Inference fallback chat | `huggingface.co/settings/tokens` → `hf_...` | Free | Fallback |
| `DECOHERE_AI` | `turbo.decohere.ai` | `decohere.ai` | Paid | Image only |
| `PICOVOICE_KEY` | Porcupine 4.x | `console.picovoice.ai` | Free | Or `pip install pvporcupine==1.9.5` |
| `ELEVENLABS_API_KEY` | Voice clone | `elevenlabs.io` | Limited | Optional (else edge-tts) |

**Minimal `.env`:**
```ini
GROQ_AI=gsk_...
OPENROUTER=sk-or-v1-...
HUGGING_FACE_READ=hf_...
```

**Runtime switches** (env vars, no code change):

| Var | Default | Effect |
|-----|---------|--------|
| `AURA_BROWSER` | `brave` | STT + cookie browser (`brave` with Chrome auto-fallback) |
| `AURA_HEADLESS` | `1` | `0` opens the browser window for mic debugging |
| `AURA_TEXT_MODE` | `0` | `1` keyboard-only, no browser/mic at all |
| `AURA_SILENCE_MS` | `3000` | Mic silence before turn ends (`800-8000`) |
| `AURA_FAST` | `1` | Realtime chat (early flush, 150-token cap, instant greetings) |
| `AURA_VOICE` | `1` | `0` text-only, zero TTS wait |
| `BRAVE_PATH` | auto-detect | Explicit `brave.exe` path if not found |

---

## How It Works
*How It Works* 5 steps:

1. **Choose Intent** — type or say `aura` + your wish (`generate image`, `what is in my hand`, `set dark theme`). No `aura` = casual chat. `stop` halts speech instantly.
2. **Capture** — Brave/Chrome Selenium STT (45s timeout, silence-based turn end), Vosk/whisper offline, or keyboard (`AURA_TEXT_MODE=1`).
3. **Classify** — fast local intents first (open/find/tasks/OCR/screen, zero LLM), then 3 parallel LLM checks decide *vision / image / system / website / chat*.
4. **Act** — best provider runs: LLaVA sees, Decohere draws, registry flips, or Groq chats with early sentence flush.
5. **Speak & Remember** — ordered TTS queue answers (in-process edge-tts, skips code/art), history saved to `conversation_history.json` for next turn.

---

## Data & Memory
AURA is local-first:

- **History** `TOOLS/Alpaca_DS_Converser.py` word-window `700` → `ASSETS/conversation_history.json` auto-saved on every turn.
- **Vosk models** `ASSETS/Vosk/` (large, gitignored).
- **Stream audios** `ASSETS/STREAM_AUDIOS/*.mp3` cleaned via `TOOLS/stream_audio_cleanup.py`.
- No cloud DB required — cloud only if you choose cloud LLMs.

---

## Troubleshooting — We’ve Been There

| You see | Why | Fix |
|---------|-----|-----|
| `UnicodeEncodeError charmap` @ `DevsDoCode.py` ❤️ | Windows cp1252 | `$env:PYTHONIOENCODING="utf-8"` |
| `getaddrinfo failed` @ `Hugging_Face_TEXT.py` | offline/no token | check Wi-Fi + `HUGGING_FACE_READ` |
| `pvporcupine missing access_key` | v4 breaking change | `pip install pvporcupine==1.9.5` or `PICOVOICE_KEY` |
| `pygame` build fail py313 | `distutils` removed, pinned `==2.5.2` | `pip install -r requirements.txt --only-binary pygame` (pins now `>=`) |
| `SessionNotCreatedException` / Brave window closes | Brave vs chromedriver mismatch or profile lock | `pip install -U selenium` + update Brave, or `AURA_BROWSER=chrome`, or `AURA_TEXT_MODE=1` |
| `NoSuchWindow: target window already closed` | browser already running with locked profile | close all Brave/Chrome windows; AURA uses isolated `%TEMP%\aura-*-profile` |
| `edge_tts NoAudioReceived` / missing mp3 | markdown/code spoken + concurrent throttle | auto-sanitized + serialized in-process synth; `AURA_VOICE=0` for text-only |
| `Listening...` hangs forever | Brave Shields blocks Google Speech / no mic | headed debug `AURA_HEADLESS=0`, allow mic, or Vosk offline / `AURA_TEXT_MODE=1` |
| Slow STT | browser roundtrip | switch `IMPORTS.py` to `vosk_recog`, or lower `AURA_SILENCE_MS` |

---

## What's New (v1.2 & v1.1)

**v1.2 Updates:**
- **Configuration Wizard:** Added `configure.py` for a smooth, interactive setup of API keys and preferences.
- **One-Click Installers:** `install.ps1` and `install.sh` scripts for fully automated setup of environments and dependencies.
- **Bulletproof Fallback Chains:** Added exponential backoff retry loops for LLMs, and a deep fallback cascade (`Groq -> OpenRouter -> DeepInfra -> HF`) in the main loop to ensure the assistant never crashes during API outages.
- **Vosk Default STT:** Automatically defaults to the much faster Vosk local STT backend if the model is detected, bypassing browser Selenium fragility.
- **Docker Security:** Added a comprehensive `.dockerignore` to secure API keys and prevent cache bloat.

**v1.1 Updates:**
- **TTS Concurrency Engine:** Fixed overlapping and repeating audio bugs in `edge_tts`. Sentences are now correctly queued with unique file IDs and a global playback lock, ensuring smooth, uninterrupted streaming voice.
- **Intent Classifier Overhaul:** Rewritten the core intent classifiers (`BISECTORS`) to use the lightning-fast Groq API (`llama-3.1-8b-instant`), bypassing DeepInfra's new web security locks. This fully restores **System Controls** (theme/taskbar) and **Image Generation**.
- **AURA Persona Upgrade:** Replaced the amnesiac/confused persona with a highly intelligent, helpful AI assistant (`human_response_v3_AVA`). AURA will now properly explain complex topics like CNNs instead of refusing.
- **Syntax & Stability:** Formatted the entire codebase using `ruff` and safely patched over 1,500 lines of bare `except:` blocks for flawless runtime stability.

---

## Roadmap — What’s Next (We’d love your ideas!)

- [x] **Your own wakeword** — `aura*.ppn` auto-detect + `custom_wakeword.md` guide (jarvis builtin fallback)
- [x] **Whisper offline** — `whisper_offline.py` (`faster-whisper`) fallback path
- [x] **Rich terminal UI** — opencode-style panels, hybrid voice+type, `/voice` + `/quit`
- [ ] **One-click installer** — auto-updates

> Got an idea? Open an issue — we build with the community, not just for it.

---

## Documentation Index

| # | Doc | Status |
|---|-----|--------|
| 1 | `PROMPTS/BISECTORS.py` — classifiers | Draft |
| 2 | `PROMPTS/INSTRUCTIONS.py` — AVA persona | Draft |
| 3 | `ENGINE/STT/DevsDoCode.py` — STT | Draft |
| 4 | `BRAIN/AI/VISION/deepInfra_VISION.py` — Vision | Draft |
| 5 | `TOOLS/Alpaca_DS_Converser.py` — Memory | Draft |
| 6 | `readme.md` — this file | Production |

Conventions: `FR-xx` features, `NFR-xx` non-functional, timestamps epoch ms if you export.

---

## Contributing

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/Amazing`)
3. Commit your Changes (`git commit -m 'feat: Amazing'`)
4. Push to the Branch (`git push origin feature/Amazing`)
5. Open a Pull Request to `ShreyasP10/AURA-AGI:main` or `readme`

---

## License
MIT — see [LICENCE](LICENCE).

---

## Authors

| Contributor | Role | GitHub |
|-------------|------|--------|
| **Shreyas Pawar** | Lead Developer (AURA-AGI) | [@ShreyasP10](https://github.com/ShreyasP10) |
| **Atharva Mahajan** | Contributor | [@mahajanatharva1042](https://github.com/mahajanatharva1042) |

<div align="center">
  <a href="https://github.com/ShreyasP10/AURA-AGI"><img alt="ShreyasP10" src="https://img.shields.io/badge/ShreyasP10-181717?style=for-the-badge&logo=github"></a>
  <a href="https://github.com/mahajanatharva1042"><img alt="AtharvaMahajan" src="https://img.shields.io/badge/mahajanatharva1042-181717?style=for-the-badge&logo=github"></a>
</div>

---

*Made with ❤️ in India — for students, builders and dreamers.*
