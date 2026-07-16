"""Replace .img-ph with real <img> tags when data-src/data-img is known."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_ph(html: str) -> str:
    # Host with data-src wrapping an img-ph
    def host_repl(m: re.Match[str]) -> str:
        before, attrs, inner, after = m.group(1), m.group(2), m.group(3), m.group(4)
        src_m = re.search(r'data-src="([^"]+)"', attrs)
        alt_m = re.search(r'data-alt="([^"]*)"', attrs) or re.search(r'data-cap="([^"]*)"', attrs)
        if not src_m:
            return m.group(0)
        src = src_m.group(1)
        alt = alt_m.group(1) if alt_m else ""
        new_inner = re.sub(
            r'<div class="img-ph"[^>]*>.*?</div>',
            f'<img src="{src}" alt="{alt}" width="1600" height="1000" loading="lazy" decoding="async" data-hydrated="true"/>',
            inner,
            count=1,
            flags=re.S,
        )
        return f"{before}{attrs}>{new_inner}{after}"

    html = re.sub(
        r'(<(?:article|div|a)[^>]*?)((?:(?!>).)*data-src="[^"]+"[^>]*)>([\s\S]*?)(</(?:article|div|a)>)',
        host_repl,
        html,
    )

    # Standalone data-img placeholders
    def ph_repl(m: re.Match[str]) -> str:
        tag = m.group(0)
        src_m = re.search(r'data-img="([^"]+)"', tag)
        if not src_m:
            return tag
        src = src_m.group(1)
        alt_m = re.search(r'aria-label="([^"]*)"', tag)
        alt = alt_m.group(1) if alt_m else ""
        style_m = re.search(r'style="([^"]*)"', tag)
        style = f' style="{style_m.group(1)}"' if style_m else ""
        return f'<img src="{src}" alt="{alt}" width="1600" height="1000" loading="lazy" decoding="async"{style}/>'

    html = re.sub(r'<div class="img-ph"[^>]*data-img="[^"]+"[^>]*>.*?</div>', ph_repl, html, flags=re.S)
    return html


def main() -> None:
    for name in [
        "galeria.html",
        "carros.html",
        "escenas.html",
        "dioramas.html",
        "categorias.html",
        "index.html",
    ]:
        fp = ROOT / name
        if not fp.exists():
            continue
        old = fp.read_text(encoding="utf-8")
        new = replace_ph(old)
        fp.write_text(new, encoding="utf-8")
        print(name, "changed" if new != old else "unchanged")


if __name__ == "__main__":
    main()
