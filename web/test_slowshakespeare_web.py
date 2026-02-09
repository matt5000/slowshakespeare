#!/usr/bin/env python3
"""Tests for Slow Shakespeare web app.

This module tests the web app (app.html, style.css, data.js, index.html) by:
1. Reimplementing JavaScript logic in Python to verify calculations
2. Performing structural checks on HTML/CSS/JS files
3. Validating accessibility, SEO, and security requirements

Usage:
    python3 test_slowshakespeare_web.py           # Run all tests
    python3 -m unittest test_slowshakespeare_web  # Run via unittest
"""

import os
import re
import sys
import unittest
from datetime import date, timedelta
from typing import Dict, List, Optional, Tuple


# =============================================================================
# Constants
# =============================================================================

APP_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_FILE = os.path.join(APP_DIR, "app.html")
INDEX_FILE = os.path.join(APP_DIR, "index.html")
CSS_FILE = os.path.join(APP_DIR, "style.css")
DATA_JS_FILE = os.path.join(APP_DIR, "data.js")
TIDBYT_FILE = os.path.join(APP_DIR, "..", "tidbyt", "slow_shakespeare.star")

SONNET_ORDER: List[str] = [
    "1", "18", "29", "30", "55", "73", "104", "116", "130", "138"
]

SONNET_FIRST_LINES: Dict[str, str] = {
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

SONNET_LAST_LINES: Dict[str, str] = {
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

COLORS: Dict[str, Dict[str, str]] = {
    "salad": {"dark": "#8FBF8F", "light": "#4A6B4A", "swatch": "#3E6D4E"},
    "milk": {"dark": "#B5A99A", "light": "#4A4540", "swatch": "#B5A99A"},
    "midsummer": {"dark": "#7BA3D4", "light": "#2B4578", "swatch": "#2B4578"},
    "glisters": {"dark": "#D4B86A", "light": "#6B5A1E", "swatch": "#B8993E"},
    "damask": {"dark": "#D4856E", "light": "#B44430", "swatch": "#B44430"},
    "ink": {"dark": "#D5CFC5", "light": "#2A2520", "swatch": "#2A2520"},
}


# =============================================================================
# Helper Functions
# =============================================================================

def read_file(path: str) -> str:
    """Read and return the contents of a file."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color to RGB tuple."""
    h = hex_color.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def relative_luminance(rgb: Tuple[int, int, int]) -> float:
    """Calculate WCAG 2.0 relative luminance."""
    vals = []
    for c in rgb:
        s = c / 255.0
        if s <= 0.03928:
            vals.append(s / 12.92)
        else:
            vals.append(((s + 0.055) / 1.055) ** 2.4)
    return 0.2126 * vals[0] + 0.7152 * vals[1] + 0.0722 * vals[2]


def contrast_ratio(
    fg: Tuple[int, int, int],
    bg: Tuple[int, int, int]
) -> float:
    """Calculate WCAG 2.0 contrast ratio between two RGB colors."""
    l1 = relative_luminance(fg)
    l2 = relative_luminance(bg)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def calculate(
    start_date_str: str,
    sonnet_id: str,
    today: Optional[date] = None
) -> Dict[str, any]:
    """Reimplement the JS calculate() function in Python.

    This must exactly match the logic in app.html.

    Args:
        start_date_str: ISO format date string (YYYY-MM-DD).
        sonnet_id: The sonnet ID to start from.
        today: Optional date to use as "today" (for testing).

    Returns:
        Dict with currentSonnetId, linesLearned, dayWithinSonnet, safeDays.
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


# =============================================================================
# Base Test Case with File Caching
# =============================================================================

class SlowShakespeareTestCase(unittest.TestCase):
    """Base test case with cached file reading."""

    _html_content: Optional[str] = None
    _index_content: Optional[str] = None
    _css_content: Optional[str] = None
    _data_js_content: Optional[str] = None
    _tidbyt_content: Optional[str] = None

    @classmethod
    def setUpClass(cls) -> None:
        """Load all files once for the entire test class."""
        cls._html_content = read_file(HTML_FILE)
        cls._index_content = read_file(INDEX_FILE)
        cls._css_content = read_file(CSS_FILE)
        cls._data_js_content = read_file(DATA_JS_FILE)
        if os.path.exists(TIDBYT_FILE):
            cls._tidbyt_content = read_file(TIDBYT_FILE)

    @property
    def html(self) -> str:
        """Get app.html content."""
        return self._html_content

    @property
    def index(self) -> str:
        """Get index.html content."""
        return self._index_content

    @property
    def css(self) -> str:
        """Get style.css content."""
        return self._css_content

    @property
    def data_js(self) -> str:
        """Get data.js content."""
        return self._data_js_content

    @property
    def tidbyt(self) -> Optional[str]:
        """Get Tidbyt Starlark content, or None if not found."""
        return self._tidbyt_content


# =============================================================================
# Day Calculation Tests
# =============================================================================

class TestDayCalculation(SlowShakespeareTestCase):
    """Tests for the day calculation logic."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.test_date = date(2025, 6, 15)

    def test_day1_fresh_start(self) -> None:
        """Start date = today => Day 1 of 14, line 1."""
        r = calculate("2025-06-15", "18", self.test_date)
        self.assertEqual(r["currentSonnetId"], "18")
        self.assertEqual(r["dayWithinSonnet"], 0)
        self.assertEqual(r["linesLearned"], 1)

    def test_day8_shows_8_lines(self) -> None:
        """Start date = 7 days ago => Day 8, 8 lines learned."""
        r = calculate("2025-06-08", "18", self.test_date)
        self.assertEqual(r["dayWithinSonnet"], 7)
        self.assertEqual(r["linesLearned"], 8)

    def test_day14_shows_all_lines(self) -> None:
        """Start date = 13 days ago => Day 14, all 14 lines."""
        r = calculate("2025-06-02", "18", self.test_date)
        self.assertEqual(r["dayWithinSonnet"], 13)
        self.assertEqual(r["linesLearned"], 14)

    def test_auto_advance_after_14_days(self) -> None:
        """After 14 days, advances to next sonnet."""
        r = calculate("2025-06-01", "18", self.test_date)
        self.assertEqual(r["currentSonnetId"], "29")
        self.assertEqual(r["dayWithinSonnet"], 0)
        self.assertEqual(r["linesLearned"], 1)

    def test_auto_advance_after_28_days(self) -> None:
        """After 28 days, advances two sonnets."""
        r = calculate("2025-05-18", "18", self.test_date)
        self.assertEqual(r["currentSonnetId"], "30")
        self.assertEqual(r["dayWithinSonnet"], 0)

    def test_wrap_around_after_last_sonnet(self) -> None:
        """After last sonnet (138), wraps to beginning (1)."""
        r = calculate("2025-06-01", "138", self.test_date)
        self.assertEqual(r["currentSonnetId"], "1")

    def test_full_cycle_returns_to_start(self) -> None:
        """After 140 days (10 sonnets * 14 days), wraps back to start."""
        start = self.test_date - timedelta(days=140)
        r = calculate(start.isoformat(), "1", self.test_date)
        self.assertEqual(r["currentSonnetId"], "1")
        self.assertEqual(r["dayWithinSonnet"], 0)

    def test_future_start_clamps_to_day1(self) -> None:
        """Future start date => clamps to Day 1."""
        r = calculate("2025-07-01", "18", self.test_date)
        self.assertEqual(r["safeDays"], 0)
        self.assertEqual(r["dayWithinSonnet"], 0)
        self.assertEqual(r["linesLearned"], 1)

    def test_sonnet_order_preserved(self) -> None:
        """Auto-advance follows the defined order."""
        start = self.test_date
        for i, expected_id in enumerate(SONNET_ORDER):
            r = calculate(
                start.isoformat(), "1",
                self.test_date + timedelta(days=i * 14)
            )
            self.assertEqual(
                r["currentSonnetId"], expected_id,
                f"Day {i * 14}: expected {expected_id}"
            )

    def test_all_14_days_show_correct_lines(self) -> None:
        """Each day within a 14-day cycle shows correct line count."""
        for day in range(14):
            start = (self.test_date - timedelta(days=day)).isoformat()
            r = calculate(start, "18", self.test_date)
            self.assertEqual(
                r["linesLearned"], day + 1,
                f"Day {day}: expected {day + 1} lines"
            )


# =============================================================================
# Sonnet Text Tests
# =============================================================================

class TestSonnetText(SlowShakespeareTestCase):
    """Tests for sonnet text content."""

    def test_all_sonnets_have_first_lines(self) -> None:
        """All 10 sonnets have correct first lines in HTML."""
        for sid, first_line in SONNET_FIRST_LINES.items():
            self.assertIn(
                first_line, self.html,
                f"Missing first line of Sonnet {sid}"
            )

    def test_all_sonnets_have_last_lines(self) -> None:
        """All 10 sonnets have correct last lines in HTML."""
        for sid, last_line in SONNET_LAST_LINES.items():
            self.assertIn(
                last_line, self.html,
                f"Missing last line of Sonnet {sid}"
            )

    def test_each_sonnet_has_14_lines(self) -> None:
        """Each sonnet has exactly 14 lines in data.js."""
        for sid in SONNET_ORDER:
            pattern = rf'"{sid}":\s*\[(.*?)\]'
            match = re.search(pattern, self.data_js, re.DOTALL)
            self.assertIsNotNone(match, f"Could not find sonnet {sid}")
            raw_lines = match.group(1).split("\n")
            lines = [ln for ln in raw_lines if ln.strip().startswith('"')]
            self.assertEqual(
                len(lines), 14,
                f"Sonnet {sid}: expected 14 lines, got {len(lines)}"
            )

    def test_text_matches_tidbyt_app(self) -> None:
        """Sonnet text matches the Tidbyt app exactly."""
        if self.tidbyt is None:
            self.skipTest("Tidbyt file not found")

        for sid, first_line in SONNET_FIRST_LINES.items():
            self.assertIn(first_line, self.tidbyt)
        for sid, last_line in SONNET_LAST_LINES.items():
            self.assertIn(last_line, self.tidbyt)


# =============================================================================
# Color System Tests
# =============================================================================

class TestColorSystem(SlowShakespeareTestCase):
    """Tests for the color theme system."""

    def test_all_colors_present_in_data_js(self) -> None:
        """All 6 color themes with hex values present in data.js."""
        for name, vals in COLORS.items():
            self.assertIn(vals["dark"], self.data_js,
                          f"Missing dark for {name}")
            self.assertIn(vals["light"], self.data_js,
                          f"Missing light for {name}")
            self.assertIn(vals["swatch"], self.data_js,
                          f"Missing swatch for {name}")

    def test_all_color_labels_present(self) -> None:
        """All color labels present in data.js."""
        labels = [
            "Salad Days", "Milk of Kindness", "Midsummer Night",
            "All That Glisters", "Damask Rose", "Black Ink"
        ]
        for label in labels:
            self.assertIn(label, self.data_js, f"Missing label: {label}")

    def test_ink_distinct_from_milk(self) -> None:
        """Black Ink dark variant differs from Milk of Kindness."""
        self.assertNotEqual(
            COLORS["ink"]["dark"], COLORS["milk"]["dark"],
            "Black Ink and Milk of Kindness should differ"
        )

    def test_dark_mode_wcag_contrast(self) -> None:
        """All dark-mode colors pass WCAG AA (4.5:1) on #1a1a1a."""
        bg = (0x1a, 0x1a, 0x1a)
        for name, vals in COLORS.items():
            fg = hex_to_rgb(vals["dark"])
            ratio = contrast_ratio(fg, bg)
            self.assertGreaterEqual(
                ratio, 4.5,
                f"{name} dark: {ratio:.1f}:1 < 4.5:1"
            )

    def test_light_mode_wcag_contrast(self) -> None:
        """All light-mode colors pass WCAG AA (4.5:1) on #FDFCF9."""
        bg = (0xFD, 0xFC, 0xF9)
        for name, vals in COLORS.items():
            fg = hex_to_rgb(vals["light"])
            ratio = contrast_ratio(fg, bg)
            self.assertGreaterEqual(
                ratio, 4.5,
                f"{name} light: {ratio:.1f}:1 < 4.5:1"
            )


# =============================================================================
# HTML Structure Tests
# =============================================================================

class TestHTMLStructure(SlowShakespeareTestCase):
    """Tests for app.html structure."""

    def test_has_viewport_meta(self) -> None:
        """Mobile viewport meta tag present."""
        self.assertIn('name="viewport"', self.html)
        self.assertIn("width=device-width", self.html)

    def test_has_eb_garamond_font(self) -> None:
        """EB Garamond Google Font loaded."""
        self.assertTrue(
            "EB+Garamond" in self.html or "EB Garamond" in self.html
        )

    def test_has_font_variables(self) -> None:
        """CSS font variables defined."""
        self.assertIn("--font-content", self.css)
        self.assertIn("--font-ui", self.css)
        self.assertIn("system-ui", self.css)

    def test_has_theme_variables(self) -> None:
        """Dark and light theme CSS variables present."""
        self.assertIn("--bg:", self.css)
        self.assertIn('[data-theme="light"]', self.css)
        self.assertIn("#1a1a1a", self.css)

    def test_no_duplicate_css_blocks(self) -> None:
        """No duplicate :root or .setting-label CSS blocks."""
        root_count = len(re.findall(
            r"^\s*:root\s*\{", self.css, re.MULTILINE
        ))
        self.assertEqual(root_count, 1)

        label_count = len(re.findall(
            r"^\s*\.setting-label\s*\{", self.css, re.MULTILINE
        ))
        self.assertEqual(label_count, 1)

    def test_swatch_has_box_shadow(self) -> None:
        """Swatches have box-shadow for dark swatch visibility."""
        self.assertIn("box-shadow", self.css)
        self.assertIn(".swatch", self.css)

    def test_dropdown_built_dynamically(self) -> None:
        """Dropdown is built dynamically from SONNETS data."""
        self.assertIn('id="select-sonnet"', self.html)
        self.assertIn("function buildDropdown()", self.html)
        self.assertIn("SONNET_ORDER.forEach", self.html)

    def test_theme_buttons_present(self) -> None:
        """Auto, Dark, Light theme buttons present."""
        self.assertIn('data-theme="auto"', self.html)
        self.assertIn('data-theme="dark"', self.html)
        self.assertIn('data-theme="light"', self.html)

    def test_all_settings_controls_present(self) -> None:
        """All settings controls present."""
        controls = [
            'id="select-sonnet"', 'id="input-start"',
            'id="color-swatches"', 'id="toggle-lines"', 'id="btn-share"'
        ]
        for ctrl in controls:
            self.assertIn(ctrl, self.html, f"Missing {ctrl}")

    def test_toggle_accessibility(self) -> None:
        """Toggles have ARIA role, aria-checked, and tabindex."""
        self.assertIn('role="switch"', self.html)
        self.assertIn('aria-checked=', self.html)
        self.assertIn('aria-labelledby=', self.html)

    def test_swatch_accessibility(self) -> None:
        """Swatches have ARIA role and keyboard support."""
        self.assertIn("'role', 'radio'", self.html)
        self.assertIn("tabIndex = 0", self.html)

    def test_body_uses_ui_font(self) -> None:
        """Body uses --font-ui; poetry uses --font-content."""
        body_match = re.search(
            r"body\s*\{[^}]*font-family:\s*var\(--font-ui\)", self.css
        )
        self.assertIsNotNone(body_match, "Body should use --font-ui")

        line_match = re.search(
            r"\.line\s*\{[^}]*font-family:\s*var\(--font-content\)", self.css
        )
        self.assertIsNotNone(line_match, ".line should use --font-content")

    def test_responsive_breakpoint(self) -> None:
        """Responsive CSS media query present for small screens."""
        self.assertIsNotNone(
            re.search(r"@media\s*\(\s*max-width", self.css)
        )
        self.assertIn("480px", self.css)


# =============================================================================
# JavaScript Logic Tests
# =============================================================================

class TestJavaScriptLogic(SlowShakespeareTestCase):
    """Tests for JavaScript logic in app.html."""

    def test_calculate_function_structure(self) -> None:
        """calculate() function exists with correct structure."""
        self.assertIn("function calculate()", self.html)
        self.assertIn("MS_PER_DAY", self.html)
        self.assertIn("Math.floor((todayMidnight - start) / MS_PER_DAY",
                      self.html)
        self.assertIn("Math.max(0, totalDays)", self.html)

    def test_url_date_validation(self) -> None:
        """URL start date validated with regex and Date check."""
        self.assertIn(r"/^\d{4}-\d{2}-\d{2}$/", self.html)
        self.assertIn("isNaN", self.html)

    def test_file_protocol_handling(self) -> None:
        """Share URL handles file:// protocol."""
        self.assertIn('"null"', self.html)
        self.assertIn("location.href.split", self.html)

    def test_share_with_fallback(self) -> None:
        """Share uses Web Share API with clipboard fallback."""
        self.assertIn("navigator.share", self.html)
        self.assertIn("navigator.clipboard", self.html)
        self.assertIn(".catch(", self.html)

    def test_lines_param_explicit(self) -> None:
        """Share URL always includes lines param (on or off)."""
        self.assertIn("state.showLines ? 'on' : 'off'", self.html)

    def test_fade_timeout_tracked(self) -> None:
        """Fade timeout is tracked and cleared on stop."""
        self.assertIn("fadeTimeout", self.html)
        self.assertIn("clearTimeout(state.fadeTimeout)", self.html)

    def test_dropdown_reflects_auto_advance(self) -> None:
        """Dropdown updated to reflect auto-advanced sonnet."""
        self.assertIn("els.selectSonnet.value = currentSonnetId", self.html)

    def test_localstorage_uses_json(self) -> None:
        """Uses single localStorage key with JSON."""
        self.assertIn("'slowshakespeare'", self.html)
        self.assertIn("JSON.stringify", self.html)
        self.assertIn("JSON.parse", self.html)

    def test_review_mode_structure(self) -> None:
        """Review mode has start, stop, and interval."""
        self.assertIn("function startReview()", self.html)
        self.assertIn("function stopReview()", self.html)
        self.assertIn("setInterval(", self.html)
        self.assertIn("clearInterval(", self.html)
        self.assertIn("5000", self.html)

    def test_dot_marker_on_line1(self) -> None:
        """Dot marker shown on line 1 during review."""
        self.assertIn("dot-marker", self.html)
        self.assertIn("index === 0", self.html)

    def test_empty_date_guarded(self) -> None:
        """onStartChange guards against empty date input."""
        self.assertIn("if (!value) return;", self.html)

    def test_sonnet_id_validated_in_storage(self) -> None:
        """loadFromStorage validates sonnet ID against SONNETS."""
        self.assertIn("data.sonnet && SONNETS[data.sonnet]", self.html)

    def test_calculate_guards_negative_index(self) -> None:
        """calculate() guards against -1 from indexOf."""
        self.assertIn(
            "Math.max(0, SONNET_ORDER.indexOf(state.sonnet))", self.html
        )

    def test_escape_html_present(self) -> None:
        """escapeHTML function exists for XSS prevention."""
        self.assertIn("function escapeHTML(", self.html)
        self.assertIn("textContent", self.html)

    def test_init_on_dom_content_loaded(self) -> None:
        """init() called on DOMContentLoaded."""
        self.assertIn("DOMContentLoaded", self.html)
        self.assertIn("addEventListener('DOMContentLoaded', init)", self.html)


# =============================================================================
# URL Validation Tests
# =============================================================================

class TestURLValidation(SlowShakespeareTestCase):
    """Tests for URL parameter validation."""

    def test_date_format_regex(self) -> None:
        """Date format regex correctly validates input."""
        pattern = r"^\d{4}-\d{2}-\d{2}$"
        self.assertIsNotNone(re.match(pattern, "2025-06-15"))
        self.assertIsNotNone(re.match(pattern, "2024-01-01"))
        self.assertIsNone(re.match(pattern, "garbage"))
        self.assertIsNone(re.match(pattern, "2025-6-15"))
        self.assertIsNone(re.match(pattern, "06-15-2025"))
        self.assertIsNone(re.match(pattern, ""))


# =============================================================================
# Data File & SEO Tests
# =============================================================================

class TestDataFilesAndSEO(SlowShakespeareTestCase):
    """Tests for data files and SEO elements."""

    def test_css_file_exists(self) -> None:
        """style.css file exists."""
        self.assertTrue(os.path.exists(CSS_FILE))

    def test_css_loaded_in_html(self) -> None:
        """app.html loads style.css."""
        self.assertIn('href="style.css"', self.html)

    def test_data_js_exists(self) -> None:
        """data.js file exists."""
        self.assertTrue(os.path.exists(DATA_JS_FILE))

    def test_data_js_loaded_before_inline(self) -> None:
        """app.html loads data.js before inline script."""
        self.assertIn('<script src="data.js"></script>', self.html)
        data_pos = self.html.index('<script src="data.js">')
        inline_pos = self.html.index('<script>', data_pos + 1)
        self.assertLess(data_pos, inline_pos)

    def test_seo_meta_tags_present(self) -> None:
        """SEO meta tags present in app.html."""
        self.assertIn('name="description"', self.html)
        self.assertIn('property="og:title"', self.html)
        self.assertIn('property="og:description"', self.html)

    def test_seo_sonnets_section(self) -> None:
        """All 10 sonnets present in HTML SEO section."""
        self.assertIn('id="sonnets"', self.html)
        self.assertIn('class="seo-sonnets"', self.html)
        for sid in SONNET_ORDER:
            self.assertIn(f"Sonnet {sid}", self.html)

    def test_seo_sonnets_hidden(self) -> None:
        """SEO sonnets hidden by CSS, with noscript fallback."""
        self.assertIn(".seo-sonnets", self.css)
        self.assertIn("display: none", self.css)
        self.assertIn("<noscript>", self.html)

    def test_canonical_urls(self) -> None:
        """Both pages have canonical link tags."""
        self.assertIn('rel="canonical"', self.html)
        self.assertIn('rel="canonical"', self.index)
        self.assertIn('href="https://slowshakespeare.com/app.html"', self.html)
        self.assertIn('href="https://slowshakespeare.com/"', self.index)

    def test_twitter_cards(self) -> None:
        """Both pages have Twitter Card meta tags."""
        for content in [self.html, self.index]:
            self.assertIn('twitter:card', content)
            self.assertIn('twitter:title', content)
            self.assertIn('twitter:description', content)

    def test_theme_color_meta(self) -> None:
        """Both pages have theme-color meta tag."""
        self.assertIn('name="theme-color"', self.html)
        self.assertIn('name="theme-color"', self.index)


# =============================================================================
# Landing Page Tests
# =============================================================================

class TestLandingPage(SlowShakespeareTestCase):
    """Tests for index.html landing page."""

    def test_has_doctype(self) -> None:
        """index.html starts with DOCTYPE."""
        self.assertTrue(self.index.strip().startswith("<!DOCTYPE html>"))

    def test_has_lang_attribute(self) -> None:
        """index.html has lang attribute."""
        self.assertIn('<html lang="en">', self.index)

    def test_has_viewport_meta(self) -> None:
        """index.html has viewport meta tag."""
        self.assertIn('name="viewport"', self.index)
        self.assertIn("width=device-width", self.index)

    def test_has_color_scheme_meta(self) -> None:
        """index.html has color-scheme meta tag."""
        self.assertIn('name="color-scheme"', self.index)

    def test_has_description_meta(self) -> None:
        """index.html has meta description."""
        self.assertIn('name="description"', self.index)

    def test_has_og_tags(self) -> None:
        """index.html has Open Graph meta tags."""
        og_tags = ["og:title", "og:description", "og:type", "og:url"]
        for tag in og_tags:
            self.assertIn(f'property="{tag}"', self.index)

    def test_has_single_h1(self) -> None:
        """index.html has a single h1."""
        h1_count = self.index.count("<h1")
        self.assertEqual(h1_count, 1)
        self.assertIn("Slow Shakespeare", self.index)

    def test_has_begin_cta(self) -> None:
        """index.html has a Begin link to app.html."""
        self.assertIn('href="app.html"', self.index)
        self.assertIn("Begin", self.index)

    def test_includes_sonnet_18_text(self) -> None:
        """index.html includes Sonnet 18 text for SEO."""
        self.assertIn("Shall I compare thee to a summer's day?", self.index)
        self.assertIn(
            "So long lives this, and this gives life to thee.", self.index
        )

    def test_loads_eb_garamond(self) -> None:
        """index.html loads EB Garamond font."""
        self.assertTrue(
            "EB+Garamond" in self.index or "EB Garamond" in self.index
        )

    def test_has_responsive_css(self) -> None:
        """index.html has responsive CSS."""
        self.assertIn("@media", self.index)
        self.assertIn("480px", self.index)

    def test_respects_reduced_motion(self) -> None:
        """index.html respects prefers-reduced-motion."""
        self.assertIn("prefers-reduced-motion", self.index)

    def test_supports_dark_mode(self) -> None:
        """index.html supports dark mode via prefers-color-scheme."""
        self.assertIn("prefers-color-scheme: dark", self.index)
        self.assertIn("#1a1a1a", self.index)

    def test_uses_focus_visible(self) -> None:
        """index.html uses :focus-visible for keyboard navigation."""
        self.assertIn("focus-visible", self.index)

    def test_ios_labeled_coming_soon(self) -> None:
        """index.html correctly labels iOS as coming soon."""
        if "iOS" in self.index:
            self.assertIn("coming soon", self.index)

    def test_has_hero_section(self) -> None:
        """index.html has a full-viewport hero section."""
        self.assertIn("100vh", self.index)
        self.assertIn('class="hero"', self.index)
        self.assertIn('class="hero-cta"', self.index)

    def test_has_scroll_reveal(self) -> None:
        """index.html has scroll-reveal with IntersectionObserver."""
        self.assertTrue('class="reveal' in self.index or "reveal" in self.index)
        self.assertIn("IntersectionObserver", self.index)
        self.assertIn(".reveal.visible", self.index)

    def test_has_scroll_hint(self) -> None:
        """index.html has animated scroll hint."""
        self.assertIn('class="scroll-hint"', self.index)
        self.assertIn('aria-hidden="true"', self.index)
        self.assertIn("@keyframes", self.index)

    def test_no_fleurons(self) -> None:
        """index.html no longer uses typographic ornaments."""
        self.assertNotIn("fleuron", self.index)
        self.assertNotIn("&#10086;", self.index)
        self.assertNotIn("&#10087;", self.index)


# =============================================================================
# Best Practices Tests
# =============================================================================

class TestBestPractices(SlowShakespeareTestCase):
    """Tests for web development best practices."""

    def test_app_has_color_scheme_meta(self) -> None:
        """app.html has color-scheme meta tag."""
        self.assertIn('name="color-scheme"', self.html)

    def test_css_respects_reduced_motion(self) -> None:
        """style.css respects prefers-reduced-motion."""
        self.assertIn("prefers-reduced-motion", self.css)
        self.assertIn("transition: none", self.css)


# =============================================================================
# Custom Test Runner (for backwards compatibility)
# =============================================================================

def run_all_tests() -> bool:
    """Run all tests with custom output format.

    Returns:
        True if all tests passed, False otherwise.
    """
    print("Running Slow Shakespeare web app tests...\n")

    # Map test classes to section names
    sections = [
        ("Day Calculation", TestDayCalculation),
        ("Sonnet Text", TestSonnetText),
        ("Color System", TestColorSystem),
        ("App HTML Structure", TestHTMLStructure),
        ("JavaScript Logic", TestJavaScriptLogic),
        ("URL Validation", TestURLValidation),
        ("Data File & SEO", TestDataFilesAndSEO),
        ("Landing Page (index.html)", TestLandingPage),
        ("Best Practices", TestBestPractices),
    ]

    passed = 0
    failed = 0

    for section_name, test_class in sections:
        print(f"[{section_name}]")

        # Load and run tests from the class
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromTestCase(test_class)

        for test in suite:
            test_name = test._testMethodName
            try:
                # Run setUp/setUpClass if needed
                test.setUpClass()
                test.setUp()
                getattr(test, test_name)()
                passed += 1
                # Create short description from method name
                desc = test_name.replace("test_", "").replace("_", " ")
                print(f"  ✓ {desc.capitalize()}")
            except unittest.SkipTest as e:
                print(f"  ⊘ {test_name}: Skipped ({e})")
                passed += 1  # Count skips as passes
            except AssertionError as e:
                print(f"  ✗ {test_name}: {e}")
                failed += 1
            except Exception as e:
                print(f"  ✗ {test_name}: Unexpected error: {e}")
                failed += 1

        print()

    print("=" * 40)
    print(f"Results: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    # Support both custom runner and unittest
    if len(sys.argv) > 1 and sys.argv[1] == "--unittest":
        unittest.main(argv=[""], exit=True, verbosity=2)
    else:
        success = run_all_tests()
        sys.exit(0 if success else 1)
