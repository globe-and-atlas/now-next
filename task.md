---
generated_by: "OpenAI Codex (GPT-6.1-sol)"
timestamp: "2026-10-18T21:55:45-05:00"
---
# Now / Next — Pebble Time 2

## Contract
- Target directive: `directives/build_watchface.md`.
- Intended execution script: `execution/verify_watchface.py`.
- Expected artifact: `watchface/build/watchface.pbw`.
- Safety: exclude `.env`, tokens, and `.tmp/` from Git.
- Safety: keep emulator captures in `.tmp/`.

## Validation Contract
- [x] The face builds for the Pebble Time 2 `emery` target.
- [x] The time is legible at 200×228 pixels.
- [x] The information field changes at each configured period boundary.
- [x] Settings allow a field choice for morning.
- [x] Settings allow a field choice for daytime.
- [x] Settings allow a field choice for evening.
- [x] Settings allow a field choice for night.
- [x] Settings allow each period start hour to be configured.
- [x] Weather fields show a clear unavailable state when phone data is absent.
- [x] Background color is configurable.
- [x] Digit color is configurable.
- [x] Accent color is configurable.
- [x] Date Off hides the date.
- [x] Date YYYY-MM-DD renders in that order.
- [x] Date MM/DD/YYYY renders in that order.
- [x] Date DD/MM/YYYY renders in that order.
- [x] Settings persist after watch restart.
- [x] `python3 execution/verify_watchface.py` passes.
- [x] A fresh verifier reviews the final build against this contract.

## Progress
- [x] Scaffold the project from the workspace template.
- [x] Implement the watchface and settings.
- [x] Verify the build and native display.
- [x] Record the build procedure in project knowledge.

## Verification evidence
- `npm ci` completed with no audit findings.
- `python3 execution/verify_watchface.py` passed after the final source change.
- Native Emery captures confirmed default color, a custom color choice, all date orders, and weather fixture delivery.
- Fresh verifier approved the source, PBW, and 200×228 preview.
