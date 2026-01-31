# Nemo Website Metrics Dashboard

## Overview

Nemo tracks engagement with exactly **4 anonymous counters**. No timestamps, no user tracking, no personal data.

## The 4 Counters

```json
{
  "download_clicks": 0,
  "marketing_pdf_clicks": 0,
  "technical_pdf_clicks": 0,
  "data_ownership_pdf_clicks": 0
}
```

That's it. Just 4 numbers.

## Privacy Promise

✅ **Completely Anonymous**
- No timestamps
- No user IDs
- No IP addresses
- No cookies
- No behavioral tracking
- Impossible to identify individual visitors

✅ **Minimal Data**
- 4 integers total
- No individual click records
- No historical data
- Data only exists in visitor's browser localStorage

✅ **No Server Tracking**
- Metrics never leave your browser
- No third-party analytics
- No data monetization
- No profiling

## Viewing Metrics

### Your Local Clicks

Open browser console and run:

```javascript
JSON.parse(localStorage.getItem('nemo_metrics'))
```

Returns:
```json
{
  "download_clicks": 3,
  "marketing_pdf_clicks": 1,
  "technical_pdf_clicks": 2,
  "data_ownership_pdf_clicks": 0
}
```

### Manual Reporting (Optional)

If you want to contribute anonymous metrics to Nemo:

1. Run the console command above
2. Copy the numbers
3. Create a GitHub issue titled "Metrics Report"
4. Paste your numbers

Community-driven, completely voluntary, 100% transparent.

## How It Works

1. **Visitor clicks a link** on nemo website
2. **JavaScript increments the counter** for that link
3. **Number is stored in browser localStorage** only
4. **No data leaves the browser**
5. **User can view their own metrics anytime**

## Events Tracked

| Counter | Triggered When |
|---------|---------------|
| `download_clicks` | User clicks "Download Nemo" button |
| `marketing_pdf_clicks` | User clicks "Marketing Guide PDF" link |
| `technical_pdf_clicks` | User clicks "Technical Documentation PDF" link |
| `data_ownership_pdf_clicks` | User clicks "Data Ownership & Invisibility" link |

## Why This Approach?

Traditional analytics violate privacy:
- ❌ Track users across the web
- ❌ Build behavioral profiles
- ❌ Sell data to third parties
- ❌ Use cookies to identify visitors
- ❌ Monetize engagement

Nemo's 4-counter approach:
- ✅ Zero identification possible
- ✅ Zero historical tracking
- ✅ Zero data extraction
- ✅ Zero profiling
- ✅ 100% voluntary sharing

## Transparency

The tracking code is **visible in the repo**:
- View source in `docs/index.html` (lines ~176-200)
- Audit it yourself
- No hidden tracking
- No dark patterns

## Clearing Your Metrics

If you want to reset your local counter:

```javascript
localStorage.removeItem('nemo_metrics')
```

This only affects your browser. Doesn't affect any server (because we don't have one tracking you).

## The Philosophy

**Nemo doesn't believe in:**
- Silently tracking visitors
- Building shadow profiles
- Inferring user intent
- Selling engagement data
- Dark analytics patterns

**Nemo does believe in:**
- Transparent metrics (you can see the code)
- Anonymous counting (just numbers)
- Optional sharing (you choose to report)
- User agency (you control your data)
- Data invisibility (no persistent tracking)

## Implementation

Total code size: **~15 lines of JavaScript**

The entire tracking system:
```javascript
const trackClick = (counterKey) => {
    let metrics = JSON.parse(localStorage.getItem('nemo_metrics') 
        || '{"download_clicks":0,"marketing_pdf_clicks":0,"technical_pdf_clicks":0,"data_ownership_pdf_clicks":0}');
    metrics[counterKey] = (metrics[counterKey] || 0) + 1;
    localStorage.setItem('nemo_metrics', JSON.stringify(metrics));
};
```

---

**The Nemo Standard for Metrics**: Count engagement, not users. Measure success, not behavior. Stay transparent, stay minimal, stay anonymous.
