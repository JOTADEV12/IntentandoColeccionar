#!/usr/bin/env python3
"""Actualiza el dominio canónico en todo el sitio."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = "https://intentandocoleccionar.com"
NEW = "https://intentandocoleccionar.xyz"

GLOBS = ["*.html", "*.xml", "*.txt", "*.js", "*.md", "*.py"]

def main() -> None:
    count = 0
    for pattern in GLOBS:
        for path in ROOT.rglob(pattern):
            if ".git" in path.parts or "__pycache__" in path.parts:
                continue
            if path.name == "set_domain.py":
                continue
            text = path.read_text(encoding="utf-8")
            if OLD not in text:
                continue
            path.write_text(text.replace(OLD, NEW), encoding="utf-8")
            print(f"updated {path.relative_to(ROOT)}")
            count += 1
    print(f"done: {count} files, domain -> {NEW}")

if __name__ == "__main__":
    main()
