#!/usr/bin/env python3
"""Tests for slow_shakespeare.star Tidbyt application.

This module contains tests to verify the slow_shakespeare.star application
renders correctly and follows expected patterns for the poetry memorization app.
"""

import os
import subprocess
import sys

APP_DIR = os.path.dirname(os.path.abspath(__file__))
STAR_FILE = os.path.join(APP_DIR, "slow_shakespeare.star")


def run_pixlet_render():
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


def read_star_file():
    """Read the star file contents.

    Returns:
        The contents of the star file as a string.
    """
    with open(STAR_FILE, "r", encoding="utf-8") as f:
        return f.read()


def test_renders_successfully():
    """Test that the app renders without errors."""
    success, stderr = run_pixlet_render()
    assert success, f"Render failed: {stderr}"
    print("✓ App renders successfully")


def test_has_required_imports():
    """Test that required imports are present."""
    content = read_star_file()
    assert 'load("render.star", "render")' in content, "Missing render import"
    assert 'load("time.star", "time")' in content, "Missing time import"
    assert 'load("schema.star", "schema")' in content, "Missing schema import"
    print("✓ Required imports present")


def test_has_main_function():
    """Test that main function exists with config parameter."""
    content = read_star_file()
    assert "def main(config):" in content, "Missing main function with config"
    print("✓ Main function exists with config parameter")


def test_has_get_schema_function():
    """Test that get_schema function exists."""
    content = read_star_file()
    assert "def get_schema():" in content, "Missing get_schema function"
    print("✓ get_schema function exists")


def test_has_all_ten_sonnets():
    """Test that all ten sonnets are present."""
    content = read_star_file()
    # Sonnet 1
    assert "From fairest creatures we desire increase," in content
    assert "To eat the world's due, by the grave and thee." in content
    # Sonnet 18
    assert "Shall I compare thee to a summer's day?" in content
    assert "So long lives this, and this gives life to thee." in content
    # Sonnet 29
    assert "When, in disgrace with fortune and men's eyes," in content
    assert "That then I scorn to change my state with kings." in content
    # Sonnet 30
    assert "When to the sessions of sweet silent thought" in content
    assert "All losses are restor'd and sorrows end." in content
    # Sonnet 55
    assert "Not marble, nor the gilded monuments" in content
    assert "You live in this, and dwell in lovers' eyes." in content
    # Sonnet 73
    assert "That time of year thou mayst in me behold" in content
    assert "To love that well which thou must leave ere long." in content
    # Sonnet 104
    assert "To me, fair friend, you never can be old," in content
    assert "Ere you were born was beauty's summer dead." in content
    # Sonnet 116
    assert "Let me not to the marriage of true minds" in content
    assert "I never writ, nor no man ever loved." in content
    # Sonnet 130
    assert "My mistress' eyes are nothing like the sun;" in content
    assert "As any she belied with false compare." in content
    # Sonnet 138
    assert "When my love swears that she is made of truth" in content
    assert "And in our faults by lies we flatter'd be." in content
    print("✓ All ten sonnets present")


def test_sonnets_dictionary_structure():
    """Test that SONNETS dictionary has correct keys."""
    content = read_star_file()
    assert 'SONNETS = {' in content, "Missing SONNETS dictionary"
    assert '"1":' in content, "Missing sonnet 1 key"
    assert '"18":' in content, "Missing sonnet 18 key"
    assert '"29":' in content, "Missing sonnet 29 key"
    assert '"30":' in content, "Missing sonnet 30 key"
    assert '"55":' in content, "Missing sonnet 55 key"
    assert '"73":' in content, "Missing sonnet 73 key"
    assert '"104":' in content, "Missing sonnet 104 key"
    assert '"116":' in content, "Missing sonnet 116 key"
    assert '"130":' in content, "Missing sonnet 130 key"
    assert '"138":' in content, "Missing sonnet 138 key"
    print("✓ SONNETS dictionary has all ten keys")


