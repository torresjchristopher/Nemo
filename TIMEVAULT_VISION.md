# Temporal Snapshot System - "TimeVault"

**Codename:** TimeVault (Git for Your Day)
**Vision:** Browse your entire day/week like Netflix, rewind to any moment
**Status:** Vision Document (Phase 2+)

---

## The Concept

```
Current Nemo:
  RIGHT ALT + LEFT → Rewind last 5 minutes of keystrokes

TimeVault (Future):
  "Show me my day in Netflix timeline"
  "Jump to 3:45 PM yesterday when I fixed the bug"
  "Restore the entire desktop to Tuesday morning"
```

Think: **Git for temporal moments instead of code commits.**

---

## Architecture

### Snapshot Structure

Every N minutes (configurable, default: 15 min), capture:

```python
class TemporalSnapshot:
    timestamp: datetime        # When snapshot taken
    keystroke_history: deque   # Last N keystrokes (NEMO CODE)
    screenshot: bytes          # PNG of full screen
    file_state: dict           # {filepath: md5_hash, modified_time}
    open_apps: list            # Which apps were open
    metadata: dict             # CPU, memory, network activity
    
    # Git-like commit info
    commit_hash: str           # SHA256(timestamp + screenshot)
    parent: str                # Previous snapshot hash
    message: str               # Auto-generated: "Coding session - IDE open"
```

### Timeline Storage

```
~/.nemo/timeVault/
├── 2026-01-31/                    # Daily folder
│   ├── 14-30-snapshot.vault       # 2:30 PM snapshot
│   ├── 14-45-snapshot.vault       # 2:45 PM snapshot
│   ├── 15-00-snapshot.vault       # 3:00 PM snapshot
│   └── ...
├── 2026-01-30/
│   ├── 09-00-snapshot.vault       # Previous day
│   └── ...
└── metadata.json                  # Index of all snapshots

Total storage: ~500MB per week (configurable retention)
```

---

## Features

### 1. Timeline Viewer (Netflix-Style)

```
┌─ NEMO TIMELINE ──────────────────────────────────┐
│                                                   │
│ Today (Jan 31)  ▼                                │
│ 22:00 ▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
│ 20:00 ▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
│ 18:00 ▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░ │
│ 16:00 ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░░ │
│ 14:00 ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░░ │
│                                                   │
│ [◄◄ Week] [◄ Day] [Hour ►] [Week ►►]           │
└─────────────────────────────────────────────────┘
```

Features:
- Density heatmap (darker = more activity)
- Click on any bar → zoom to that hour
- Scrub timeline like YouTube video
- See snapshot preview on hover
- Jump to bookmarks ("Bug fixed here!", "Finished proposal", etc.)

### 2. Rewind to Any Moment

```
User interaction:
1. Open Timeline viewer
2. Click on "3:45 PM yesterday"
3. See screenshot from that moment
4. Click "REWIND TO HERE"
5. System:
   - Closes current apps
   - Restores desktop
   - Re-opens files that were open
   - Positions windows where they were
   - → User sees yesterday's desktop

6. User can:
   - Browse files as they existed then
   - Read what was in open editors
   - See what they were working on
   - Then "FORWARD" to get back to now
```

### 3. Diff Between Moments

```
"Show me what changed between 2:00 PM and 3:00 PM"

System displays:
- Files modified (with diff)
- Keystrokes during that window
- Screenshot before/after
- Apps opened/closed
- Git-like changelog
```

### 4. Bookmarking (Manual Commits)

```
User hotkey: RIGHT SHIFT + B (or gesture)
→ "Great progress!" bookmark
→ Saved snapshot with message
→ Shows in timeline as starred

Then: "Jump back to all my bookmarks from today"
```

### 5. Search Time

```
"Find the moment I was writing the email about..."
"Show me every screenshot with 'error' dialog"
"When did I open that one file?"
"Go back to when Slack was open"

Uses:
- OCR on screenshots (find text)
- File access logs
- App history
- Keystroke keywords
```

---

## Implementation Phases

### Phase 2.1: Basic Snapshots (Foundation)

