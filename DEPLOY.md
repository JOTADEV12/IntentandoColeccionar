# Deploy en Vercel — Intentando Coleccionar

Sitio estático listo para Vercel.

**Repo:** https://github.com/JOTADEV12/IntentandoColeccionar

Dominio canónico en código: **https://www.intentandocoleccionar.autos**  
Si cambias de dominio en Vercel, actualiza `SITE_ORIGIN` (sección 5).

---

## 1. Importar en Vercel

1. [vercel.com/new](https://vercel.com/new) → inicia sesión con GitHub.
2. Importa **IntentandoColeccionar**.
3. Framework: **Other** · Build Command: *(vacío)* · Output: *(vacío)*.
4. Deploy.

## 2. Comprar y conectar el dominio (.com o .xyz)

1. Proyecto → **Settings** → **Domains**.
2. **Buy** → busca tu dominio (ej. `intentandocoleccionar.com`).
3. Completa la compra. Vercel enlaza DNS al proyecto.
4. Añade también `www.` y redirige a la raíz (Vercel lo ofrece al agregar el dominio).

Si el dominio nuevo es distinto al de `SITE_ORIGIN`, sigue la **sección 5** antes del siguiente deploy.

## 3. Analítica de visitas (cómo verlas)

El sitio ya envía visitas con `js/analytics.js`. **Tú las visualizas en el panel de Vercel**, no en una página pública del sitio.

### A) Activar (una sola vez)

1. En Vercel → tu proyecto → **Analytics**.
2. Pulsa **Enable** en **Web Analytics**.
3. (Opcional) En **Speed Insights** → **Enable** (velocidad de carga).
4. Haz un **Redeploy** (Deployments → ⋮ → Redeploy).  
   Eso crea las rutas `/_vercel/insights/*` y `/_vercel/speed-insights/*`.

### B) Ver los datos

1. Abre el proyecto en Vercel → **Analytics**.
2. Verás:
   - Visitantes y pageviews
   - Páginas más visitadas
   - Países / dispositivos
   - Referrers (de dónde llegan)
3. Comprueba que funciona: abre tu sitio en producción → DevTools → Network → busca `/_vercel/insights/view`.

Los clics a WhatsApp se registran como evento `whatsapp_click` (útil cuando tengas plan Pro o uses GA4).

### C) Google Analytics 4 (opcional, panel aparte)

1. [analytics.google.com](https://analytics.google.com) → Admin → **Crear propiedad**.
2. Flujo Web con la URL de tu dominio (`.com` o `.xyz`).
3. Copia el ID (`G-XXXXXXXXXX`) en `js/site-config.js`:

```js
GA_MEASUREMENT_ID: "G-XXXXXXXXXX",
```

4. Commit + push → Vercel redeploya.

### D) Google Search Console

1. [search.google.com/search-console](https://search.google.com/search-console) → Añadir propiedad.
2. Verifica (DNS en Vercel o meta tag).
3. Sitemap: `https://TU-DOMINIO/sitemap.xml`.

## 4. Verificar tras el deploy

- `https://TU-DOMINIO/`
- `https://TU-DOMINIO/sitemap.xml`
- `https://TU-DOMINIO/robots.txt`
- Vercel → **Analytics** (tras unas visitas reales)

## 5. Si cambias de dominio (p. ej. a .com)

Edita `SITE_ORIGIN` en:

- `js/site-config.js`
- `scripts/apply_seo_analytics.py`
- `scripts/apply_site_upgrades.py`

Luego:

```bash
python scripts/set_domain.py
python scripts/apply_seo_analytics.py
```

Actualiza también el redirect `www` en `vercel.json` al dominio nuevo.

Commit + push → Vercel redeploya.

## Mantenimiento

- Nav/footer: `python scripts/sync_shell.py`
- SEO + keywords + analytics scripts: `python scripts/apply_seo_analytics.py`
- Upgrades legacy (tipografía/srcset): `python scripts/apply_site_upgrades.py` (después vuelve a correr `apply_seo_analytics.py`)
