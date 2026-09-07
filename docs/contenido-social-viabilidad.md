# Viabilidad: traer publicaciones de las redes al sitio

Pregunta: ¿podemos actualizar la web con las publicaciones que ya tienen en Instagram, TikTok y Facebook, ya sea embebiendo desde la web o descargando y adaptando?

**Respuesta corta:** sí, se puede. La vía correcta es **embeber con los reproductores oficiales**. **No** scrapear ni descargar videos desde esas apps.

---

## Decisión recomendada

| Vía | ¿La usamos? | Por qué |
|---|---|---|
| A. Embed oficial (el video se ve en nuestra página, pero se reproduce desde TikTok/Instagram/Facebook) | **Sí — principal** | Legal, se actualiza, no pesa el hosting, atribuye a la cuenta |
| B. Archivos originales que el taller ya tiene en el celular/PC (no bajados de la red) | **Sí — complemento** | El dueño es el autor; podemos convertir a MP4/WebP y hospedarlos |
| C. Descargar / scrapear videos desde Instagram, TikTok o Facebook | **No** | Viola los términos de esas plataformas y es frágil |

Este sitio es estático en Vercel (HTML/CSS/JS, sin backend). Encaja mejor con embeds + una lista curada de URLs que con APIs complejas.

---

## Por red

### TikTok — la más fácil y ya comprobada

- **Embed de perfil:** oficial. TikTok confirma el perfil `@intentandocoleccionar` y entrega HTML de embed tipo `creator`. Ese widget muestra hasta **10 videos recientes**.
- **Embed de video suelto:** también oficial (`https://www.tiktok.com/oembed?url=...`). Sirve para destacar 3–6 piezas concretas.
- **Descargar desde TikTok:** no.
- **API Display (login OAuth):** posible más adelante si quieren un feed automático sin pegar URLs. Requiere cuenta Business y tokens. No hace falta para la primera versión.

**Veredicto TikTok:** sí, ahora. Prioridad 1.

### Instagram — sí, con URLs de posts públicos

- **oEmbed oficial (desde jun 2026, sin token):** `GET https://graph.facebook.com/v25.0/instagram_oembed?url={url-del-post}`
- Soporta foto, carrusel, video y Reel. **No** soporta Stories.
- La cuenta debe ser **pública** y tener **Embeds activado** en Instagram.
- Un embed de *perfil* no trae el grid completo de forma fiable; hay que pegar URLs de Reels/posts (`/reel/...` o `/p/...`).
- **Descargar desde Instagram:** no.

**Veredicto Instagram:** sí, si nos pasan 4–8 URLs de Reels/posts públicos. Prioridad 2.

### Facebook — sí, con posts/Reels públicos

- La página existe (~1.3K followers, pestaña Reels y Photos).
- oEmbed oficial de post y de video (también tokenless desde jun 2026).
- Algunos posts no se ven sin iniciar sesión: esos **no** se pueden embeber. Solo URLs públicas.
- Page Plugin de Facebook es otra opción (muestra el muro), más pesado y menos control de diseño.

**Veredicto Facebook:** sí, curando Reels/posts públicos. Prioridad 3 (refuerzo, no el centro).

### WhatsApp — no hay publicaciones

WhatsApp no tiene feed. Se deja como CTA de cotización junto a la nueva sección de videos.

---

## Embed vs descargar (detalle)

### Embed (vía web)

Cómo se ve para el visitante: el video **está en nuestra página**, con el player de TikTok/Instagram/Facebook, créditos y enlace a la cuenta.

Pros:

- No copiamos el archivo.
- Si suben un video nuevo y usamos el embed de perfil de TikTok, puede aparecer solo.
- No inflamos el repo (los videos 9:16 pesan mucho).
- Cumple términos de las plataformas.

Contras:

- Depende de que la red esté en pie y el post siga público.
- El look del player es el de la red (no 100% “marca propia”).
- Algunos visitantes con bloqueadores pueden no ver el embed.

### Hospedar archivos propios (adaptar a la página)

Válido **solo** si el taller entrega el archivo original (lo que grabaron en el celular), no un MP4 bajado de TikTok/IG.

Pros:

- Control total de diseño, autoplay silencioso, poster WebP, lazy-load.
- No depende de Instagram/TikTok en el momento de la visita.
- Encaja con la galería actual (`assets/trabajos/`).

Contras:

- Hay que comprimir (1080×1920, H.264, ~8–20 MB por clip).
- Cada pieza nueva implica commit + deploy.
- Hay que respetar música con copyright: si el TikTok usa audio de la app, **no** reusar ese audio en el archivo hospedado.

---

## Qué no vamos a hacer

- Scripts tipo yt-dlp / scrapers contra Instagram, TikTok o Facebook.
- Hotlink de CDN internos de Meta/TikTok (URLs firmadas que caducan).
- Widgets de terceros de pago (Elfsight, SnapWidget, etc.) salvo que el cliente los pida después.
- Traer Stories (caducan y no hay embed oficial estable).

---

## Encaje con este repo

- Sitio estático → un JSON de URLs + un JS que pinta blockquotes oficiales es suficiente.
- Ya hay sección de redes en el home y popup “Mira los últimos trabajos”: el contenido nuevo **sustituye la promesa vacía** con videos reales.
- La galería hoy es solo fotos (`galeria.html`). Se puede añadir una pestaña o bloque “Proceso en video”.
- Vercel Hobby aguanta bien embeds (son iframes de terceros). Los MP4 propios sí hay que limitar cantidad.

---

## Recomendación de producto

**Fase 1 (implementar):** bloque “Del taller a tu vitrina” en el home:

1. Embed de perfil TikTok (feed vivo, hasta 10).
2. 4–6 Reels/posts de Instagram y/o Facebook elegidos a mano (URLs en un JSON).
3. WhatsApp al lado, para cotizar lo que acaban de ver.

**Fase 1b (opcional, mismo sprint si hay archivos):** 2–3 videos cortos propios en `assets/video/` (proceso de pintura, unboxing, detalle 1/43), sin música de TikTok.

**Fase 2 (después):** si quieren que el sitio se actualice solo cada vez que publican, conectar Instagram Graph / TikTok Display API con cuenta Business. Eso ya no es un sitio 100% estático.

---

## Lo que necesitamos del taller para arrancar

1. Confirmar que Instagram es **público** y Embeds está **activado**.
2. Pegar 6–10 URLs de las mejores piezas (Reels IG, videos TikTok, Reels FB).
3. Si hay videos originales en el celular: enviarlos por Drive/WhatsApp (sin bajarlos de la app).
4. Decidir si el bloque nuevo va solo en Inicio o también en Galería.