```python
class TemporalSnapshotEngine:
    def take_snapshot(self) -> TemporalSnapshot:
        """Take a snapshot every 15 minutes"""
        snapshot = TemporalSnapshot(
            timestamp=datetime.now(),
            keystroke_history=nemo_code.get_history(),  # REUSE!
            screenshot=screen_capture.capture(),         # REUSE!
            file_state=self._scan_files(),
            open_apps=self._get_open_apps(),
        )
        self._save_snapshot(snapshot)
        return snapshot
    
    def save_snapshot(self, snapshot: TemporalSnapshot) -> None:
        """Save to ~/.nemo/timeVault/"""
        # Git-like storage
        pass
```

### Phase 2.2: Timeline Viewer

```
TUI (Terminal UI) version:
- Arrow keys to navigate timeline
- Enter to jump to moment
- 's' to see screenshot
- 'f' to see file diffs
- 'b' to bookmark
```

### Phase 2.3: Desktop Restoration

```python
def restore_to_moment(snapshot: TemporalSnapshot) -> None:
    """Restore entire desktop to that moment"""
    # Close all current apps (safe)
    # Re-open apps that were open
    # Restore file contents (from git-like history)
    # Position windows
    # Set environment
    # → User sees yesterday's desktop
```

### Phase 2.4: Search & Query

```python
def search_timeVault(query: str) -> List[TemporalSnapshot]:
    """Find moments matching query"""
    # OCR all screenshots
    # Search file diffs
    # Search keystroke history
    # Return matching moments
```

### Phase 3: Web UI (Netflix-Style)

```
Browser at localhost:8080
- Interactive timeline scrubber
- Calendar view (which days were productive?)
- Statistics (coding hours, app usage)
- Video-like playback
```

---

## Data Structure: Git-Like Versioning

```
Git analogy:
  git commit = temporal_snapshot
  git branch = daily/weekly view
  git tag = bookmarks
  git log = timeline
  git diff = changes between moments
  git checkout = restore_to_moment
```

### TimeVault "Commits"

```
commit 7a3f9e2c (Jan 31, 2026 15:45)
Parent: 8d4c2e1b (Jan 31, 2026 15:30)

  [Active] IDE open, writing main.py
  
  Modified files:
  - main.py (+47 -12)
  - config.json (+1 -0)
  
  Keystrokes: 437 (coding)
  Apps: VSCode, Terminal, Firefox
  
  Screenshot: [thumbnail]
```

---

## Privacy & Storage Considerations

### Data Minimization

- **Only save diffs**, not full files (unless small)
- **Only save screenshot hash**, not full PNG (unless user requests)
- **Compress heavily** (ZSTD compression)
- **Auto-delete old snapshots** (configurable, default: keep 2 weeks)

### User Control

```python
class TimeVaultConfig:
    enabled = True
    snapshot_interval = 15  # minutes
    retention_days = 14     # auto-delete after 2 weeks
    storage_limit_gb = 5    # max storage
    compress = True
    include_screenshots = True
    include_files = True
```

### Encryption (Future)

- Optional: Encrypt snapshots locally
- User keeps decryption key
- Even cloud backups are secure

---

## Storage Estimates

### Per Day (8 hours active)

```
15-min snapshots = 32 per day

Per snapshot:
  - Screenshot (compressed PNG): 200KB → 50KB compressed
  - Keystroke history: 1KB
  - File diffs: 10KB
  - Metadata: 1KB
  Total per snapshot: ~60KB

32 snapshots × 60KB = ~2MB per day
14 days = ~30MB per week
8 weeks = ~250MB per month
```

**Totally manageable on any modern machine.**

---

## Integration with Existing Nemo

### Reuses

✅ **ScreenCapture tool** - Take snapshots
✅ **NEMO CODE** - Track keystrokes (already stored)
✅ **NemoKey lifecycle** - Hook snapshots into key events
✅ **NemoEngine** - Manage snapshot scheduler

### New Components

❌ **TemporalSnapshotEngine** - Periodic capture + storage
❌ **TimeVaultViewer** - Browse timeline
❌ **TemporalDiff** - Show changes between moments
❌ **SnapshotSearch** - OCR + query

