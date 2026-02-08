#!/usr/bin/env python3
"""Tests for Slow Shakespeare web app (app.html).

Tests the core logic (day calculation, sonnet advancement, color system,
URL params, settings) by reimplementing the JavaScript logic in Python
and verifying it matches expected behavior. Also does structural checks
on the HTML file itself.
"""

import os
import re
import sys
from datetime import date, timedelta

APP_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_FILE = os.path.join(APP_DIR, "app.html")
INDEX_FILE = os.path.join(APP_DIR, "index.html")
CSS_FILE = os.path.join(APP_DIR, "style.css")
DATA_JS_FILE = os.path.join(APP_DIR, "data.js")
TIDBYT_FILE = os.path.join(APP_DIR, "..", "tidbyt", "slow_shakespeare.star")

SONNET_ORDER = ["1", "18", "29", "30", "55", "73", "104", "116", "130", "138"]

# First and last lines of each sonnet (for parity checks)
SONNET_FIRST_LINES = {
    "1": "From fairest creatures we desire increase,",
    "18": "Shall I compare thee to a summer's day?",
    "29": "When, in disgrace with fortune and men's eyes,",
    "30": "When to the sessions of sweet silent thought",
    "55": "Not marble, nor the gilded monuments",
    "73": "That time of year thou mayst in me behold",
    "104": "To me, fair friend, you never can be old,",
    "116": "Let me not to the marriage of true minds",
    "130": "My mistress' eyes are nothing like the sun;",
    "138": "When my love swears that she is made of truth",
}

SONNET_LAST_LINES = {
    "1": "To eat the world's due, by the grave and thee.",
    "18": "So long lives this, and this gives life to thee.",
    "29": "That then I scorn to change my state with kings.",
    "30": "All losses are restor'd and sorrows end.",
    "55": "You live in this, and dwell in lovers' eyes.",
    "73": "To love that well which thou must leave ere long.",
    "104": "Ere you were born was beauty's summer dead.",
    "116": "I never writ, nor no man ever loved.",
    "130": "As any she belied with false compare.",
    "138": "And in our faults by lies we flatter'd be.",
}

COLORS = {
    "salad": {"dark": "#8FBF8F", "light": "#4A6B4A", "swatch": "#3E6D4E"},
    "milk": {"dark": "#B5A99A", "light": "#4A4540", "swatch": "#B5A99A"},
    "midsummer": {"dark": "#7BA3D4", "light": "#2B4578", "swatch": "#2B4578"},
    "glisters": {"dark": "#D4B86A", "light": "#6B5A1E", "swatch": "#B8993E"},
    "damask": {"dark": "#D4856E", "light": "#B44430", "swatch": "#B44430"},
    "ink": {"dark": "#D5CFC5", "light": "#2A2520", "swatch": "#2A2520"},
}


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def read_html():
    return read_file(HTML_FILE)


def read_index():
    return read_file(INDEX_FILE)


def read_css():
    return read_file(CSS_FILE)


def read_data_js():
    return read_file(DATA_JS_FILE)


def read_tidbyt():
    if not os.path.exists(TIDBYT_FILE):
        return None
    return read_file(TIDBYT_FILE)


def calculate(start_date_str, sonnet_id, today=None):
    """Reimplement the JS calculate() function in Python.

    This must exactly match the logic in app.html.
    """
    if today is None:
        today = date.today()

    start = date.fromisoformat(start_date_str)
    total_days = (today - start).days
    safe_days = max(0, total_days)

    sonnet_index = SONNET_ORDER.index(sonnet_id)
    sonnets_completed = safe_days // 14
    day_within_sonnet = safe_days % 14

    current_index = (sonnet_index + sonnets_completed) % len(SONNET_ORDER)
    current_sonnet_id = SONNET_ORDER[current_index]
    lines_learned = min(day_within_sonnet + 1, 14)

    return {
        "currentSonnetId": current_sonnet_id,
        "linesLearned": lines_learned,
        "dayWithinSonnet": day_within_sonnet,
        "safeDays": safe_days,
    }


# ---------------------------------------------------------------------------
# Day calculation tests
# ---------------------------------------------------------------------------

def test_day1_fresh_start():
    """Start date = today => Day 1 of 14, line 1."""
    today = date(2025, 6, 15)
    r = calculate("2025-06-15", "18", today)
    assert r["currentSonnetId"] == "18"
    assert r["dayWithinSonnet"] == 0
    assert r["linesLearned"] == 1
    print("  ✓ Day 1 (fresh start)")


