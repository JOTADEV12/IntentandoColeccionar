#!/usr/bin/env python3
"""Aplica SEO completo + analítica a todas las páginas públicas."""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://www.intentandocoleccionar.autos"
OG_IMAGE = f"{SITE}/assets/img/hero-tag-brick.webp"
TODAY = date.today().isoformat()

# Keywords por página (español Colombia — búsquedas reales)
PAGES: dict[str, dict] = {
    "index.html": {
        "title": "Carros a Escala y Réplicas Personalizadas Colombia | Intentando Coleccionar",
        "description": (
            "Taller colombiano de carros a escala 1/43 metalizados, réplicas personalizadas "
            "de tu vehículo, figuras, dioramas y escenas hechas a mano. Cotiza por WhatsApp."
        ),
        "keywords": (
            "intentando coleccionar, carros a escala colombia, réplicas personalizadas, "
            "carros 1/43 metalizados, miniaturas resina 3D, dioramas personalizados, "
            "figuras a escala, coleccionables colombia, réplica de mi carro, "
            "escenas personalizadas, hecho a mano colombia"
        ),
        "priority": "1.0",
    },
    "categorias.html": {
        "title": "Categorías: Carros, Figuras, Dioramas y Escenas | Intentando Coleccionar",
        "description": (
            "Explora carros a escala, figuras personalizadas, dioramas y escenas "
            "cinematográficas. Líneas de Intentando Coleccionar en Colombia."
        ),
        "keywords": (
            "categorías coleccionables, carros a escala, figuras personalizadas, "
            "dioramas, escenas cinematográficas, intentando coleccionar"
        ),
        "priority": "0.9",
    },
    "galeria.html": {
        "title": "Galería de Trabajos Reales | Intentando Coleccionar",
        "description": (
            "Galería de creaciones reales: carros a escala, figuras, escenas y dioramas "
            "en resina 3D hechos a mano en Colombia."
        ),
        "keywords": (
            "galería miniaturas, trabajos carros a escala, dioramas hechos a mano, "
            "figuras resina 3D colombia, portfolio intentando coleccionar"
        ),
        "priority": "0.9",
    },
    "carros.html": {
        "title": "Carros a Escala 1/43 Metalizados y Réplicas Personalizadas | Intentando Coleccionar",
        "description": (
            "Réplicas a escala de tu vehículo real y carros 1/43 metalizados con placa "
            "y diseños a medida. Cotización gratuita en Colombia."
        ),
        "keywords": (
            "carros a escala 1/43, carros metalizados, réplica de mi carro, "
            "miniatura auto personalizada, diecast colombia, placa personalizada, "
            "carros a escala colombia"
        ),
        "priority": "0.9",
    },
    "escenas.html": {
        "title": "Escenas Personalizadas y Rápido y Furioso | Intentando Coleccionar",
        "description": (
            "Escenas cinematográficas personalizadas, incluyendo temática Rápido y Furioso. "
            "Composiciones únicas hechas a mano en Colombia."
        ),
        "keywords": (
            "escenas personalizadas, rápido y furioso escala, escenas cinematográficas, "
            "diorama carros, figuras escena colombia"
        ),
        "priority": "0.8",
    },
    "dioramas.html": {
        "title": "Dioramas a Escala Personalizados | Intentando Coleccionar",
        "description": (
            "Dioramas a escala personalizados en resina 3D. Ambientaciones únicas "
            "para coleccionar o regalar. Hecho a mano en Colombia."
        ),
        "keywords": (
            "dioramas personalizados, diorama a escala, ambientación miniatura, "
            "diorama resina 3D colombia, regalo coleccionista"
        ),
        "priority": "0.8",
    },
    "sobre-nosotros.html": {
        "title": "Sobre Nosotros — Taller de Miniaturas en Colombia | Intentando Coleccionar",
        "description": (
            "Conoce el taller colombiano de miniaturas en resina 3D: historia, proceso, "
            "cotización a medida y preguntas frecuentes."
        ),
        "keywords": (
            "taller miniaturas colombia, resina 3D, proceso cotización, "
            "intentando coleccionar historia, FAQ réplicas"
        ),
        "priority": "0.7",
    },
    "testimonios.html": {
        "title": "Opiniones de Clientes Coleccionistas | Intentando Coleccionar",
        "description": (
            "Lo que dicen coleccionistas sobre réplicas, escenas y dioramas "
            "personalizados de Intentando Coleccionar."
        ),
        "keywords": (
            "testimonios coleccionistas, opiniones réplicas, clientes intentando coleccionar, "
            "reseñas dioramas colombia"
        ),
        "priority": "0.7",
    },
    "contacto.html": {
        "title": "Contacto y Cotización por WhatsApp | Intentando Coleccionar",
        "description": (
            "Cotiza tu carro a escala, réplica o diorama por WhatsApp. "
            "Respuesta rápida, sin compromiso. Intentando Coleccionar — Colombia."
        ),
        "keywords": (
            "cotizar carro a escala, contacto intentando coleccionar, whatsapp réplicas, "
            "pedir diorama personalizado colombia"
        ),
        "priority": "0.8",
    },
}

