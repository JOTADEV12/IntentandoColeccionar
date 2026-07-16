# Validación e inventario — Intentando Coleccionar

Fuente analizada: `Downloads/index (2).html` (monolito HTML/CSS/JS ~2430 líneas).

---

## A) Errores y hallazgos técnicos (HTML original)

### Estructura y arquitectura
- **Todo en un solo archivo**: CSS (~1300 líneas) y JS (~200 líneas) embebidos; dificulta mantenimiento y caché.
- **Landing de una sola página** con anclas (`#servicios`, `#escenas`, etc.), no sitio multipágina.
- **Dependencia CDN sin pin de versión**: `lucide@latest` puede romper iconos en actualizaciones.
- **Imágenes no embebidas ni presentes**: todas las rutas `img/*.jpg` están comentadas o usan placeholders CSS; el lightbox referencia `data-src` a archivos inexistentes en el archivo entregado.

### Semántica / HTML
- `role="navigation"` en `<nav>` es redundante (el navegador ya lo infiere).
- Lightbox: `<img id="lb-img" src="" alt=""/>` con `src` vacío (malo para validadores y accesibilidad hasta que se abre).
- Handlers `onclick="closeMnav()"` en atributos HTML (preferible listeners en JS).
- Year del footer: **© 2025** (desactualizado respecto a 2026).

