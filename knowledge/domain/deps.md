---
generated_by: "OpenAI Codex (GPT-6.1-sol)"
timestamp: "2026-10-18T22:08:00-05:00"
---
# Dependencies

- `@rebble/clay` 1.1.0: pinned in `watchface/package.json` and lockfile for Pebble settings page. Its saved colors are numeric RGB values sent by AppMessage.
- Pebble SDK 4.33.1: local build tool observed during Emery verification; it is not vendored by this repository.
- Open-Meteo forecast API: phone-side weather feed for current temperature, current precipitation probability, and daily sunset. Missing responses do not silently become zero.
- Pillow 12.3.0: pinned for validating and assembling native Emery screenshots into the animated RePebble preview. Installed locally when the release media workflow was created.