LOCAL_BUSINESS = {
    "@context": "https://schema.org",
    "@type": ["LocalBusiness", "Organization"],
    "@id": f"{SITE}/#business",
    "name": "Intentando Coleccionar",
    "alternateName": "IntentandoColeccionar",
    "description": (
        "Réplicas a escala personalizadas, carros 1/43 metalizados con placa y diseños "
        "a medida, figuras, dioramas y escenas hechas a mano en Colombia."
    ),
    "url": f"{SITE}/",
    "image": OG_IMAGE,
    "logo": f"{SITE}/assets/img/logo-lettering-only.png",
    "telephone": "+573115152006",
    "priceRange": "$$",
    "currenciesAccepted": "COP",
    "paymentAccepted": "Transferencia, Nequi, Daviplata",
    "address": {
        "@type": "PostalAddress",
        "addressCountry": "CO",
        "addressLocality": "Colombia",
    },
    "areaServed": {"@type": "Country", "name": "Colombia"},
    "sameAs": [
        "https://www.instagram.com/intentando_coleccionar/",
        "https://www.tiktok.com/@intentandocoleccionar",
        "https://www.facebook.com/intentando.coleccionar",
        "https://wa.me/573115152006",
    ],
    "contactPoint": {
        "@type": "ContactPoint",
        "telephone": "+573115152006",
        "contactType": "sales",
        "availableLanguage": ["Spanish"],
        "areaServed": "CO",
    },
    "knowsAbout": [
        "carros a escala",
        "réplicas personalizadas",
        "dioramas",
        "miniaturas en resina 3D",
        "escenas cinematográficas",
    ],
}

WEBSITE_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "@id": f"{SITE}/#website",
    "name": "Intentando Coleccionar",
    "url": f"{SITE}/",
    "inLanguage": "es-CO",
    "publisher": {"@id": f"{SITE}/#business"},
    "about": {
        "@type": "Thing",
        "name": "Réplicas a escala, carros 1/43 y dioramas personalizados",
    },
}

FAQ_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        {
            "@type": "Question",
            "name": "¿Cómo cotizo una pieza?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": (
                    "Escríbenos por WhatsApp al +57 311 515 2006 o usa el formulario de Contacto. "
                    "Cuéntanos qué quieres, adjunta fotos o referencias y te armamos una "
                    "cotización personalizada, sin compromiso."
                ),
            },
        },
        {
            "@type": "Question",
            "name": "¿Por qué no hay precios en la web?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": (
                    "Porque cada pieza es distinta: el valor depende de la figura o el diseño "
                    "que elijas (escala, detalle, cantidad de elementos). Cotizamos a medida."
                ),
            },
        },
        {
            "@type": "Question",
            "name": "¿Qué escalas manejan?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": (
                    "Hacemos réplicas a escala personalizadas según lo que tú quieras. "
                    "En carros trabajamos mucho la escala 1/43 metalizada, con placa y "
                    "diseños personalizados."
                ),
            },
        },
        {
            "@type": "Question",
            "name": "¿Hacen envíos a todo Colombia?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": (
                    "Sí. Empaque premium de protección y envío nacional. Si algo llega "
                    "dañado, lo rehacemos según nuestra garantía de entrega."
                ),
            },
        },
        {
            "@type": "Question",
            "name": "¿Puedo pedir escenas tipo Rápido y Furioso?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": (
                    "Sí. Creamos escenas personalizadas de alta demanda, incluyendo temática "
                    "cinematográfica. Cada composición se diseña a tu medida."
                ),
            },
        },
    ],
}


def dump_jsonld(obj: dict) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2)


def build_jsonld_block(page: str) -> str:
    blocks = [LOCAL_BUSINESS]
    if page == "index.html":
        blocks.append(WEBSITE_SCHEMA)
    if page == "sobre-nosotros.html":
        blocks.append(FAQ_SCHEMA)

    parts = []
    for obj in blocks:
        parts.append(
            f'  <script type="application/ld+json">\n{dump_jsonld(obj)}\n  </script>'
        )
    return "\n".join(parts)


