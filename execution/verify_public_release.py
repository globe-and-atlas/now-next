"""Verify the public RePebble PBW matches the local production build."""

import argparse
import hashlib
import io
import json
import zipfile
from pathlib import Path
from urllib.parse import urlparse

import requests


ROOT = Path(__file__).resolve().parents[1]
FACE = ROOT / "watchface"


def component_hash(archive: zipfile.ZipFile, name: str) -> str:
    return hashlib.sha256(archive.read(name)).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pbw_url")
    args = parser.parse_args()
    parsed = urlparse(args.pbw_url)
    if parsed.scheme != "https" or parsed.netloc != "appstore-api.repebble.com":
        raise ValueError("Expected an official RePebble PBW URL")
    response = requests.get(args.pbw_url, timeout=30)
    response.raise_for_status()
    package = json.loads((FACE / "package.json").read_text())
    local = FACE / "build/watchface.pbw"
    with zipfile.ZipFile(local) as production, zipfile.ZipFile(io.BytesIO(response.content)) as public:
        local_info = json.loads(production.read("appinfo.json"))
        public_info = json.loads(public.read("appinfo.json"))
        if public_info["uuid"].lower() != package["pebble"]["uuid"].lower():
            raise ValueError("Public PBW UUID mismatch")
        if public_info["versionLabel"] != package["version"]:
            raise ValueError("Public PBW version mismatch")
        if public_info != local_info:
            raise ValueError("Public PBW appinfo differs from production")
        for name in ("emery/pebble-app.bin", "pebble-js-app.js"):
            if component_hash(public, name) != component_hash(production, name):
                raise ValueError(f"Public PBW component differs: {name}")
    print(f"PASS: public PBW {package['version']} matches production binary and JS")


if __name__ == "__main__":
    main()
