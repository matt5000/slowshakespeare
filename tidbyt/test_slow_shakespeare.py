#!/usr/bin/env python3
"""Tests for slow_shakespeare.star Tidbyt application.

This module tests the Tidbyt Starlark app by:
1. Verifying it renders successfully with pixlet
2. Checking structural requirements (imports, functions, schema)
3. Validating sonnet content and display settings

Usage:
    python3 test_slow_shakespeare.py           # Run all tests
    python3 -m unittest test_slow_shakespeare  # Run via unittest
"""

import os
import subprocess
import sys
import unittest
from typing import Optional, Tuple


# =============================================================================
# Constants
# =============================================================================

APP_DIR = os.path.dirname(os.path.abspath(__file__))
STAR_FILE = os.path.join(APP_DIR, "slow_shakespeare.star")

SONNET_IDS = ["1", "18", "29", "30", "55", "73", "104", "116", "130", "138"]

FIRST_LINES = {
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

LAST_LINES = {
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

COLOR_NAMES = [
    "Salad Days",
    "Milk of Kindness",
    "Midsummer Night",
    "All That Glisters",
    "Damask Rose",
]


# =============================================================================
# Helper Functions
# =============================================================================

def run_pixlet_render() -> Tuple[bool, str]:
    """Render the app and return success/failure.

    Returns:
        A tuple of (success: bool, stderr: str).
    """
    result = subprocess.run(
        ["pixlet", "render", STAR_FILE],
        capture_output=True,
        text=True,
        cwd=APP_DIR,
        check=False,
    )
    return result.returncode == 0, result.stderr


def read_star_file() -> str:
    """Read the star file contents.

    Returns:
        The contents of the star file as a string.
    """
    with open(STAR_FILE, "r", encoding="utf-8") as f:
        return f.read()


# =============================================================================
# Base Test Case
# =============================================================================

class TidbytTestCase(unittest.TestCase):
    """Base test case with cached file reading."""

    _content: Optional[str] = None

    @classmethod
    def setUpClass(cls) -> None:
        """Load the star file once for all tests."""
        cls._content = read_star_file()

    @property
    def content(self) -> str:
        """Get the star file content."""
        return self._content


# =============================================================================
# Render Tests
# =============================================================================

class TestRender(TidbytTestCase):
    """Tests for pixlet rendering."""

    def test_renders_successfully(self) -> None:
        """App renders without errors."""
        success, stderr = run_pixlet_render()
        self.assertTrue(success, f"Render failed: {stderr}")

    def test_webp_output_created(self) -> None:
        """Rendering produces a webp file."""
        webp_path = os.path.join(APP_DIR, "slow_shakespeare.webp")
        if os.path.exists(webp_path):
            os.remove(webp_path)
        success, _ = run_pixlet_render()
        self.assertTrue(success, "Render failed")
        self.assertTrue(
            os.path.exists(webp_path),
            "slow_shakespeare.webp not created"
        )


# =============================================================================
# Structure Tests
# =============================================================================

class TestStructure(TidbytTestCase):
    """Tests for app structure and imports."""

    def test_has_render_import(self) -> None:
        """render.star imported."""
        self.assertIn('load("render.star", "render")', self.content)

    def test_has_time_import(self) -> None:
        """time.star imported."""
        self.assertIn('load("time.star", "time")', self.content)

    def test_has_schema_import(self) -> None:
        """schema.star imported."""
        self.assertIn('load("schema.star", "schema")', self.content)

    def test_has_main_function(self) -> None:
        """main function exists with config parameter."""
        self.assertIn("def main(config):", self.content)

    def test_has_get_schema_function(self) -> None:
        """get_schema function exists."""
        self.assertIn("def get_schema():", self.content)


# =============================================================================
# Sonnet Content Tests
# =============================================================================

class TestSonnetContent(TidbytTestCase):
    """Tests for sonnet text content."""

    def test_sonnets_dictionary_exists(self) -> None:
        """SONNETS dictionary exists."""
        self.assertIn("SONNETS = {", self.content)

    def test_all_sonnet_keys_present(self) -> None:
        """All 10 sonnet keys present in dictionary."""
        for sid in SONNET_IDS:
            self.assertIn(f'"{sid}":', self.content,
                          f"Missing sonnet {sid} key")

    def test_all_first_lines_present(self) -> None:
        """All sonnet first lines present."""
        for sid, line in FIRST_LINES.items():
            self.assertIn(line, self.content,
                          f"Missing first line of Sonnet {sid}")

    def test_all_last_lines_present(self) -> None:
        """All sonnet last lines present."""
        for sid, line in LAST_LINES.items():
            self.assertIn(line, self.content,
                          f"Missing last line of Sonnet {sid}")


# =============================================================================
# Schema Tests
# =============================================================================

class TestSchema(TidbytTestCase):
    """Tests for Tidbyt schema configuration."""

    def test_has_sonnet_dropdown(self) -> None:
        """Schema has sonnet dropdown."""
        self.assertIn("schema.Dropdown(", self.content)
        self.assertIn('id = "sonnet"', self.content)

    def test_sonnet_dropdown_has_all_options(self) -> None:
        """Sonnet dropdown has all 10 options."""
        for sid in SONNET_IDS:
            self.assertIn(f'value = "{sid}"', self.content,
                          f"Missing sonnet {sid} option")

    def test_has_color_dropdown(self) -> None:
        """Schema has color dropdown with Shakespeare names."""
        self.assertIn('id = "color"', self.content)
        for name in COLOR_NAMES:
            self.assertIn(name, self.content, f"Missing {name} option")

    def test_default_color_is_salad_days(self) -> None:
        """Default color is Salad Days green."""
        self.assertIn("#8FBF8F", self.content)
        self.assertIn('default = "#8FBF8F"', self.content)

    def test_has_start_date_picker(self) -> None:
        """Schema has start date picker."""
        self.assertIn("schema.DateTime", self.content)
        self.assertIn('id = "start_date"', self.content)

    def test_config_uses_default_sonnet(self) -> None:
        """Config.get uses default sonnet 18."""
        self.assertIn('config.get("sonnet", "18")', self.content)


# =============================================================================
# Display Tests
# =============================================================================

class TestDisplay(TidbytTestCase):
    """Tests for display settings."""

    def test_uses_tom_thumb_font(self) -> None:
        """tom-thumb font used for LED display."""
        self.assertIn('font = "tom-thumb"', self.content)

    def test_text_is_left_aligned(self) -> None:
        """Text is left aligned."""
        self.assertIn('align = "left"', self.content)

    def test_has_padding(self) -> None:
        """Padding applied to content."""
        self.assertIn("pad = (2, 2, 2, 2)", self.content)

    def test_no_box_widget(self) -> None:
        """No Box widget (which centers content)."""
        self.assertNotIn("render.Box", self.content)


# =============================================================================
# Production Mode Tests
# =============================================================================

class TestProductionMode(TidbytTestCase):
    """Tests for production mode (not test mode)."""

    def test_uses_real_day_calculation(self) -> None:
        """Uses real day calculation."""
        self.assertIn("lines_learned = day_within_sonnet + 1", self.content)

    def test_uses_unix_timestamp(self) -> None:
        """Uses unix timestamp for reliable day calculation."""
        self.assertIn("now_unix = now.unix", self.content)

    def test_has_seconds_per_day(self) -> None:
        """Has seconds-per-day constant."""
        self.assertIn("86400", self.content)

    def test_lines_clamped_upper(self) -> None:
        """Lines learned clamped to max."""
        self.assertIn("if lines_learned > len(lines):", self.content)

    def test_lines_clamped_lower(self) -> None:
        """Lines learned clamped to min 1."""
        self.assertIn("if lines_learned < 1:", self.content)


# =============================================================================
# Custom Test Runner (for backwards compatibility)
# =============================================================================

def run_all_tests() -> bool:
    """Run all tests with custom output format.

    Returns:
        True if all tests passed, False otherwise.
    """
    print("Running sonnet.star tests...\n")

    # Collect all test classes
    test_classes = [
        TestRender,
        TestStructure,
        TestSonnetContent,
        TestSchema,
        TestDisplay,
        TestProductionMode,
    ]

    passed = 0
    failed = 0

    for test_class in test_classes:
        # Load and run tests from the class
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromTestCase(test_class)

        for test in suite:
            test_name = test._testMethodName
            try:
                test.setUpClass()
                getattr(test, test_name)()
                passed += 1
                # Create short description from docstring or method name
                doc = getattr(test, test_name).__doc__
                desc = doc.split('.')[0] if doc else test_name
                print(f"✓ {desc}")
            except unittest.SkipTest as e:
                print(f"⊘ {test_name}: Skipped ({e})")
                passed += 1
            except AssertionError as e:
                print(f"✗ {test_name}: {e}")
                failed += 1
            except Exception as e:
                print(f"✗ {test_name}: Unexpected error: {e}")
                failed += 1

    print(f"\n{'=' * 40}")
    print(f"Results: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    # Support both custom runner and unittest
    if len(sys.argv) > 1 and sys.argv[1] == "--unittest":
        unittest.main(argv=[""], exit=True, verbosity=2)
    else:
        success = run_all_tests()
        sys.exit(0 if success else 1)
