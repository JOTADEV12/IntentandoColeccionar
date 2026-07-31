(() => {
  "use strict";

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const IC = (window.IC = window.IC || {});

  /* ---------- Toast ---------- */
  const ensureToastHost = () => {
    let host = document.querySelector(".ic-toast-host");
    if (host) return host;
    host = document.createElement("div");
    host.className = "ic-toast-host";
    host.setAttribute("aria-live", "polite");
    host.setAttribute("aria-relevant", "additions");
    document.body.appendChild(host);
    return host;
  };

  IC.toast = (title, body = "", { duration = 3800 } = {}) => {
    const host = ensureToastHost();
    const el = document.createElement("div");
    el.className = "ic-toast";
    el.setAttribute("role", "status");
    el.innerHTML = `
      <span class="ic-toast__mark" aria-hidden="true">◆</span>
      <div>
        <p class="ic-toast__title"></p>
        <p class="ic-toast__body"></p>
      </div>
      <button type="button" class="ic-toast__close" aria-label="Cerrar">×</button>
    `;
    el.querySelector(".ic-toast__title").textContent = title;
    el.querySelector(".ic-toast__body").textContent = body;
    const close = () => {
      el.classList.remove("is-in");
      el.classList.add("is-out");
      window.setTimeout(() => el.remove(), reduceMotion ? 40 : 280);
    };
    el.querySelector(".ic-toast__close").addEventListener("click", close);
    host.appendChild(el);
    requestAnimationFrame(() => el.classList.add("is-in"));
    if (duration > 0) window.setTimeout(close, duration);
    return el;
  };

  /* ---------- Preloader ---------- */
  const PRELOADER_KEY = "ic_vitrina_seen";

  const mountPreloader = () => {
    if (document.getElementById("ic-preloader")) return document.getElementById("ic-preloader");
    const root = document.createElement("div");
    root.id = "ic-preloader";
    root.className = "ic-preloader";
    root.setAttribute("role", "status");
    root.setAttribute("aria-live", "polite");
    root.setAttribute("aria-label", "Abriendo la vitrina");
    root.innerHTML = `
      <div class="ic-preloader__stage">
        <div class="ic-preloader__case" aria-hidden="true" data-ic-case>
          <div class="ic-preloader__spotlight"></div>
          <div class="ic-preloader__shelf"></div>
          <div class="ic-preloader__shelf"></div>
          <div class="ic-preloader__piece ic-preloader__piece--1">
            <img src="assets/trabajos/atos-taxi-bogota.webp" alt="" width="400" height="400" decoding="async"/>
          </div>
          <div class="ic-preloader__piece ic-preloader__piece--2">
            <img src="assets/trabajos/batman-streetwear.webp" alt="" width="400" height="400" decoding="async"/>
          </div>
          <div class="ic-preloader__piece ic-preloader__piece--3">
            <img src="assets/trabajos/civic-verde-ff.webp" alt="" width="400" height="400" decoding="async" fetchpriority="high"/>
          </div>
          <div class="ic-preloader__piece ic-preloader__piece--4">
            <img src="assets/trabajos/clio-negro-escala.webp" alt="" width="400" height="400" decoding="async"/>
          </div>
          <div class="ic-preloader__piece ic-preloader__piece--5">
            <img src="assets/trabajos/diorama-porsche-rosa-dinos.webp" alt="" width="400" height="400" decoding="async"/>
          </div>
          <div class="ic-preloader__doors">
            <div class="ic-preloader__door ic-preloader__door--l"></div>
            <div class="ic-preloader__door ic-preloader__door--r"></div>
          </div>
          <div class="ic-preloader__glass"></div>
        </div>
        <p class="ic-preloader__brand">Intentando Coleccionar</p>
        <p class="ic-preloader__label" data-ic-label>Abriendo la vitrina</p>
        <div class="ic-preloader__bar" aria-hidden="true"><span data-ic-bar></span></div>
        <div class="ic-preloader__pct" data-ic-pct>0%</div>
      </div>
    `;
    document.body.prepend(root);
    return root;
  };

  const waitForCritical = () => {
    const fontsReady =
      document.fonts && document.fonts.ready
        ? document.fonts.ready.catch(() => undefined)
        : Promise.resolve();

    const imgs = [
      ...document.querySelectorAll(
        'img[fetchpriority="high"], .hero img, .ic-preloader__piece img'
      ),
    ]
      .slice(0, 6)
      .map(
        (img) =>
          new Promise((resolve) => {
            if (img.complete) return resolve();
            img.addEventListener("load", resolve, { once: true });
            img.addEventListener("error", resolve, { once: true });
          })
      );

    return Promise.all([fontsReady, ...imgs]);
  };

  const PRELOADER_LABELS = [
    "Abriendo la vitrina",
    "Acomodando piezas",
    "Encendiendo el spotlight",
    "Lista para coleccionar",
  ];

  const runPreloader = async () => {
    const seen = sessionStorage.getItem(PRELOADER_KEY) === "1";
    const minMs = reduceMotion ? 200 : seen ? 900 : 1600;
    const maxMs = reduceMotion ? 400 : seen ? 1800 : 2800;

    document.documentElement.classList.add("is-booting");
    const root = mountPreloader();
    const bar = root.querySelector("[data-ic-bar]");
    const pct = root.querySelector("[data-ic-pct]");
    const label = root.querySelector("[data-ic-label]");
    const caseEl = root.querySelector("[data-ic-case]");

    let progress = 0;
    let doorsOpened = false;
    const setProgress = (value) => {
      progress = Math.max(progress, Math.min(100, value));
      if (bar) bar.style.width = `${progress}%`;
      if (pct) pct.textContent = `${Math.round(progress)}%`;
      if (label) {
        if (progress < 30) label.textContent = PRELOADER_LABELS[0];
        else if (progress < 55) label.textContent = PRELOADER_LABELS[1];
        else if (progress < 85) label.textContent = PRELOADER_LABELS[2];
        else label.textContent = PRELOADER_LABELS[3];
      }
      /* Abrir puertas a mitad del progreso (como el mockup) */
      if (!doorsOpened && progress >= 35) {
        doorsOpened = true;
        root.classList.add("is-opening");
        if (caseEl) caseEl.classList.add("is-open");
      }
    };

    const started = performance.now();
    const tick = window.setInterval(() => {
      const elapsed = performance.now() - started;
      const pseudo = Math.min(86, (elapsed / maxMs) * 90);
      setProgress(pseudo);
    }, 80);

    await Promise.race([
      waitForCritical().then(() => setProgress(92)),
      new Promise((r) => window.setTimeout(r, maxMs)),
    ]);

    const elapsed = performance.now() - started;
    if (elapsed < minMs) {
      await new Promise((r) => window.setTimeout(r, minMs - elapsed));
    }

    window.clearInterval(tick);
    setProgress(100);
    root.classList.add("is-opening");
    if (caseEl) caseEl.classList.add("is-open");

    await new Promise((r) => window.setTimeout(r, reduceMotion ? 60 : 720));
    root.classList.add("is-done");
    document.documentElement.classList.remove("is-booting");
    document.documentElement.classList.add("is-ready");
    sessionStorage.setItem(PRELOADER_KEY, "1");

    window.setTimeout(() => root.remove(), reduceMotion ? 80 : 700);
    window.setTimeout(() => showSocialInvite(false), reduceMotion ? 120 : 900);
  };

  /* ---------- Social invite popup ---------- */
  const SOCIAL = {
    facebook: "https://www.facebook.com/intentando.coleccionar",
    instagram: "https://www.instagram.com/intentando_coleccionar/",
    tiktok: "https://www.tiktok.com/@intentandocoleccionar",
    whatsapp:
      "https://wa.me/573115152006?text=" +
      encodeURIComponent("Hola, quiero cotizar una pieza personalizada"),
  };

  const SOCIAL_KEY = "ic_social_invite_seen";

  const icons = {
    facebook:
      '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 13.5h2.5l.5-3H14v-2c0-.9.2-1.5 1.6-1.5H17V4.1C16.5 4 15.4 4 14.4 4 11.9 4 10 5.5 10 8.2V10.5H7.5v3H10V20h4v-6.5z"/></svg>',
    instagram:
      '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 2h10a5 5 0 0 1 5 5v10a5 5 0 0 1-5 5H7a5 5 0 0 1-5-5V7a5 5 0 0 1 5-5zm5 5.2A4.8 4.8 0 1 0 16.8 12 4.8 4.8 0 0 0 12 7.2zm6.2-.9a1.1 1.1 0 1 0 1.1 1.1 1.1 1.1 0 0 0-1.1-1.1zM12 9.4A2.6 2.6 0 1 1 9.4 12 2.6 2.6 0 0 1 12 9.4z"/></svg>',
    tiktok:
      '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 1 1-2.09-2.78V9.4a6.34 6.34 0 1 0 5.54 6.28V9.33a8.17 8.17 0 0 0 4.77 1.52V6.87a4.85 4.85 0 0 1-1-.18z"/></svg>',
    whatsapp:
      '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 11.7A8.3 8.3 0 0 1 6.4 18L4 20.3l2.4-.6A8.3 8.3 0 1 1 20 11.7zm-8.1 6.5a6.8 6.8 0 0 0 3.6-1l.3-.2 2.1.5-.5-2 .2-.3a6.8 6.8 0 1 0-5.7 3zm3.7-4.9c-.2-.1-1.2-.6-1.4-.7s-.3-.1-.5.1-.5.7-.7.8-.3.2-.5.1a5.6 5.6 0 0 1-1.6-1 6.1 6.1 0 0 1-1.1-1.4c-.1-.2 0-.3.1-.4l.3-.3.2-.3c.1-.1 0-.3 0-.4s-.5-1.2-.7-1.6-.4-.4-.5-.4h-.4c-.2 0-.4.1-.6.4s-.7.7-.7 1.8.8 2.1.9 2.2a8.2 8.2 0 0 0 3.3 2.5c1.2.4 1.5.3 1.8.3s.9-.4 1-.7.1-.6.1-.7-.1-.2-.3-.3z"/></svg>',
  };

  const ensureSocialModal = () => {
    let modal = document.getElementById("ic-social-modal");
    if (modal) return modal;

    modal = document.createElement("div");
    modal.id = "ic-social-modal";
    modal.className = "ic-social-modal";
    modal.setAttribute("role", "dialog");
    modal.setAttribute("aria-modal", "true");
    modal.setAttribute("aria-labelledby", "ic-social-title");
    modal.innerHTML = `
      <div class="ic-social-modal__panel">
        <div class="ic-social-modal__aura" aria-hidden="true"></div>
        <button type="button" class="ic-social-modal__close" data-ic-social-close aria-label="Cerrar">×</button>
        <p class="ic-social-modal__eyebrow"><span class="ic-social-modal__live" aria-hidden="true"></span> Comunidad coleccionista</p>
        <h2 id="ic-social-title" class="ic-social-modal__title">Mira los últimos trabajos</h2>
        <p class="ic-social-modal__text">
          Cada semana subimos piezas nuevas, procesos y escenas personalizadas.
          Entra a nuestras redes y inspírate con lo que acaba de salir del taller.
        </p>
        <div class="ic-social-modal__grid">
          <a class="ic-social-modal__link ic-social-modal__link--facebook" href="${SOCIAL.facebook}" target="_blank" rel="noopener noreferrer">
            <span class="ic-social-modal__icon ic-social-modal__icon--facebook" aria-hidden="true"><span class="ic-social-modal__metal">${icons.facebook}</span></span>
            <span class="ic-social-modal__meta"><strong>Facebook</strong><span>intentando.coleccionar</span></span>
            <span class="ic-social-modal__go" aria-hidden="true">↗</span>
          </a>
          <a class="ic-social-modal__link ic-social-modal__link--instagram" href="${SOCIAL.instagram}" target="_blank" rel="noopener noreferrer">
            <span class="ic-social-modal__icon ic-social-modal__icon--instagram" aria-hidden="true"><span class="ic-social-modal__metal">${icons.instagram}</span></span>
            <span class="ic-social-modal__meta"><strong>Instagram</strong><span>@intentando_coleccionar</span></span>
            <span class="ic-social-modal__go" aria-hidden="true">↗</span>
          </a>
          <a class="ic-social-modal__link ic-social-modal__link--tiktok" href="${SOCIAL.tiktok}" target="_blank" rel="noopener noreferrer">
            <span class="ic-social-modal__icon ic-social-modal__icon--tiktok" aria-hidden="true"><span class="ic-social-modal__metal">${icons.tiktok}</span></span>
            <span class="ic-social-modal__meta"><strong>TikTok</strong><span>@intentandocoleccionar</span></span>
            <span class="ic-social-modal__go" aria-hidden="true">↗</span>
          </a>
          <a class="ic-social-modal__link ic-social-modal__link--whatsapp" href="${SOCIAL.whatsapp}" target="_blank" rel="noopener noreferrer">
            <span class="ic-social-modal__icon ic-social-modal__icon--whatsapp" aria-hidden="true"><span class="ic-social-modal__metal">${icons.whatsapp}</span></span>
            <span class="ic-social-modal__meta"><strong>WhatsApp</strong><span>Cotiza tu pieza</span></span>
            <span class="ic-social-modal__go" aria-hidden="true">↗</span>
          </a>
        </div>
        <button type="button" class="ic-social-modal__skip" data-ic-social-close>Seguir explorando el sitio</button>
      </div>
    `;
    document.body.appendChild(modal);

    const close = () => {
      modal.classList.remove("is-open");
      sessionStorage.setItem(SOCIAL_KEY, "1");
      document.body.style.overflow = "";
    };

    modal.querySelectorAll("[data-ic-social-close]").forEach((btn) => {
      btn.addEventListener("click", close);
    });
    modal.addEventListener("click", (e) => {
      if (e.target === modal) close();
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && modal.classList.contains("is-open")) close();
    });

    return modal;
  };

  const showSocialInvite = (force = false) => {
    if (!force && sessionStorage.getItem(SOCIAL_KEY) === "1") return;
    const modal = ensureSocialModal();
    modal.classList.add("is-open");
    document.body.style.overflow = "hidden";
  };

  const mountSocialFab = () => {
    if (document.querySelector(".ic-social-fab")) return;
    const fab = document.createElement("button");
    fab.type = "button";
    fab.className = "ic-social-fab";
    fab.setAttribute("aria-label", "Ver redes sociales y últimos trabajos");
    fab.innerHTML = `<span class="ic-social-fab__pulse" aria-hidden="true"></span> Redes · Trabajos`;
    fab.addEventListener("click", () => showSocialInvite(true));
    document.body.appendChild(fab);
  };

  IC.showSocial = () => showSocialInvite(true);

  /* ---------- Tilt ---------- */
  const initTilt = () => {
    if (reduceMotion) return;
    if (!window.matchMedia("(pointer: fine)").matches) return;

    const nodes = document.querySelectorAll(
      ".gal-item, .cat-card, .compare__card, .hero__stage"
    );
    nodes.forEach((el) => {
      el.setAttribute("data-tilt", "");
      const max = el.classList.contains("hero__stage") ? 5 : 8;

      el.addEventListener("pointermove", (e) => {
        const r = el.getBoundingClientRect();
        const px = (e.clientX - r.left) / r.width - 0.5;
        const py = (e.clientY - r.top) / r.height - 0.5;
        const rx = (-py * max).toFixed(2);
        const ry = (px * max).toFixed(2);
        el.style.transform = `perspective(900px) rotateX(${rx}deg) rotateY(${ry}deg) translateY(-2px)`;
      });

      el.addEventListener("pointerleave", () => {
        el.style.transform = "";
      });
    });
  };

  /* ---------- Badges ---------- */
  const placeBadges = () => {
    const map = [
      [".cat-card[href='carros.html'] .cat-card__media", "Hecho a mano", "ic-badge ic-badge--float"],
      [".cat-card[href='escenas.html'] .cat-card__media", "Edición única", "ic-badge ic-badge--float"],
      [".cat-card[href='dioramas.html'] .cat-card__media", "Escena custom", "ic-badge ic-badge--float"],
      [".compare__card", "Réplica real", "ic-badge ic-badge--float ic-badge--light"],
      [".gal-item--wide", "Pieza destacada", "ic-badge ic-badge--float"],
    ];

    map.forEach(([sel, label, cls]) => {
      document.querySelectorAll(sel).forEach((host, i) => {
        if (host.querySelector(".ic-badge")) return;
        if (sel === ".compare__card" && i > 1) return;
        if (sel === ".gal-item--wide" && i > 0) return;
        const badge = document.createElement("span");
        badge.className = cls;
        badge.textContent = label;
        host.appendChild(badge);
      });
    });
  };

  /* ---------- Gallery filter feedback ---------- */
  const enhanceFilters = () => {
    const group = document.querySelector("[data-filters], [data-works-filters]");
    const grid = document.querySelector(".gal-grid, [data-carousel]");
    if (!group || !grid) return;

    group.addEventListener("click", (e) => {
      if (!e.target.closest("[data-filter], [data-works-filter]")) return;
      grid.classList.add("is-filtering");
      window.setTimeout(() => grid.classList.remove("is-filtering"), reduceMotion ? 40 : 220);
    });
  };

  /* ---------- Contact form toast ---------- */
  const enhanceContact = () => {
    const form = document.querySelector("[data-contact-form]");
    if (!form) return;
    form.addEventListener(
      "submit",
      () => {
        IC.toast(
          "Abriendo tu cotización…",
          "Te llevamos a WhatsApp con el mensaje listo — como abrir la caja de tu próxima pieza."
        );
      },
      true
    );
  };

  /* ---------- WA / CTA subtle toast once ---------- */
  const enhanceCtas = () => {
    document.querySelectorAll('a[href*="wa.me"]').forEach((a) => {
      a.addEventListener("click", () => {
        if (a.closest("form")) return;
        if (sessionStorage.getItem("ic_wa_toast") === "1") return;
        sessionStorage.setItem("ic_wa_toast", "1");
        IC.toast("Te abrimos WhatsApp", "Cuéntanos tu idea — cada pieza nace conversando.");
      });
    });
  };

  /* Boot */
  const boot = () => {
    window.IC = Object.assign(window.IC || {}, {
      toast: IC.toast,
      showSocial: () => showSocialInvite(true),
    });
    runPreloader().catch(() => {
      document.documentElement.classList.remove("is-booting");
      document.documentElement.classList.add("is-ready");
      showSocialInvite(false);
    });
    initTilt();
    placeBadges();
    enhanceFilters();
    enhanceContact();
    enhanceCtas();
    mountSocialFab();
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot, { once: true });
  } else {
    boot();
  }
})();