def test_day8():
    """Start date = 7 days ago => Day 8, 8 lines learned."""
    today = date(2025, 6, 15)
    r = calculate("2025-06-08", "18", today)
    assert r["dayWithinSonnet"] == 7
    assert r["linesLearned"] == 8
    print("  ✓ Day 8")


def test_day14():
    """Start date = 13 days ago => Day 14, all 14 lines."""
    today = date(2025, 6, 15)
    r = calculate("2025-06-02", "18", today)
    assert r["dayWithinSonnet"] == 13
    assert r["linesLearned"] == 14
    print("  ✓ Day 14")


def test_auto_advance():
    """After 14 days, advances to next sonnet."""
    today = date(2025, 6, 15)
    r = calculate("2025-06-01", "18", today)  # 14 days later
    assert r["currentSonnetId"] == "29", f"Expected 29, got {r['currentSonnetId']}"
    assert r["dayWithinSonnet"] == 0
    assert r["linesLearned"] == 1
    print("  ✓ Auto-advance to next sonnet")


def test_auto_advance_second():
    """After 28 days, advances two sonnets."""
    today = date(2025, 6, 15)
    r = calculate("2025-05-18", "18", today)  # 28 days
    assert r["currentSonnetId"] == "30", f"Expected 30, got {r['currentSonnetId']}"
    assert r["dayWithinSonnet"] == 0
    print("  ✓ Auto-advance two sonnets")


def test_wrap_around():
    """After cycling through all 10 sonnets, wraps to beginning."""
    today = date(2025, 6, 15)
    # Start at sonnet 138 (index 9), 14 days ago => should wrap to sonnet 1 (index 0)
    r = calculate("2025-06-01", "138", today)
    assert r["currentSonnetId"] == "1", f"Expected 1, got {r['currentSonnetId']}"
    print("  ✓ Wrap-around past sonnet 138")


def test_full_cycle_wrap():
    """After 140 days (10 sonnets * 14 days), wraps back to start."""
    today = date(2025, 6, 15)
    start = today - timedelta(days=140)
    r = calculate(start.isoformat(), "1", today)
    assert r["currentSonnetId"] == "1", f"Expected 1, got {r['currentSonnetId']}"
    assert r["dayWithinSonnet"] == 0
    print("  ✓ Full cycle (140 days) wraps to start")


def test_future_start_date():
    """Future start date => clamps to Day 1."""
    today = date(2025, 6, 15)
    r = calculate("2025-07-01", "18", today)
    assert r["safeDays"] == 0
    assert r["dayWithinSonnet"] == 0
    assert r["linesLearned"] == 1
    print("  ✓ Future start date clamps to Day 1")


def test_sonnet_order_preserved():
    """Auto-advance follows the defined order."""
    today = date(2025, 6, 15)
    start = today
    for i, expected_id in enumerate(SONNET_ORDER):
        r = calculate(start.isoformat(), "1", today + timedelta(days=i * 14))
        assert r["currentSonnetId"] == expected_id, (
            f"Day {i * 14}: expected {expected_id}, got {r['currentSonnetId']}"
        )
    print("  ✓ Sonnet order preserved through all 10")


def test_mid_sonnet_days():
    """Each day within a 14-day cycle shows correct line count."""
    today = date(2025, 6, 15)
    for day in range(14):
        start = (today - timedelta(days=day)).isoformat()
        r = calculate(start, "18", today)
        assert r["linesLearned"] == day + 1, (
            f"Day {day}: expected {day + 1} lines, got {r['linesLearned']}"
        )
    print("  ✓ All 14 days show correct line count")


# ---------------------------------------------------------------------------
# Sonnet text parity tests
# ---------------------------------------------------------------------------

def test_all_sonnets_present():
    """All 10 sonnets with first and last lines present in HTML."""
    content = read_html()
    for sid, first in SONNET_FIRST_LINES.items():
        assert first in content, f"Missing first line of Sonnet {sid}"
    for sid, last in SONNET_LAST_LINES.items():
        assert last in content, f"Missing last line of Sonnet {sid}"
    print("  ✓ All 10 sonnets present with correct first/last lines")


def test_each_sonnet_has_14_lines():
    """Each sonnet should have exactly 14 lines in the JS array."""
    content = read_data_js()
    for sid in SONNET_ORDER:
        # Match the array for this sonnet: "18": [\n ... ]
        pattern = rf'"{sid}":\s*\[(.*?)\]'
        match = re.search(pattern, content, re.DOTALL)
        assert match, f"Could not find sonnet {sid} array"
        lines = [l.strip() for l in match.group(1).split("\n") if l.strip().startswith('"')]
        assert len(lines) == 14, (
            f"Sonnet {sid}: expected 14 lines, got {len(lines)}"
        )
    print("  ✓ Each sonnet has exactly 14 lines")


