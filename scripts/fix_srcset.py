#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

for p in ROOT.glob("*.html"):
    t = p.read_text(encoding="utf-8")
    t2 = re.sub(r"/(\s+srcset=)", r"\1", t)
    if t2 != t:
        p.write_text(t2, encoding="utf-8")
        print(f"fixed {p.name}")

# Fix future srcset injection in apply script
script = ROOT / "scripts" / "apply_site_upgrades.py"
s = script.read_text(encoding="utf-8")
s2 = s.replace(
    """        pattern = re.compile(
            rf'(<img\\s+)([^>]*src="{re.escape(std)}"[^>]*)(/?>)',
            re.I,
        )

        def repl(m: re.Match) -> str:
            attrs = m.group(2)
            if "srcset=" in attrs:
                return m.group(0)
            attrs = attrs.rstrip()
            attrs += f' srcset="{std} 1x, {hd} 2x" sizes="(max-width: 768px) 100vw, 50vw"'
            return f"{m.group(1)}{attrs}{m.group(3)}"
""",
    """        pattern = re.compile(
            rf'(<img\\b)([^>]*?\\bsrc="{re.escape(std)}"[^>]*?)(\\s*/?>)',
            re.I,
        )

        def repl(m: re.Match) -> str:
            attrs = m.group(2)
            if "srcset=" in attrs:
                return m.group(0)
            attrs = attrs.rstrip().rstrip("/")
            sizes = "(max-width: 768px) 100vw, 50vw"
            attrs += f' srcset="{std} 1x, {hd} 2x" sizes="{sizes}"'
            return f"{m.group(1)}{attrs}>"
""",
)
if s2 != s:
    script.write_text(s2, encoding="utf-8")
    print("apply_site_upgrades.py pattern fixed")
else:
    print("apply script unchanged (pattern may already differ)")
