"""Capture original 200x228 Emery frames with deterministic media-only weather/time fixtures."""

import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
FACE = ROOT / "watchface"
TMP = ROOT / ".tmp"
CAPTURES = TMP / "listing-captures"
RUNLOG = TMP / "runlog.md"
PACKAGE = json.loads((FACE / "package.json").read_text())
KEYS = json.loads((FACE / "build/js/message_keys.json").read_text())
UUID = PACKAGE["pebble"]["uuid"]

SCENES = (
    {"name": "night", "hour": 22, "minute": 16, "date": 1,
     "fields": (0, 1, 2, 3), "colors": (0x005555, 0xFFFFFF, 0xAAFFAA)},
    {"name": "morning", "hour": 8, "minute": 24, "date": 2,
     "fields": (0, 1, 2, 3), "colors": (0xFFFFAA, 0x000055, 0xAA5500)},
    {"name": "daytime", "hour": 13, "minute": 47, "date": 3,
     "fields": (0, 1, 2, 3), "colors": (0x0055AA, 0xFFFFAA, 0xAAFFFF)},
    {"name": "evening", "hour": 18, "minute": 12, "date": 0,
     "fields": (0, 1, 2, 3), "colors": (0x005500, 0xFFFFFF, 0xAAFF55)},
    {"name": "night_rain", "hour": 22, "minute": 16, "date": 1,
     "fields": (0, 1, 2, 0), "colors": (0x5500AA, 0xFFFFFF, 0xAAFFFF)},
    {"name": "morning_battery", "hour": 8, "minute": 24, "date": 0,
     "fields": (3, 1, 2, 3), "colors": (0x555500, 0xFFFFFF, 0xFFAA00)},
)


def log(message: str) -> None:
    if not RUNLOG.exists():
        RUNLOG.write_text(
            '---\ngenerated_by: "OpenAI Codex (GPT-6.1-sol)"\n'
            f'timestamp: "{datetime.now().astimezone().isoformat()}"\n---\n'
            '# Now / Next release capture\n\n'
        )
    with RUNLOG.open("a") as stream:
        stream.write(f"- {datetime.now().astimezone().isoformat(timespec='seconds')}: {message}\n")


def run(*args: str, env: dict[str, str] | None = None) -> None:
    result = subprocess.run(args, cwd=FACE, env=env, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.returncode:
        log(f"FAILED {' '.join(args)}: {result.stdout[-1000:]}")
        raise RuntimeError(f"{' '.join(args)} failed:\n{result.stdout[-2000:]}")


def production_env() -> dict[str, str]:
    return {key: value for key, value in os.environ.items() if not key.startswith("NN_MEDIA_")}


def build(env: dict[str, str]) -> None:
    run("pebble", "clean", env=env)
    run("pebble", "build", env=env)
    if not (FACE / "build/watchface.pbw").is_file():
        raise RuntimeError("Pebble build produced no PBW")


def send_settings(scene: dict) -> None:
    background, digits, accent = scene["colors"]
    settings = {
        "SETTING_BG": background, "SETTING_DIGITS": digits,
        "SETTING_ACCENT": accent, "SETTING_DATE": scene["date"],
    }
    for index, field in enumerate(scene["fields"]):
        settings[f"SETTING_FIELD_{index}"] = field
    for index, start in enumerate((6, 11, 17, 21)):
        settings[f"SETTING_START_{index}"] = start
    args = ["pebble", "send-app-message", "--emulator", "emery",
            "--app-uuid", UUID, "--int"]
    args.extend(f"{KEYS[key]}={value}" for key, value in settings.items())
    run(*args)


def capture(scene: dict) -> None:
    name = scene["name"]
    output = CAPTURES / f"{name}.png"
    run("pebble", "install", "--emulator", "emery", "build/watchface.pbw")
    time.sleep(3)
    send_settings(scene)
    background = scene["colors"][0]
    expected = tuple(((background >> shift) & 0xFF) // 64 * 85
                     for shift in (16, 8, 0))
    for attempt in range(15):
        time.sleep(1)
        run("pebble", "screenshot", "--emulator", "emery", "--no-open",
            "--no-correction", str(output))
        with Image.open(output) as image:
            if image.size != (200, 228):
                raise ValueError(f"Wrong Emery dimensions: {output}")
            if image.convert("RGB").getpixel((0, 0)) == expected:
                log(f"Matched {name} background after {attempt + 1} checks")
                break
    else:
        raise RuntimeError(f"{name} never rendered expected background {expected}")
    log(f"Captured {name} at 200x228")
    print(output)


def main() -> None:
    CAPTURES.mkdir(parents=True, exist_ok=True)
    clean_env = production_env()
    log("Started media fixture capture; production PBW will be rebuilt afterward")
    build(clean_env)
    run("pebble", "install", "--emulator", "emery", "build/watchface.pbw")
    try:
        for scene in SCENES:
            fixture_env = dict(clean_env)
            fixture_env.update(NN_MEDIA_FIXTURE="1", NN_MEDIA_HOUR=str(scene["hour"]),
                               NN_MEDIA_MINUTE=str(scene["minute"]))
            build(fixture_env)
            (TMP / "media_fixture.pbw").write_bytes((FACE / "build/watchface.pbw").read_bytes())
            capture(scene)
    finally:
        build(clean_env)
        log("Rebuilt production PBW without media fixture defines")
    print(f"Captured {len(SCENES)} native Emery frames; production PBW restored")


if __name__ == "__main__":
    main()