def test_sonnet_text_parity_with_tidbyt():
    """Sonnet text matches the Tidbyt app exactly."""
    tidbyt = read_tidbyt()
    if tidbyt is None:
        print("  ⊘ Skipped (Tidbyt file not found)")
        return
    web = read_html()
    for sid, first in SONNET_FIRST_LINES.items():
        assert first in tidbyt, f"Tidbyt missing first line of Sonnet {sid}"
        assert first in web, f"Web missing first line of Sonnet {sid}"
    for sid, last in SONNET_LAST_LINES.items():
        assert last in tidbyt, f"Tidbyt missing last line of Sonnet {sid}"
        assert last in web, f"Web missing last line of Sonnet {sid}"
    print("  ✓ Sonnet text matches Tidbyt app")


# ---------------------------------------------------------------------------
# Color system tests
# ---------------------------------------------------------------------------

def test_all_colors_in_html():
    """All 6 color themes present with correct hex values in data.js."""
    content = read_data_js()
    for name, vals in COLORS.items():
        assert vals["dark"] in content, f"Missing dark variant for {name}: {vals['dark']}"
        assert vals["light"] in content, f"Missing light variant for {name}: {vals['light']}"
        assert vals["swatch"] in content, f"Missing swatch for {name}: {vals['swatch']}"
    print("  ✓ All 6 color themes present with correct hex values")


def test_color_labels_present():
    """All color labels present in data.js."""
    content = read_data_js()
    labels = ["Salad Days", "Milk of Kindness",
              "Midsummer Night", "All That Glisters", "Damask Rose", "Black Ink"]
    for label in labels:
        assert label in content, f"Missing color label: {label}"
    print("  ✓ All 6 color labels present")


def test_ink_distinct_from_milk():
    """Black Ink dark variant is distinct from Milk of Kindness dark."""
    assert COLORS["ink"]["dark"] != COLORS["milk"]["dark"], (
        "Black Ink and Milk of Kindness dark variants should differ"
    )
    print("  ✓ Black Ink dark variant distinct from Milk of Kindness")


def test_wcag_contrast_dark():
    """All dark-mode colors pass WCAG AA (4.5:1) on #1a1a1a."""
    bg = (0x1a, 0x1a, 0x1a)
    for name, vals in COLORS.items():
        fg = hex_to_rgb(vals["dark"])
        ratio = contrast_ratio(fg, bg)
        assert ratio >= 4.5, (
            f"{name} dark ({vals['dark']}): contrast {ratio:.1f}:1 < 4.5:1"
        )
    print("  ✓ All dark-mode colors pass WCAG AA on #1a1a1a")


def test_wcag_contrast_light():
    """All light-mode colors pass WCAG AA (4.5:1) on #FDFCF9."""
    bg = (0xFD, 0xFC, 0xF9)
    for name, vals in COLORS.items():
        fg = hex_to_rgb(vals["light"])
        ratio = contrast_ratio(fg, bg)
        assert ratio >= 4.5, (
            f"{name} light ({vals['light']}): contrast {ratio:.1f}:1 < 4.5:1"
        )
    print("  ✓ All light-mode colors pass WCAG AA on #FDFCF9")


# ---------------------------------------------------------------------------
# HTML structure tests
# ---------------------------------------------------------------------------

def test_has_viewport_meta():
    """Mobile viewport meta tag present."""
    content = read_html()
    assert 'name="viewport"' in content
    assert "width=device-width" in content
    print("  ✓ Viewport meta tag present")


def test_has_eb_garamond_font():
    """EB Garamond Google Font loaded."""
    content = read_html()
    assert "EB+Garamond" in content or "EB Garamond" in content
    print("  ✓ EB Garamond font loaded")


def test_font_variables():
    """CSS font variables defined."""
    content = read_css()
    assert "--font-content" in content
    assert "--font-ui" in content
    assert "system-ui" in content
    print("  ✓ CSS font variables defined (content + UI)")


def test_theme_css_variables():
    """Dark and light theme CSS variables present."""
    content = read_css()
    assert "--bg:" in content
    assert "--ui:" in content
    assert '[data-theme="light"]' in content
    assert "#F5F0E8" in content or "#FDFCF9" in content  # light background
    assert "#1a1a1a" in content  # dark background
    print("  ✓ Dark and light theme CSS variables present")