### Accesibilidad
- Buenas prácticas presentes: `aria-label` en WhatsApp flotante, menú, lightbox; `aria-expanded` en hamburger; `aria-labelledby` en varias secciones.
- Contraste: cuerpo sobre `--void` con `--subtle` (#7a7a88) puede quedar **borde** en WCAG AA según tamaño.
- Overlay grain `body::after` con `z-index: 9999` no bloquea clics (`pointer-events: none`), OK; puede distraer.
- Stats del hero con emoji 🇨🇴 como “número” es decorativo más que informativo.

### SEO / performance
- Meta description y title correctos; **faltan Open Graph / Twitter cards**.
- Sin `loading="lazy"` efectivo porque no hay `<img>` reales cargadas.
- Animaciones CSS contínuas (grid, streaks, marquee) sin `prefers-reduced-motion` completo en el original.
- Sin sitemap / canonical / favicon en el archivo analizado.

### Contenido ambiguo (no inventado; señalar)
| Tema | Estado |
|------|--------|
| Precios | **No existen** en el HTML |
| Email / dirección física | **No existen** |
| Biografía / fundador / equipo | **No existen** |
| “100+ piezas entregadas” | Claim de marketing; **no verificable** desde el HTML |
| Insignia “Verificado” en testimonios | Presente en UI; **sin fuente de verificación** |
| Archivos `img/*.jpg` | Solo nombres referenciados; **archivos no incluidos** en el monolito |
| Testimonios | Textos incluidos en el original; autenticidad **no verificable** aquí |

---

## B) Inventario de contenido real extraído

### Marca
- **Nombre:** Intentando Coleccionar  
- **Eslogan:** “No es un producto, es una creación”  
- **Propuesta:** Miniaturas en resina 3D, réplicas de vehículo real, escenas cinematográficas personalizadas  
- **Origen / logística:** Hecho a mano en Colombia · Envíos a todo Colombia · Cotización gratuita / sin compromiso  

### Contacto y redes
- **WhatsApp:** +57 311 515 2006 → `https://wa.me/573115152006`  
  - Mensajes precargados: cotizar figura / cotizar escena personalizada  
- **TikTok:** https://www.tiktok.com/@intentandocoleccionar  
- **Instagram:** https://www.instagram.com/intentando_coleccionar/  

### Servicios / categorías (copy original)
1. **Carros en escala** — fidelidad, colecciones temáticas, escala a medida (`Disponible`)  
2. **Figuras personalizadas** — pose/ropa/accesorios, diseño desde cero (`Más solicitado`)  
3. **Escenas cinematográficas** — dioramas Hollywood; F&F, Batman; carro + figura + ambiente (`Exclusivo`)  
4. **Tu carro en miniatura** — réplica del vehículo real con fotos (`Premium`)  

### Escenas especiales (copy)
- Fast & Furious Collection — **diorama completo · 14 figuras + 6 carros**  
- Dioramas estilo Fast & Furious  
- Escenarios personalizados (neón, garajes, circuitos)  
- Recreación de momentos reales  

### Proceso (4 pasos)
1. Cuéntanos tu idea  
2. Evaluamos cada detalle (cotización transparente)  
3. Diseñamos & producimos (avances fotográficos)  
4. Entregamos (empaque premium, Colombia; llegan perfectas o se rehace)  

Cita de proceso: *“Cada proyecto es una creación irrepetible — no existe una segunda copia igual en ningún lugar del mundo.”*

### Piezas / referencias nombradas en galería y textos
| Pieza | Categoría en original |
|-------|------------------------|
| Fast & Furious · escena completa (14 figuras + 6 carros) | Escena |
| Vin Diesel · figura resina 3D | Figura |
| Toyota Supra naranja | Carro |
| Batman · diorama caja acrílica | Diorama |
| Nissan Skyline R34 azul | Escena |
| Son Goku Super Saiyan | Figura |
| Suki · diorama caja neon | Diorama |
| Dodge Charger rojo | Escena |
| Batman · figura + Batmóvil | Figura |
| Honda Civic naranja | Carro |
| Colección 14 figuras F&F | Figura / Colección |
| Batman · ciudad oscura Gotham | Diorama |
| Renault 4 (solo testimonio) | Réplica regalo |

### Archivos de imagen referenciados (nombres originales → nuevos WebP sugeridos)
- `ff-escena-grupo.jpg` → `ff-escena-grupo.webp`  
- `vin-diesel.jpg` → `vin-diesel.webp`  
- `supra-naranja.jpg` → `supra-naranja.webp`  
- `batman-box.jpg` → `batman-box.webp`  
- `skyline-azul.jpg` → `skyline-azul.webp`  
- `goku.jpg` → `goku.webp`  
- `suki-neon.jpg` → `suki-neon.webp`  
- `charger-rojo.jpg` → `charger-rojo.webp`  
- `batman-figura.jpg` → `batman-figura.webp`  
- `civic-naranja.jpg` → `civic-naranja.webp`  
- `coleccion-ff.jpg` → `coleccion-ff.webp`  
- `batman-ciudad.jpg` → `batman-ciudad.webp`  

### Testimonios (texto íntegro del original)
1. **Juan M. — Medellín** · Réplica Honda Civic  
2. **Sebastián R. — Bogotá** · Escena F&F 14 figuras + carros  
3. **Camila P. — Cali** · Diorama Batman ciudad oscura  
4. **Andrea F. — Barranquilla** · Réplica Renault 4  
5. **Diego T. — Pereira** · Nissan Skyline  
6. **Luis G. — Bucaramanga** · Figura personalizada · personaje original  

### Diferenciadores
Ideas hechas realidad · Resina 3D de precisión · Personalización sin límites · Una sola en el mundo · Envíos a todo Colombia · Nivel cinematográfico  

### Stats / claims del hero original
- 100+ piezas entregadas  
- ∞ diseños únicos posibles  
- 3D resina de alta precisión  
- Envíos nacionales  

---

## C) Qué se hizo en el rediseño (resumen)
- Sitio multipágina semántico (`index`, categorías, dioramas, carros, escenas, galería, nosotros, testimonios, contacto).  
- CSS/JS externos (`css/main.css`, `js/main.js`).  
- Copy y datos de contacto **solo** del inventario anterior.  
- Imágenes reales en `assets/trabajos/` (+ variantes HD).  

## D) Mejoras posteriores (julio 2026)
- Tipografía unificada (Anton / Work Sans / JetBrains Mono).  
- SEO: `canonical`, `og:image`, `twitter:image`, `sitemap.xml`, `robots.txt`, JSON-LD LocalBusiness.  
- Nosotros: historia de marca, rangos orientativos COP, plazos, FAQ.  
- Contacto: sin notas internas; checklist de cotización.  
- Badges “Verificado” retirados.  
- `srcset` HD donde hay par en `assets/trabajos/hd/`.  
- Shell compartido: `partials/shell.py` + `scripts/sync_shell.py`.  
- Deploy: `netlify.toml` + `DEPLOY.md`.  
- Assets sueltos de raíz → `assets/_inbox/`.  

