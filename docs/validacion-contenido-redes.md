# Validación de contenido en redes — 6 de septiembre de 2026

Objetivo: identificar qué redes están escritas en el sitio, qué publicaciones públicas existen hoy, y qué se puede llevar al home sin scrapear ni descargar videos.

Fuentes de esta pasada:

- Código del sitio (HTML, `js/site-config.js`, `js/experience.js`, footer)
- Dominio de producción `https://www.intentandocoleccionar.autos/`
- Perfiles públicos: TikTok, Instagram y Facebook
- oEmbed oficial de TikTok e Instagram (sin token)

---

## 1. Estado del sitio web

### Producción

El dominio canónico **está pausado** en Vercel (`live: false`). Al abrir `www.intentandocoleccionar.autos` aparece:

> This deployment is temporarily paused

El último deploy de producción listo es `dpl_Cp13S8J3Wk5epS2dykdqC6Bj7uWs`. El contenido de redes se validó contra el código local y contra las cuentas públicas, no contra la web en vivo.

### Qué muestra el sitio hoy (código local)

El visitante **no ve publicaciones**. Solo ve enlaces que lo sacan a otra app.

| Superficie | Archivo | Qué hay |
|---|---|---|
| Home — “Encuéntranos en redes” | `index.html` | 4 tarjetas: Facebook, TikTok, Instagram, WhatsApp |
| Popup “Mira los últimos trabajos” | `js/experience.js` | Mismos 4 enlaces. El copy promete piezas y procesos, pero no los reproduce |
| FAB “Redes · Trabajos” | `js/experience.js` | Reabre el popup |
| Contacto | `contacto.html` | Listado de handles + CTA WhatsApp |
| Footer (todas las páginas) | HTML + `partials/shell.py` | WhatsApp, Facebook, Instagram, TikTok |
| SEO `sameAs` | JSON-LD de cada HTML | Las 3 redes + `wa.me` |

No hay YouTube, Threads, X/Twitter ni Pinterest. Las meta tags `twitter:*` son Open Graph para previews al compartir.

Hallazgo de layout: `.social-row` está en **3 columnas** y hay **4 tarjetas**, así que WhatsApp queda solo en la segunda fila.

---

## 2. Cuentas escritas en la página (sin cambios de handle)

| Canal | Handle / página | URL | Rol en el sitio |
|---|---|---|---|
| TikTok | `@intentandocoleccionar` | https://www.tiktok.com/@intentandocoleccionar | Enlace |
| Instagram | `@intentando_coleccionar` | https://www.instagram.com/intentando_coleccionar/ | Enlace |
| Facebook | `intentando.coleccionar` | https://www.facebook.com/intentando.coleccionar | Enlace |
| WhatsApp | +57 311 515 2006 | https://wa.me/573115152006 | Cotización (no es feed) |

Handles consistentes en home, contacto, footer, popup y JSON-LD.

---

## 3. Lo hallado en las cuentas públicas (6 sep 2026)

### TikTok — canal más fuerte y embebible ya

Perfil público confirmado por oEmbed (`embed_type: profile`).

| Dato | Valor visto |
|---|---|
| Nombre | Intentando Coleccionar |
| Handle | `@intentandocoleccionar` |
| Seguidores | 3.072 |
| Likes | 23,2K |
| Bio | apunta a Instagram `@intentando_coleccionar` |
| oEmbed perfil | Sí |
| oEmbed video suelto | Sí (probado en 6 URLs) |

Videos visibles en el perfil (recortes de vistas; 3 pines):

