# Nemo Public Architecture

## Public vs. Proprietary Modules

### ✅ Public (Open-Source, Visible)

**Speech-to-Text Engine**
- `nemo/systems/task-screen-simulator/voice_input.py`
- Multi-engine fallback (Google → Sphinx → Bing)
- Configurable energy threshold and microphone
- Full implementation visible for community contribution

**Gemini Integration**
- `nemo/systems/task-screen-simulator/gemini_handler.py`
- Voice + screenshot capture pipeline
- API documentation in TECHNICAL.md
- Users can extend with custom models

**Hotkey Framework**
- `nemo/systems/task-screen-simulator/keyboard_hotkeys.py`
- Keyboard event detection and debouncing
- Callback system for custom hotkeys
- Full source available for customization

**Core Orchestrator**
- `nemo/core/buttons_start_new.py`
- Hotkey-to-action routing
- Module loading system
- Configuration management

### 🔒 Proprietary (Closed-Source, Not Visible)

**Temporal Rewind Engine** (RIGHT ALT + LEFT)
- Keystroke behavior synthesis (not recording)
- Activity classification and pattern matching
- Natural language narrative generation
- Competitive advantage: inference without data retention

**Temporal Forward Prediction** (RIGHT ALT + RIGHT)
- Future context prediction
- Behavioral trend extrapolation
- Coming in v1.1+

**Agentic Synthesis** (RIGHT ALT + UP)
- File extraction with temporal context wrapping
- Multi-turn conversation management with artifacts
- Coming in v1.1+

---

## Why This Architecture?

### Transparency + Innovation Balance

**Open-Source Benefits** ✅
- Users see what we claim: no data retention
- Community can audit safety-critical code (STT, Gemini)
- Developers can extend the hotkey framework
- Builds trust through visibility

**Competitive Moat** ✅
- Temporal synthesis (rewind/forward) is proprietary
- Agentic reasoning engine is protected
- Implementation details of behavior analysis hidden
- Architecture is defensible for licensing/partnerships

**User Privacy** ✅
- Can inspect voice_input.py to verify no persistence
- Can inspect gemini_handler.py to verify screenshot handling
- Can verify keyboard_hotkeys.py has no telemetry
- Proprietary modules are *more* secure (less surface for attack)

---

## Public API Documentation

Users and developers can integrate with Nemo via documented APIs:

### VoiceInput Module (Public)

```python
from nemo.systems.task_screen_simulator.voice_input import VoiceInput, VoiceInputConfig

config = VoiceInputConfig(
    mic_timeout=5,
    energy_threshold=300,
    language='en-US'
)

voice = VoiceInput(config)
voice.start()

# When RIGHT SHIFT pressed, this fires
def on_transcribed(text):
    print(f"User said: {text}")

voice.on_transcribed_callback = on_transcribed
```

### GeminiHandler Module (Public)

```python
from nemo.systems.task_screen_simulator.gemini_handler import GeminiHandler, GeminiConfig

config = GeminiConfig(
    api_key=os.getenv('GEMINI_API_KEY'),
    screenshot_enabled=True,
    global_context=True
)

gemini = GeminiHandler(config)
response = gemini.process_voice_with_screenshot(
    voice_text="Analyze this screenshot",
    screenshot_path="screenshot.png"
)
```

### KeyboardHotkeys Module (Public)

```python
from nemo.systems.task_screen_simulator.keyboard_hotkeys import KeyboardHotkeys

hotkeys = KeyboardHotkeys()

# Register custom hotkey
hotkeys.register_callback('custom_action', my_handler_function)

# Listen for system-wide hotkeys
hotkeys.start()
```

### Proprietary Module Interface (Black Box)

```python
# Users don't see implementation, just interface

# Rewind engine available but internals protected
from nemo.systems.task_screen_simulator import temporal_rewind
result = temporal_rewind.infer_past_activity(minutes_back=5)
# Returns: "You were coding in VS Code 3 minutes ago, switched to email 1 minute ago"

# Forward engine (coming soon)
from nemo.systems.task_screen_simulator import temporal_forward
prediction = temporal_forward.predict_next_activity()
```

