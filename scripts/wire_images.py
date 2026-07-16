from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    index = ROOT / "index.html"
    t = index.read_text(encoding="utf-8")
    t2 = re.sub(r"assets/trabajos/(escena-\d+)\.jpg", r"assets/trabajos/\1.webp", t)
    index.write_text(t2, encoding="utf-8")
    print("index escena jpg->webp")

    for name in ["categorias.html", "carros.html", "escenas.html", "dioramas.html", "galeria.html"]:
        fp = ROOT / name
        html = fp.read_text(encoding="utf-8")

        def add_data_img(match: re.Match[str]) -> str:
            block = match.group(0)
            if "data-img=" in block:
                return block
            found = re.search(r"([a-z0-9\-]+\.webp)", block, re.I)
            if not found:
                return block
            file = found.group(1).lower()
            return block.replace('class="img-ph"', f'class="img-ph" data-img="assets/img/{file}"', 1)

        html2 = re.sub(r'<div class="img-ph"[^>]*>.*?</div>', add_data_img, html, flags=re.S)
        fp.write_text(html2, encoding="utf-8")
        print(f"wired {name}")

    # Honest captions for key gallery items
    gal = ROOT / "galeria.html"
    g = gal.read_text(encoding="utf-8")
    replacements = {
        'data-cap="Vin Diesel · Figura resina 3D"': 'data-cap="Escena personalizada del taller"',
        'data-alt="Vin Diesel · Figura resina 3D"': 'data-alt="Escena personalizada del taller"',
        "Vin Diesel · Figura<span>": "Escena del taller<span>",
        "Vin Diesel · Figura resina 3D</div>": "Escena personalizada</div>",
        'data-cap="Son Goku Super Saiyan · Resina 3D"': 'data-cap="Majin Buu + Skyline · Escena personalizada"',
        'data-alt="Son Goku Super Saiyan"': 'data-alt="Majin Buu streetwear junto a Nissan Skyline"',
        "Goku · Super Saiyan<span>": "Majin Buu · Skyline<span>",
        "Son Goku Super Saiyan</div>": "Majin Buu + Skyline</div>",
        'data-cap="Batman · Diorama caja acrílica"': 'data-cap="Diorama / escena personalizada del taller"',
        'data-alt="Batman · Diorama caja acrílica"': 'data-alt="Diorama personalizado del taller"',
        "Batman · Diorama<span>": "Diorama personalizado<span>",
        "Batman · Diorama caja acrílica</div>": "Diorama del taller</div>",
        'data-cap="Batman · Figura + Batmóvil en escena"': 'data-cap="Figura y escena a escala"',
        'data-alt="Batman · Figura + Batmóvil"': 'data-alt="Figura personalizada en escena"',
        "Batman · Batmóvil<span>": "Figura en escena<span>",
        "Batman · Figura + Batmóvil</div>": "Figura personalizada</div>",
        'data-cap="Batman · Diorama ciudad oscura Gotham"': 'data-cap="Ambiente cinematográfico · referencia visual"',
        'data-alt="Batman · Ciudad oscura Gotham"': 'data-alt="Ambiente urbano cinematográfico"',
        "Batman · Ciudad oscura<span>": "Ambiente cinematográfico<span>",
        "Batman · Ciudad oscura Gotham</div>": "Referencia visual urbana</div>",
        'data-cap="Fast & Furious · Escena completa con 14 figuras y 6 carros"': 'data-cap="Escena personalizada estilo Rápido y Furioso"',
        'data-alt="Fast & Furious · Escena completa"': 'data-alt="Escena estilo Rápido y Furioso"',
        "14 figuras + 6 carros</div>": "Carro + figura a escala</div>",
        'data-cap="Colección completa · 14 figuras Fast & Furious"': 'data-cap="Colección / escena del taller"',
        'data-alt="Colección 14 figuras Fast & Furious"': 'data-alt="Colección y escena del taller"',
        "14 figuras Fast &amp; Furious</div>": "Trabajos del taller</div>",
        'data-cap="Toyota Supra naranja · Réplica en escala"': 'data-cap="Estilo deportivo · Cotiza tu réplica"',
        'data-alt="Toyota Supra naranja"': 'data-alt="Referencia visual deportiva"',
        "Toyota Supra naranja</div>": "Estilo deportivo · cotiza</div>",
        'data-cap="Honda Civic naranja · Réplica personalizada"': 'data-cap="Estilo street · Cotiza tu réplica"',
        'data-alt="Honda Civic naranja"': 'data-alt="Referencia visual street"',
        "Honda Civic naranja</div>": "Estilo street · cotiza</div>",
        'data-cap="Dodge Charger rojo · Escena de acción"': 'data-cap="Estilo muscle · Cotiza tu réplica"',
        'data-alt="Dodge Charger rojo"': 'data-alt="Referencia visual muscle car"',
        "Dodge Charger rojo</div>": "Estilo muscle · cotiza</div>",
        'data-cap="Nissan Skyline R34 azul · Escena nocturna"': 'data-cap="Skyline azul + figura · escena personalizada"',
        'data-alt="Nissan Skyline R34 azul"': 'data-alt="Nissan Skyline azul a escala con figura"',
        "Nissan Skyline R34 azul</div>": "Skyline + figura personalizada</div>",
        'data-cap="Suki · Diorama caja neon"': 'data-cap="Escena personalizada · estilo Suki / F&F"',
        'data-alt="Suki · Diorama caja neon"': 'data-alt="Escena personalizada carro rosa y figura"',
        "Suki · Diorama caja neon</div>": "Escena F&amp;F personalizada</div>",
    }
    for a, b in replacements.items():
        g = g.replace(a, b)
    gal.write_text(g, encoding="utf-8")
    print("galeria captions updated")


if __name__ == "__main__":
    main()