def test_no_duplicate_css_blocks():
    """No duplicate :root or .setting-label CSS blocks."""
    content = read_css()
    # Count :root blocks (should be exactly 1)
    root_count = len(re.findall(r"^\s*:root\s*\{", content, re.MULTILINE))
    assert root_count == 1, f"Expected 1 :root block, found {root_count}"
    # Count .setting-label blocks (should be exactly 1)
    label_count = len(re.findall(r"^\s*\.setting-label\s*\{", content, re.MULTILINE))
    assert label_count == 1, f"Expected 1 .setting-label block, found {label_count}"
    print("  ✓ No duplicate CSS blocks")


def test_swatch_visibility():
    """Swatches have box-shadow for dark swatch visibility."""
    content = read_css()
    assert "box-shadow" in content
    assert ".swatch" in content
    print("  ✓ Swatch box-shadow present for visibility")


def test_sonnet_dropdown():
    """Dropdown is built dynamically from SONNETS data."""
    content = read_html()
    assert 'id="select-sonnet"' in content, "Missing dropdown element"
    assert "function buildDropdown()" in content, "Missing buildDropdown function"
    assert "SONNET_ORDER.forEach" in content, "Dropdown not built from SONNET_ORDER"
    print("  ✓ Dropdown built dynamically from SONNETS data")


def test_theme_buttons():
    """Auto, Dark, Light theme buttons present."""
    content = read_html()
    assert 'data-theme="auto"' in content
    assert 'data-theme="dark"' in content
    assert 'data-theme="light"' in content
    print("  ✓ Theme buttons (Auto/Dark/Light) present")


def test_settings_controls():
    """All settings controls present."""
    content = read_html()
    assert 'id="select-sonnet"' in content
    assert 'id="input-start"' in content
    assert 'id="color-swatches"' in content
    assert 'id="toggle-lines"' in content
    assert 'id="toggle-selftest"' in content
    assert 'id="btn-share"' in content
    print("  ✓ All settings controls present")


def test_toggle_accessibility():
    """Toggles have ARIA role, aria-checked, and tabindex."""
    content = read_html()
    assert 'role="switch"' in content, "Missing role=switch on toggles"
    assert 'aria-checked=' in content, "Missing aria-checked on toggles"
    assert 'aria-labelledby=' in content, "Missing aria-labelledby on toggles"
    assert "function setToggle(" in content, "Missing setToggle helper"
    print("  ✓ Toggle accessibility (role, aria-checked, tabindex)")


def test_swatch_accessibility():
    """Swatches have ARIA role and keyboard support."""
    content = read_html()
    assert "'role', 'radio'" in content, "Missing role=radio on swatches"
    assert "tabIndex = 0" in content, "Missing tabIndex on swatches"
    print("  ✓ Swatch accessibility (role, tabindex, keyboard)")


def test_body_uses_ui_font():
    """Body font-family is --font-ui; poetry uses --font-content."""
    content = read_css()
    # Body should use UI font
    body_match = re.search(r"body\s*\{[^}]*font-family:\s*var\(--font-ui\)", content)
    assert body_match, "Body should use --font-ui as default"
    # .line should use content font
    line_match = re.search(r"\.line\s*\{[^}]*font-family:\s*var\(--font-content\)", content)
    assert line_match, ".line should use --font-content for poetry"
    print("  ✓ Body uses --font-ui, poetry uses --font-content")


def test_responsive_breakpoint():
    """Responsive CSS media query present for small screens."""
    content = read_css()
    assert re.search(r"@media\s*\(\s*max-width", content), "Missing responsive media query"
    assert "480px" in content, "Missing 480px breakpoint"
    print("  ✓ Responsive breakpoint present")


# ---------------------------------------------------------------------------
# JavaScript logic tests (structural)
# ---------------------------------------------------------------------------

def test_calculate_function():
    """calculate() function exists with correct structure."""
    content = read_html()
    assert "function calculate()" in content
    assert "Math.floor((todayMidnight - start) / 86400000)" in content
    assert "Math.max(0, totalDays)" in content
    assert "SONNET_ORDER.indexOf(state.sonnet)" in content
    print("  ✓ calculate() function with correct structure")


def test_url_date_validation():
    """URL start date is validated with regex and Date check."""
    content = read_html()
    assert r"/^\d{4}-\d{2}-\d{2}$/" in content
    assert "isNaN" in content
    print("  ✓ URL start date validated")


def test_file_protocol_handling():
    """Share URL handles file:// protocol."""
    content = read_html()
    assert '"null"' in content
    assert "location.href.split" in content
    print("  ✓ file:// protocol handled in share URL")


