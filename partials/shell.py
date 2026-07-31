# Shell compartido (header / footer)
# Fuente de verdad para sincronizar navegación entre páginas HTML.
# Uso: python scripts/sync_shell.py

HEADER_SOLID = '''  <header class="site-header site-header--solid" data-header>
    <div class="nav-inner" data-nav>
      <a href="index.html" class="brand" aria-label="Intentando Coleccionar — Inicio">
        <span class="brand__lockup">
          <span class="brand__name">Intentando</span>
          <span class="brand__tag">Coleccionar</span>
        </span>
      </a>
      <nav class="nav-desktop" aria-label="Navegación principal">
        <a href="index.html">Inicio</a>
        <a href="categorias.html">Categorías</a>
        <a href="galeria.html">Galería</a>
        <a href="sobre-nosotros.html">Nosotros</a>
        <a href="testimonios.html">Clientes</a>
        <a href="contacto.html">Contacto</a>
        <a class="nav-cta" href="https://wa.me/573115152006?text=Hola%2C%20quiero%20cotizar%20una%20figura%20personalizada" target="_blank" rel="noopener noreferrer">Cotizar ahora</a>
      </nav>
      <button class="nav-toggle" type="button" data-nav-toggle aria-controls="nav-mobile" aria-expanded="false" aria-label="Abrir menú"><span></span><span></span><span></span></button>
    </div>
  </header>
  <div class="nav-mobile" id="nav-mobile" data-nav-mobile data-nav role="dialog" aria-modal="true" aria-label="Menú de navegación">
    <a href="index.html">Inicio</a>
    <a href="categorias.html">Categorías</a>
    <a href="galeria.html">Galería</a>
    <a href="sobre-nosotros.html">Nosotros</a>
    <a href="testimonios.html">Clientes</a>
    <a href="contacto.html">Contacto</a>
    <div class="nav-mobile__quick">
      <a href="carros.html">Carros a escala</a>
      <a href="escenas.html">Rápido y Furioso</a>
      <a href="dioramas.html">Dioramas</a>
    </div>
    <a class="nav-cta-mobile" href="https://wa.me/573115152006?text=Hola%2C%20quiero%20cotizar%20una%20figura%20personalizada" target="_blank" rel="noopener noreferrer">Cotizar mi pieza ↗</a>
  </div>'''

FOOTER = '''  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <img class="footer-brand-logo" src="assets/img/logo-lettering-only.png" alt="" width="220" height="120" decoding="async"/>
          <div class="footer-brand">Intentando<span>&nbsp;Coleccionar</span></div>
          <p>Réplicas a escala personalizadas y carros 1/43 metalizados. Hecho a mano en Colombia.</p>
        </div>
        <div class="footer-col">
          <h4>Explorar</h4>
          <a href="categorias.html">Categorías</a>
          <a href="galeria.html">Galería</a>
          <a href="sobre-nosotros.html">Sobre nosotros</a>
          <a href="testimonios.html">Clientes</a>
          <a href="sobre-nosotros.html#faq">FAQ</a>
          <a href="sobre-nosotros.html#cotizar">Cotizar</a>
        </div>
        <div class="footer-col">
          <h4>Contacto</h4>
          <a href="contacto.html">Formulario</a>
          <a href="https://wa.me/573115152006" target="_blank" rel="noopener noreferrer">WhatsApp</a>
          <a href="https://www.facebook.com/intentando.coleccionar" target="_blank" rel="noopener noreferrer">Facebook</a>
          <a href="https://www.instagram.com/intentando_coleccionar/" target="_blank" rel="noopener noreferrer">Instagram</a>
          <a href="https://www.tiktok.com/@intentandocoleccionar" target="_blank" rel="noopener noreferrer">TikTok</a>
        </div>
      </div>
      <div class="footer-bottom">
        <p>© 2026 Intentando Coleccionar · Hecho en Colombia</p>
        <p>No es un producto, es una creación</p>
      </div>
    </div>
  </footer>'''
