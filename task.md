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

## 2026-10-18 — Battery heading simplification

- [x] A battery field shows only its period name above the percentage.
- [x] A rain percentage retains its rain-chance label.
- [x] `python3 execution/verify_watchface.py` passes after the edit.
- [x] The Emery preview shows the simplified night heading.

## 2026-10-18 — RePebble publication

### Contract
- Target directive: `directives/publish_watchface.md`.
- Intended execution scripts: `execution/capture_listing.py`, `execution/prepare_listing.py`, `execution/publish_release.py`, `execution/verify_public_release.py`.
- Expected local artifacts: `listing/` media and text, production `watchface/build/watchface.pbw`.
- Expected external artifact: public RePebble watchface listing.
- Safety: keep `.env`, tokens, waf locks, and `.tmp/` out of Git.

### Validation Contract
- [x] The production PBW targets Emery.
- [x] The production PBW has the Now / Next UUID.
- [x] The first uploaded Emery screenshot is an animated GIF.
- [x] The GIF has six distinct native 200×228 frames.
- [x] The GIF shows morning.
- [x] The GIF shows daytime.
- [x] The GIF shows evening.
- [x] The GIF shows night.
- [x] The GIF shows four distinct background colors.
- [x] The GIF shows the Off date choice.
- [x] The GIF shows YYYY-MM-DD.
- [x] The GIF shows MM/DD/YYYY.
- [x] The GIF shows DD/MM/YYYY.
- [x] No uploaded screenshot exceeds 4.4 MB.
- [x] The uploaded screenshots use a production-equivalent watchface rendering path.
- [x] The published description matches the implemented controls.
- [x] The public listing serves the current PBW.
- [x] The public listing displays the GIF first.
- [x] The public search card uses the GIF preview.
- [x] A fresh verifier reviews the release artifacts.

### Progress
- [x] Capture native Emery variants.
- [x] Assemble and validate listing media.
- [x] Publish the watchface.
- [x] Verify the public listing.

### Release evidence

- Public listing: https://apps.repebble.com/68afcbcc6c18416c98b6a1b7
- Public search: https://apps.repebble.com/search?query=Now%20%2F%20Next&type=faces&page=1
- Public PBW: downloaded and matched production `emery/pebble-app.bin` and `pebble-js-app.js` by SHA-256 with `execution/verify_public_release.py`.
- RePebble listed five Emery screenshots; the first asset is a GIF. The search card visibly advanced from evening green to daytime blue during browser review.
- Physical Pebble Time 2 installation remains untested.
