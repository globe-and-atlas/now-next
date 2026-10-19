# Project Context

## Identity

- Name: `now-next`
- Profile: `workflow-python`
- Deploy: `local-only`
- Runtime: `pebble`

## Purpose

A glanceable Pebble Time 2 clock that shows one context value selected by the current daily period.

## Constraints

- Native Emery resolution is 200×228, with a 64-color e-paper display.
- Weather requires phone location and network access; unavailable data stays visibly unavailable.
- Date controls follow the workspace Off / ISO / MDY / DMY convention.

## Out of Scope

- This first build does not use Garmin proprietary health metrics.
- Physical watch behavior and RePebble release are separate from the Emery emulator build.
