"""
Enhance workshop photos to Full HD WebP + map named site assets.
"""
from __future__ import annotations

import io
import urllib.request
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
TRABAJOS = ROOT / "assets" / "trabajos"
IMG = ROOT / "assets" / "img"
OUT_HD = TRABAJOS / "hd"
TARGET_LONG = 1920
WEBP_Q = 88

UA = "IntentandoColeccionarAssetBot/1.0 (local build; +https://intentandocoleccionar.local)"


def open_rgb(path: Path) -> Image.Image:
    im = Image.open(path)
    im = ImageOps.exif_transpose(im)
    if im.mode in ("RGBA", "LA"):
        bg = Image.new("RGB", im.size, (10, 9, 8))
        bg.paste(im, mask=im.split()[-1])
        return bg
    return im.convert("RGB")


def upscale_to_hd(im: Image.Image, target_long: int = TARGET_LONG) -> Image.Image:
    w, h = im.size
    long_side = max(w, h)
    if long_side >= target_long:
        # still light polish, keep native if already HD+
        scale = 1.0
    else:
        scale = target_long / long_side
    # Cap absurd enlargements of tiny sources
    scale = min(scale, 3.5)
    if scale > 1.01:
        nw, nh = int(w * scale), int(h * scale)
        im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    return im


def grade(im: Image.Image) -> Image.Image:
    im = ImageEnhance.Contrast(im).enhance(1.08)
    im = ImageEnhance.Color(im).enhance(1.12)
    im = ImageEnhance.Brightness(im).enhance(1.03)
    im = ImageEnhance.Sharpness(im).enhance(1.35)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.4, percent=120, threshold=2))
    return im


def save_webp(im: Image.Image, dest: Path, quality: int = WEBP_Q) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "WEBP", quality=quality, method=6)


def save_jpg(im: Image.Image, dest: Path, quality: int = 92) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "JPEG", quality=quality, optimize=True, progressive=True)


def center_crop(im: Image.Image, ratio_w: float, ratio_h: float) -> Image.Image:
    w, h = im.size
    target = ratio_w / ratio_h
    current = w / h
    if current > target:
        nw = int(h * target)
        left = (w - nw) // 2
        return im.crop((left, 0, left + nw, h))
    nh = int(w / target)
    top = (h - nh) // 2
    return im.crop((0, top, w, top + nh))


def download(url: str) -> Image.Image:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
    im = Image.open(io.BytesIO(data))
    im = ImageOps.exif_transpose(im).convert("RGB")
    return im


def enhance_file(src: Path) -> Image.Image:
    im = open_rgb(src)
    im = upscale_to_hd(im)
    im = grade(im)
    return im


