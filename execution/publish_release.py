"""Validate and publish the GIF-first Now / Next RePebble listing."""

import argparse
import json
import os
import subprocess
import zipfile
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
FACE = ROOT / "watchface"
LISTING = ROOT / "listing"
MEDIA = [
    LISTING / "emery_00_preview.gif",
    LISTING / "emery_01_night.png",
    LISTING / "emery_02_morning.png",
    LISTING / "emery_03_daytime.png",
    LISTING / "emery_04_evening.png",
]
LIMIT = 4_400_000


def validate() -> dict:
    package = json.loads((FACE / "package.json").read_text())
    pebble = package["pebble"]
    if pebble["displayName"] != "Now / Next" or pebble["targetPlatforms"] != ["emery"]:
        raise ValueError("Unexpected watchface package")
    if pebble["watchapp"]["watchface"] is not True:
        raise ValueError("Package is not a watchface")
    bundle = FACE / "build/watchface.pbw"
    if not bundle.is_file() or bundle.stat().st_size >= LIMIT:
        raise ValueError("Production PBW missing or oversized")
    with zipfile.ZipFile(bundle) as archive:
        info = json.loads(archive.read("appinfo.json"))
    if info["uuid"].lower() != pebble["uuid"].lower():
        raise ValueError("PBW UUID differs from package")
    for path in MEDIA:
        if not path.is_file() or path.stat().st_size >= LIMIT:
            raise ValueError(f"Listing image missing or oversized: {path}")
        with Image.open(path) as image:
            if image.size != (200, 228):
                raise ValueError(f"Listing image is not 200x228: {path}")
            if path.suffix == ".gif" and image.n_frames != 6:
                raise ValueError("Preview must have six animated frames")
    if MEDIA[0].suffix != ".gif":
        raise ValueError("First media item must be GIF")
    description = (LISTING / "description.txt").read_text().strip()
    notes = (LISTING / "release-notes.txt").read_text().strip()
    if not description or not notes:
        raise ValueError("Listing text is empty")
    return package


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    package = validate()
    if args.dry_run:
        print("PASS: Emery PBW, six-frame GIF first, four static images, listing text")
        return
    command = [
        "pebble", "publish", "--non-interactive", "--is-published",
        "--no-gif-all-platforms", "--name", "Now / Next",
        "--version", package["version"],
        "--description", (LISTING / "description.txt").read_text().strip(),
        "--release-notes", (LISTING / "release-notes.txt").read_text().strip(),
        "--screenshots", *(str(path) for path in MEDIA),
    ]
    env = {key: value for key, value in os.environ.items() if not key.startswith("NN_MEDIA_")}
    subprocess.run(command, cwd=FACE, env=env, check=True)


if __name__ == "__main__":
    main()
