"""
Import Cursor-uploaded workshop photos → polished WebP HD in assets/trabajos/.
Also mirrors same files into assets/img/ for page reuse.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
CURSOR_ASSETS = Path(
    r"C:\Users\Jose Rojas\.cursor\projects"
    r"\c-Users-Jose-Rojas-Documents-IntentandoColeccionar-RepoColeccionar\assets"
)
OUT_TRABAJOS = ROOT / "assets" / "trabajos"
OUT_NUEVOS = OUT_TRABAJOS / "nuevos"
OUT_IMG = ROOT / "assets" / "img"
TARGET_LONG = 1920
MAX_SCALE = 3.0
WEBP_Q = 88

# (filename fragment to match, output stem)
IMPORTS: list[tuple[str, str]] = [
    ("Renault_clio_esca__1_43-9d4d66d5-0f70-4851-9a10-a7b8a79cbf6a", "clio-negro-escala"),
    ("477572593_122142566678496824_4509193973570285700_n-df4e7374-b2b8-4b11-9950-2c8b6ce739b9", "suki-rosa-ff"),
    ("480119179_122142566426496824_7091444679294255483_n-e0bbb070-0dbd-4a3e-a9bb-520176259681", "carrera-starter-rx7-eclipse"),
    ("477575481_122142566588496824_6970776527901223219_n-9c9dd292-6e4e-4b98-b9bb-7887993c000b", "diorama-supra-naranja-ff"),
    ("Majin_buu_escala_1_64-9e55c694-cbec-4e92-8459-3013ebfed130", "majin-buu-skyline"),
    ("734756176_27418593247792961_1467957245092168603_n-f731108f-b552-4677-acae-9bf83399b498", "batman-streetwear"),
    ("480159405_122142566318496824_355134166546417428_n-8e2d026f-12c9-4714-b6ba-96b848371eb8", "skyline-azul-figuras"),
    ("734387651_27418595461126073_1797736138839381973_n-e6fef3fd-1779-417a-a1ae-f0a937a2f257", "civic-verde-ff"),
    ("735608372_27418593101126309_7451923249020394875_n-43cdb773-2147-478f-a11e-49413cd65341", "figuras-personalizadas"),
    ("736367255_27418592747793011_559827847129485724_n-740988db-25a9-44eb-ac0b-85dc9f9806f3", "paul-walker-supra-mano"),
    ("736045143_27418593827792903_2198897045977143563_n-b2a4fd08-6d97-4de8-acf9-3cac6d090c8c", "halo-spartan-warthog"),
    ("carro_swift-012ed2b5-ad0f-4d16-add5-fb877a82bcb5", "swift-blanco-rampa"),
    ("738625286_27418594607792825_909422296372230593_n-687121cc-829c-4aa9-9eaa-71184342d54f", "diorama-porsche-rosa-dinos"),
    ("Atos_taxi-067845bc-11e6-4b94-8b2c-719bfe1424f3", "atos-taxi-bogota"),
    ("cheverolet_sprint_escala_1_43-9b86beb1-0ad3-40ee-b4b4-f0f4f7e46cdb", "chevrolet-sprint-teal"),
    ("CARROTWINGOESCALA_1_43-95bc84c1-e908-42ab-8818-bfd6d394c85d", "twingo-plata"),
]


def win_long(path: Path) -> str:
    """Windows extended-length path so names >260 chars still open."""
    resolved = str(path.resolve())
    if resolved.startswith("\\\\?\\"):
        return resolved
    if resolved.startswith("\\\\"):
        return "\\\\?\\UNC\\" + resolved[2:]
    return "\\\\?\\" + resolved


def find_src(fragment: str) -> Path:
    matches = list(CURSOR_ASSETS.glob(f"*{fragment}*.png"))
    if not matches:
        raise FileNotFoundError(f"Missing source matching *{fragment}*.png")
    return matches[0]


def open_rgb(path: Path) -> Image.Image:
    with open(win_long(path), "rb") as fh:
        im = Image.open(fh)
        im.load()
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
        return im
    scale = min(target_long / long_side, MAX_SCALE)
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


def save_webp(im: Image.Image, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "WEBP", quality=WEBP_Q, method=6)


def main() -> None:
    OUT_TRABAJOS.mkdir(parents=True, exist_ok=True)
    OUT_NUEVOS.mkdir(parents=True, exist_ok=True)
    OUT_IMG.mkdir(parents=True, exist_ok=True)

    for fragment, stem in IMPORTS:
        src = find_src(fragment)
        print(f"{stem} <- {src.name}", flush=True)
        base = open_rgb(src)
        # Keep RGB PNG under nuevos for provenance (short local name)
        base.save(OUT_NUEVOS / f"{stem}.png", "PNG", optimize=True)
        im = grade(upscale_to_hd(base))
        w, h = im.size
        for dest in (
            OUT_TRABAJOS / f"{stem}.webp",
            OUT_NUEVOS / f"{stem}.webp",
            OUT_IMG / f"{stem}.webp",
        ):
            save_webp(im, dest)
        print(f"  -> {stem}.webp ({w}x{h})", flush=True)

    print(f"done. {len(IMPORTS)} assets imported.", flush=True)


if __name__ == "__main__":
    main()
