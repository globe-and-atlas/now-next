---
generated_by: "OpenAI Codex (GPT-6.1-sol)"
timestamp: "2026-10-18T22:23:52-05:00"
---
# Publish Now / Next

Purpose: release the current Emery watchface with a GIF-first preview showing scheduled fields, date options, and varied color choices.

Inputs: tested `watchface/build/watchface.pbw`, authenticated Pebble developer session, native Emery captures.

Execution: `execution/capture_listing.py` builds media-only fixtures and captures native display frames; `execution/prepare_listing.py` validates and packages up to five Emery media files; `execution/publish_release.py` checks the production PBW and submits the listing; `execution/verify_public_release.py` compares the public PBW with the production build.

Outputs: `listing/` media and text; public RePebble listing URL.

Safety: media-only fixture binaries stay in `.tmp/`; rebuild the production PBW without fixture defines before publishing. Exclude `.env`, tokens, `.tmp/`, and waf locks from Git.

Edge cases: stale shared emulator face, incremental screenshots, invalid weather, animated GIF size, appstore propagation delay.

## Validation Contract
- The production PBW targets Emery.
- The production PBW identifies as a watchface.
- The production PBW uses the Now / Next UUID.
- Screenshot 1 is a GIF.
- The GIF has six frames.
- The GIF is 200×228.
- Four static Emery screenshots are uploaded.
- Each static screenshot is 200×228.
- The GIF includes morning.
- The GIF includes daytime.
- The GIF includes evening.
- The GIF includes night.
- The GIF includes four distinct backgrounds.
- The GIF includes date Off.
- The GIF includes date YYYY-MM-DD.
- The GIF includes date MM/DD/YYYY.
- The GIF includes date DD/MM/YYYY.
- Each media file is below 4.4 MB.
- The public listing serves the production PBW.
- The public listing shows the GIF first.
- The public search card uses the GIF.
- A fresh verifier approves the artifacts.

## Learnings — 2026-10-18

- A shared Emery simulator can display a different face after `pebble install` succeeds. Capture only after the active scene matches the expected native palette.
- A fixture build with deterministic time and weather values makes all period and date choices visible while preserving native rendering. Rebuild without fixture defines before publishing.
- Verify the public PBW by comparing its appinfo, Emery binary, and JavaScript with the local production bundle. Inspect the search card in a browser to confirm GIF animation.