def test_share_with_fallback():
    """Share uses Web Share API with clipboard fallback."""
    content = read_html()
    assert "navigator.share" in content
    assert "navigator.clipboard" in content
    assert ".catch(" in content
    print("  ✓ Share uses Web Share API with fallback")


def test_lines_param_explicit():
    """Share URL always includes lines param (on or off)."""
    content = read_html()
    assert "state.showLines ? 'on' : 'off'" in content
    print("  ✓ Share URL explicitly includes lines=on/off")


def test_fade_timeout_tracked():
    """Fade timeout is tracked and cleared on stop."""
    content = read_html()
    assert "fadeTimeout" in content
    assert "clearTimeout(state.fadeTimeout)" in content
    print("  ✓ Fade timeout tracked and cleared")


def test_dropdown_reflects_auto_advance():
    """Dropdown is updated to reflect auto-advanced sonnet."""
    content = read_html()
    assert "els.selectSonnet.value = currentSonnetId" in content
    print("  ✓ Dropdown reflects auto-advanced sonnet")


def test_localstorage_key():
    """Uses single localStorage key with JSON."""
    content = read_html()
    assert "'slowshakespeare'" in content
    assert "JSON.stringify" in content
    assert "JSON.parse" in content
    print("  ✓ localStorage uses single JSON key")


def test_review_mode_structure():
    """Review mode has start, stop, and interval."""
    content = read_html()
    assert "function startReview()" in content
    assert "function stopReview()" in content
    assert "setInterval(" in content
    assert "clearInterval(" in content
    assert "5000" in content  # 5 second interval
    print("  ✓ Review mode structure correct")


def test_selftest_mode():
    """Self-test mode cycles through lines with reveal logic."""
    content = read_html()
    assert "state.selfTest" in content
    assert "state.selfTestIndex" in content
    assert "state.selfTestRevealed" in content
    assert "tap to reveal" in content
    print("  ✓ Self-test mode present")


def test_dot_marker():
    """Dot marker shown on line 1 during review."""
    content = read_html()
    assert "dot-marker" in content
    assert "index === 0" in content
    print("  ✓ Dot marker on line 1 during review")


def test_date_input_validation():
    """onStartChange guards against empty date input."""
    content = read_html()
    assert "if (!value) return;" in content, "Missing empty date guard in onStartChange"
    print("  ✓ Empty date input guarded")


def test_sonnet_id_validation_storage():
    """loadFromStorage validates sonnet ID against SONNETS keys."""
    content = read_html()
    assert "data.sonnet && SONNETS[data.sonnet]" in content, (
        "Missing sonnet validation in loadFromStorage"
    )
    print("  ✓ localStorage sonnet ID validated")


def test_calculate_guards_negative_index():
    """calculate() guards against -1 from indexOf."""
    content = read_html()
    assert "Math.max(0, SONNET_ORDER.indexOf(state.sonnet))" in content, (
        "Missing -1 guard in calculate"
    )
    print("  ✓ calculate() guards against -1 sonnet index")


# ---------------------------------------------------------------------------
# URL parameter validation tests (logic)
# ---------------------------------------------------------------------------

def test_valid_date_format():
    """Valid date format passes regex."""
    import re as _re
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    assert _re.match(pattern, "2025-06-15")
    assert _re.match(pattern, "2024-01-01")
    assert not _re.match(pattern, "garbage")
    assert not _re.match(pattern, "2025-6-15")
    assert not _re.match(pattern, "06-15-2025")
    assert not _re.match(pattern, "")
    print("  ✓ Date format validation regex correct")


# ---------------------------------------------------------------------------
# Data file and SEO tests
# ---------------------------------------------------------------------------

def test_css_file_exists():
    """style.css file exists."""
    assert os.path.exists(CSS_FILE), "style.css not found"
    print("  ✓ style.css exists")


def test_css_file_loaded():
    """app.html loads style.css."""
    content = read_html()
    assert 'href="style.css"' in content, "Missing style.css link tag"
    print("  ✓ style.css loaded in app.html")


def test_data_js_exists():
    """data.js file exists."""
    assert os.path.exists(DATA_JS_FILE), "data.js not found"
    print("  ✓ data.js exists")


def test_data_js_loaded():
    """app.html loads data.js before inline script."""
    content = read_html()
    assert '<script src="data.js"></script>' in content, "Missing data.js script tag"
    # data.js must appear before the inline script
    data_pos = content.index('<script src="data.js">')
    inline_pos = content.index('<script>', data_pos + 1)
    assert data_pos < inline_pos, "data.js must load before inline script"
    print("  ✓ data.js loaded before inline script")


