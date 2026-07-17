#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).resolve().parents[1]
for p in root.glob("*.html"):
    t = p.read_text(encoding="utf-8")
    t2 = t.replace(
        'href="sobre-nosotros.html#inversion">Inversión</a>',
        'href="sobre-nosotros.html#cotizar">Cotizar</a>',
    )
    t2 = t2.replace("sobre-nosotros.html#inversion", "sobre-nosotros.html#cotizar")
    if t2 != t:
        p.write_text(t2, encoding="utf-8")
        print("updated", p.name)
