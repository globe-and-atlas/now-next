---
generated_by: "OpenAI Codex (GPT-6.1-sol)"
timestamp: "2026-10-18T22:41:00-05:00"
---
# RePebble release procedure

1. Ensure no other process is installing a face in the shared Emery emulator. A successful `pebble install` can be displaced before screenshot capture.
2. Run `python3 execution/capture_listing.py`. It builds media-only native fixtures, checks each expected 2-bit Emery background, and rebuilds the production PBW in `finally`.
3. Run `python3 execution/prepare_listing.py` to assemble the six-frame 200×228 GIF as `listing/emery_00_preview.gif` and four static PNGs.
4. Inspect all six native frames for correct date order, legible text, and field choice. The media fixture weather examples are 35% rain, 72F, and 18:31 sunset.
5. Run `python3 execution/verify_watchface.py` and `python3 execution/publish_release.py --dry-run`.
6. After independent verification, run `python3 execution/publish_release.py` using the existing Pebble CLI login. Check the public listing and search card, allowing for cache propagation.

Keep `.tmp/` and credentials out of Git. The original emulator state was saved temporarily in `.tmp/emery-original-session`, then restored after capture; the published PBW is compiled without `NN_MEDIA_FIXTURE`.

## 2026-10-18 release

- `python3 execution/publish_release.py` created public listing `https://apps.repebble.com/68afcbcc6c18416c98b6a1b7` for version 0.1.0.
- The public listing showed five Emery screenshots, with the GIF first; the public search card visibly animated through different palettes.
- `python3 execution/verify_public_release.py <PBW URL from the listing>` confirmed the public PBW appinfo, Emery binary, and JS match the local production build.
- An independent read-only verifier approved the local media and PBW before publication.