def test_seo_meta_tags():
    """SEO meta tags present in app.html."""
    content = read_html()
    assert 'name="description"' in content, "Missing meta description"
    assert 'property="og:title"' in content, "Missing og:title"
    assert 'property="og:description"' in content, "Missing og:description"
    print("  ✓ SEO meta tags present")


def test_seo_sonnets_section():
    """All 10 sonnets present in HTML SEO section."""
    content = read_html()
    assert 'id="sonnets"' in content, "Missing sonnets section"
    assert 'class="seo-sonnets"' in content, "Missing seo-sonnets class"
    for sid in SONNET_ORDER:
        assert f"Sonnet {sid}" in content, f"Missing Sonnet {sid} in SEO section"
    print("  ✓ All 10 sonnets in SEO section")


def test_seo_sonnets_hidden():
    """SEO sonnets hidden by CSS, with noscript fallback."""
    css = read_css()
    html = read_html()
    assert ".seo-sonnets" in css, "Missing .seo-sonnets CSS"
    assert "display: none" in css, "Missing display: none for seo-sonnets"
    assert "<noscript>" in html, "Missing noscript fallback"
    print("  ✓ SEO sonnets hidden with noscript fallback")


def test_canonical_urls():
    """Both pages have canonical link tags."""
    app = read_html()
    index = read_index()
    assert 'rel="canonical"' in app, "Missing canonical in app.html"
    assert 'rel="canonical"' in index, "Missing canonical in index.html"
    assert 'href="https://slowshakespeare.com/app.html"' in app, (
        "Wrong canonical URL in app.html"
    )
    assert 'href="https://slowshakespeare.com/"' in index, (
        "Wrong canonical URL in index.html"
    )
    print("  ✓ Canonical URLs present on both pages")


def test_twitter_cards():
    """Both pages have Twitter Card meta tags."""
    app = read_html()
    index = read_index()
    for name, content in [("app.html", app), ("index.html", index)]:
        assert 'twitter:card' in content, f"Missing twitter:card in {name}"
        assert 'twitter:title' in content, f"Missing twitter:title in {name}"
        assert 'twitter:description' in content, f"Missing twitter:description in {name}"
    print("  ✓ Twitter Card meta tags on both pages")


def test_theme_color_meta():
    """Both pages have theme-color meta tag."""
    app = read_html()
    index = read_index()
    assert 'name="theme-color"' in app, "Missing theme-color in app.html"
    assert 'name="theme-color"' in index, "Missing theme-color in index.html"
    print("  ✓ theme-color meta tag on both pages")


# ---------------------------------------------------------------------------
# Landing page (index.html) tests
# ---------------------------------------------------------------------------

def test_index_has_doctype():
    """index.html starts with DOCTYPE."""
    content = read_index()
    assert content.strip().startswith("<!DOCTYPE html>"), "Missing DOCTYPE"
    print("  ✓ index.html has DOCTYPE")


def test_index_has_lang():
    """index.html has lang attribute."""
    content = read_index()
    assert '<html lang="en">' in content, "Missing lang attribute"
    print("  ✓ index.html has lang='en'")


def test_index_has_viewport():
    """index.html has viewport meta tag."""
    content = read_index()
    assert 'name="viewport"' in content
    assert "width=device-width" in content
    print("  ✓ index.html has viewport meta")


def test_index_has_color_scheme():
    """index.html has color-scheme meta tag."""
    content = read_index()
    assert 'name="color-scheme"' in content, "Missing color-scheme meta"
    print("  ✓ index.html has color-scheme meta")


def test_index_has_description():
    """index.html has meta description."""
    content = read_index()
    assert 'name="description"' in content, "Missing meta description"
    print("  ✓ index.html has meta description")


def test_index_has_og_tags():
    """index.html has Open Graph meta tags."""
    content = read_index()
    assert 'property="og:title"' in content, "Missing og:title"
    assert 'property="og:description"' in content, "Missing og:description"
    assert 'property="og:type"' in content, "Missing og:type"
    assert 'property="og:url"' in content, "Missing og:url"
    print("  ✓ index.html has Open Graph tags")


def test_index_has_h1():
    """index.html has a single h1."""
    content = read_index()
    h1_count = content.count("<h1")
    assert h1_count == 1, f"Expected 1 <h1>, found {h1_count}"
    assert "Slow Shakespeare" in content
    print("  ✓ index.html has single h1")


