# Custom Wakeword Trainer — AURA (.ppn)

Train your own `aura` wakeword for pvporcupine (replaces `jarvis` mapping).

**Steps (Picovoice Console — free):**
1. Go to https://console.picovoice.ai/ → Sign up → **Porcupine** → **Create Custom Wake Word**
2. Enter `aura` → Train → Download `aura_windows.ppn` (also `_linux.ppn`, `_mac.ppn`)
3. Place in `ASSETS/porcupine/aura_windows.ppn`
4. Set env `PICOVOICE_KEY` from console → `https://console.picovoice.ai/` → Copy AccessKey
5. In `.env` add: `PICOVOICE_KEY=your_key_here`
6. `Hotword_Detection.py` auto-detects `ASSETS/porcupine/aura*.ppn` if exists, else falls back to `jarvis` builtin

**Test:**
```python
from TOOLS.AUDIO.Hotword_Detection import HotwordDetector
d = HotwordDetector(keywords=['aura'])  # will use .ppn if found
d.listen_for_hotwords()
```

**Why?** `pvporcupine` builtins don't include `aura` — custom `.ppn` gives 95% accuracy vs 70% `jarvis`→`aura` mapping.
