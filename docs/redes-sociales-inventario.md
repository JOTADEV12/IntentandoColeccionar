# Inventario de redes sociales — Intentando Coleccionar

Fuente: el código del sitio (`index.html`, `contacto.html`, `js/site-config.js`, `js/experience.js`, `partials/shell.py`) y las URLs públicas enlazadas.

Fecha de revisión: 3 de septiembre de 2026.  
**Actualización en vivo:** 6 de septiembre de 2026 — ver `docs/validacion-contenido-redes.md`.

---

## Resumen

El sitio **no muestra publicaciones**. Solo enlaza a las cuentas y a WhatsApp. Hoy el visitante sale del sitio para ver el contenido.

Hay **cuatro canales** en la web:

| Canal | Tipo | ¿Hay feed de publicaciones? | Uso actual en el sitio |
|---|---|---|---|
| Instagram | Red social (fotos, Reels, carruseles) | No | Enlace + popup de bienvenida |
| TikTok | Red social (videos cortos) | No | Enlace + popup de bienvenida |
| Facebook | Página (posts, fotos, Reels) | No | Enlace + popup de bienvenida |
| WhatsApp | Chat de ventas | No aplica | Cotización (CTA principal) |

No hay YouTube, Threads, X/Twitter ni Pinterest en el sitio. Las meta tags `twitter:*` son Open Graph para previews al compartir, no una cuenta de Twitter.

---

## Cuentas confirmadas

### 1. Instagram

- **Handle:** `@intentando_coleccionar`
- **URL:** https://www.instagram.com/intentando_coleccionar/
- **Dónde aparece:** JSON-LD `sameAs`, footer de todas las páginas, fila “Encuéntranos en redes” del home, popup de bienvenida (`js/experience.js`), página Contacto.
- **Nota:** un script antiguo (`scripts/fix_instagram_url.py`) corrige un handle mal escrito (`@intentandocoleccionar` → `@intentando_coleccionar`). El sitio ya usa el handle con guion bajo.

### 2. TikTok

- **Handle:** `@intentandocoleccionar`
- **URL:** https://www.tiktok.com/@intentandocoleccionar
- **Dónde aparece:** mismos sitios que Instagram.
- **Comprobado el 3 sep 2026:** el oEmbed oficial de TikTok responde perfil público:

```json
{
  "author_name": "Intentando Coleccionar",
  "embed_type": "profile",
  "embed_product_id": "intentandocoleccionar"
}
```

Ese embed oficial puede mostrar hasta **10 videos recientes** del creador, sin descargar archivos.

### 3. Facebook

- **Página:** Intentando Coleccionar
- **URL:** https://www.facebook.com/intentando.coleccionar
- **Tipo de perfil visto en público:** Digital creator
- **Seguidores (público, sep 2026):** ~1.3K
- **Pestañas públicas:** Posts, About, Reels, Photos
- **Dónde aparece:** mismos sitios que Instagram (añadido con `scripts/add_facebook_social.py`).
- **Nota:** algunos posts recientes no se ven sin sesión (“This content isn't available”). Los Reels y fotos de la página sí existen. Para embeber hay que usar **URLs de posts/Reels públicos**, no el feed privado.

### 4. WhatsApp (canal de venta, no de publicaciones)

- **Número:** +57 311 515 2006
- **URL base:** https://wa.me/573115152006
- **Config central:** `js/site-config.js` → `WA: "573115152006"`
- **Dónde aparece:** CTA del nav, botón flotante, formulario de contacto (abre WhatsApp con el mensaje), JSON-LD `contactPoint`, analítica `whatsapp_click`.
- **No es un feed.** No hay “publicaciones” que traer. Sigue siendo el canal para cotizar.

---

## Dónde están en la interfaz

1. **Home — sección “Encuéntranos en redes”** (`index.html`): cuatro tarjetas (Facebook, TikTok, Instagram, WhatsApp). Solo enlaces.
2. **Popup de bienvenida** (`js/experience.js`): “Mira los últimos trabajos” — también solo enlaces. El copy promete piezas y procesos, pero no los muestra.
3. **Contacto:** listado de canales con handles.
4. **Footer** de todas las páginas (fuente: `partials/shell.py`).
5. **SEO:** `sameAs` en JSON-LD de cada HTML.

---

## Conclusión del inventario

Sí hay redes activas y enlazadas de forma consistente. Lo que **falta** es una sección que **reproduzca** el contenido (Reels / TikToks / posts) dentro del propio sitio, en lugar de mandar al visitante a otra app.