def seo_meta_snippet(page: str, meta: dict) -> str:
    title = meta["title"]
    desc = meta["description"]
    keywords = meta["keywords"]
    if page == "index.html":
        canonical = f"{SITE}/"
    else:
        canonical = f"{SITE}/{page}"

    return f'''  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <meta name="description" content="{desc}"/>
  <meta name="keywords" content="{keywords}"/>
  <meta name="author" content="Intentando Coleccionar"/>
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"/>
  <meta name="googlebot" content="index, follow"/>
  <meta name="language" content="Spanish"/>
  <meta name="geo.region" content="CO"/>
  <meta name="geo.placename" content="Colombia"/>
  <meta name="theme-color" content="#0a0908"/>
  <link rel="canonical" href="{canonical}"/>
  <link rel="alternate" hreflang="es-CO" href="{canonical}"/>
  <link rel="alternate" hreflang="es" href="{canonical}"/>
  <link rel="alternate" hreflang="x-default" href="{SITE}/"/>
  <meta property="og:type" content="website"/>
  <meta property="og:url" content="{canonical}"/>
  <meta property="og:title" content="{title}"/>
  <meta property="og:description" content="{desc}"/>
  <meta property="og:image" content="{OG_IMAGE}"/>
  <meta property="og:image:alt" content="Intentando Coleccionar — piezas únicas a escala"/>
  <meta property="og:locale" content="es_CO"/>
  <meta property="og:site_name" content="Intentando Coleccionar"/>
  <meta name="twitter:card" content="summary_large_image"/>
  <meta name="twitter:title" content="{title}"/>
  <meta name="twitter:description" content="{desc}"/>
  <meta name="twitter:image" content="{OG_IMAGE}"/>
  <title>{title}</title>'''


def replace_seo_head(html: str, page: str, meta: dict) -> str:
    """Reemplaza el bloque meta SEO (charset → title) y el JSON-LD, sin tocar CSS."""
    new_meta = seo_meta_snippet(page, meta)

    # Desde charset hasta </title> inclusive (el boot script queda antes)
    html = re.sub(
        r"  <meta charset=\"UTF-8\"/>.*?  <title>.*?</title>",
        new_meta,
        html,
        count=1,
        flags=re.S,
    )

    # Reemplazar todos los bloques JSON-LD existentes por los nuevos
    html = re.sub(
        r"\s*<script type=\"application/ld\+json\">.*?</script>",
        "",
        html,
        flags=re.S,
    )

    jsonld = build_jsonld_block(page)
    # Insertar JSON-LD justo antes de </head>
    html = html.replace("</head>", f"{jsonld}\n</head>", 1)
    return html


def ensure_analytics_script(html: str) -> str:
    if "js/analytics.js" in html:
        return html
    # Tras site-config.js
    if 'src="js/site-config.js"' in html:
        return html.replace(
            '<script src="js/site-config.js" defer></script>',
            '<script src="js/site-config.js" defer></script>\n'
            '  <script src="js/analytics.js" defer></script>',
            1,
        )
    # Fallback: antes de </body>
    return html.replace(
        "</body>",
        '  <script src="js/site-config.js" defer></script>\n'
        '  <script src="js/analytics.js" defer></script>\n</body>',
        1,
    )


def write_robots() -> None:
    (ROOT / "robots.txt").write_text(
        f"""User-agent: *
Allow: /

# No indexar mockups / borradores de diseño
Disallow: /mockups/
Disallow: /scripts/
Disallow: /partials/
Disallow: /social/

Sitemap: {SITE}/sitemap.xml
""",
        encoding="utf-8",
    )


def write_sitemap() -> None:
    urls = []
    for page, meta in PAGES.items():
        loc = f"{SITE}/" if page == "index.html" else f"{SITE}/{page}"
        prio = meta["priority"]
        urls.append(
            f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{prio}</priority>
  </url>"""
        )
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n",
        encoding="utf-8",
    )


def noindex_mockups() -> None:
    mockups = ROOT / "mockups"
    if not mockups.exists():
        return
    for path in mockups.glob("*.html"):
        html = path.read_text(encoding="utf-8")
        if 'name="robots"' not in html:
            html = html.replace(
                '<meta name="viewport" content="width=device-width, initial-scale=1.0"/>',
                '<meta name="viewport" content="width=device-width, initial-scale=1.0"/>\n'
                '  <meta name="robots" content="noindex, nofollow"/>',
                1,
            )
            path.write_text(html, encoding="utf-8")
            print(f"noindex {path.relative_to(ROOT)}")


def main() -> None:
    write_robots()
    write_sitemap()
    noindex_mockups()
    print("wrote robots.txt + sitemap.xml")

    for page, meta in PAGES.items():
        path = ROOT / page
        if not path.exists():
            print(f"skip missing {page}")
            continue
        html = path.read_text(encoding="utf-8")
        html = replace_seo_head(html, page, meta)
        html = ensure_analytics_script(html)
        path.write_text(html, encoding="utf-8")
        print(f"seo+analytics {page}")


if __name__ == "__main__":
    main()