| Orden | Vistas | Estado | URL |
|---|---|---|---|
| 1 | 1.654 | Pinned | https://www.tiktok.com/@intentandocoleccionar/video/7657019753432681749 |
| 2 | 9.162 | Pinned | https://www.tiktok.com/@intentandocoleccionar/video/7657385840028552468 |
| 3 | 19K | Pinned | https://www.tiktok.com/@intentandocoleccionar/video/7659996575640390932 |
| 4 | 415 | — | https://www.tiktok.com/@intentandocoleccionar/video/7680435047907757330 |
| 5 | 32,5K | — | https://www.tiktok.com/@intentandocoleccionar/video/7680001573728128277 |
| 6 | 8.232 | — | https://www.tiktok.com/@intentandocoleccionar/video/7679279669383843093 |
| 7 | 32,8K | — | https://www.tiktok.com/@intentandocoleccionar/video/7675563664593784084 |
| 8 | 1.489 | — | https://www.tiktok.com/@intentandocoleccionar/video/7675032698162842901 |
| 9 | 1.628 | — | https://www.tiktok.com/@intentandocoleccionar/video/7674835597973867797 |
| 10 | 2.326 | — | https://www.tiktok.com/@intentandocoleccionar/video/7674089397746158868 |
| 11 | 1.154 | — | https://www.tiktok.com/@intentandocoleccionar/video/7674086359929228564 |
| 12 | 7.101 | — | https://www.tiktok.com/@intentandocoleccionar/video/7673688388829973781 |
| 13 | 11K | — | https://www.tiktok.com/@intentandocoleccionar/video/7672964675440577813 |
| 14 | 2.398 | — | https://www.tiktok.com/@intentandocoleccionar/video/7672569012873645333 |
| 15 | 2.893 | — | https://www.tiktok.com/@intentandocoleccionar/video/7671853891641789716 |
| 16 | 16K | — | https://www.tiktok.com/@intentandocoleccionar/video/7671502746708725012 |
| 17 | 1.111 | — | https://www.tiktok.com/@intentandocoleccionar/video/7670965121312656660 |
| 18 | 1.300 | — | https://www.tiktok.com/@intentandocoleccionar/video/7670598198578122004 |
| 19 | 19,5K | — | https://www.tiktok.com/@intentandocoleccionar/video/7667413466105269525 |

Títulos oficiales vía oEmbed (sin hashtags de relleno):

| Pieza | Título |
|---|---|
| Pinned 1.654 | Herbie a toda marcha escala 1/64 Custom |
| Pinned 9.162 | Renault Twingo a escala 1/43 |
| Pinned 19K | Chevrolet Sprint escala 1/43 |
| 32,8K | Chevrolet Swift escala 1/43 · más queridos de Colombia |
| 32,5K | Aveo escala 1/43 · más queridos de Colombia |
| 19,5K | Renault 4 escala 1/43 personalizado |

Temática alineada con el sitio: réplicas 1/43, tuning, Hot Wheels custom, “más queridos de Colombia”.

### Instagram — público, embeds oficiales OK

| Dato | Valor visto |
|---|---|
| Handle | `@intentando_coleccionar` |
| Nombre | Intentando Coleccionar |
| Seguidores | 202 |
| Siguiendo | 185 |
| Bio | Amante de los autos a escala / Modificaciones / Fotos y videos |
| Pestañas | Posts, Reels, Tagged |
| oEmbed (sin token) | Sí — `graph.facebook.com/v25.0/instagram_oembed` |

Reels públicos hallados:

- https://www.instagram.com/reel/Daeh-1ONUfp/
- https://www.instagram.com/reel/DaQOft3gV6s/
- https://www.instagram.com/reel/DZG1ZhyxvZ3/
- https://www.instagram.com/reel/DWxZi29Cajx/
- https://www.instagram.com/reel/DWAaBsIgG_Q/
- https://www.instagram.com/reel/DVP0l6UjL8A/
- https://www.instagram.com/reel/DGTmveXJjws/
- https://www.instagram.com/reel/DGPcjOZOTyZ/
- https://www.instagram.com/reel/DGMyX9fuI--/
- https://www.instagram.com/reel/DAXMPk3Bcee/
- https://www.instagram.com/reel/C_EO2mfq_t7/

Carrusel:

