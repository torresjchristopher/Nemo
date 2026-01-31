# Nemo - Temporal Git for Your Life

> **Git for your entire week** | Full context preservation | Netflix-style timeline browsing | Zero data leakage

## 🎯 What is Nemo?

Nemo is **Git for your life**. Every 15 minutes, we capture a complete snapshot of your desktop:
- 📸 What you see (screenshots)
- ⌨️ What you type (keystrokes)
- 📁 What changes (file diffs)
- 🪟 What's open (app context)

Then you browse like **Netflix**. Jump to any moment. See what happened. Restore if needed.

**One week of history. Complete context. Full control.**

## 🚀 Quick Start

```bash
cd C:\Users\serro\Yukora\nemo
pip install -r requirements.txt
python -m nemo.cli.main
```

**What you get:**
- ✅ 5-minute temporal rewind (v1.0 NOW)
- 🔜 15-minute snapshots (v2.0 Q2 2026)
- 🎬 Netflix timeline browser (v2.5 Q2/Q3 2026)
- 📅 Full week coverage (v3.0 Q3 2026)

## 📊 Core Features

| Feature | Timeline | Status |
|---------|----------|--------|
| Desktop rewind (5 min) | NOW | ✅ Live |
| Temporal snapshots (15 min) | Q2 2026 | 🔨 Building |
| Netflix timeline UI | Q2/Q3 2026 | 🎬 Coming |
| Full week coverage | Q3 2026 | 📅 Planned |
| Desktop restoration | Q3 2026 | 🔄 Planned |
| Web interface | Q3/Q4 2026 | 🌐 Planned |

## 🏗️ Architecture (Implementation Abstracted)

**User sees:** Temporal browsing interface  
**Behind the scenes:** Smart capture + context preservation

```
Timeline Browser UI
    ↓
Temporal Context Engine
    ↓
Snapshot System (15-min intervals)
    ↓
Desktop Capture & Storage
```

No configuration needed. Just download and go.

## 🎬 What Makes Nemo Special

### 1. One-Week Temporal Window
Access 7 days of history with efficient compression:
- 96 snapshots per day (every 15 min)
- ~2 MB per day (~14 MB per week)
- Complete restoration from any moment

