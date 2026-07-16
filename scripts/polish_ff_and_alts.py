from __future__ import annotations

import re
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(__file__).resolve().parents[1]
IMG = ROOT / "assets" / "img"
T = ROOT / "assets" / "trabajos"


def main() -> None:
    src = ImageOps.exif_transpose(Image.open(T / "escena-01.webp")).convert("RGB")
    canvas = Image.new("RGB", (1920, 1200), (10, 9, 8))
    h = 1200
    w = int(src.width * (h / src.height))
    im = src.resize((w, h), Image.Resampling.LANCZOS)
    if w > 1920:
        x = (w - 1920) // 2
        im = im.crop((x, 0, x + 1920, h))
        canvas.paste(im, (0, 0))
    else:
        canvas.paste(im, ((1920 - w) // 2, 0))
    canvas = ImageEnhance.Color(canvas).enhance(1.08)
    canvas = ImageEnhance.Contrast(canvas).enhance(1.05)
    canvas = ImageEnhance.Sharpness(canvas).enhance(1.1)
    canvas.save(IMG / "ff-escena-grupo.webp", "WEBP", quality=90, method=6)
    canvas.save(IMG / "suki-neon-wide.webp", "WEBP", quality=90, method=6)
    print("ff", canvas.size)

    for name in ["galeria.html", "carros.html", "escenas.html", "dioramas.html"]:
        p = ROOT / name
        t = p.read_text(encoding="utf-8")

        def fix(m: re.Match[str]) -> str:
            block = m.group(0)
            if 'alt=""' not in block:
                return block
            alt = re.search(r'data-alt="([^"]*)"', block) or re.search(
                r'data-cap="([^"]*)"', block
            )
            a = alt.group(1) if alt else "Creación Intentando Coleccionar"
            return block.replace('alt=""', f'alt="{a}"', 1)

        p.write_text(re.sub(r"<article[\s\S]*?</article>", fix, t), encoding="utf-8")
        print("alts", name)


if __name__ == "__main__":
    main()