def test_schema_has_sonnet_dropdown():
    """Test that schema has sonnet dropdown with all options."""
    content = read_star_file()
    assert 'schema.Dropdown(' in content, "Missing Dropdown in schema"
    assert 'id = "sonnet"' in content, "Missing sonnet id in dropdown"
    assert 'value = "1"' in content, "Missing sonnet 1 option"
    assert 'value = "18"' in content, "Missing sonnet 18 option"
    assert 'value = "29"' in content, "Missing sonnet 29 option"
    assert 'value = "30"' in content, "Missing sonnet 30 option"
    assert 'value = "55"' in content, "Missing sonnet 55 option"
    assert 'value = "73"' in content, "Missing sonnet 73 option"
    assert 'value = "104"' in content, "Missing sonnet 104 option"
    assert 'value = "116"' in content, "Missing sonnet 116 option"
    assert 'value = "130"' in content, "Missing sonnet 130 option"
    assert 'value = "138"' in content, "Missing sonnet 138 option"
    print("✓ Schema has sonnet dropdown with all ten options")


def test_schema_has_color_dropdown():
    """Test that schema has color dropdown with Shakespeare-inspired names."""
    content = read_star_file()
    assert 'id = "color"' in content, "Missing color id in schema"
    assert "Salad Days" in content, "Missing Salad Days option"
    assert "Yellow Leaves" in content, "Missing Yellow Leaves option"
    assert "Milk of Kindness" in content, "Missing Milk of Kindness option"
    assert "Midsummer Night" in content, "Missing Midsummer Night option"
    assert "All That Glisters" in content, "Missing All That Glisters option"
    assert "Damask Rose" in content, "Missing Damask Rose option"
    print("✓ Schema has color dropdown with Shakespeare-inspired names")


def test_default_color_is_salad_days():
    """Test that default color is Salad Days green."""
    content = read_star_file()
    assert "#6B8E6B" in content, "Missing Salad Days green color"
    assert 'default = "#6B8E6B"' in content, "Default color should be Salad Days"
    print("✓ Default color is Salad Days (#6B8E6B)")


def test_has_review_mode_at_minute_zero():
    """Test that review mode triggers at minute 0."""
    content = read_star_file()
    assert "current_minute == 0" in content, (
        "Missing minute 0 check for review mode"
    )
    assert "for _ in range(3)" in content, "Missing 3x review loop"
    print("✓ Review mode at :00 with 3x loop")


def test_has_dot_marker_for_first_line():
    """Test that dot marker exists for first line."""
    content = read_star_file()
    assert "if i == 0:" in content, "Missing first line check"
    assert "render.Circle" in content, "Missing Circle for dot marker"
    assert "diameter = 3" in content, "Missing dot diameter"
    print("✓ Dot marker for first line present")


def test_uses_tom_thumb_font():
    """Test that tom-thumb font is used."""
    content = read_star_file()
    assert 'font = "tom-thumb"' in content, "Missing tom-thumb font"
    print("✓ tom-thumb font used")


def test_text_is_left_aligned():
    """Test that text is left aligned."""
    content = read_star_file()
    assert 'align = "left"' in content, "Missing left alignment"
    print("✓ Text left aligned")


def test_has_padding():
    """Test that padding is applied."""
    content = read_star_file()
    assert "pad = (2, 2, 2, 2)" in content, "Missing padding"
    print("✓ Padding applied")


def test_animation_delay_is_5_seconds():
    """Test that animation delay is 5 seconds (5000ms)."""
    content = read_star_file()
    assert "delay = 5000" in content, "Missing 5 second delay"
    print("✓ Animation delay is 5 seconds")


