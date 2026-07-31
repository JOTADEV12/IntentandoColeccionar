#!/usr/bin/env python3
"""Inyecta (o actualiza) la meta de verificación de Google Search Console.

Uso:
  python scripts/set_gsc_verification.py TU_CODIGO_DE_VERIFICACION

El código lo obtienes en Search Console → Propiedad → Verificación HTML tag.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    "index.html",
    "categorias.html",
    "galeria.html",
    "sobre-nosotros.html",
    "testimonios.html",
    "contacto.html",
    "carros.html",
    "dioramas.html",
    "escenas.html",
]

META_RE = re.compile(
    r'\s*<meta\s+name=["\']google-site-verification["\']\s+content=["\'][^"\']*["\']\s*/?>\s*',
    re.I,
)


def main() -> None:
    if len(sys.argv) < 2 or not sys.argv[1].strip():
        print("Uso: python scripts/set_gsc_verification.py CODIGO")
        sys.exit(1)

    code = sys.argv[1].strip()
    meta = f'  <meta name="google-site-verification" content="{code}"/>\n'
    updated = 0

    for name in PAGES:
        path = ROOT / name
        if not path.exists():
            print(f"skip missing {name}")
            continue
        html = path.read_text(encoding="utf-8")
        html = META_RE.sub("\n", html)
        # Insertar justo después de robots / googlebot si existen, si no tras charset
        if 'name="googlebot"' in html:
            html = html.replace(
                '<meta name="googlebot" content="index, follow"/>',
                '<meta name="googlebot" content="index, follow"/>\n' + meta.rstrip(),
                1,
            )
        elif "<head>" in html:
            html = html.replace("<head>", "<head>\n" + meta.rstrip(), 1)
        else:
            print(f"no <head> in {name}")
            continue
        path.write_text(html, encoding="utf-8")
        print(f"updated {name}")
        updated += 1

    # Guardar también en site-config para referencia
    cfg = ROOT / "js" / "site-config.js"
    if cfg.exists():
        text = cfg.read_text(encoding="utf-8")
        if "GOOGLE_SITE_VERIFICATION" in text:
            text = re.sub(
                r'GOOGLE_SITE_VERIFICATION:\s*"[^"]*"',
                f'GOOGLE_SITE_VERIFICATION: "{code}"',
                text,
            )
        else:
            text = text.replace(
                'GA_MEASUREMENT_ID: ""',
                f'GA_MEASUREMENT_ID: "",\n  GOOGLE_SITE_VERIFICATION: "{code}"',
            )
        cfg.write_text(text, encoding="utf-8")
        print("updated js/site-config.js")

    print(f"done: {updated} pages. Commit + push y luego pulsa Verificar en Search Console.")


if __name__ == "__main__":
    main()