---

## The Magic: Why This Works

### Current State
```
Rewind: "Last 5 minutes, keystroke level"
You can undo your last actions.
```

### With TimeVault
```
Rewind: "Back to anytime today, anytime this week, restore full desktop"
You can travel through your day like a movie.
You can see what you were doing at any moment.
You can restore your entire state to that moment.
```

### Use Cases

1. **"I had a great idea earlier today"**
   - Timeline viewer → 2:30 PM
   - See what you were looking at
   - Remember the idea

2. **"The code worked yesterday"**
   - Show yesterday at 4:00 PM
   - See the working code
   - Understand what changed

3. **"I need to continue where I left off"**
   - Restore desktop to when you stopped
   - All windows, files, apps exactly as they were

4. **"When did the bug start?"**
   - Search for error messages in screenshots
   - See exact moment bug was introduced
   - Rewind and understand context

5. **"How productive was I?"**
   - Timeline heatmap shows active hours
   - Analytics: hours in IDE vs email vs browser
   - Daily/weekly reports

---

## Roadmap

**v1.0 (NOW):** Desktop rewind (5 min keystroke history)
**v1.5:** NEMO CODE Phase 2 (Shift combinations)
**v2.0:** TimeVault Phase 1 (Basic snapshots)
**v2.5:** TimeVault Phase 2 (Timeline viewer)
**v3.0:** Desktop restoration + search
**v3.5:** Web UI (Netflix-style)
**v4.0:** Mobile OS with TimeVault native
**Future:** TimeVault becomes industry standard

---

## The Vision

Imagine an OS where:
- **Every moment is captured** (like git)
- **You can travel to any moment** (like netflix)
- **Your work is never lost** (git + time machine)
- **You can learn from the past** (analytics + temporal context)

**TimeVault is the bridge between traditional computing and temporal computing.**

It transforms your computer from:
```
"What I have now"
↓
"What I had yesterday and what changed"
```

This is beyond undo. This is **temporal awareness as a core OS feature.**

---

## Implementation Notes

### Storage Format

```
# ~/.nemo/timeVault/YYYY-MM-DD/HH-MM-snapshot.vault

[HEADER]
timestamp=2026-01-31T15:45:00
parent_hash=8d4c2e1b
commit_hash=7a3f9e2c

[METADATA]
keystrokes=437
open_apps=["VSCode", "Terminal", "Firefox"]
cpu_usage=45.2
memory_usage=62.1

[KEYSTROKE_HISTORY]
# Compressed NEMO CODE history

[FILE_STATE]
main.py=7f8d2e1c (hash)
config.json=9e3c4d2b (hash)

[FILE_DIFFS]
main.py +47 -12
config.json +1 -0

[SCREENSHOT]
# Compressed PNG or hash + storage reference
```

### Query Language

```
timeVault.find("error")
timeVault.find_by_app("VSCode")
timeVault.find_by_time("2026-01-31 14:00:00")
timeVault.find_by_keystroke_count(">500")
timeVault.diff("2026-01-31 14:00", "2026-01-31 15:00")
timeVault.restore("2026-01-30 09:00")
```

---

## Why This Matters

**Current computers are ephemeral:**
- Close an app → lose the state
- Restart → lose what you were doing
- Can't travel back in time

**TimeVault makes computers persistent & temporal:**
- Every moment is a "commit"
- You can travel through time
- You can learn from the past
- Your work is never truly lost

**This is a paradigm shift.**

From: "I need to be careful, one mistake and it's gone"
To: "Everything is captured, I can always go back"

---

## Next Steps

1. **Finalize Nemo v1.0** (desktop rewind working)
2. **User testing** (real-world validation)
3. **Phase 2 planning** (Shift combinations, Advanced NEMO CODE)
4. **TimeVault scoping** (decide what to capture, storage limits)
5. **Design timeline UI** (Netflix-style browsing)
6. **Build Phase 2.1** (Basic snapshots)

---

**TimeVault is the future of computing. Every moment captured, every moment available.**

From ephemeral to eternal. 🕐✨
