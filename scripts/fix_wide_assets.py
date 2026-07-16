"""Rebuild wide gallery assets from native landscape workshop photos."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
TRABAJOS = ROOT / "assets" / "trabajos"
IMG = ROOT / "assets" / "img"


def load(name: str) -> Image.Image:
    for ext in (".webp", ".jpg", ".png"):
        p = TRABAJOS / f"{name}{ext}"
        if p.exists():
            im = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
            return im
    raise FileNotFoundError(name)


def polish(im: Image.Image, long: int = 1920) -> Image.Image:
    w, h = im.size
    s = long / max(w, h)
    if s > 1.01:
        # Prefer subtle upscale only; avoid extreme stretch
        s = min(s, 1.75)
        im = im.resize((int(w * s), int(h * s)), Image.Resampling.LANCZOS)
    elif max(w, h) > 2400:
        s = 2400 / max(w, h)
        im = im.resize((int(w * s), int(h * s)), Image.Resampling.LANCZOS)
    im = ImageEnhance.Contrast(im).enhance(1.06)
    im = ImageEnhance.Color(im).enhance(1.08)
    im = ImageEnhance.Sharpness(im).enhance(1.15)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.0, percent=90, threshold=3))
    return im


def crop1610(im: Image.Image) -> Image.Image:
    w, h = im.size
    target = 16 / 10
    if w / h > target:
        nw = int(h * target)
        x = (w - nw) // 2
        return im.crop((x, 0, x + nw, h))
    nh = int(w / target)
    y = (h - nh) // 2
    return im.crop((0, y, w, y + nh))


def save(name: str, im: Image.Image) -> None:
    im.save(IMG / f"{name}.webp", "WEBP", quality=90, method=6)
    im.save(IMG / f"{name}.jpg", "JPEG", quality=93, optimize=True, progressive=True)
    print(name, im.size)


def main() -> None:
    # Wide / cinematic slots from native landscape scenes
    save("ff-escena-grupo", polish(crop1610(load("escena-06"))))
    save("coleccion-ff", polish(crop1610(load("escena-08"))))
    save("hero-coleccion-cinematica", polish(crop1610(load("escena-09"))))
    save("vin-diesel", polish(load("escena-10")))
    # Keep portrait showcase high quality without forced landscape crop
    save("suki-neon", polish(load("escena-01")))
    save("batman-figura", polish(load("escena-04")))
    save("batman-box", polish(load("escena-03")))
    print("fixed")


if __name__ == "__main__":
    main()