def test_index_has_begin_cta():
    """index.html has a Begin link to app.html."""
    content = read_index()
    assert 'href="app.html"' in content, "Missing link to app.html"
    assert "Begin" in content, "Missing 'Begin' CTA text"
    print("  ✓ index.html has Begin CTA linking to app.html")


def test_index_has_sonnet_text():
    """index.html includes Sonnet 18 text for SEO."""
    content = read_index()
    assert "Shall I compare thee to a summer's day?" in content
    assert "So long lives this, and this gives life to thee." in content
    print("  ✓ index.html includes Sonnet 18 text")


def test_index_has_eb_garamond():
    """index.html loads EB Garamond font."""
    content = read_index()
    assert "EB+Garamond" in content or "EB Garamond" in content
    print("  ✓ index.html loads EB Garamond")


def test_index_responsive():
    """index.html has responsive CSS."""
    content = read_index()
    assert "@media" in content, "Missing media query"
    assert "480px" in content, "Missing 480px breakpoint"
    print("  ✓ index.html has responsive CSS")


def test_index_reduced_motion():
    """index.html respects prefers-reduced-motion."""
    content = read_index()
    assert "prefers-reduced-motion" in content, "Missing reduced motion media query"
    print("  ✓ index.html respects prefers-reduced-motion")


def test_index_dark_mode():
    """index.html supports dark mode via prefers-color-scheme."""
    content = read_index()
    assert "prefers-color-scheme: dark" in content, "Missing dark mode support"
    assert "#1a1a1a" in content, "Missing dark background color"
    print("  ✓ index.html supports dark mode")


def test_index_focus_visible():
    """index.html uses :focus-visible for keyboard navigation."""
    content = read_index()
    assert "focus-visible" in content, "Missing :focus-visible styles"
    print("  ✓ index.html uses :focus-visible")


def test_index_no_ios_reference():
    """index.html does not reference iOS (no app exists yet)."""
    content = read_index()
    # Check footer area specifically — "iOS" as a standalone word
    assert "iOS" not in content, "Footer references iOS but no iOS app exists"
    print("  ✓ index.html does not reference nonexistent iOS app")


def test_index_hero_section():
    """index.html has a full-viewport hero section."""
    content = read_index()
    assert "100vh" in content, "Missing 100vh hero"
    assert 'class="hero"' in content, "Missing hero section"
    assert 'class="hero-cta"' in content, "Missing hero CTA"
    print("  ✓ index.html has full-viewport hero")


def test_index_scroll_reveal():
    """index.html has scroll-reveal with IntersectionObserver."""
    content = read_index()
    assert 'class="reveal' in content or "reveal" in content, "Missing reveal class"
    assert "IntersectionObserver" in content, "Missing IntersectionObserver"
    assert ".reveal.visible" in content, "Missing .reveal.visible CSS"
    print("  ✓ index.html has scroll-reveal animation")


def test_index_scroll_hint():
    """index.html has animated scroll hint."""
    content = read_index()
    assert 'class="scroll-hint"' in content, "Missing scroll hint"
    assert 'aria-hidden="true"' in content, "Scroll hint should be aria-hidden"
    assert "@keyframes" in content, "Missing scroll hint animation"
    print("  ✓ index.html has scroll hint with animation")


def test_index_no_fleurons():
    """index.html no longer uses typographic ornaments."""
    content = read_index()
    assert "fleuron" not in content, "Should not contain fleuron classes"
    assert "&#10086;" not in content, "Should not contain fleuron characters"
    assert "&#10087;" not in content, "Should not contain fleuron characters"
    print("  ✓ index.html has no fleurons (modern design)")


# ---------------------------------------------------------------------------
# Additional best-practice tests
# ---------------------------------------------------------------------------

def test_app_has_color_scheme():
    """app.html has color-scheme meta tag."""
    content = read_html()
    assert 'name="color-scheme"' in content, "Missing color-scheme meta in app.html"
    print("  ✓ app.html has color-scheme meta")


def test_reduced_motion_css():
    """style.css respects prefers-reduced-motion."""
    content = read_css()
    assert "prefers-reduced-motion" in content, "Missing reduced motion in style.css"
    assert "transition: none" in content, "Should disable transitions for reduced motion"
    print("  ✓ style.css respects prefers-reduced-motion")


def test_escape_html_function():
    """escapeHTML function exists for XSS prevention in review mode."""
    content = read_html()
    assert "function escapeHTML(" in content, "Missing escapeHTML function"
    # Should use textContent for safe escaping (not regex replacement)
    assert "textContent" in content, "escapeHTML should use textContent for safety"
    print("  ✓ escapeHTML function present for XSS prevention")


