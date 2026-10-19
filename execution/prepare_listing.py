"""Assemble and verify a GIF-first Emery listing from six native captures."""

from pathlib import Path

from PIL import Image, ImageChops


ROOT = Path(__file__).resolve().parents[1]
CAPTURES = ROOT / ".tmp/listing-captures"
LISTING = ROOT / "listing"
NAMES = ("night", "morning", "daytime", "evening", "night_rain", "morning_battery")
STATIC = NAMES[:4]
LIMIT = 4_400_000


def occupied(image: Image.Image, box: tuple[int, int, int, int]) -> bool:
    background = Image.new("RGB", image.size, image.getpixel((0, 0)))
    return ImageChops.difference(image, background).crop(box).getbbox() is not None


def main() -> None:
    LISTING.mkdir(exist_ok=True)
    frames: list[Image.Image] = []
    for name in NAMES:
        source = CAPTURES / f"{name}.png"
        with Image.open(source) as image:
            if image.size != (200, 228):
                raise ValueError(f"Not a native Emery capture: {source}")
            frame = image.convert("RGB")
        if not occupied(frame, (40, 4, 195, 34)):
            raise ValueError(f"Missing title region in {source}; likely incremental screenshot")
        if not occupied(frame, (10, 42, 190, 110)):
            raise ValueError(f"Missing clock region in {source}")
        if not occupied(frame, (10, 145, 190, 205)):
            raise ValueError(f"Missing context region in {source}")
        frames.append(frame)
    if len({frame.tobytes() for frame in frames}) != len(NAMES):
        raise ValueError("Animated frames are not distinct")
    backgrounds = [frame.getpixel((0, 0)) for frame in frames]
    if len(set(backgrounds)) < 4:
        raise ValueError("Animated preview needs four distinct backgrounds")
    output = LISTING / "emery_00_preview.gif"
    frames[0].save(output, save_all=True, append_images=frames[1:],
                   duration=1300, loop=0, optimize=False, disposal=2)
    with Image.open(output) as gif:
        if gif.size != (200, 228) or gif.n_frames != 6:
            raise ValueError("Animated preview has wrong size or frame count")
    media = [output]
    for number, name in enumerate(STATIC, 1):
        static = LISTING / f"emery_{number:02d}_{name}.png"
        static.write_bytes((CAPTURES / f"{name}.png").read_bytes())
        media.append(static)
    for path in media:
        if path.stat().st_size > LIMIT:
            raise ValueError(f"Oversize listing media: {path}")
    print(f"Prepared {len(media)} Emery listing images; GIF first with 6 frames")


if __name__ == "__main__":
    main()
