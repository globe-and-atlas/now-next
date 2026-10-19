# Decisions

## Initial Decision

- Template profile: `workflow-python`
- Deploy target: `local-only`
- Runtime: `pebble`

## 2026-10-18 — Period-based context

- Decision: four ascending local-hour boundaries select one field at a time; the final period wraps midnight.
- Alternatives considered: dense fixed data dashboard; rules based on calendar and activity state.
- Reason: the concept stays glanceable on 200×228 and makes the schedule explicit in settings.

## 2026-10-18 — Weather source

- Decision: use phone location and Open-Meteo for rain chance, temperature, and sunset, with a one-hour freshness limit.
- Alternatives considered: Garmin data fields; weather-free first build.
- Reason: the selected example fields need weather, while Garmin-only metrics cannot transfer to Pebble.
