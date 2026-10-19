---
generated_by: "OpenAI Codex (GPT-6.1-sol)"
timestamp: "2026-10-18T21:55:45-05:00"
---
# Build Now / Next

Purpose: show large time with one context field selected by four configurable daily periods.

Input: local clock, saved period settings, watch battery, and phone weather.

Execution: `execution/verify_watchface.py` checks settings, host logic, and the Emery PBW.

Visual check: `execution/capture_preview.py` captures period states and full face date/color states from an already running Emery emulator. Period captures may be incremental; full face date/color captures reinstall the PBW first.

Output: `watchface/build/watchface.pbw`; review captures in `.tmp/`.

Edge cases: missing weather, stale weather, midnight rollover, invalid schedule, and date Off.

## Validation Contract
- The native Emery bundle builds.
- The display remains legible at 200×228 pixels.
- The active period changes at all configured boundaries.
- Four period field choices are configurable.
- Four period start hours are configurable.
- Background, digit, and accent colors are configurable.
- Date Off hides the date.
- YYYY-MM-DD is selectable.
- MM/DD/YYYY is selectable.
- DD/MM/YYYY is selectable.
- Saved settings survive watch restart.
- Weather absence is visible rather than silently substituted.
- `python3 execution/verify_watchface.py` passes.
- A fresh verifier approves the output.
