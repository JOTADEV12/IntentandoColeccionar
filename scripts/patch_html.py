from pathlib import Path
import re

root = Path(r"C:\Users\Jose Rojas\Documents\IntentandoColeccionar\RepoColeccionar")

FONT = (
    'https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Syne:wght@400;600;700;800'
    '&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&family=Rubik+Dirt&display=swap'
)

HEAD_EXTRA = """  <link rel="icon" href="assets/logo/svg/favicon.svg" type="image/svg+xml"/>
  <link rel="icon" href="assets/logo/png/favicon-32.png" sizes="32x32" type="image/png"/>
  <link rel="apple-touch-icon" href="assets/logo/png/favicon-180.png"/>
"""

BRAND = """      <a href="index.html" class="brand" aria-label="Intentando Coleccionar — Inicio">
        <img class="brand__icon" src="assets/logo/svg/logo-icon.svg" alt="" width="40" height="40"/>
        <img class="brand__logo" src="assets/logo/svg/logo-horizontal.svg" alt="Intentando Coleccionar" width="220" height="40" decoding="async"/>
      </a>"""

FOOTER_BRAND_NEW = (
    '<img class="footer-brand-logo" src="assets/logo/svg/logo-horizontal.svg" '
    'alt="Intentando Coleccionar" width="220" height="40" decoding="async"/>'
    '\n          <div class="footer-brand">Intentando<span>&nbsp;Coleccionar</span></div>'
)

FOOTER_BRAND_OLD = re.compile(
    r'<div class="footer-brand">Intentando<span>&nbsp;Coleccionar</span></div>',
    re.I,
)

brand_re = re.compile(
    r'<a href="index\.html" class="brand"[^>]*>.*?</a>',
    re.S,
)

for html in root.glob("*.html"):
    text = html.read_text(encoding="utf-8")

    # fonts
    text = re.sub(
        r'href="https://fonts\.googleapis\.com/css2\?[^"]+"',
        f'href="{FONT}"',
        text,
        count=1,
    )

    # premium css
    if "premium.css" not in text:
        text = text.replace(
            '<link rel="stylesheet" href="css/main.css"/>',
            '<link rel="stylesheet" href="css/main.css"/>\n  <link rel="stylesheet" href="css/premium.css"/>',
        )

    # favicons
    if 'rel="icon"' not in text:
        text = text.replace(
            '<link rel="stylesheet" href="css/main.css"/>',
            HEAD_EXTRA + '  <link rel="stylesheet" href="css/main.css"/>',
        )

    # brand
    text, n = brand_re.subn(BRAND, text, count=1)
    if n == 0:
        print("brand miss", html.name)

    # footer logo
    if "footer-brand-logo" not in text:
        text = FOOTER_BRAND_OLD.sub(FOOTER_BRAND_NEW, text, count=1)

    html.write_text(text, encoding="utf-8")
    print("updated", html.name)
