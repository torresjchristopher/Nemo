# Project Nemo - AI-Powered Temporal Keyboard Assistant

> **Data Invisibility Guaranteed** | Keyboard-driven AI | Temporal Reasoning | Zero Persistence

## Overview

Nemo is a revolutionary personal AI assistant built on a **5-hotkey system** that emphasizes **data invisibility**—your data never persists. It combines keyboard orchestration with temporal reasoning (rewind/forward) to understand user intent in real-time.

## Architecture

```
Yukora/
├── nemo/                          # This repository
│   ├── nemo/
│   │   ├── core/                 # Main orchestrator
│   │   ├── cli/                  # Command-line interface
│   │   └── keys/                 # Modular key implementations
│   │       ├── right_shift_stt/         # Speech-to-text (PUBLIC)
│   │       ├── right_alt_gemini/        # Gemini voice AI (PUBLIC)
│   │       ├── right_alt_left_rewind/   # Rewind engine (PROPRIETARY)
│   │       ├── right_alt_right_forward/ # Forward prediction (PROPRIETARY)
│   │       └── right_alt_up_agent/      # Agentic synthesis (PROPRIETARY)
│   └── README.md
├── scriptcommander/               # Legacy CLI tool
├── portfolio/                     # Portfolio projects
└── memory_app/                    # Memory management application
```

## The 5 Hotkeys

| Key | Function | Status |
|-----|----------|--------|
| **RIGHT SHIFT** | Speech-to-text (hold to record) | ✅ Working |
| **RIGHT ALT** | Gemini voice AI + screenshot | ✅ Working |
| **RIGHT ALT + LEFT** | Rewind (temporal reversal) | 🚧 Testing |
| **RIGHT ALT + RIGHT** | Forward (temporal prediction) | ⏳ Pending |
| **RIGHT ALT + UP** | Agentic synthesis | ⏳ Pending |

## Data Ownership & Invisibility

✅ **Zero persistent storage** - No databases, no profiles, no logs
✅ **Real-time processing** - In-memory only
✅ **You own your data** - Nothing sent to external servers without consent
✅ **Temporal reasoning** - Understands context without storing context

See [DATA-OWNERSHIP.md](docs/DATA-OWNERSHIP.md) for details.

## NEMO CODE - The Secret Sauce

Nemo's rewind is powered by **NEMO CODE**, a proprietary keystroke reversal library:

```
User types: "hello"
NEMO CODE: ['backspace', 'backspace', 'backspace', 'backspace', 'backspace']
Rewind: Press all 5 backspaces in order → "hello" disappears
```

**Why it works:**
- Ultra-lightweight (87 entries, 1-2 byte per keystroke)
- Zero state tracking (just keystroke → instruction mapping)
- O(1) lookup and O(1) execution per keystroke
- 5-minute rolling window (5000 max keystrokes)

See [nemo/keys/right_alt_left_rewind/NEMO_CODE_ANALYSIS.md](nemo/keys/right_alt_left_rewind/NEMO_CODE_ANALYSIS.md) for technical details.

## Installation

```bash
cd C:\Users\serro\Yukora\nemo
pip install -r requirements.txt
python -m nemo.cli.buttons_start
```

**Requirements:**
- Python 3.8+
- `keyboard` library (system-level hotkey capture)
- `speech_recognition` (STT)
- `google-generativeai` (Gemini integration)
- `pyaudio` (microphone input)

## Public vs. Proprietary

### Public Modules (Auditable)
- `nemo/keys/right_shift_stt/` - Speech-to-text engine
- `nemo/keys/right_alt_gemini/` - Gemini integration

Users can audit, fork, and extend these.

### Proprietary Modules (Competitive Moat)
- `nemo/keys/right_alt_left_rewind/` - NEMO CODE reversal
- `nemo/keys/right_alt_right_forward/` - Temporal prediction
- `nemo/keys/right_alt_up_agent/` - Agentic synthesis

Source code excluded from git. Distributed as compiled bytecode in releases.

## Testing NEMO CODE

```bash
cd nemo/keys/right_alt_left_rewind/
python test_nemo_code.py
```

Current status: **18/27 tests passing** (Phase 1 complete)

Remaining gaps: Shift combinations, Caps Lock, Ctrl+V (paste tracking)

## Development Philosophy

1. **Modularity** - Each hotkey has its own folder for independent development
2. **Simplicity** - Simpler is better. No unnecessary state tracking.
3. **Performance** - Latency is critical. O(1) operations everywhere.
4. **Data Invisibility** - Nothing persists unless explicitly requested.
5. **Transparency** - Public code builds trust. Proprietary code protects innovation.

## Roadmap

### Phase 1: Foundation ✅
- [x] 5-hotkey framework
- [x] Speech-to-text (RIGHT SHIFT)
- [x] Gemini integration (RIGHT ALT)
- [x] NEMO CODE rewind logic
- [x] Modular architecture

### Phase 2: Completion 🚧
- [ ] Integrate NEMO CODE with keyboard listener
- [ ] Add Shift combination handling
- [ ] Test rewind latency
- [ ] Forward prediction engine (RIGHT ALT + RIGHT)

### Phase 3: Advanced ⏳
- [ ] Caps Lock state tracking
- [ ] Paste length tracking (Ctrl+V)
- [ ] Agentic synthesis (RIGHT ALT + UP)
- [ ] Multi-application context awareness

## License

**Nemo** is proprietary software. Public modules are auditable. Proprietary modules are distributed under commercial license.

---

**Built for data invisibility. Powered by temporal reasoning.**

For more info: https://downloadnemo.com
