#!/usr/bin/env python3
"""Aplica mejoras globales al sitio: head SEO, tipografía, extras CSS, srcset HD."""
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE_ORIGIN = "https://intentandocoleccionar.com"
OG_IMAGE = f"{SITE_ORIGIN}/assets/img/hero-tag-brick.webp"
FONTS = (
    "https://fonts.googleapis.com/css2?family=Anton&family=JetBrains+Mono:wght@400;500;600"
    "&family=Permanent+Marker&family=Work+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap"
)

# Map gallery/work filenames -> HD src for srcset (when available)
HD_MAP = {
    "atos-taxi-bogota.webp": ("assets/trabajos/atos-taxi-bogota.webp", "assets/trabajos/hd/atos-taxi.webp"),
    "clio-negro-escala.webp": ("assets/trabajos/clio-negro-escala.webp", "assets/trabajos/hd/renault-clio-escala.webp"),
    "chevrolet-sprint-teal.webp": ("assets/trabajos/chevrolet-sprint-teal.webp", "assets/trabajos/hd/chevrolet-sprint-escala.webp"),
    "twingo-plata.webp": ("assets/trabajos/twingo-plata.webp", "assets/trabajos/hd/carro-twingo-escala.webp"),
    "swift-blanco-rampa.webp": ("assets/trabajos/swift-blanco-rampa.webp", "assets/trabajos/hd/carro-swift.webp"),
    "majin-buu-skyline.webp": ("assets/trabajos/majin-buu-skyline.webp", "assets/trabajos/hd/majin-buu-escala.webp"),
}

PAGES = {
    "index.html": {
        "title": "Intentando Coleccionar | Piezas Únicas · No es un producto, es una creación",
        "description": "Intentando Coleccionar — Piezas únicas en resina 3D, réplicas personalizadas y escenas cinematográficas. No es un producto, es una creación. Colombia.",
        "extra_css": ["css/hero.css", "css/works.css"],
        "solid_header": False,
    },
    "categorias.html": {
        "title": "Categorías | Intentando Coleccionar",
        "description": "Carros a escala, figuras, dioramas y escenas personalizadas. Explora las líneas de Intentando Coleccionar.",
    },
    "galeria.html": {
        "title": "Galería | Intentando Coleccionar",
        "description": "Galería de creaciones reales: carros, figuras, escenas y dioramas en resina 3D hechos a mano en Colombia.",
    },
    "sobre-nosotros.html": {
        "title": "Sobre nosotros | Intentando Coleccionar",
        "description": "Taller colombiano de miniaturas en resina 3D. Historia, proceso, inversión orientativa y FAQ de Intentando Coleccionar.",
    },
    "testimonios.html": {
        "title": "Clientes | Intentando Coleccionar",
        "description": "Lo que dicen coleccionistas sobre réplicas, escenas y dioramas personalizados de Intentando Coleccionar.",
    },
    "contacto.html": {
        "title": "Contacto | Intentando Coleccionar",
        "description": "Cotiza por WhatsApp. Respuesta rápida, sin compromiso. Intentando Coleccionar — Colombia.",
    },
    "carros.html": {
        "title": "Carros a escala | Intentando Coleccionar",
        "description": "Réplicas de tu vehículo real y carros a escala en resina 3D. Cotización gratuita.",
    },
    "escenas.html": {
        "title": "Escenas personalizadas | Intentando Coleccionar",
        "description": "Escenas cinematográficas personalizadas, incluyendo temática Rápido y Furioso. Hecho a mano en Colombia.",
    },
    "dioramas.html": {
        "title": "Dioramas | Intentando Coleccionar",
        "description": "Dioramas a escala personalizados en resina 3D. Ambientaciones únicas para coleccionar o regalar.",
    },
}


def build_head(page: str, meta: dict) -> str:
    title = meta["title"]
    desc = meta["description"]
    canonical = f"{SITE_ORIGIN}/{page if page != 'index.html' else ''}".rstrip("/") or SITE_ORIGIN
    if page == "index.html":
        canonical = SITE_ORIGIN + "/"
    else:
        canonical = f"{SITE_ORIGIN}/{page}"

    css_links = [
        '<link rel="stylesheet" href="css/main.css"/>',
        '<link rel="stylesheet" href="css/premium.css"/>',
        '<link rel="stylesheet" href="css/motion.css?v=4"/>',
        '<link rel="stylesheet" href="css/site-extras.css"/>',
    ]
    for extra in meta.get("extra_css", []):
        css_links.append(f'<link rel="stylesheet" href="{extra}"/>')

    return f'''<!DOCTYPE html>
<html lang="es">
<head>
  <script>document.documentElement.classList.add("is-booting");</script>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <meta name="description" content="{desc}"/>
  <meta name="theme-color" content="#0a0908"/>
  <link rel="canonical" href="{canonical}"/>
  <meta property="og:type" content="website"/>
  <meta property="og:url" content="{canonical}"/>
  <meta property="og:title" content="{title}"/>
  <meta property="og:description" content="{desc}"/>
  <meta property="og:image" content="{OG_IMAGE}"/>
  <meta property="og:locale" content="es_CO"/>
  <meta property="og:site_name" content="Intentando Coleccionar"/>
  <meta name="twitter:card" content="summary_large_image"/>
  <meta name="twitter:title" content="{title}"/>
  <meta name="twitter:description" content="{desc}"/>
  <meta name="twitter:image" content="{OG_IMAGE}"/>
  <title>{title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
  <link href="{FONTS}" rel="stylesheet"/>
  <link rel="icon" href="assets/logo/svg/favicon.svg" type="image/svg+xml"/>
  <link rel="icon" href="assets/logo/png/favicon-32.png" sizes="32x32" type="image/png"/>
  <link rel="apple-touch-icon" href="assets/logo/png/favicon-180.png"/>
  {chr(10).join(css_links)}
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": "Intentando Coleccionar",
    "description": "Miniaturas en resina 3D, réplicas personalizadas y escenas cinematográficas hechas a mano en Colombia.",
    "url": "{SITE_ORIGIN}/",
    "image": "{OG_IMAGE}",
    "telephone": "+573115152006",
    "address": {{
      "@type": "PostalAddress",
      "addressCountry": "CO"
    }},
    "areaServed": "CO",
    "sameAs": [
      "https://www.instagram.com/intentando_coleccionar/",
      "https://www.tiktok.com/@intentandocoleccionar",
      "https://www.facebook.com/intentando.coleccionar",
      "https://wa.me/573115152006"
    ]
  }}
  </script>
</head>'''


