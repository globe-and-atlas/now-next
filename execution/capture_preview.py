"""Capture deterministic native Emery previews from a running Now / Next emulator."""

import json
import subprocess
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KEYS = json.loads((ROOT / "watchface/build/js/message_keys.json").read_text())
OUT = ROOT / ".tmp"


def run(*args: str) -> None:
    subprocess.run(("pebble", *args, "--emulator", "emery"), cwd=ROOT / "watchface", check=True)


def message(values: dict[str, int]) -> None:
    assignments = [f"{KEYS[key]}={value}" for key, value in values.items()]
    run("send-app-message", "--int", *assignments)


def redraw_full_face() -> None:
    run("install", "build/watchface.pbw")


def capture(name: str) -> None:
    time.sleep(5)
    run("screenshot", "--no-open", "--no-correction", str(OUT / f"{name}.png"))


def main() -> None:
    OUT.mkdir(exist_ok=True)
    message({"SETTING_FIELD_3": 3})
    for hour, minute, name in [(8, 24, "morning"), (13, 47, "daytime"),
                               (18, 12, "evening"), (22, 9, "night")]:
        run("emu-set-time", f"{hour:02}:{minute:02}:00")
        capture(name)
    run("emu-set-time", "13:47:00")
    for date, name in [(0, "date-off"), (1, "date-iso"),
                       (2, "date-mdy"), (3, "date-dmy")]:
        message({"SETTING_DATE": date})
        redraw_full_face()
        capture(name)
    message({"SETTING_DATE": 1, "SETTING_BG": 0x183C56,
             "SETTING_DIGITS": 0xFFE39A, "SETTING_ACCENT": 0xFF9276})
    redraw_full_face()
    capture("color-option")
    message({"SETTING_BG": 0x102834, "SETTING_DIGITS": 0xF6F1DE,
             "SETTING_ACCENT": 0x6FD6C0})
    print(f"Captured 9 previews in {OUT}")


if __name__ == "__main__":
    main()
