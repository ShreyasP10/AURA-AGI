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
Your voice is the command line. AURA listens continuously and respects `aura` as wakeword.

| Feature | Description |
|---------|-------------|
| **`aura` wakeword** | Prefix or suffix: `aura what is capital` or `what is capital aura` → routed; otherwise continuous chat `main.py:50` |
| **Selenium STT** | `ENGINE/STT/DevsDoCode.py` headless Chrome → `realtime-stt-devs-do-code.netlify.app` streaming, language `en-IN` |
| **Offline STT** | Vosk `vosk_recog.py` + `NetHyTech` alternative (`IMPORTS.py:9`) — no internet needed |
| **Hotword Detection** | `TOOLS/AUDIO/Hotword_Detection.py` `pvporcupine` (jarvis model → mapped to AURA) with activation sound |
| **Interruptible Playback** | `Interrupted_Playsound.py` `pygame.mixer` + `stop_event` threads — interrupt mid-sentence, it listens again |

### 🧠 LLM Router — Your Intent, Best Brain
One utterance → 3 parallel classifications → best provider.

| Feature | Description |
|---------|-------------|
| **Parallel Classification** | 3x `deepInfra_TEXT.generate()` fan-out `main.py:54` with `BISECTORS.image_requests_v3` + `complex_task_classifier_v6` + `INSTRUCTIONS.human_response_v3_AVA` |
| **Provider Zoo (16 adapters)** | `BRAIN/AI/TEXT/API/` — DeepInfra, OpenRouter, Groq (`llama3-70b-8192`), HuggingFace, Pi, Liaobots, Phind, etc. |
| **Local LLM** | `BRAIN/AI/TEXT/LOCAL/llama_CPP.py` — fully offline via `llama.cpp` |
| **Streaming** | `BRAIN/AI/TEXT/STREAM/` sentence-level TTS streaming |

### 🖼️ Vision & Image — See & Create
| Feature | Description |
|---------|-------------|
| **Real-time Vision** | `PLAYGROUND/CAMERA/camera_vision.py` `cv2.VideoCapture(0)` → `BRAIN/AI/VISION/deepInfra_VISION.py` LLaVA 1.5 `vision_realtime_v1` |
| **Image Generation** | `BRAIN/AI/IMAGE/decohere_ai.py` → `turbo.decohere.ai` (steps/seed/enhance, safety filter) |

### 🌐 Web & Automation — Act, Don’t Just Answer
| Feature | Description |
|---------|-------------|
| **Website Assistant** | `PLAYGROUND/WEBSITE_ASSISTANT/jenna_reader.py` + `chrome_latest_url.py` → `openrouter` summarization |
| **Web Search** | `TOOLS/Web_Results.py`, `BRAIN/TOOLS/groq_web_access.py` tool-call `get_web_info` |
| **Code Execution** | `TOOLS/RawDog.py` `webscout.AIutel.RawDog` (opt-in, `confirm_script=False`) |
| **System Control** | `TOOLS/SYSTEM_SETTINGS/system_theme.py` + `taskbar.py` — dark/light, taskbar align/temperature via registry |

### 🔊 TTS — Voices That Stay With You
Drawing toolbar equivalent for voice: pick your voice, color your reply.

| Feature | Description |
|---------|-------------|
| **Voices** | Speechify default `ENGINE/TTS/speechify.py`, EdgeTTS, DeepGram, ElevenLabs, StreamElements, `STREAMING/DeepGram.py` |
| **Sticky Notes Analogy** | Persistent `conversation_history.json` = your sticky notes that never fall off |

### 💾 Memory & Playground
| Feature | Description |
|---------|-------------|
| **Conversation Manager** | `TOOLS/Alpaca_DS_Converser.py` word-window `history_offset=700` → `ASSETS/conversation_history.json` |
| **Playground** | ADB calls `PLAYGROUND/ADB_CALL/`, CLAP audio classifier `CLAP_NN/`, proxy `ProxyAPI.py` |

---

## Supported Intents & Commands

