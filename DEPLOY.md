# Intentando Coleccionar — sitio estático

## Publicar (Netlify — recomendado)

1. Crea una cuenta en [Netlify](https://www.netlify.com/).
2. Arrastra esta carpeta a **Deploy**, o conecta el repo de GitHub.
3. El archivo `netlify.toml` ya define `publish = "."`.
4. Asigna tu dominio y actualiza `SITE_ORIGIN` en:
   - `js/site-config.js`
   - `scripts/apply_site_upgrades.py` (`SITE_ORIGIN`)
   - Vuelve a correr: `python scripts/apply_site_upgrades.py`

## Publicar (GitHub Pages)

1. Sube el repo a GitHub.
2. Settings → Pages → Source: Deploy from branch `master` / root.
3. Actualiza el dominio canónico como arriba.

## Mantenimiento

- Unificar nav/footer: `python scripts/sync_shell.py`
- Reaplicar SEO/tipografía/srcset: `python scripts/apply_site_upgrades.py`
