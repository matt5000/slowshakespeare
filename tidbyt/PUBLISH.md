# Slow Shakespeare - Publishing Notes

## App Info

**Name:** Slow Shakespeare

**Summary:** Learn sonnets daily

**Description:**
Learn a Shakespeare sonnet one line at a time over 14 days. Each day reveals one new line — today's focus line is always on display.

Choose from ten sonnets:
- Sonnet 1 – "From fairest creatures we desire increase"
- Sonnet 18 – "Shall I compare thee to a summer's day?"
- Sonnet 29 – "When, in disgrace with fortune..."
- Sonnet 30 – "When to the sessions of sweet silent thought"
- Sonnet 55 – "Not marble, nor the gilded monuments"
- Sonnet 73 – "That time of year thou mayst in me behold"
- Sonnet 104 – "To me, fair friend, you never can be old"
- Sonnet 116 – "Let me not to the marriage of true minds"
- Sonnet 130 – "My mistress' eyes are nothing like the sun"
- Sonnet 138 – "When my love swears that she is made of truth"

## Files

- `slow_shakespeare.star` - Main app (10 sonnets, 5 colors)
- `manifest.yaml` - Publishing metadata
- `test_slow_shakespeare.py` - 26 passing tests
- `push.sh` - Local deploy script

## Before Publishing

1. Run tests: `python3 test_slow_shakespeare.py`
2. Run validation: `pixlet check slow_shakespeare.star`
3. Preview: `pixlet serve slow_shakespeare.star`

## Publishing Checklist

- [x] App docstring with Applet, Author, Summary, Description
- [x] manifest.yaml with all required fields
- [x] Summary under 27 characters
- [x] `pixlet format` — no changes needed
- [x] `pixlet lint` — no warnings
- [x] `pixlet check` passes all 8 validations
- [x] All 26 tests pass
- [x] App renders with no config (all defaults work)
- [x] Render time under 1 second
- [x] Pixlet version matches community repo (v0.34.0)

## Submission Steps

1. Sync fork to latest `main`: https://github.com/matt5000/community
2. Copy `slow_shakespeare.star` and `manifest.yaml` to `apps/slowshakespeare/`
3. Run `pixlet check apps/slowshakespeare/slow_shakespeare.star` from community repo
4. Commit and push to fork
5. Open PR to `tidbyt/community`
6. Sign the CLA when the bot comments on the PR
7. Wait for review by Tidbyt maintainers

## Features

- **Start date picker** - Pick a past date to jump ahead, or match a friend's start date to learn together
- **Auto-advance sonnets** - After completing 14 days, automatically moves to the next sonnet
- **Line number toggle** - Optional line numbers in bottom-right corner
- **5 Shakespeare-inspired colors** - Salad Days, Milk of Kindness, Midsummer Night, All That Glisters, Damask Rose

## Design Decisions

- **Static display only** - Always shows today's newest line; no animation (Tidbyt's ~15s rotation window makes multi-line review impractical)
- **Color picker not mentioned in description** - Users discover it when configuring
- **10 sonnets** - Curated selection of most famous; memory is not a constraint (could add all 154)
- **tom-thumb font** - Very small but readable on 64x32 display
- **Left-aligned text** - Book-like feel, no Box wrapper (causes centering)
- **Unix timestamp calculation** - Reliable day counting across timezones
