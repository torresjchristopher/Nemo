# Nemo Keys - Idealized Functionality Specifications

**Version:** 1.0 (Vision)
**Status:** Specification Phase
**Date:** 2026-01-31

---

## RIGHT SHIFT - Speech-to-Text (STT)

### Ideal Behavior
**Hold RIGHT SHIFT to record and transcribe speech into the active text field.**

#### User Flow
```
1. User position cursor in text field
2. Press and HOLD right shift
   → Microphone activates (silent, no visual interruption yet)
3. User speaks naturally
4. Release right shift
   → Transcript appears as typed text
5. Done
```

#### Technical Specification

**Input Phase (Hold):**
- Listen via `AudioCapture` tool
- Energy threshold: 300 (low, catches all speech)
- Timeout: 5 seconds max recording
- Real-time audio level monitoring (optional visual feedback)

**Processing Phase (Release):**
- Try STT engines in order:
  1. Google Speech Recognition (fast, accurate)
  2. Sphinx (offline fallback)
  3. Microsoft Bing (cloud fallback)
- Confidence scoring (only insert if >80% confident)
- Error handling:
  - Silent recording? → Nothing inserted
  - Timeout? → Use best guess or prompt retry
  - Network error? → Fall back to offline

**Output Phase:**
- Insert text at cursor position
- Respect existing text (don't overwrite)
- Preserve formatting context
- Optional: Add punctuation if confident

#### Error Handling
```python
if confidence < 80%:
    show_notification("Low confidence. Manually review?")
    # Allow user to accept/reject/re-record
    
if no_audio_detected:
    pass  # Silent operation, no insertion
    
if all_engines_fail:
    notify_user("STT unavailable")
```

#### Configuration
```python
class STTKeyConfig:
    energy_threshold = 300       # Sensitivity
    timeout = 5                  # Max record seconds
    confidence_threshold = 0.80  # Min confidence
    languages = ['en-US']        # Support multi-lang later
    offline_mode = False         # Fall back to Sphinx if True
```

---

## RIGHT ALT - Gemini Voice AI

### Ideal Behavior
**Hold RIGHT ALT to ask Gemini a question with voice + screen context.**

#### User Flow
```
1. User has question about screen, selected text, or current task
2. Press and HOLD right alt
   → Screenshot captures (silent)
   → Microphone activates
3. User speaks question naturally
4. Release right alt
   → Gemini processes speech + screenshot
   → Response appears (modal? floating window?)
5. User can interact with response or dismiss
```

#### Technical Specification

**Input Phase (Hold):**
- Capture screenshot (full screen or selected region) using `ScreenCapture` tool
- Record audio using `AudioCapture` tool
- Combine: screenshot + audio transcript

**Processing Phase (Release):**
- Transcribe audio (STT)
- Convert screenshot to base64
- Send to Gemini Pro Vision with:
  ```
  Prompt: user_transcription
  Image: screenshot_base64
  Context: "User asking about visible screen"
  ```

**Output Phase:**
- Display response in:
  - Option A: Floating window (draggable, copyable)
  - Option B: Modal overlay (focus grabbing)
  - Option C: Console output (simple, non-intrusive)
- Allow:
  - Copy response
  - Ask follow-up (YES → loop back to input phase)
  - Save as artifact (YES → copy to clipboard + optional file)
  - Dismiss

#### Gemini Integration
```python
import google.generativeai as genai

def query_gemini_with_context(transcript, screenshot_base64):
    model = genai.GenerativeModel('gemini-pro-vision')
    image_data = genai.types.ImageData(mime_type="image/png", data=screenshot_base64)
    
    response = model.generate_content([
        transcript,
        image_data,
        "Context: User is asking about what they see on screen"
    ])
    
    return response.text
```

#### Configuration
```python
class GeminiVoiceKeyConfig:
    screenshot_enabled = True
    screenshot_include_cursor = True
    response_display_mode = "floating"  # or "modal", "console"
    artifact_save_enabled = True
    gemini_model = "gemini-pro-vision"
    api_key_env = "GEMINI_API_KEY"
```

---

## RIGHT ALT + LEFT - Rewind (NEMO CODE v1.0)

### Ideal Behavior
**Hold RIGHT ALT + LEFT to rewind through 5 minutes of typed text.**

#### User Flow
```
1. User has been typing/editing for a while
2. Makes a mistake or wants to see what they had 2 minutes ago
3. Press and HOLD right alt + left
   → Text starts disappearing (backspacing)
   → Keeps going while held down
4. Release when satisfied
   → Rewind stops at that point
5. Can resume typing or hold rewind again
```

#### Technical Specification

**Rewind Mechanics (NEMO CODE v1.0 - LOCKED):**
- Use `NemoCodeV1_0` from keystroke_processor tool
- Maintains 5-minute rolling history (5000 keystrokes max)
- On hold, pops stack in reverse:
  ```
  while user_holds_rewind:
      keystroke, nemo_code = stack.pop()
      execute(nemo_code)
      time.sleep(0.05)  # ~20 replay per second
  ```

**Visual Feedback (Optional - Phase 2):**
- Show countdown timer ("4:32 / 5:00")
- Show keystroke count being reversed
- Optional: Show text preview of what's being undone

**On Release:**
- Stop popping stack
- Maintain current position
- User can type from current position
- User can rewind again if needed

#### Edge Cases
```python
if stack_empty:
    # Can't rewind anymore (at start of 5-min window)
    pass  # Silent, just release
    
if keystroke_in_readonly_editor:
    # Skip execution (some apps block backspace)
    # But still pop from stack
    pass
    
if user_switches_apps_during_rewind:
    # Tricky: Stop rewind, clear stack?
    # Decision: Clear stack (safety)
    pass
```

#### Configuration
```python
class RewindKeyConfig:
    max_history = 5000        # 5 minutes
    replay_speed = 0.05       # seconds between keypresses
    visual_feedback = False   # Enable timer/counter (Phase 2)
    app_aware = False         # Detect app switches (Phase 2)
```

---

## RIGHT ALT + RIGHT - Forward (Prediction)

### Ideal Behavior
**Hold RIGHT ALT + RIGHT to predict what you're about to do next.**

#### User Flow
```
1. User has typed several sentences, established pattern
2. Curious what Nemo thinks comes next
3. Press and HOLD right alt + right
   → Nemo analyzes recent typing pattern
   → Shows suggestion ("Next: ' and then'")
4. Release to dismiss suggestion
5. Can use suggested completion or ignore
```

#### Technical Specification

**Pattern Analysis Phase (Hold):**
- Analyze last 30 keystrokes from NEMO CODE history
- Extract patterns:
  - Frequent word transitions
  - Punctuation patterns
  - Capitalization patterns
  - Common completions
- Use TemporalReasoner tool (proprietary)

**Prediction Phase:**
- Generate 1-3 predictions:
  - Most likely next word
  - Most likely next punctuation
  - Most likely next action (new line? delete?)
- Confidence scoring (0-100%)

**Output Phase:**
- Display suggestions as:
  - Option A: Hover suggestion ("...and then")
  - Option B: Small popup with 3 choices
  - Option C: Status bar notification
- User can:
  - TAB to accept suggestion (auto-complete)
  - Ignore and type manually
  - See explanation ("Common after 'if'")

#### Example

```
User has typed: "def check_password(pwd):"
Last patterns: Multiple def statements, parameter checking

Forward suggests:
  1. "if len(pwd)" (80% confidence)
  2. "return" (60% confidence)
  3. "pass" (45% confidence)

User presses TAB → Auto-completes to "if len(pwd)"
```

#### Configuration
```python
class ForwardKeyConfig:
    pattern_window = 30        # Last 30 keystrokes to analyze
    suggestion_count = 3       # Show top 3 predictions
    display_mode = "popup"     # or "hover", "status_bar"
    min_confidence = 0.40      # Only show if >40% confident
    auto_complete_key = "tab"  # TAB to accept
```

---

## RIGHT ALT + UP - Agent Synthesis

### Ideal Behavior
**Hold RIGHT ALT + UP to extract relevant context and ask Nemo's AI agent for insights.**

#### User Flow
```
1. User is working on a complex task (debugging, writing, research)
2. Wants AI perspective with full context
3. Press and HOLD right alt + up
   → Captures screenshot
   → Extracts relevant files (code, docs, etc.)
   → Records voice question
4. Release
   → Nemo synthesizes: files + screenshot + question
   → Sends to Gemini with full context
   → Returns structured response (analysis, suggestions, artifacts)
5. Can save insights or iterate
```

#### Technical Specification

**Context Extraction Phase (Hold):**
- Screenshot (current state)
- File detection:
  - Extract path from active window title
  - Look for open files in IDE / editor
  - Read recently modified files in directory
- Temporal context:
  - Use TemporalReasoner tool
  - Get last 5 minutes of keystroke history
  - Understand what user was doing

**Synthesis Phase (Release):**
- Transcribe voice question (STT)
- Build comprehensive context prompt:
  ```
  Files involved:
  - main.py (source code excerpt)
  - config.json (configuration)
  
  Screenshot: [image]
  
  Recent activity (from keystroke history):
  - Typed 47 characters
  - Navigated 12 times
  - Edited same file 3 times
  
  User question: "Why is this loop hanging?"
  
  Please analyze and provide:
  1. Root cause analysis
  2. Suggested fix (code snippet)
  3. Prevention strategies
  ```
- Send to Gemini with artifact generation enabled

**Output Phase:**
- Display response with sections:
  - Analysis (markdown)
  - Code suggestions (syntax highlighted)
  - Related files
  - Artifacts (save-able)
- User can:
  - Copy code snippets
  - Save artifacts to files
  - Ask follow-ups
  - Iterate on context

#### Example

```
User working on Python debugging. Holds RIGHT ALT + UP.

Nemo extracts:
- main.py (active)
- error.log (recent)
- Last 5 min of typing: variable assignments, loop edits

User asks: "Why crashes after iteration 100?"

Gemini synthesizes:
→ "Memory leak in loop. Array grows unbounded."
→ Suggests fix with code snippet
→ User can apply directly or ask more
```

#### Configuration
```python
class AgentSynthesisKeyConfig:
    extract_files = True
    extract_screenshots = True
    extract_temporal_context = True
    temporal_window = 300        # 5 minutes
    supported_file_types = ['.py', '.js', '.txt', '.md', '.json']
    artifact_save_enabled = True
    response_format = "structured"  # Markdown + sections
```

---

## Summary: The 5 Keys Idealized

| Key | Focus | Input | Output | Ideal UX |
|-----|-------|-------|--------|----------|
| **RIGHT SHIFT** | STT | Voice | Text | Seamless transcription |
| **RIGHT ALT** | Gemini + Context | Voice + Screenshot | Response | Rich Q&A with context |
| **RIGHT ALT + LEFT** | Rewind | Hold duration | Reversed text | Travel back in time |
| **RIGHT ALT + RIGHT** | Forward | Pattern analysis | Suggestions | Predictive AI |
| **RIGHT ALT + UP** | Agent Synthesis | Voice + Files + Context | Insights | Full-context analysis |

---

## Technical Integration Points

All 5 keys use the **OOP architecture:**

```
NemoEngine
  ├── STTKey (uses AudioCapture)
  ├── GeminiVoiceKey (uses AudioCapture + ScreenCapture)
  ├── RewindKey (uses NemoCodeV1_0)
  ├── ForwardKey (uses TemporalReasoner)
  └── AgentSynthesisKey (uses ScreenCapture + TemporalReasoner)
```

All tools are:
- **Public** (auditable): NemoEngine, AudioCapture, ScreenCapture
- **Proprietary** (bytecode): NemoCodeV1_0, TemporalReasoner

---

## Implementation Roadmap

**Phase 1 (NOW):** Specs locked, Ready for implementation
**Phase 2:** Build STTKey implementation
**Phase 3:** Build GeminiVoiceKey implementation
**Phase 4:** Build RewindKey implementation  
**Phase 5:** Build ForwardKey implementation
**Phase 6:** Build AgentSynthesisKey implementation

---

**Status: All 5 keys idealized. Ready to build.**
