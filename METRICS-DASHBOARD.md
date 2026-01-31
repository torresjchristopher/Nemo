# Nemo Website Metrics Dashboard

## Overview

This document describes how Nemo tracks website metrics in a privacy-respecting way.

## Tracking Mechanism

### How It Works

1. **Client-Side Tracking**: Click events are logged to visitor's browser `localStorage`
2. **No Server Tracking**: Clicks are NOT sent to external servers (respects visitor privacy)
3. **Events Tracked**:
   - Download button clicks
   - Marketing Guide PDF clicks
   - Technical Documentation PDF clicks
   - Data Ownership & Invisibility PDF clicks

### Data Collected Per Click

```json
{
    "type": "download|doc_Marketing|doc_Technical|doc_Data",
    "timestamp": "2026-01-31T17:45:00.000Z",
    "href": "https://github.com/torresjchristopher/nemo/releases/..."
}
```

**No Personal Data Collected**:
- No IP addresses
- No user IDs
- No cookies
- No localStorage is shared with Nemo servers
- Completely client-side

## Viewing Metrics

### For Website Visitors

If you want to see what's being tracked locally, open your browser console and run:

```javascript
JSON.parse(localStorage.getItem('nemo_clicks'))
```

This shows all clicks recorded in your browser session.

### For Developers

To export your local metrics:

```javascript
// Copy to clipboard
copy(localStorage.getItem('nemo_clicks'))
```

Then paste into a `.json` file for analysis.

## Privacy Philosophy

**Nemo's metrics approach aligns with data invisibility principles**:

✅ **Visitor Privacy Preserved**
- No tracking across sites
- No profiling
- No analytics cookies
- Metrics exist only in visitor's own browser

✅ **No Monetization**
- Clicks are not sold to advertisers
- No behavioral targeting
- No third-party data sharing

✅ **Transparent**
- Code is visible in `docs/index.html`
- No hidden tracking
- Users can disable via browser dev tools

## Future Enhancement (Optional)

If you want server-side metrics with privacy preservation:

### Option A: GitHub Discussions Analytics
- Create a workflow that users can manually report interesting stats
- Community-driven transparency

### Option B: Opt-In Webhook
- Users can optionally send anonymized metrics to a webhook
- Completely voluntary
- Could look like:

```javascript
// Optional: send anonymized daily summary
const sendOptionalMetrics = () => {
    const metrics = JSON.parse(localStorage.getItem('nemo_clicks') || '[]');
    const summary = {
        total_clicks: metrics.length,
        download_clicks: metrics.filter(m => m.type === 'download').length,
        doc_clicks: metrics.filter(m => m.type.startsWith('doc')).length,
        date: new Date().toISOString().split('T')[0]
    };
    
    // User would need to explicitly enable this
    if (localStorage.getItem('nemo_metrics_opt_in') === 'true') {
        fetch('https://your-analytics-endpoint.com/metrics', {
            method: 'POST',
            body: JSON.stringify(summary)
        });
    }
};
```

## Current Metrics Available

### Browser Console Commands

**View all clicks this session**:
```javascript
JSON.parse(localStorage.getItem('nemo_clicks'))
```

**Count downloads**:
```javascript
JSON.parse(localStorage.getItem('nemo_clicks')).filter(c => c.type === 'download').length
```

**Count doc clicks**:
```javascript
JSON.parse(localStorage.getItem('nemo_clicks')).filter(c => c.type.startsWith('doc')).length
```

**Clear metrics** (if needed):
```javascript
localStorage.removeItem('nemo_clicks')
```

## Tracking Events Explained

| Event | Triggered When |
|-------|---------------|
| `download` | User clicks "Download Nemo" button |
| `doc_Marketing` | User clicks "Marketing Guide PDF" link |
| `doc_Technical` | User clicks "Technical Documentation PDF" link |
| `doc_Data` | User clicks "Data Ownership & Invisibility" link |

## Why No Server Metrics?

**Nemo's commitment to data invisibility means**:
- We don't track visitors across the web
- We don't build user profiles
- We don't claim to know how many people use Nemo
- We trust users to tell us if they find value

**Alternative**: If we want engagement metrics, we ask users to:
- ⭐ Star the repo on GitHub (public, transparent)
- 💬 Comment on discussions (community dialogue)
- 📊 Voluntarily share feedback (no coercion)

## Implementation Details

The tracking code in `docs/index.html` (lines ~176-205):

1. **trackClick()** function captures event data
2. **DOMContentLoaded** listener finds all tracked elements
3. **localStorage** stores clicks in JSON format
4. **Browser console** shows metrics in real-time

## Security Notes

- XSS safe: No user input is executed
- No CORS issues: Data never leaves browser
- No privacy impact: Metrics are browser-local only
- No storage bloat: Old metrics can be manually cleared

## Future: Community Analytics

Instead of corporate surveillance, Nemo could support:

```markdown
# Nemo User Spotlight

Users who want to share their Nemo story can submit:
- How they use Nemo daily
- Favorite hotkey combinations
- Productivity improvements
- Custom configurations

This creates human-scale metrics instead of algorithmic tracking.
```

---

**The Nemo Philosophy**: Count clicks if you want, but count users never. Measure engagement, not behavior. Listen to humans, not algorithms.
