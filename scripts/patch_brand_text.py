from pathlib import Path
import re

root = Path(".")
BRAND = """      <a href="index.html" class="brand" aria-label="Intentando Coleccionar — Inicio">
        <span class="brand__lockup">
          <span class="brand__name">Intentando</span>
          <span class="brand__tag">Coleccionar</span>
        </span>
      </a>"""

brand_re = re.compile(r'<a href="index\.html" class="brand"[^>]*>.*?</a>', re.S)
for html in root.glob("*.html"):
    text = html.read_text(encoding="utf-8")
    text, n = brand_re.subn(BRAND, text, count=1)
    html.write_text(text, encoding="utf-8")
    print(html.name, n)
