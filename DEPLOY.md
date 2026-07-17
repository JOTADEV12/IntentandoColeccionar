# Deploy en Vercel + dominio

Este sitio es **estático** (HTML/CSS/JS). Se publica en [Vercel](https://vercel.com) y el dominio se compra allí mismo.

## 1. Repo en GitHub (ya listo si hiciste push)

Proyecto: conectar el repositorio `RepoColeccionar` (o el nombre que uses) a Vercel.

## 2. Importar en Vercel

1. Entra a [vercel.com/new](https://vercel.com/new) e inicia sesión (GitHub).
2. **Import** el repo.
3. Framework Preset: **Other** (o déjalo vacío).
4. Build Command: *(vacío)*.
5. Output Directory: *(vacío / `.`)*.
6. Deploy.

Quedarás con una URL temporal tipo:
`https://repo-coleccionar.vercel.app`

## 3. Comprar dominio en Vercel (económico)

1. Proyecto → **Settings** → **Domains**.
2. **Buy** / buscar dominio.
3. Opciones usualmente más baratas (elige la que esté libre y te guste):
   - `intentandocoleccionar.co`
   - `intentandocoleccionar.com`
   - `icoleccionar.com`
   - `intentando.co`
4. Completa la compra con tu cuenta Vercel.
5. Vercel asigna DNS automáticamente al proyecto.

## 4. Actualizar SEO al dominio real

Cuando ya tengas el dominio comprado, actualiza `SITE_ORIGIN` en:

- `js/site-config.js`
- `scripts/apply_site_upgrades.py`

Luego corre:

```bash
python scripts/apply_site_upgrades.py
```

Haz commit + push; Vercel redeploya solo.

## 5. Mantenimiento local

- Unificar nav/footer: `python scripts/sync_shell.py`
- Reaplicar SEO: `python scripts/apply_site_upgrades.py`

## Nota

`netlify.toml` quedó por compatibilidad; el flujo oficial de este proyecto es **Vercel**.
