#!/usr/bin/env python3
"""Sincroniza header (solid) y footer desde partials/shell.py en páginas internas."""
from __future__ import annotations

import re
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    "categorias.html",
    "galeria.html",
    "testimonios.html",
    "carros.html",
    "escenas.html",
    "dioramas.html",
    "contacto.html",
    "sobre-nosotros.html",
]


def load_shell():
    spec = importlib.util.spec_from_file_location("shell", ROOT / "partials" / "shell.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod


def sync(html: str, header: str, footer: str) -> str:
    html = re.sub(
        r"(?s)<header class=\"site-header.*?</div>\s*(?=<main)",
        header.strip() + "\n\n  ",
        html,
        count=1,
    )
    html = re.sub(
        r"(?s)<footer class=\"site-footer\">.*?</footer>",
        footer.strip(),
        html,
        count=1,
    )
    return html


def main() -> None:
    shell = load_shell()
    for name in PAGES:
        path = ROOT / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        text = sync(text, shell.HEADER_SOLID, shell.FOOTER)
        path.write_text(text, encoding="utf-8")
        print(f"synced shell -> {name}")


if __name__ == "__main__":
    main()
