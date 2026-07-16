"""Download complementary Full HD Unsplash fills for missing model slots."""
from __future__ import annotations

import io
import urllib.request
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
IMG = ROOT / "assets" / "img"
UA = "IntentandoColeccionarAssetBot/1.0"

FILLS = {
    # orange sports coupe (Supra-style atmosphere)
    "supra-naranja": "https://images.unsplash.com/photo-1542362567-b07e54358753?auto=format&fit=crop&w=2400&q=90",
    # sporty orange / street car vibe
    "civic-naranja": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=2400&q=90",
    # red muscle car
    "charger-rojo": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=2400&q=90",
    # dark city skyline for cinematic diorama mood
    "batman-ciudad": "https://images.unsplash.com/photo-1514565131-fce0801e5785?auto=format&fit=crop&w=2400&q=90",
}


def fetch(url: str) -> Image.Image:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = resp.read()
    im = Image.open(io.BytesIO(data))
    return ImageOps.exif_transpose(im).convert("RGB")


def polish(im: Image.Image) -> Image.Image:
    w, h = im.size
    long_side = max(w, h)
    if long_side < 1920:
        s = 1920 / long_side
        im = im.resize((int(w * s), int(h * s)), Image.Resampling.LANCZOS)
    im = ImageEnhance.Contrast(im).enhance(1.06)
    im = ImageEnhance.Color(im).enhance(1.1)
    im = ImageEnhance.Sharpness(im).enhance(1.25)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=110, threshold=2))
    return im


def main() -> None:
    IMG.mkdir(parents=True, exist_ok=True)
    for name, url in FILLS.items():
        print(f"fetch {name}", flush=True)
        im = polish(fetch(url))
        im.save(IMG / f"{name}.webp", "WEBP", quality=88, method=6)
        im.save(IMG / f"{name}.jpg", "JPEG", quality=92, optimize=True, progressive=True)
        (IMG / f"{name}.ATTRIBUTION.txt").write_text(
            f"Source: Unsplash\nURL: {url}\nNote: complementary visual atmosphere for UI slots.\n",
            encoding="utf-8",
        )
        print(f"  saved {im.size}", flush=True)
    print("ok")


if __name__ == "__main__":
    main()