def replace_head(html: str, page: str, meta: dict) -> str:
    new_head = build_head(page, meta)
    # Replace from DOCTYPE through </head>
    return re.sub(r"(?is)<!DOCTYPE html>.*?</head>", new_head, html, count=1)


def strip_verified(html: str) -> str:
    html = re.sub(r'\s*<span class="test-verified">Verificado</span>', "", html)
    html = re.sub(
        r"<p class=\"lead\">Testimonios publicados en el sitio original\.[^<]*</p>",
        '<p class="lead">Historias de coleccionistas que encargaron piezas únicas — réplicas, escenas y dioramas personalizados.</p>',
        html,
        count=1,
    )
    return html


def add_srcset(html: str) -> str:
    for name, (std, hd) in HD_MAP.items():
        hd_path = ROOT / hd
        if not hd_path.exists():
            continue
        # Match img tags that use this file as src
        pattern = re.compile(
            rf'(<img\b)([^>]*?\bsrc="{re.escape(std)}"[^>]*?)(\s*/?>)',
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

        html = pattern.sub(repl, html)
    return html


def ensure_scripts(html: str) -> str:
    # Ensure site-config + extras are loaded before main
    if "js/site-config.js" not in html:
        html = html.replace(
            '<script src="js/main.js',
            '<script src="js/site-config.js" defer></script>\n  <script src="js/main.js',
        )
    # bump cache
    html = html.replace("js/main.js?v=2", "js/main.js?v=5")
    html = html.replace('src="js/main.js"', 'src="js/main.js?v=5"')
    html = html.replace("js/experience.js?v=4", "js/experience.js?v=5")
    return html


def clean_root_media() -> None:
    inbox = ROOT / "assets" / "_inbox"
    inbox.mkdir(parents=True, exist_ok=True)
    for p in ROOT.iterdir():
        if p.is_file() and p.suffix.lower() in {".jpg", ".jpeg", ".png"} and p.name not in {
            # keep nothing at root
        }:
            # Skip if already logo-like at root only
            dest = inbox / p.name
            if not dest.exists():
                shutil.move(str(p), str(dest))
                print(f"moved {p.name} -> assets/_inbox/")


def write_seo_files() -> None:
    pages = [
        ("", "1.0"),
        ("categorias.html", "0.9"),
        ("galeria.html", "0.9"),
        ("carros.html", "0.8"),
        ("escenas.html", "0.8"),
        ("dioramas.html", "0.8"),
        ("sobre-nosotros.html", "0.7"),
        ("testimonios.html", "0.7"),
        ("contacto.html", "0.8"),
    ]
    urls = []
    for path, prio in pages:
        loc = f"{SITE_ORIGIN}/" if not path else f"{SITE_ORIGIN}/{path}"
        urls.append(
            f"  <url>\n    <loc>{loc}</loc>\n    <changefreq>weekly</changefreq>\n    <priority>{prio}</priority>\n  </url>"
        )
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n",
        encoding="utf-8",
    )
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE_ORIGIN}/sitemap.xml\n",
        encoding="utf-8",
    )
    (ROOT / "netlify.toml").write_text(
        '''[build]
  publish = "."

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "SAMEORIGIN"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"

[[headers]]
  for = "/assets/*"
  [headers.values]
    Cache-Control = "public, max-age=604800"
''',
        encoding="utf-8",
    )
    gitignore = ROOT / ".gitignore"
    if not gitignore.exists():
        gitignore.write_text(
            ".DS_Store\nThumbs.db\n*.log\n.node_modules/\n.vercel\n.netlify\n",
            encoding="utf-8",
        )


def patch_fonts_css() -> None:
    css = ROOT / "css" / "main.css"
    text = css.read_text(encoding="utf-8")
    text = text.replace(
        '''  --display: "Bebas Neue", Impact, sans-serif;
  --heading: "Syne", system-ui, sans-serif;
  --body: "DM Sans", system-ui, sans-serif;
  --brand: "Rubik Dirt", "Bebas Neue", Impact, sans-serif;''',
        '''  --display: "Anton", Impact, sans-serif;
  --heading: "Work Sans", system-ui, sans-serif;
  --body: "Work Sans", system-ui, sans-serif;
  --brand: "Permanent Marker", "Anton", Impact, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, monospace;''',
    )
    css.write_text(text, encoding="utf-8")


def main() -> None:
    patch_fonts_css()
    write_seo_files()
    clean_root_media()

    for page, meta in PAGES.items():
        path = ROOT / page
        if not path.exists():
            print(f"skip missing {page}")
            continue
        html = path.read_text(encoding="utf-8")
        html = replace_head(html, page, meta)
        html = strip_verified(html)
        html = add_srcset(html)
        html = ensure_scripts(html)
        path.write_text(html, encoding="utf-8")
        print(f"patched {page}")


if __name__ == "__main__":
    main()