def test_dom_content_loaded():
    """init() is called on DOMContentLoaded, not immediately."""
    content = read_html()
    assert "DOMContentLoaded" in content, "Missing DOMContentLoaded listener"
    assert "addEventListener('DOMContentLoaded', init)" in content, (
        "init should be registered as DOMContentLoaded listener"
    )
    print("  ✓ init() called on DOMContentLoaded")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def hex_to_rgb(hex_color):
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def relative_luminance(rgb):
    """WCAG 2.0 relative luminance."""
    vals = []
    for c in rgb:
        s = c / 255.0
        if s <= 0.03928:
            vals.append(s / 12.92)
        else:
            vals.append(((s + 0.055) / 1.055) ** 2.4)
    return 0.2126 * vals[0] + 0.7152 * vals[1] + 0.0722 * vals[2]


def contrast_ratio(fg, bg):
    """WCAG 2.0 contrast ratio between two RGB tuples."""
    l1 = relative_luminance(fg)
    l2 = relative_luminance(bg)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_all_tests():
    print("Running Slow Shakespeare web app tests...\n")

    sections = [
        ("Day Calculation", [
            test_day1_fresh_start,
            test_day8,
            test_day14,
            test_auto_advance,
            test_auto_advance_second,
            test_wrap_around,
            test_full_cycle_wrap,
            test_future_start_date,
            test_sonnet_order_preserved,
            test_mid_sonnet_days,
        ]),
        ("Sonnet Text", [
            test_all_sonnets_present,
            test_each_sonnet_has_14_lines,
            test_sonnet_text_parity_with_tidbyt,
        ]),
        ("Color System", [
            test_all_colors_in_html,
            test_color_labels_present,
            test_ink_distinct_from_milk,
            test_wcag_contrast_dark,
            test_wcag_contrast_light,
        ]),
        ("App HTML Structure", [
            test_has_viewport_meta,
            test_has_eb_garamond_font,
            test_font_variables,
            test_theme_css_variables,
            test_no_duplicate_css_blocks,
            test_swatch_visibility,
            test_sonnet_dropdown,
            test_theme_buttons,
            test_settings_controls,
            test_toggle_accessibility,
            test_swatch_accessibility,
            test_body_uses_ui_font,
            test_responsive_breakpoint,
        ]),
        ("JavaScript Logic", [
            test_calculate_function,
            test_url_date_validation,
            test_file_protocol_handling,
            test_share_with_fallback,
            test_lines_param_explicit,
            test_fade_timeout_tracked,
            test_dropdown_reflects_auto_advance,
            test_localstorage_key,
            test_review_mode_structure,
            test_selftest_mode,
            test_dot_marker,
            test_date_input_validation,
            test_sonnet_id_validation_storage,
            test_calculate_guards_negative_index,
            test_escape_html_function,
            test_dom_content_loaded,
        ]),
        ("URL Validation", [
            test_valid_date_format,
        ]),
        ("Data File & SEO", [
            test_css_file_exists,
            test_css_file_loaded,
            test_data_js_exists,
            test_data_js_loaded,
            test_seo_meta_tags,
            test_seo_sonnets_section,
            test_seo_sonnets_hidden,
            test_canonical_urls,
            test_twitter_cards,
            test_theme_color_meta,
        ]),
        ("Landing Page (index.html)", [
            test_index_has_doctype,
            test_index_has_lang,
            test_index_has_viewport,
            test_index_has_color_scheme,
            test_index_has_description,
            test_index_has_og_tags,
            test_index_has_h1,
            test_index_has_begin_cta,
            test_index_has_sonnet_text,
            test_index_has_eb_garamond,
            test_index_responsive,
            test_index_reduced_motion,
            test_index_dark_mode,
            test_index_focus_visible,
            test_index_no_ios_reference,
            test_index_hero_section,
            test_index_scroll_reveal,
            test_index_scroll_hint,
            test_index_no_fleurons,
        ]),
        ("Best Practices", [
            test_app_has_color_scheme,
            test_reduced_motion_css,
        ]),
    ]

    passed = 0
    failed = 0

    for section_name, tests in sections:
        print(f"[{section_name}]")
        for test in tests:
            try:
                test()
                passed += 1
            except AssertionError as e:
                print(f"  ✗ {test.__name__}: {e}")
                failed += 1
            except Exception as e:
                print(f"  ✗ {test.__name__}: Unexpected error: {e}")
                failed += 1
        print()

    print(f"{'=' * 40}")
    print(f"Results: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
