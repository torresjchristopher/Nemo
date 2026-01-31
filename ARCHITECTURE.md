# Nemo OOP Architecture - Tools & Keys Framework

## Core Philosophy

**Clean separation of concerns:**
- **Tools** (`nemo/tools/`): Reusable technology components
- **Keys** (`nemo/keys/`): Unique hotkey implementations that USE tools

Each key is a class extending `NemoKey`. Each tool is a class that any key can import and use.

---

## Architecture Overview

```
NemoEngine (Orchestrator)
    ↓
    Manages all registered keys
    ├── RIGHT SHIFT (SpeechToTextKey)
    ├── RIGHT ALT (GeminiVoiceKey)
    ├── RIGHT ALT + LEFT (RewindKey)
    ├── RIGHT ALT + RIGHT (ForwardKey)
    └── RIGHT ALT + UP (AgentSynthesisKey)
    
Each Key Uses Tools:
    ├── AudioCapture → microphone input
    ├── ScreenCapture → screenshot
    ├── KeystrokeProcessor → NEMO CODE (proprietary)
    └── TemporalReasoner → rewind/forward (proprietary)
```

---

## Tools: Reusable Technology Components

### Public Tools (Auditable)

#### NemoEngine
**Location:** `nemo/tools/nemo_engine/`

Core orchestrator. Manages:
- Hotkey registration
- Event routing (press/hold/release)
- Global configuration
- Status monitoring

```python
from nemo.tools import NemoEngine

engine = NemoEngine()
engine.register_key(my_key)
engine.on_key_press('right shift')
```

#### NemoKey (Base Class)
**Location:** `nemo/tools/nemo_key/`

Abstract base class. Every key extends this.

Lifecycle hooks:
- `on_press()` - Called when key pressed
- `on_hold(duration)` - Called while held
- `on_release(total_duration)` - Called when released
- `execute()` - Execute key logic

```python
from nemo.tools import NemoKey

class MyKey(NemoKey):
    def on_press(self):
        print("Key pressed!")
    
    def on_hold(self, duration):
        print(f"Held for {duration}s")
    
    def on_release(self, total_duration):
        print(f"Released after {total_duration}s")
```

#### AudioCapture
**Location:** `nemo/tools/audio_capture/`

Microphone input abstraction. Used by:
- RIGHT SHIFT (speech-to-text)
- RIGHT ALT (Gemini voice)

```python
from nemo.tools import AudioCapture

audio = AudioCapture(energy_threshold=300)
audio.start_recording()
# ... record audio ...
transcript = audio.stop_recording()
```

#### ScreenCapture
**Location:** `nemo/tools/screen_capture/`

Screenshot abstraction. Used by:
- RIGHT ALT (Gemini with screenshots)
- RIGHT ALT + UP (Agent synthesis)

```python
from nemo.tools import ScreenCapture

screen = ScreenCapture()
screenshot_bytes = screen.capture()
screenshot_base64 = screen.capture_base64()  # For API calls
```

---

### Proprietary Tools (Compiled Only)

#### KeystrokeProcessor
**Location:** `nemo/tools/keystroke_processor/`
**Status:** PROPRIETARY - Source excluded from git, distributed as bytecode

NEMO CODE management:
- Track keystrokes
- Generate reverse instructions
- Execute NEMO CODE

Used by:
- Rewind key
- Forward key (proprietary logic)

---

#### TemporalReasoner
**Location:** `nemo/tools/temporal_reasoner/`
**Status:** PROPRIETARY - Source excluded from git, distributed as bytecode

Temporal inference:
- Understand keystroke sequences
- Predict next actions
- Reason about screen state changes

Used by:
- Rewind key
- Forward key
- Agent synthesis key

---

## Keys: Unique Hotkey Implementations

Each key folder contains:
- `__init__.py` - Module marker
- `config.py` - Key configuration
- `implementation.py` (or module) - Key class extending NemoKey

### Example: Speech-to-Text Key

**Location:** `nemo/keys/right_shift_stt/`

```python
from nemo.tools import NemoKey, AudioCapture

class SpeechToTextKey(NemoKey):
    def __init__(self):
        super().__init__(
            key_name="Speech-to-Text",
            key_combo="right shift",
            description="Hold to record and transcribe"
        )
        self.audio = AudioCapture()
    
    def on_press(self):
        self.audio.start_recording()
    
    def on_hold(self, duration):
        pass  # Keep recording
    
    def on_release(self, total_duration):
        transcript = self.audio.stop_recording()
        print(f"Transcribed: {transcript}")
```

### Example: Gemini Voice Key

**Location:** `nemo/keys/right_alt_gemini/`

Uses both `AudioCapture` and `ScreenCapture`:

```python
from nemo.tools import NemoKey, AudioCapture, ScreenCapture

class GeminiVoiceKey(NemoKey):
    def __init__(self):
        super().__init__(...)
        self.audio = AudioCapture()
        self.screen = ScreenCapture()
    
    def on_release(self, total_duration):
        transcript = self.audio.stop_recording()
        screenshot = self.screen.capture_base64()
        
        # Send to Gemini with context
        response = gemini.query(
            prompt=transcript,
            image=screenshot
        )
        print(response)
```

---

## Adding New Keys

### Process

1. Create folder under `nemo/keys/new_key_name/`
2. Create class extending `NemoKey`:

```python
# nemo/keys/my_key/implementation.py
from nemo.tools import NemoKey, AudioCapture  # Import tools

class MyKey(NemoKey):
    def __init__(self):
        super().__init__(
            key_name="My Key",
            key_combo="right ctrl",  # Your hotkey
            description="What it does"
        )
        self.audio = AudioCapture()
    
    def on_press(self):
        # Your logic
        pass
    
    def on_hold(self, duration):
        pass
    
    def on_release(self, total_duration):
        # Execute key logic using tools
        pass
```

3. Register with engine:

```python
engine = NemoEngine()
engine.register_key(MyKey())
```

That's it! Your key now has:
- ✅ Lifecycle management
- ✅ Configuration support
- ✅ Status tracking
- ✅ Access to all tools

---

## Public vs. Proprietary

### What's Public (Auditable)
- `NemoEngine` - Orchestrator logic
- `NemoKey` - Base class
- `AudioCapture` - Microphone wrapper
- `ScreenCapture` - Screenshot wrapper
- All key implementations (except rewind/forward/agent)

Users can review, audit, and verify data handling.

### What's Proprietary (Bytecode Only)
- `KeystrokeProcessor` - NEMO CODE reversal
- `TemporalReasoner` - Temporal inference
- Rewind/Forward/Agent key implementations

Competitive advantage. Distributed compiled only.

---

## Benefits of This Architecture

✅ **Modularity** - Tools are independently testable
✅ **Reusability** - One tool, many keys
✅ **Scalability** - Add new keys without modifying tools
✅ **Maintainability** - Clean separation of concerns
✅ **Auditability** - Public tools fully transparent
✅ **Security** - Proprietary logic protected
✅ **Testability** - Each tool has unit tests

---

## Next Steps

1. **Implement key classes** using the tools
2. **Integrate with keyboard listener** 
3. **Test all keys** with real hotkey presses
4. **Add new keys** following the pattern
5. **Distribute** - Compile proprietary tools, release

---

**Status:** OOP Architecture Complete | Ready for Key Implementation
