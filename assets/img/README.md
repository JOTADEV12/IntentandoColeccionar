# Imágenes — Intentando Coleccionar

Assets listos en **Full HD WebP** (lado largo ≥ 1920 px cuando la fuente lo permite).

## Taller (preferidas)

| Archivo | Origen | Notas |
|---------|--------|-------|
| `atos-taxi.webp` | Taller | Réplica Atos taxi Bogotá |
| `clio.webp` / `twingo.webp` / `sprint.webp` / `swift.webp` | Taller | Carros a escala |
| `skyline-azul.webp` / `majin-buu.webp` / `goku.webp` | Taller | Skyline + Majin Buu |
| `ff-escena-grupo.webp` / `suki-neon.webp` / `coleccion-ff.webp` | Taller | Escenas estilo F&F |
| `batman-box.webp` / `batman-figura.webp` / `vin-diesel.webp` | Taller | Escenas/dioramas (nombres legacy de ruta) |
| `hero-tag-brick.webp` | Logo tag | Fondo hero Full HD |
| `hero-coleccion-cinematica.webp` | Taller | Cinemática horizontal |

También: `assets/trabajos/*.webp` y `assets/trabajos/hd/`.

## Complementos web (Unsplash)

Referencias de atmósfera / estilo para cotizar. Ver `*.ATTRIBUTION.txt`:

- `supra-naranja.webp`
- `civic-naranja.webp`
- `charger-rojo.webp`
- `batman-ciudad.webp`

## Regenerar

```bash
python scripts/enhance_images.py
python scripts/fetch_web_fills.py
python scripts/wire_images.py
```
