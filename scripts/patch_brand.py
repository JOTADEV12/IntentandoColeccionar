from pathlib import Path
import re

root = Path(r"C:\Users\Jose Rojas\Documents\IntentandoColeccionar\RepoColeccionar")

BRAND = """      <a href="index.html" class="brand" aria-label="Intentando Coleccionar — Inicio">
        <span class="brand__mark-wrap" aria-hidden="true">
          <img class="brand__mark" src="assets/logo/png/logo-nav-white.png" alt="" width="135" height="72" decoding="async"/>
        </span>
        <span class="brand__lockup">
          <span class="brand__name">Intentando</span>
          <span class="brand__tag">Coleccionar</span>
        </span>
      </a>"""

FOOTER_BLOCK = """        <div>
          <a href="index.html" class="footer-brand-link" aria-label="Intentando Coleccionar">
            <img class="footer-brand-logo" src="assets/logo/png/logo-stack-white.png" alt="" width="220" height="120" decoding="async"/>
            <span class="footer-brand">Intentando<span>&nbsp;Coleccionar</span></span>
          </a>
          <p>Piezas únicas en resina 3D, réplicas personalizadas y escenas cinematográficas. Hecho a mano en Colombia.</p>
        </div>"""

# simpler footer replace - just logo + text line patterns vary
brand_re = re.compile(r'<a href="index\.html" class="brand"[^>]*>.*?</a>', re.S)

footer_logo_re = re.compile(
    r'<img class="footer-brand-logo"[^>]*>\s*'
    r'(?:<div class="footer-brand">.*?</div>)?',
    re.S,
)

for html in root.glob("*.html"):
    text = html.read_text(encoding="utf-8")
    text, n = brand_re.subn(BRAND, text, count=1)
    text = footer_logo_re.sub(
        '<img class="footer-brand-logo" src="assets/logo/png/logo-stack-white.png" alt="" width="220" height="120" decoding="async"/>\n'
        '          <div class="footer-brand">Intentando<span>&nbsp;Coleccionar</span></div>',
        text,
        count=1,
    )
    html.write_text(text, encoding="utf-8")
    print(html.name, "brand", n)
