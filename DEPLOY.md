# Deploy en Vercel — intentandocoleccionar.xyz

Sitio estático listo para Vercel. Dominio configurado en código: **https://intentandocoleccionar.xyz**

**Repo:** https://github.com/JOTADEV12/IntentandoColeccionar

---

## 1. Importar en Vercel

1. [vercel.com/new](https://vercel.com/new) → inicia sesión con GitHub.
2. Importa **IntentandoColeccionar**.
3. Framework: **Other** · Build Command: *(vacío)* · Output: *(vacío)*.
4. Deploy.

## 2. Comprar y conectar el dominio

1. Proyecto → **Settings** → **Domains**.
2. **Buy** → busca: `intentandocoleccionar.xyz`
3. Completa la compra. Vercel enlaza DNS al proyecto.
4. Opcional: añade `www.intentandocoleccionar.xyz` y redirige a la raíz (Vercel lo ofrece al agregar el dominio).

No hace falta cambiar código: canonical, Open Graph, sitemap y JSON-LD ya apuntan a `.xyz`.

## 3. Verificar tras el deploy

- https://intentandocoleccionar.xyz/
- https://intentandocoleccionar.xyz/sitemap.xml
- https://intentandocoleccionar.xyz/robots.txt
- Compartir enlace (preview OG con imagen del hero)

## 4. Si cambias de dominio en el futuro

Edita `SITE_ORIGIN` en:

- `js/site-config.js`
- `scripts/apply_site_upgrades.py`

Luego:

```bash
python scripts/set_domain.py
python scripts/apply_site_upgrades.py
```

Commit + push → Vercel redeploya.

## Mantenimiento

- Nav/footer: `python scripts/sync_shell.py`
- SEO global: `python scripts/apply_site_upgrades.py`