### 2. Full Context Preservation
Not just undo. Complete desktop state recovery:
- Screenshots (what you see)
- Keystrokes (what you type)
- File changes (diffs)
- Apps & windows (what's open)

### 3. Netflix-Style Navigation
Browse like you browse Netflix:
- Horizontal timeline scrubber
- Hover to preview any moment
- Click to jump
- Search by app, file, or time

### 4. Forward & Backward Scrubbing
Most tools only go backward (undo). Nemo lets you:
- 🔙 Go backward: "What was I doing 6 hours ago?"
- ⏭️ Go forward: "How did this evolve over time?"
- 🔍 Explore: Understand your workflow

### 5. Zero Data Leakage
Everything stays on your machine:
- ✅ Local storage only (no servers)
- ✅ Zero telemetry (we don't know what you do)
- ✅ No cloud by default (optional encrypted backup v4+)
- ✅ You control retention (auto-purge 2 weeks, configurable)
## 📈 Roadmap (Netflix Scrubbing Timeline)

### v1.0 (NOW) - Foundation ✅
**Status:** Live Beta
- Desktop rewind (5 min window)
- Full context capture
- Zero data persistence

### v1.5 (Q1 2026) - Keystroke Perfection 🔨
**Target:** Feb/Mar
- Shift combinations (shift+a, ctrl+v)
- Caps Lock tracking
- Complex sequences
- Latency: <20ms

### v2.0 (Q2 2026) - TimeVault Snapshots 🏗️
**Target:** Apr/May
- 15-min snapshots started
- Git-like versioning
- File diff tracking
- Storage: ~2MB/day

### v2.5 (Q2/Q3 2026) - Netflix Timeline UI 🎬
**Target:** May/Jun ← **NETFLIX BROWSING ARRIVES**
- Timeline scrubber shipped
- Moment preview on hover
- Smooth forward/backward scrubbing
- Search by app/file/time
- Tagging & bookmarks

### v3.0 (Q3 2026) - Full Week Coverage 📅
**Target:** Jul/Aug
- 7-day temporal window complete
- Desktop state restoration
- OCR screenshot search
- Productivity analytics

### v3.5+ (Q4 2026+) - Enterprise Ready 🌐
**Target:** Sep+
- Web interface
- Mobile apps (iOS/Android)
- Cross-platform sync
- Optional cloud backup (encrypted)

---

## 🎬 When Do I Get Netflix Scrubbing?

**Q2-Q3 2026 (May-August)**

| Milestone | Timeline | Feature |
|-----------|----------|---------|
| v2.0 shipped | Q2 (Apr/May) | Snapshots working |
| v2.5 shipped | Q2/Q3 (May/Jun) | **Netflix UI live** ← HERE |
| v3.0 shipped | Q3 (Jul/Aug) | Full week + restoration |

**Expected:** By August 2026, you'll have:
- Full Netflix-style timeline browser
- Complete week of history
- Desktop restoration capability
- OCR-based search
- Productivity analytics

---

## 🔐 Privacy & Security

### What We Store
✅ Screenshots (compressed)  
✅ Keystroke log (for reversal)  
✅ File metadata & diffs  
✅ App context

### What We DON'T Store
❌ Passwords (except as keystrokes, user responsibility)  
❌ Telemetry (no tracking)  
❌ User profiles  
❌ External uploads  

### Privacy Guarantees
- **Local first:** Everything on your machine
- **Encrypted:** All snapshots encrypted by default
- **Reversible:** Delete any snapshot anytime
- **Owned by you:** Nobody else has access

---

## 💾 Storage Efficiency

**Example: One Week of History**

| Metric | Value |
|--------|-------|
| Per snapshot (raw) | ~800 KB |
| Per snapshot (compressed) | ~200 KB |
| Per day (96 snapshots) | ~2 MB |
| Full week (7 days) | ~14 MB |
| Storage footprint | Negligible |

Your entire week fits on a USB stick.

---

## 🎯 Use Cases

### "I deleted something important. Can I get it back?"
✅ Yes. Jump to yesterday. Find it. Restore it.

### "What was I working on 3 days ago?"
✅ Jump to that moment. See your desktop exactly as it was.

### "How did this evolve over time?"
✅ Scrub through the timeline. Watch the progression.

### "I need to understand my workflow."
✅ Browse your week. See patterns. Learn from yourself.

### "I'm afraid to make changes."
✅ Temporal git means: fear nothing. Everything's captured.

---

## 🚀 Installation


```bash
# Windows
cd C:\Users\serro\Yukora\nemo
pip install -r requirements.txt
python -m nemo.cli.main
```

**System Requirements:**
- Python 3.8+
- Windows 10+ (macOS/Linux v2.0+)
- 100MB free disk space (for week of snapshots)
- Modern CPU (for compression/OCR v3+)

---

## 🎬 The Vision

### What is Temporal Computing?

Traditional computing paradigm:
> "I need to be careful. One mistake and it's gone."

Temporal computing paradigm:
> "Everything is captured. I can always go back."

**Nemo makes temporal computing real.**

### The 5-Year Roadmap

**2026:** Desktop temporal computing (Windows)  
**2027:** macOS + Linux + full week  
**2028:** Mobile OS temporal awareness  
**2029:** NemoOS prototype  
**2030+:** Industry standard adoption  

### The Endgame

In 5 years:
- Rewind becomes expected on all devices
- TimeVault becomes industry standard
- Temporal snapshots are normal
- "Non-rewindable computing" seems barbaric

---

## 📚 Documentation

- **[MARKETING.md](MARKETING.md)** - Features & positioning
- **[TECHNICAL.md](TECHNICAL.md)** - Architecture & specifications
- **[NEMO_MASTER_VISION.md](NEMO_MASTER_VISION.md)** - Long-term vision
- **[TIMEVAULT_VISION.md](TIMEVAULT_VISION.md)** - Temporal snapshot concept
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - OOP design patterns

---

## 🤝 Open Source & Proprietary

### Open Source (Auditable)
Public modules available for review and contribution:
- Snapshot system architecture
- Timeline navigation logic
- Storage & compression
- API specifications

### Proprietary (Competitive Moat)
Certain advanced features distributed as compiled:
- Keystroke reversal engine (v1.0)
- Temporal prediction engine (v2.0+)
- Advanced AI synthesis (v3.0+)

**Why?** Open architecture builds trust. Proprietary core protects innovation.

---

## 🔗 Resources

- **GitHub:** https://github.com/torresjchristopher/Nemo
- **Website:** https://downloadnemo.com
- **Issues:** Report bugs & request features on GitHub
- **Discussions:** Join our community conversations

---

## 📊 Status

- ✅ v1.0 Live (Beta)
- 🔨 v1.5 Building (Q1 2026)
- 📅 v2.0 Planned (Q2 2026)
- 🎬 v2.5 Planned (Q2/Q3 2026) ← Netflix UI
- 🌐 v3.0 Planned (Q3 2026)
- 📱 v4.0 Planned (Q4 2026)

---

## 💡 Philosophy

Nemo is built on these principles:

1. **Temporal First** - Time is a first-class citizen
2. **Context Matters** - Full context, always
3. **Zero Fear** - Everything captured, always recoverable
4. **Privacy Sacred** - Local storage, zero telemetry
5. **Elegant** - Simple, intuitive, beautiful

---

## 🚀 The Future

Temporal computing isn't science fiction. It's here.

Rewind your week. Browse any moment. Restore your entire desktop.

**That's Nemo. That's the future of computing.**
