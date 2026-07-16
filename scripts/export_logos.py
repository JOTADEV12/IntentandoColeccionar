from PIL import Image
from pathlib import Path
import shutil

cursor = Path(r"C:\Users\Jose Rojas\.cursor\projects\c-Users-Jose-Rojas-Documents-IntentandoColeccionar-RepoColeccionar\assets")
dst = Path(r"C:\Users\Jose Rojas\Documents\IntentandoColeccionar\RepoColeccionar\assets\logo\png")
dst.mkdir(parents=True, exist_ok=True)

for name in [
    "logo-horizontal-dark.png",
    "favicon-ic.png",
]:
    src = cursor / name
    if src.exists():
        shutil.copy2(src, dst / name)

def upscale_to_4k(src_name, out_name, canvas=(3840, 2160), bg=(0, 0, 0, 0)):
    src = Image.open(dst / src_name).convert("RGBA")
    canvas_img = Image.new("RGBA", canvas, bg)
    margin = 160
    fitted = src.copy()
    fitted.thumbnail((canvas[0] - margin, canvas[1] - margin), Image.Resampling.LANCZOS)
    x = (canvas[0] - fitted.width) // 2
    y = (canvas[1] - fitted.height) // 2
    canvas_img.paste(fitted, (x, y), fitted)
    if bg[3] == 255:
        canvas_img.convert("RGB").save(dst / out_name, "PNG", optimize=True)
    else:
        canvas_img.save(dst / out_name, "PNG", optimize=True)
    print(out_name, canvas)

upscale_to_4k("logo-full-transparent.png", "logo-full-transparent-4k.png")
upscale_to_4k("logo-horizontal-transparent.png", "logo-horizontal-transparent-4k.png")
upscale_to_4k("logo-full-brick.png", "logo-full-brick-4k.png", bg=(10, 10, 10, 255))

icon = Image.open(dst / "logo-icon-ic.png").convert("RGBA")
for size in (16, 32, 48, 180, 512):
    i = icon.copy()
    i.thumbnail((size, size), Image.Resampling.LANCZOS)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(i, ((size - i.width) // 2, (size - i.height) // 2), i)
    out.save(dst / f"favicon-{size}.png", "PNG")
    print(f"favicon-{size}.png")

print("done")
