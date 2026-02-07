# Slow Shakespeare Web App Plan

A web version of Slow Shakespeare for mobile and desktop browsers.

## Goal

Replicate the Tidbyt app's memorization functionality in a web app that works on any device, with enhanced features that take advantage of the larger screen and interactivity.

## Core Features (matching Tidbyt)

1. **Daily line progression** — one new line per day, based on calendar days
2. **10 sonnets** — 1, 18, 29, 30, 55, 73, 104, 116, 130, 138
3. **Auto-advance** — moves to next sonnet after 14 days
4. **Start date picker** — set when you began (or sync with friends)
5. **7 color themes** — WCAG AAA (7:1+) in both dark and light modes
   - Salad Days (dark: #8FBF8F, light: #4A6B4A)
   - Yellow Leaves (dark: #D4A76A, light: #7A5C2E)
   - Milk of Kindness (dark: #E8DFD0, light: #4A4540)
   - Midsummer Night (dark: #8BBDD4, light: #3A6478)
   - All That Glisters (dark: #D4B85A, light: #6B5A1E)
   - Damask Rose (dark: #D4A0A8, light: #7A4A52)
   - Black Ink (dark: #D5CFC5, light: #2A2520)
6. **Line number toggle**
7. **Dark/Light/Auto theme** — respects system preference by default
8. **Settings persistence** — saved in localStorage

## Enhanced Features (web advantages)

1. **Review button** — tap to cycle through all learned lines (replaces hourly :00 review from Tidbyt)
2. **Self-test mode** — lines hidden by default, tap to reveal (for active recall practice)
3. **Progress indicator** — "Day 7 of 14"
4. **Share link** — URL with start date and sonnet encoded so friends can sync
5. **PWA support** — add to home screen, works offline

## Technical Approach

### Stack
- **Template + data file** — `app.html` is the template, `data.js` has sonnets/colors/config
- **No build tools, no dependencies** (besides Google Fonts CDN)
- **Vanilla JavaScript** — no frameworks
- **CSS variables** for theming
- **localStorage** for settings persistence
- **URL parameters** for sharing
- **SEO**: Sonnet text in HTML source (hidden section) + meta/OG tags

### URL Parameters
```
?start=2025-02-05&sonnet=18&color=salad&lines=on&theme=dark
```

### localStorage Key
Single JSON object stored under key `"slowshakespeare"`:
```javascript
{
  "sonnet": "18",
  "startDate": "2025-02-05",
  "colorName": "salad",
  "showLines": false,
  "selfTest": false,
  "themePref": "auto"
}
```

### Day Calculation Logic
Same as Tidbyt version, normalized to midnight:
```javascript
const start = new Date(state.startDate + 'T00:00:00');
const now = new Date();
const todayMidnight = new Date(now.getFullYear(), now.getMonth(), now.getDate());
const totalDays = Math.floor((todayMidnight - start) / 86400000);
const safeDays = Math.max(0, totalDays);
const sonnetsCompleted = Math.floor(safeDays / 14);
const dayWithinSonnet = safeDays % 14;
const linesLearned = Math.min(dayWithinSonnet + 1, lines.length);
```

## File Structure

```
web/
├── index.html                    # Landing page (SEO, Sonnet 18, "Begin" CTA)
├── app.html                      # Daily-use app (template — loads style.css + data.js)
├── style.css                     # All CSS (themes, layout, components, responsive)
├── data.js                       # Sonnet text, color palettes, sonnet order
├── CNAME                         # Custom domain for GitHub Pages
├── PLAN.md                       # This file (gitignored)
├── test_slowshakespeare_web.py   # Automated tests
└── dev/                          # Development files (gitignored)
    └── styleguide.html           # Visual style reference
```

## Design

### Visual Style
- **Dark mode:** #1a1a1a background, light text — like Tidbyt
- **Light mode:** #FDFCF9 warm snow background, dark text
- **Auto mode:** follows system `prefers-color-scheme`
- **Font pairing:**
  - **Poetry text:** EB Garamond (Google Fonts) — old-style roman serif, revival of Claude Garamond's types (contemporary of the First Folio's punchcutter Pierre Haultin). Georgia fallback.
  - **UI elements:** system-ui stack — buttons, labels, selects, progress, review indicator. Clean and native-feeling, follows Kindle/Apple Books pattern of serif content + sans-serif chrome.
- Minimal UI — focus on the poetry
- Mobile-first, responsive

### Layout
```
┌─────────────────────────────────┐
│         Sonnet 18               │  <- sonnet title
│         Day 3 of 14             │  <- progress (day only, no sonnet count)
├─────────────────────────────────┤
│                                 │
│  "Rough winds do shake the      │
│   darling buds of May,"         │  <- today's line (large)
│                                 │
│                            3    │  <- line number (optional)
├─────────────────────────────────┤
│  [Review]  [Settings]           │  <- controls
└─────────────────────────────────┘
```

### Settings Panel (collapsible)
- Sonnet dropdown
- Start date picker
- Color theme selector (swatches)
- Theme toggle (Auto / Dark / Light)
- Line numbers toggle
- Self-test toggle
- Share link button

### Review Mode
- Triggered by "Review" button
- Cycles through all learned lines (5s each)
- Shows dot marker on line 1
- "Stop" button to exit

### Self-Test Mode
- Toggle in settings
- Shows "Tap to reveal" instead of line text
- Tap reveals the line
- Encourages active recall

## Hosting Options

1. **GitHub Pages** — free, push to repo, automatic deployment
2. **Local file** — just open `index.html` in browser
3. **Any static host** — Netlify, Vercel, Cloudflare Pages

## Implementation Steps

1. [ ] Create basic HTML structure with sonnet data
2. [ ] Implement day calculation logic
3. [ ] Add localStorage for settings
4. [ ] Style with CSS (dark theme, responsive)
5. [ ] Add settings panel
6. [ ] Implement review mode animation
7. [ ] Add URL parameter support for sharing
8. [ ] Add PWA manifest for home screen install
9. [ ] Test on mobile Safari, Chrome
10. [ ] Update README with usage instructions

## Testing

### Manual Test Cases

1. **Day 1 (fresh start)** — start date = today, should show line 1, "Day 1 of 14"
2. **Day 8** — start date = 7 days ago, should show line 8
3. **Day 14** — start date = 13 days ago, should show line 14
4. **Auto-advance** — start date = 14+ days ago, should show next sonnet in order, "Day 1 of 14"
5. **Wrap-around** — start date far enough back to cycle past sonnet 138, should wrap to sonnet 1
6. **Future start date** — should clamp to Day 1
7. **Color themes** — click each swatch, verify text color changes
8. **Line numbers** — toggle on/off, verify number appears/disappears in bottom-right
9. **Self-test** — toggle on, verify "tap to reveal" shown; tap to reveal line; toggle off, verify line shown normally
10. **Review mode** — click Review, verify lines cycle every 5s with dot marker on line 1; click Stop to exit
11. **Settings persistence** — change settings, reload page, verify settings restored from localStorage
12. **URL params** — open share URL in new tab, verify settings applied from URL
13. **URL overrides localStorage** — set different values in localStorage vs URL params, verify URL wins
14. **Sonnet change** — switch sonnet in dropdown, verify new sonnet line displayed and day resets
15. **Mobile layout** — resize to 375px wide, verify text wraps and settings panel is usable
16. **Dark mode** — click Dark, verify dark background with light text
17. **Light mode** — click Light, verify parchment background with dark text
18. **Auto mode** — click Auto, verify it follows system preference
19. **Theme + color** — switch theme while a color is selected, verify text color adapts (dark variant vs light variant)

### Parity with Tidbyt App

- Same 10 sonnets with identical text
- Same day calculation logic (total_days // 14 for sonnet advance, % 14 for day within)
- Same 6 color theme names plus Black Ink (hex values updated for AAA accessibility)
- Same auto-advance order: 1, 18, 29, 30, 55, 73, 104, 116, 130, 138

## Future Enhancements

- Audio pronunciation of lines
- Notification reminders (via service worker)
- Statistics tracking (streak, total lines learned)
- Print view for offline study
- Multiple language translations