---

## Repository Structure

```
nemo/
├── README.md                          # Public - describes open/closed modules
├── API-DOCUMENTATION.md               # Public - how to use modules
├── .gitignore                         # Excludes proprietary .pyc, __pycache__
├── nemo/
│   ├── core/
│   │   └── buttons_start_new.py       # ✅ PUBLIC - hotkey orchestrator
│   └── systems/
│       └── task-screen-simulator/
│           ├── voice_input.py         # ✅ PUBLIC - STT engine
│           ├── gemini_handler.py      # ✅ PUBLIC - Gemini integration
│           ├── keyboard_hotkeys.py    # ✅ PUBLIC - keyboard framework
│           ├── temporal_rewind.py     # 🔒 PROPRIETARY - not in repo
│           ├── temporal_forward.py    # 🔒 PROPRIETARY - not in repo
│           └── agentic_synthesis.py   # 🔒 PROPRIETARY - not in repo
├── docs/
│   └── index.html                     # ✅ PUBLIC - website
├── MARKETING.md                       # ✅ PUBLIC - v2 marketing guide
├── TECHNICAL.md                       # ✅ PUBLIC - v2 technical guide
└── DATA-OWNERSHIP-INVISIBILITY.md     # ✅ PUBLIC - privacy promise
```

---

## .gitignore Strategy

```
# Proprietary modules (not committed)
nemo/systems/task-screen-simulator/temporal_rewind.py
nemo/systems/task-screen-simulator/temporal_forward.py
nemo/systems/task-screen-simulator/agentic_synthesis.py

# Binary artifacts
*.pyc
__pycache__/
*.so

# API keys
.env
.env.local
```

When users install Nemo, proprietary modules are:
- Downloaded as pre-compiled `.pyd` (Windows) or `.so` (Linux/Mac)
- Included in releases but not in source repo
- Treated as black boxes (can't inspect, but can use)

---

## Distribution Strategy

### Source Distribution (GitHub)
- Public modules visible
- README explains architecture
- Users can fork and extend public APIs
- Clear documentation of what's proprietary

### Binary Distribution (Releases)
- Pre-compiled wheel includes proprietary modules
- Users get full functionality out-of-the-box
- Compiled code is harder to reverse-engineer
- Version-specific (protects against tampering)

### For Developers
```bash
pip install nemo  # Gets all modules including proprietary

# Source inspection
git clone https://github.com/torresjchristopher/nemo.git
# Will see public modules, documentation for proprietary ones
```

---

## Messaging to Users

### In README.md

> **Nemo combines open innovation with proprietary intelligence.**
>
> **Open-Source Components** (inspect and customize):
> - Voice-to-text engine (multi-fallback STT)
> - Gemini integration (voice + screenshot pipeline)
> - Hotkey framework (build your own hotkeys)
>
> **Proprietary Components** (trusted black box):
> - Temporal rewind inference (behavior synthesis)
> - Temporal forward prediction (trend extrapolation)
> - Agentic synthesis engine (file extraction + context)
>
> Our transparency builds trust. Our intellectual property builds moat.

### Privacy Assurance

> You can audit the code that handles your voice and screenshots. The temporal reasoning that understands your behavior is proprietary because *understanding without recording* is our competitive advantage.

---

## Future: Selective Open-Sourcing

As Nemo matures:

**Year 1 (Now)**: Voice, Gemini, Hotkeys open. Temporal/Agentic closed.

**Year 2**: Could open-source rewind engine (if product is differentiated enough)

**Year 3+**: Possible full open-source after fundraising/acquisition

But nothing is permanent—you control this based on business strategy.

---

## Competitive Protection

This hybrid approach protects against:

✅ **Code Copying**: Hard to copy compiled modules
✅ **Architecture Theft**: Implementation details hidden
✅ **Model Extraction**: Temporal synthesis logic proprietary
✅ **User Trust**: Can audit safety-critical code
✅ **Partnerships**: Clear IP for licensing deals

---

**Summary**: Nemo is open where it builds trust (voice, Gemini, transparency) and closed where it builds moat (temporal reasoning, agentic synthesis).