| Intent | Example Utterance | Route | Output |
|--------|-------------------|-------|--------|
| **Image** | `aura generate image of futuristic city` | `BISECTORS.image_requests_v3` → `decohere_ai` | `ASSETS/image.jpg` + `Sure Sir, Generating...` |
| **System Control** | `aura set dark theme` / `move taskbar left` | `system control` → `system_theme`/`taskbar` | Registry flip + toast `TOOLS/SYSTEM_SETTINGS/Alarms.py` |
| **Vision** | `aura what is in my hand` | `vision` → `camera_vision` + `deepInfra_VISION` | `You are holding a pen` |
| **Website** | `aura summarize this website` | `website` → `jenna_reader` + `openrouter` | Short summary via `Salli` voice |
| **Call** | `aura call mum` | `call` → `PLAYGROUND/ADB_CALL/make_call.py` (stub) | `Sure Sir. Calling` |
| **Chat** | `aura hello` / `hello` (no wakeword) | `default` `human_response_v3_AVA` / `Hugging_Face_TEXT` | AVA persona + history persist |

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

| Path | What it is |
|------|------------|
| `main.py` | Entry loop, wakeword `aura` dispatch `main.py:50` |
| `IMPORTS.py` | Central aggregator — STT/TTS/BRAIN/TOOLS wiring |
| `PROMPTS/` | `BISECTORS.py` classifiers, `INSTRUCTIONS.py` AVA persona, `SYSTEM.py` |
| `BRAIN/AI/TEXT/API/` | 16 LLM adapters |
| `BRAIN/AI/TEXT/LOCAL/` | `llama_CPP.py` offline |
| `BRAIN/AI/VISION/` | `deepInfra_VISION.py` LLaVA |
| `BRAIN/AI/IMAGE/` | `decohere_ai.py` |
| `ENGINE/STT/` | `DevsDoCode.py`, `vosk_recog.py`, `NetHyTech.py`, `src/index.html` |
| `ENGINE/TTS/` | `speechify.py`, `edge_tts.py`, `DeepGram.py` + `STREAMING/` |
| `TOOLS/` | `Alpaca_DS_Converser.py`, `Hotword_Detection.py`, `RawDog.py`, `SYSTEM_SETTINGS/` |
| `PLAYGROUND/` | `CAMERA/`, `WEBSITE_ASSISTANT/`, `ADB_CALL/`, `CLAP_NN/` |
| `ASSETS/` | `SOUNDS/`, `Vosk/`, `conversation_history.json`, `STREAM_AUDIOS/` |
| `requirements.txt` | Pinned deps (python-dotenv, groq, webscout…) |

<details>
<summary>Full tree (click to expand)</summary>

```
AURA-AGI/
├── .env / .env.example
├── main.py
├── IMPORTS.py
├── requirements.txt
├── ASSETS/
│   ├── SOUNDS/activation_sound.wav
│   ├── Vosk/vosk-model-small-en-us-0.15/
│   ├── STREAM_AUDIOS/
│   └── conversation_history.json
├── BRAIN/
│   ├── AI/TEXT/API/            # 16 adapters
│   ├── AI/TEXT/LOCAL/llama_CPP.py
│   ├── AI/TEXT/STREAM/
│   ├── AI/VISION/deepInfra_VISION.py
│   ├── AI/IMAGE/decohere_ai.py
│   └── TOOLS/groq_web_access.py
├── ENGINE/
│   ├── STT/DevsDoCode.py
│   └── TTS/speechify.py, edge_tts.py, DeepGram.py + STREAMING/
├── PROMPTS/BISECTORS.py, INSTRUCTIONS.py
├── TOOLS/AUDIO/, SYSTEM_SETTINGS/, Alpaca_DS_Converser.py
└── PLAYGROUND/CAMERA/, WEBSITE_ASSISTANT/, ADB_CALL/, CLAP_NN/
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

## Getting Started

### Prerequisites
- **Python 3.10+** + **Google Chrome** + **Microphone** + **Git**
- Windows recommended (registry system control), macOS/Linux works for voice/vision

### Quick Start for Users (No Code)
1. **Clone**: `git clone https://github.com/ShreyasP10/AURA-AGI.git && cd AURA-AGI`
2. **Env**: `Copy-Item .env.example .env` → fill one key (see Configuration)
3. **Run**: `$env:PYTHONIOENCODING="utf-8"; python main.py` → say `aura hello`
4. **No install needed** for chat — just speak. Vision needs camera permission.

