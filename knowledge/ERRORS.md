# Errors

Record deterministic errors, root causes, and fixes here.

- 2026-10-18 21:55: A file search included `watchface/` before it existed. Cause: scaffold has no Pebble directory. Fix: search only existing paths until implementation creates it. Graduated to the project build directive.
- 2026-10-18 21:55: The first contract patch failed because it contained an empty update hunk. Cause: malformed patch. Fix: split the edit into valid file-specific hunks. Graduated to the project build directive.
- 2026-10-18 21:56: A second contract patch failed because it deleted and added the same path in one patch. Cause: unsupported combined operation. Fix: replace file content with a `pathlib` write, then use ordinary update hunks for other files. Graduated to the project build directive.
- 2026-10-18 21:59: Emery build rejected file-scope arrays initialized with generated `MESSAGE_KEY_*` names. Cause: the SDK exposes those names as nonconstant values. Fix: resolve the keys in a function at runtime. Graduated to `knowledge/procedural/build_and_check.md`.
- 2026-10-18 22:02: Emery screenshot showed stale Little Errand nonresponse after Now / Next install success. Cause: shared emulator retained a prior face state. Fix: perform a clean emulator restart and select the installed Now / Next face before accepting a capture. Graduated to `knowledge/procedural/build_and_check.md`.
- 2026-10-18 22:05: Rapid fixture captures contained incomplete e-paper draws; the weather fixture still showed UNAVAILABLE. Cause: capture delay was too short, while weather AppMessage delivery needs independent confirmation. Fix: lengthen settle time and inspect emulator logs/message delivery before using captures as evidence. Graduated to `knowledge/procedural/build_and_check.md`.
- 2026-10-18 22:08: Longer waits did not make incremental emulator screenshots complete; screenshots sometimes contained only changed glyphs. Cause: the emulator screenshot path captured an incremental display update. Fix: reinstall the current PBW to force a full face draw before taking a release-quality screenshot. Graduated to `knowledge/procedural/build_and_check.md`.
- 2026-10-18 22:09: Documentation patch failed due an empty DECISIONS.md update hunk. Cause: malformed patch. Fix: omit that file until a valid decision entry is ready. Graduated to the project documentation procedure.
- 2026-10-18 22:09: Error-log patch failed because it referred to a line from the failed documentation patch. Cause: no partial application occurred. Fix: inspect the file and append against the actual final line. Graduated to the project documentation procedure.
- 2026-10-18 22:11: A health-check command targeted `project-template/scripts/health_check.py`, which does not exist. Cause: scaffold copied the script into the project. Fix: run `python3 scripts/health_check.py` from `now-next`. Graduated to `knowledge/procedural/build_and_check.md`.
- 2026-10-18 22:12: Hook inspection targeted `.git/hooks/post-commit`, which does not exist. Cause: commit checkpointing uses a configured hooks path or another hook. Fix: inspect `core.hooksPath` before choosing how to finalize the session log. Graduated to the project session procedure.
- 2026-10-18 22:20: Initial publication file search included `listing/` and `prod/` before those directories existed. Cause: Now / Next has not been published yet. Fix: search existing paths and create `listing/` through the publication workflow. Graduated to `directives/publish_watchface.md`.
## 2026-10-18 — Listing capture grabbed stale emulator frames

- Error: the first three native screenshots showed Seven Days or partial pixels; only later screenshots showed Now / Next.
- Cause: `pebble install` returned before the emulator finished switching and drawing the new face; the two-second capture delay was insufficient.
- Fix: install each fixture, send scene settings after launch, retry screenshots until the expected quantized background appears, and validate title, clock, and context regions when assembling the GIF.
- Graduated-to: `execution/capture_listing.py` after the capture retry is verified.

## 2026-10-18 — Screenshot output path used the wrong working directory

- Error: a direct `pebble screenshot` probe failed because `.tmp/listing-captures/current.png` was resolved under `watchface/`.
- Cause: the CLI ran from `watchface/`, while the temporary directory is at the project root.
- Fix: pass an absolute `Path` to screenshot commands, as the capture script does.
- Graduated-to: `knowledge/procedural/publish_watchface.md` after release.

## 2026-10-18 — Emery did not switch to the installed face

- Error: retrying fifteen screenshots still showed Pocket Familiar's “not responding” screen instead of Now / Next.
- Cause: another active process was running from `/Users/danielbally/Git/pocket-familiar/watchface` against the same Emery emulator; its installs displaced Now / Next during capture.
- Fix: stopped the shared emulator after the other live log session ended, captured in a fresh Emery state, then restored the prior simulator state from `.tmp/emery-original-session`.
- Graduated-to: `execution/capture_listing.py` after a clean capture succeeds.

## 2026-10-18 — Bundle inspection raced a clean build

- Error: `watchface/build/watchface.pbw` was absent while inspecting app metadata.
- Cause: the screenshot process was rebuilding the bundle and had temporarily removed `build/`.
- Fix: wait for capture completion before inspecting or publishing the production PBW.
- Graduated-to: `execution/publish_release.py` release validation.

## 2026-10-18 — Capture error handling hid the CLI failure

- Error: the capture script raised `AttributeError: CompletedProcess has no attribute output` after `pebble send-app-message` failed.
- Cause: `subprocess.run` returned combined text in `stdout`, but the handler read `result.output`.
- Fix: read `result.stdout` so the real Pebble CLI error can be diagnosed.
- Graduated-to: `execution/capture_listing.py`.


## 2026-10-18 — Knowledge patch context mismatch

- Error: a documentation patch failed because the expected prior text did not match the file.
- Cause: the target line had moved or changed during earlier edits.
- Fix: inspect the file before applying a narrower patch.
- Graduated-to: local edit procedure.

## 2026-10-18 — Public listing unavailable to text web opener

- Error: the web text opener returned “not accessible” for the new RePebble app URL.
- Cause: likely a client-rendered route or early propagation; the response does not establish public availability.
- Fix: inspect the listing in a browser and verify public media URLs there.
- Graduated-to: `knowledge/procedural/publish_watchface.md`.