def test_static_display_no_box_wrapper():
    """Test that static display doesn't use Box (which centers content)."""
    content = read_star_file()
    else_idx = content.find("else:")
    if else_idx != -1:
        else_block = content[else_idx:]
        assert "return render.Root" in else_block, "Missing Root in else block"
        assert "render.Box" not in else_block, (
            "Static display should not use Box (causes centering)"
        )
    print("✓ Static display uses Padding (no Box centering)")


def test_not_in_test_mode():
    """Test that app is in production mode (not test mode)."""
    content = read_star_file()
    # Should have real time logic
    assert "current_minute = now.minute" in content, (
        "Missing real minute calculation"
    )
    assert "lines_learned = day_within_sonnet + 1" in content, (
        "Missing real day calculation"
    )
    # Should use unix timestamp for reliable day calculation
    assert "now_unix = now.unix" in content, (
        "Missing unix timestamp calculation"
    )
    assert "86400" in content, (
        "Missing seconds-per-day constant for day calculation"
    )
    print("✓ App is in production mode")


def test_has_start_date_picker():
    """Test that schema has start date picker."""
    content = read_star_file()
    assert "schema.DateTime" in content, "Missing DateTime schema"
    assert 'id = "start_date"' in content, "Missing start_date id"
    print("✓ Start date picker in schema")


def test_lines_clamped():
    """Test that lines_learned is clamped to valid range."""
    content = read_star_file()
    assert "if lines_learned > len(lines):" in content, (
        "Missing upper clamp for lines"
    )
    assert "if lines_learned < 1:" in content, "Missing lower clamp for lines"
    print("✓ Lines learned is clamped to valid range")


def test_animation_frames_no_box():
    """Test that animation frames don't use Box (which centers content)."""
    content = read_star_file()
    else_idx = content.find("else:")
    review_section = content[:else_idx] if else_idx != -1 else content
    append_idx = review_section.find("frames.append")
    if append_idx != -1:
        append_section = review_section[append_idx:append_idx + 200]
        assert "render.Box" not in append_section, (
            "Animation frames should not use Box (causes centering)"
        )
    print("✓ Animation frames use Stack (no Box centering)")


def test_webp_output_exists_after_render():
    """Test that rendering produces a webp file."""
    webp_path = os.path.join(APP_DIR, "slow_shakespeare.webp")
    if os.path.exists(webp_path):
        os.remove(webp_path)
    success, _ = run_pixlet_render()
    assert success, "Render failed"
    assert os.path.exists(webp_path), "slow_shakespeare.webp not created after render"
    print("✓ WebP output created after render")


def test_config_get_with_default():
    """Test that config.get uses default value for sonnet."""
    content = read_star_file()
    assert 'config.get("sonnet", "18")' in content, (
        "Missing config.get with default sonnet 18"
    )
    print("✓ Config uses default sonnet 18")


def run_all_tests():
    """Run all tests and report results.

    Returns:
        True if all tests passed, False otherwise.
    """
    print("Running sonnet.star tests...\n")

    tests = [
        test_renders_successfully,
        test_has_required_imports,
        test_has_main_function,
        test_has_get_schema_function,
        test_has_all_ten_sonnets,
        test_sonnets_dictionary_structure,
        test_schema_has_sonnet_dropdown,
        test_schema_has_color_dropdown,
        test_default_color_is_salad_days,
        test_has_review_mode_at_minute_zero,
        test_has_dot_marker_for_first_line,
        test_uses_tom_thumb_font,
        test_text_is_left_aligned,
        test_has_padding,
        test_animation_delay_is_5_seconds,
        test_static_display_no_box_wrapper,
        test_not_in_test_mode,
        test_has_start_date_picker,
        test_lines_clamped,
        test_animation_frames_no_box,
        test_webp_output_exists_after_render,
        test_config_get_with_default,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__}: {e}")
            failed += 1
        except Exception as e:  # pylint: disable=broad-except
            print(f"✗ {test.__name__}: Unexpected error: {e}")
            failed += 1

    print(f"\n{'=' * 40}")
    print(f"Results: {passed} passed, {failed} failed")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
