# Slow Shakespeare - Publishing Notes

## App Info

**Name:** Slow Shakespeare

**Summary:** Learn sonnets daily

**Description:**
Learn a sonnet through slow, daily repetition in 14 days. Each day reveals one new line. At the top of every hour, review all lines you've learned so far. The rest of the hour shows your newest line.

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

- `slow_shakespeare.star` - Main app (10 sonnets, 6 colors)
- `manifest.yaml` - Publishing metadata
- `test_slow_shakespeare.py` - 22 passing tests
- `push.sh` - Local deploy script

## Before Publishing

1. Run tests: `python3 test_slow_shakespeare.py`
2. Run validation: `pixlet check slow_shakespeare.star`
3. Preview: `pixlet serve --watch slow_shakespeare.star`

## Publishing Checklist

- [x] App docstring with Applet, Author, Summary, Description
- [x] manifest.yaml with all required fields
- [x] Summary under 27 characters
- [x] `pixlet format` applied
- [x] `pixlet lint --fix` applied
- [x] `pixlet check` passes
- [x] All tests pass

## To Publish

1. Fork https://github.com/tidbyt/community (done: https://github.com/matt5000/community)
2. Clone the fork locally
3. Copy `slow_shakespeare.star` and `manifest.yaml` to `apps/slowshakespeare/`
4. Commit and push to fork
5. Open PR to tidbyt/community

## Features

- **Start date picker** - Pick a past date to jump ahead, or match a friend's start date to learn together
- **Auto-advance sonnets** - After completing 14 days, automatically moves to the next sonnet
- **Line number toggle** - Optional line numbers in bottom-right corner
- **Test mode toggle** - Force review mode for testing (disable before publishing)
- **6 Shakespeare-inspired colors** - Salad Days, Yellow Leaves, Milk of Kindness, Midsummer Night, All That Glisters, Damask Rose

## Design Decisions

- **No rotation speed option** - Users who want full review at :00 can manage their own rotation settings
- **Color picker not mentioned in description** - Users discover it when configuring
- **10 sonnets** - Curated selection of most famous; memory is not a constraint (could add all 154)
- **tom-thumb font** - Very small but readable on 64x32 display
- **Left-aligned text** - Book-like feel, no Box wrapper (causes centering)
- **Dot marker** - 3px circle on bottom-right for first line only during review mode (when line numbers off)
- **5 second delay** - Per line during review animation
- **Unix timestamp calculation** - Reliable day counting across timezones

## Testing Notes

- `pixlet render` has a default `--max_duration` of 15 seconds (15000ms)
- With 5 second frames, only 3 frames show by default
- Use `--max_duration 150000` to see full animation locally
- The actual Tidbyt device does NOT have this limit