- https://www.instagram.com/p/C_EA_wpOu2M/

En el grid se ven piezas del taller (Twingo en stand, Clio negro, auto real a replicar) y algunos Reels con watermark de TikTok `@intentandocoleccionar` (el mismo contenido cruza redes).

### Facebook — página activa, posts no embebibbles desde público

| Dato | Valor visto |
|---|---|
| Página | Intentando Coleccionar |
| Tipo | Digital creator |
| Seguidores | ~1,3K |
| Siguiendo | 144 |
| Pestañas | Posts, About, Reels, Photos |
| Fotos públicas | Miniaturas (Hot Wheels / 1/43) visibles en la tira |

El post visible “August 11 at 6:24 AM” (`pfbid0HYoizS4JkT4DRUhxwqRqGuCMffMHBPufxiuiT66eKPo8KhajA9683iAtBy6MKBF4l`) muestra:

> This content isn't available right now

**No se incluye en el JSON de embeds.** Facebook se deja como enlace de seguimiento.

### WhatsApp

Sigue siendo el único canal de venta. No hay publicaciones que traer.

---

## 4. Brecha producto

| Promesa actual | Realidad | Cambio a implementar |
|---|---|---|
| “Mira el proceso en tiempo real” (home) | Solo enlaces | Sección con players oficiales |
| “Mira los últimos trabajos” (popup) | Solo enlaces | El home ya muestra los videos; el popup puede apuntar a `#del-taller` |
| Galería | Solo fotos | Bloque corto “Proceso en video” |

Vía correcta (ya definida en `docs/contenido-social-viabilidad.md`): **embed oficial**. No descargar desde las apps.

---

## 5. Curaduría para Fase 1 (6 piezas)

Máximo 6 embeds en el home. Mezcla TikTok (volumen + oEmbed de video) + Instagram (Reels recientes, oEmbed OK). Sin Facebook.

| # | Plataforma | Título en sitio | URL | Por qué |
|---|---|---|---|---|
| 1 | TikTok | Chevrolet Sprint 1/43 | …/video/7659996575640390932 | Pinned, 19K |
| 2 | TikTok | Chevrolet Swift 1/43 | …/video/7675563664593784084 | 32,8K, más visto |
| 3 | TikTok | Aveo 1/43 | …/video/7680001573728128277 | 32,5K |
| 4 | Instagram | Reel del taller | https://www.instagram.com/reel/DZG1ZhyxvZ3/ | Tercer Reel público; el 4.º TikTok no hidrató el iframe en local |
| 5 | Instagram | Reel reciente | https://www.instagram.com/reel/Daeh-1ONUfp/ | Último del grid, oEmbed OK |
| 6 | Instagram | Trabajo terminado | https://www.instagram.com/reel/DaQOft3gV6s/ | Caption visible “Trabajo Terminado…” |

TikToks pinned que quedan fuera del grid (siguen en el perfil): Herbie 1/64, Twingo 1/43 y Renault 4. En local, TikTok `embed.js` hidrató de forma estable **tres** players; el cuarto se deja como Reel de Instagram para no mostrar un hueco. Se pueden rotar después editando `data/social-embeds.json`.

---

## 6. Implementación que arranca a partir de este hallazgo

1. `data/social-embeds.json` con las 6 URLs de arriba.
2. `js/social-feed.js` + `css/social-feed.css`: blockquotes oficiales, lazy-load, fallback con enlace.
3. Nueva sección en `index.html` entre Trabajos y “Encuéntranos en redes”.
4. Unificar handles en `js/site-config.js`.
5. CTA WhatsApp debajo del grid.
6. Galería: bloque compacto opcional.
7. No autoplay con sonido. Respetar `prefers-reduced-motion`.
8. Producción pausada: el código se verifica en local; el deploy a `www` requiere despausar el proyecto Vercel.

Fuera de este sprint: Graph/Display API, MP4 propios, widgets de pago, scrapers.
