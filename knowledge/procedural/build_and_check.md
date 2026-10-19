---
generated_by: "OpenAI Codex (GPT-6.1-sol)"
timestamp: "2026-10-18T22:08:00-05:00"
---
# Build and check Now / Next

1. Run `npm ci` inside `watchface/` after dependency changes.
2. Run `python3 execution/verify_watchface.py` from the project root. It checks JS settings, weather mapping, C period boundaries, and the Emery PBW.
3. Install `watchface/build/watchface.pbw` with `pebble install --emulator emery`.
4. Reinstall once after an emulator boot, then confirm that Now / Next is the active face before capture. The shared emulator can display a stale face after reported install success.
5. For a complete screenshot after changing settings, reinstall the PBW before `pebble screenshot --emulator emery --no-open --no-correction`. Incremental captures may show only changed glyphs even after a long wait.
6. Run `python3 execution/capture_preview.py` only after the emulator is running and the current PBW is installed. Its date and color images reinstall before capture; its period captures may remain incremental.

The generated `MESSAGE_KEY_*` names are not compile-time constants in this SDK; resolve them inside a function rather than initializing a file-scope array. Emulator time jumps before the last weather update intentionally make weather stale; inject fixtures at current watch time when checking weather display.

## 2026-10-18 — Battery heading

The current battery field displays the period name alone above its percentage. Rain chance keeps a named heading because it also displays a percentage. Run `python3 execution/verify_watchface.py`, install the PBW on Emery, and capture a full face screenshot after reinstalling to check the label.