### Setup for Developers (Full Build)
```bash
git clone https://github.com/ShreyasP10/AURA-AGI.git
cd AURA-AGI
Copy-Item .env.example .env   # fill GROQ_AI / OPENROUTER / HUGGING_FACE_READ

# install (py313 needs binary pygame)
pip install --upgrade pip
pip install pygame --only-binary :all:
pip install playsound==1.2.2 huggingface_hub python-dotenv requests edge-tts opencv-python pvporcupine vosk groq googlesearch-python webscout

# verify
python -c "import sys; sys.stdout.reconfigure(encoding='utf-8'); import IMPORTS; print('OK')"

# Vosk offline (optional)
# download https://github.com/alphacep/vosk-api/releases → ASSETS/Vosk/
python -c "from ENGINE.STT.vosk_recog import speech_to_text; print(list(speech_to_text('ASSETS/Vosk/vosk-model-small-en-us-0.15'))[:1])"

# push your branch
git checkout -b feature/amazing
git push -u origin feature/amazing
```

---

## Configuration

*Configure Keys* + Firebase setup — AURA’s `.env`:

| Key | Provider | Where to get | Free tier | Required? |
|-----|----------|--------------|-----------|-----------|
| `GROQ_AI` | Groq `llama3-70b-8192` `BRAIN/TOOLS/groq_web_access.py:64` | `console.groq.com` → `gsk_...` | **Generous free** | Recommended |
| `OPENROUTER` | OpenRouter `openrouter.py:69` | `openrouter.ai/keys` → `sk-or-v1-...` (`:free` models) | $5 credit | For website `main.py:101` |
| `HUGGING_FACE_READ` | HF Inference `Hugging_Face_TEXT.py:46` | `huggingface.co/settings/tokens` → `hf_...` | Free | Fallback `main.py:118` |
| `DEEPINFRA` | DeepInfra (scrapes without) | `deepinfra.com` | $5 | Optional |
| `DECOHERE_AI` | `turbo.decohere.ai` | `decohere.ai` | Paid | Image only |
| `PICOVOICE_KEY` | Porcupine 4.x | `console.picovoice.ai` | Free | Or `pip install pvporcupine==1.9.5` |

**Minimal `.env`:**
```ini
GROQ_AI=gsk_...
OPENROUTER=sk-or-v1-...
HUGGING_FACE_READ=hf_...
```

---

## How It Works
*How It Works* 5 steps:

1. **Choose Intent** — say `aura` + your wish (`generate image`, `what is in my hand`, `set dark theme`).
2. **Capture** — Selenium STT streams your voice, or Vosk offline; `listener.listen()` `main.py:48`.
3. **Classify** — 3 parallel LLM checks decide *vision / image / system / website / chat*.
4. **Act** — best provider runs: LLaVA sees, Decohere draws, registry flips, or HF chats.
5. **Speak & Remember** — interruptible TTS answers, history saved to `conversation_history.json` for next turn.

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
| `UnicodeEncodeError charmap` @ `DevsDoCode.py:34` ❤️ | Windows cp1252 | `$env:PYTHONIOENCODING="utf-8"` |
| `getaddrinfo failed` @ `Hugging_Face_TEXT.py:73` | offline/no token | check Wi-Fi + `HUGGING_FACE_READ` |
| `pvporcupine missing access_key` | v4 breaking change | `pip install pvporcupine==1.9.5` or `PICOVOICE_KEY` |
| `pygame` build fail py313 | `distutils` removed | `pip install pygame --only-binary :all:` |
| Slow STT | netlify roundtrip | switch `IMPORTS.py:9` to `vosk_recog` |

---

## Roadmap — What’s Next (We’d love your ideas!)

- [ ] **Your own wakeword** — train `aura` `.ppn` properly
- [ ] **Whisper offline** — no internet, no problem
- [ ] **Beautiful UI** — sidebar, dark/light `ThemeManager`
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
