#!/usr/bin/env python3
"""Actualiza el dominio canónico en todo el sitio.

Uso:
  python scripts/set_domain.py
  python scripts/set_domain.py https://intentandocoleccionar.com

Por defecto migra .xyz → .com (dominio a comprar en Vercel).
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = "https://intentandocoleccionar.xyz"
NEW = "https://intentandocoleccionar.com"

GLOBS = ["*.html", "*.xml", "*.txt", "*.js", "*.md", "*.py", "*.json"]


def main() -> None:
    old, new = OLD, NEW
    if len(sys.argv) >= 2:
        new = sys.argv[1].rstrip("/")
    if len(sys.argv) >= 3:
        old = sys.argv[2].rstrip("/")

    count = 0
    for pattern in GLOBS:
        for path in ROOT.rglob(pattern):
            if ".git" in path.parts or "__pycache__" in path.parts:
                continue
            if path.name == "set_domain.py":
                continue
            if "node_modules" in path.parts or "videos" in path.parts:
                continue
            text = path.read_text(encoding="utf-8")
            if old not in text:
                continue
            path.write_text(text.replace(old, new), encoding="utf-8")
            print(f"updated {path.relative_to(ROOT)}")
            count += 1

    # Redirect www en vercel.json
    vj = ROOT / "vercel.json"
    if vj.exists():
        text = vj.read_text(encoding="utf-8")
        old_host = old.replace("https://", "").replace("http://", "")
        new_host = new.replace("https://", "").replace("http://", "")
        updated = text.replace(f"www.{old_host}", f"www.{new_host}").replace(
            old, new
        )
        if updated != text:
            vj.write_text(updated, encoding="utf-8")
            print("updated vercel.json")
            count += 1

    print(f"done: {count} files, domain {old} -> {new}")


if __name__ == "__main__":
    main()