def main() -> None:
    OUT_HD.mkdir(parents=True, exist_ok=True)
    IMG.mkdir(parents=True, exist_ok=True)

    sources = sorted(
        [
            p
            for p in TRABAJOS.iterdir()
            if p.is_file()
            and p.suffix.lower() in {".png", ".jpg", ".jpeg"}
            and "-hd" not in p.stem
            and not p.name.endswith(".webp")
        ]
    )

    enhanced: dict[str, Image.Image] = {}
    for src in sources:
        print(f"enhance {src.name} …", flush=True)
        im = enhance_file(src)
        enhanced[src.stem] = im
        save_webp(im, OUT_HD / f"{src.stem}.webp")
        # also refresh root trabajos with polished jpg/webp companions
        save_webp(im, TRABAJOS / f"{src.stem}.webp")
        if src.suffix.lower() in {".jpg", ".jpeg", ".png"}:
            # keep original binary; write polished jpg preview
            save_jpg(im, TRABAJOS / f"{src.stem}-hd.jpg")

    # Named mappings from workshop → site slots (honest captions updated in HTML)
    mapping = {
        "ff-escena-grupo": "escena-01",
        "suki-neon": "escena-01",
        "coleccion-ff": "escena-02",
        "skyline-azul": "majin-buu-escala",
        "goku": "majin-buu-escala",  # DB figure (Majin Buu) — caption fix in HTML
        "atos-taxi": "atos-taxi",
        "supra-naranja": "chevrolet-sprint-escala",  # interim until web fill
        "civic-naranja": "renault-clio-escala",
        "charger-rojo": "carro-swift",
        "hero-coleccion-cinematica": "escena-06",
        "batman-box": "escena-03",
        "batman-ciudad": "escena-05",
        "batman-figura": "escena-04",
        "vin-diesel": "escena-08",
    }

    for name, key in mapping.items():
        im = enhanced.get(key)
        if im is None:
            print(f"skip map {name}: missing {key}")
            continue
        out = grade(upscale_to_hd(im.copy()))
        # landscape preference for wide gallery tiles
        if name in {"ff-escena-grupo", "coleccion-ff", "hero-coleccion-cinematica", "batman-ciudad"}:
            framed = center_crop(out, 16, 10)
            if max(framed.size) < TARGET_LONG:
                framed = upscale_to_hd(framed)
            save_webp(framed, IMG / f"{name}.webp")
            save_jpg(framed, IMG / f"{name}.jpg")
        else:
            save_webp(out, IMG / f"{name}.webp")
            save_jpg(out, IMG / f"{name}.jpg")
        print(f"mapped {name}.webp <- {key}", flush=True)

    # Complementary Full HD diecast / miniature atmosphere from Unsplash (license: Unsplash)
    # Used only where workshop has no exact model photo.
    web_fills = {
        # orange sports coupé / diecast vibe → supra slot
        "supra-naranja": "https://images.unsplash.com/photo-1542362567-b07e54358753?auto=format&fit=crop&w=1920&q=85",
        # hatch / civic-like orange street
        "civic-naranja": "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?auto=format&fit=crop&w=1920&q=85",
        # muscular red american muscle → charger vibe
        "charger-rojo": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1920&q=85",
        # dark city / comic-adjacent atmosphere for batman diorama placeholders (no copyrighted characters)
        "batman-ciudad": "https://images.unsplash.com/photo-1514565131-fce0801e5785?auto=format&fit=crop&w=1920&q=85",
        # neon night street for suki/neon diorama atmosphere complement kept separate? keep suki from workshop
        "vin-diesel": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?auto=format&fit=crop&w=1920&q=85",
    }

    for name, url in web_fills.items():
        try:
            print(f"download web fill {name} …", flush=True)
            im = download(url)
            im = grade(upscale_to_hd(center_crop(im, 16, 10)))
            # Prefer blending with workshop for authenticity if mapped already exists — overwrite with web
            # only when name reserved for car models that aren't in folder.
            save_webp(im, IMG / f"{name}.webp")
            save_jpg(im, IMG / f"{name}.jpg")
            # also save attribution sidecars once
            (IMG / f"{name}.ATTRIBUTION.txt").write_text(
                f"Source: Unsplash\nURL: {url}\nUsage: complementary atmosphere / model reference for web UI.\n",
                encoding="utf-8",
            )
        except Exception as exc:  # noqa: BLE001
            print(f"web fill failed {name}: {exc}")

    # Prefer authentic workshop shots when we have better matches:
    # restore skyline/goku/suki/ff from workshop (overwrite web if any)
    prefer_workshop = {
        "skyline-azul": "majin-buu-escala",
        "goku": "majin-buu-escala",
        "suki-neon": "escena-01",
        "ff-escena-grupo": "escena-01",
        "coleccion-ff": "escena-02",
        "batman-box": "escena-03",
        "batman-figura": "escena-04",
        "atos-taxi": "atos-taxi",
        "twingo": "carro-twingo-escala",
        "clio": "renault-clio-escala",
        "sprint": "chevrolet-sprint-escala",
        "swift": "carro-swift",
        "majin-buu": "majin-buu-escala",
    }
    for name, key in prefer_workshop.items():
        im = enhanced.get(key)
        if im is None:
            continue
        out = grade(upscale_to_hd(im.copy()))
        if name in {"ff-escena-grupo", "coleccion-ff"}:
            out = center_crop(out, 16, 10)
            out = upscale_to_hd(out)
        save_webp(out, IMG / f"{name}.webp")
        save_jpg(out, IMG / f"{name}.jpg")
        print(f"workshop prefer {name}", flush=True)

    print("done.")


if __name__ == "__main__":
    main()
