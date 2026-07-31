(() => {
  "use strict";

  const WA_BASE =
    "https://wa.me/573115152006?text=" +
    encodeURIComponent("Hola, quiero cotizar una figura personalizada");

  /* Sticky header */
  const header = document.querySelector("[data-header]");
  if (header) {
    const onScroll = () => {
      header.classList.toggle("is-stuck", window.scrollY > 40);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* Mobile nav */
  const toggle = document.querySelector("[data-nav-toggle]");
  const mobileNav = document.querySelector("[data-nav-mobile]");

  const setNavOpen = (open) => {
    if (!toggle || !mobileNav) return;
    toggle.setAttribute("aria-expanded", String(open));
    mobileNav.classList.toggle("is-open", open);
    document.body.classList.toggle("nav-open", open);
  };

  if (toggle && mobileNav) {
    toggle.addEventListener("click", () => {
      const open = toggle.getAttribute("aria-expanded") !== "true";
      setNavOpen(open);
    });

    mobileNav.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => setNavOpen(false));
    });

    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") setNavOpen(false);
    });
  }

  /* Current page highlight */
  const path = (location.pathname.split("/").pop() || "index.html").toLowerCase();
  document.querySelectorAll("[data-nav] a[href]").forEach((a) => {
    const href = (a.getAttribute("href") || "").split("#")[0].toLowerCase();
    if (!href || href.startsWith("http")) return;
    if (href === path || (path === "" && href === "index.html")) {
      a.setAttribute("aria-current", "page");
    }
  });

  /* Scroll reveal (Intersection Observer) */
  const revealEls = document.querySelectorAll(".reveal, .stagger");
  if (revealEls.length && "IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -8% 0px" }
    );
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add("is-visible"));
  }

  /* Hydrate placeholders: insert into DOM first so loading can proceed */
  const hydratePh = (ph, src, alt) => {
    if (!ph || !src) return;
    const img = document.createElement("img");
    img.alt = alt || "";
    img.decoding = "async";
    img.loading = "eager";
    img.setAttribute("data-hydrated", "true");
    ph.replaceWith(img);
    img.addEventListener("error", () => {
      const fallback = document.createElement("div");
      fallback.className = "img-ph";
      fallback.textContent = alt || "Imagen pendiente";
      img.replaceWith(fallback);
    });
    img.src = src;
  };

  document.querySelectorAll("[data-src]").forEach((host) => {
    const src = host.getAttribute("data-src");
    const ph = host.querySelector(".img-ph");
    if (!src || !ph || host.querySelector("img[data-hydrated]")) return;
    hydratePh(ph, src, host.getAttribute("data-alt") || host.getAttribute("data-cap") || "");
  });

  document.querySelectorAll("[data-img]").forEach((ph) => {
    const src = ph.getAttribute("data-img");
    if (!src || ph.tagName === "IMG" || ph.closest("[data-src]")) return;
    hydratePh(ph, src, ph.getAttribute("aria-label") || ph.getAttribute("data-alt") || "");
  });

  /* Gallery filters */
  const filterGroup = document.querySelector("[data-filters]");
  const galleryItems = document.querySelectorAll("[data-gal-item]");

  if (filterGroup && galleryItems.length) {
    filterGroup.addEventListener("click", (e) => {
      const btn = e.target.closest("[data-filter]");
      if (!btn) return;

      filterGroup.querySelectorAll("[data-filter]").forEach((b) => {
        b.classList.toggle("is-active", b === btn);
        b.setAttribute("aria-pressed", String(b === btn));
      });

      const filter = btn.dataset.filter;
      galleryItems.forEach((item) => {
        const cat = item.dataset.cat;
        const show = filter === "all" || cat === filter;
        item.classList.toggle("is-hidden", !show);
      });
    });
  }

  /* Lightbox */
  const lb = document.querySelector("[data-lightbox]");
  if (lb) {
    const lbImg = lb.querySelector("[data-lb-img]");
    const lbPh = lb.querySelector("[data-lb-ph]");
    const lbCap = lb.querySelector("[data-lb-cap]");
    const items = [...document.querySelectorAll("[data-gal-item]")];
    let index = 0;

    const show = (i) => {
      const visible = items.filter((el) => !el.classList.contains("is-hidden"));
      if (!visible.length) return;
      index = ((i % visible.length) + visible.length) % visible.length;
      const item = visible[index];
      const src = item.dataset.src || "";
      const cap = item.dataset.cap || "";
      const alt = item.dataset.alt || cap;

      if (lbImg && src) {
        lbImg.hidden = false;
        if (lbPh) lbPh.hidden = true;
        lbImg.src = src;
        lbImg.alt = alt;
        lbImg.onerror = () => {
          lbImg.hidden = true;
          if (lbPh) {
            lbPh.hidden = false;
            lbPh.textContent = alt || "Imagen pendiente de cargar";
          }
        };
      } else if (lbPh) {
        if (lbImg) lbImg.hidden = true;
        lbPh.hidden = false;
        lbPh.innerHTML = `${alt}<span>${item.dataset.file || "archivo pendiente"}</span>`;
      }

      if (lbCap) lbCap.textContent = cap;
      lb.classList.add("is-open");
      lb.setAttribute("aria-hidden", "false");
      document.body.style.overflow = "hidden";
    };

    const close = () => {
      lb.classList.remove("is-open");
      lb.setAttribute("aria-hidden", "true");
      document.body.style.overflow = "";
    };

    items.forEach((item, i) => {
      item.addEventListener("click", () => show(i));
      item.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          show(i);
        }
      });
    });

    lb.querySelector("[data-lb-close]")?.addEventListener("click", close);
    lb.querySelector("[data-lb-prev]")?.addEventListener("click", () => show(index - 1));
    lb.querySelector("[data-lb-next]")?.addEventListener("click", () => show(index + 1));
    lb.addEventListener("click", (e) => {
      if (e.target === lb) close();
    });

    document.addEventListener("keydown", (e) => {
      if (!lb.classList.contains("is-open")) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowLeft") show(index - 1);
      if (e.key === "ArrowRight") show(index + 1);
    });
  }

  /* Contact form → WhatsApp prefill (no backend) */
  const form = document.querySelector("[data-contact-form]");
  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const data = new FormData(form);
      const name = String(data.get("nombre") || "").trim();
      const interest = String(data.get("interes") || "").trim();
      const message = String(data.get("mensaje") || "").trim();
      const city = String(data.get("ciudad") || "").trim();

      const lines = [
        "Hola, quiero cotizar una pieza personalizada.",
        name ? `Nombre: ${name}` : "",
        city ? `Ciudad: ${city}` : "",
        interest ? `Interés: ${interest}` : "",
        message ? `Detalle: ${message}` : "",
      ].filter(Boolean);

      window.open(
        "https://wa.me/573115152006?text=" + encodeURIComponent(lines.join("\n")),
        "_blank",
        "noopener,noreferrer"
      );
    });
  }

  /* Expose WA without wiping experience.js helpers (toast, etc.) */
  window.IC = Object.assign(window.IC || {}, { WA_BASE });

  /* Hero FX: parallax pointer + scroll (mockup A) */
  const hero = document.querySelector("[data-hero]") || document.querySelector(".hero");
  const heroImg =
    document.querySelector("[data-fx-media] img") ||
    document.querySelector(".hero__fx-media img") ||
    document.querySelector(".hero__bg-photo img") ||
    document.querySelector(".hero__bg img");
  const canParallax =
    hero &&
    heroImg &&
    !window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (canParallax) {
    hero.classList.add("is-parallax");
    let ticking = false;
    let px = 0;
    let py = 0;

    const apply = () => {
      heroImg.style.setProperty("--px", `${px}px`);
      heroImg.style.setProperty("--py", `${py}px`);
      ticking = false;
    };

    if (window.matchMedia("(pointer: fine)").matches) {
      hero.addEventListener(
        "pointermove",
        (e) => {
          const r = hero.getBoundingClientRect();
          px = -((e.clientX - r.left) / r.width - 0.5) * 18;
          py = -((e.clientY - r.top) / r.height - 0.5) * 12;
          if (!ticking) {
            ticking = true;
            requestAnimationFrame(apply);
          }
        },
        { passive: true }
      );
      hero.addEventListener("pointerleave", () => {
        px = 0;
        py = 0;
        requestAnimationFrame(apply);
      });
    }

    window.addEventListener(
      "scroll",
      () => {
        const scrollY = Math.min(40, window.scrollY * 0.08);
        if (!window.matchMedia("(pointer: fine)").matches || px === 0) {
          py = scrollY;
        } else {
          py = py * 0.5 + scrollY;
        }
        if (!ticking) {
          ticking = true;
          requestAnimationFrame(apply);
        }
      },
      { passive: true }
    );
  }

  /* Trabajos carousel + filters */
  const carousel = document.querySelector("[data-carousel]");
  if (carousel) {
    const track = carousel.querySelector("[data-carousel-track]");
    const dotsRoot = carousel.querySelector("[data-carousel-dots]");
    const btnPrev = carousel.querySelector("[data-carousel-prev]");
    const btnNext = carousel.querySelector("[data-carousel-next]");
    const filters = document.querySelectorAll("[data-works-filter]");
    let filter = "all";
    let index = 0;
    let timer = null;
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    const visibleSlides = () =>
      [...track.querySelectorAll("[data-works-item]")].filter((slide) => {
        const cat = slide.getAttribute("data-cat");
        const show = filter === "all" || cat === filter;
        slide.classList.toggle("is-hidden", !show);
        return show;
      });

    const buildDots = (slides) => {
      if (!dotsRoot) return;
      dotsRoot.innerHTML = "";
      slides.forEach((_, i) => {
        const dot = document.createElement("button");
        dot.type = "button";
        dot.className = "carousel__dot" + (i === index ? " is-active" : "");
        dot.setAttribute("aria-label", `Ir al trabajo ${i + 1}`);
        dot.addEventListener("click", () => goTo(i));
        dotsRoot.appendChild(dot);
      });
    };

    const render = () => {
      const slides = visibleSlides();
      if (!slides.length) {
        track.style.transform = "translateX(0)";
        if (dotsRoot) dotsRoot.innerHTML = "";
        return;
      }
      if (index >= slides.length) index = 0;
      if (index < 0) index = slides.length - 1;
      const viewport = carousel.querySelector(".carousel__viewport");
      const width = viewport ? viewport.clientWidth : 0;
      track.style.transform = `translateX(-${index * width}px)`;
      track.querySelectorAll("[data-works-item]").forEach((s) => s.classList.remove("is-active"));
      slides[index].classList.add("is-active");
      buildDots(slides);
      if (dotsRoot) {
        [...dotsRoot.children].forEach((d, i) => d.classList.toggle("is-active", i === index));
      }
    };

    window.addEventListener("resize", () => render(), { passive: true });

    const goTo = (i) => {
      index = i;
      render();
      restartAutoplay();
    };

    const step = (dir) => {
      const slides = visibleSlides();
      if (!slides.length) return;
      index = (index + dir + slides.length) % slides.length;
      render();
      restartAutoplay();
    };

    const restartAutoplay = () => {
      if (timer) clearInterval(timer);
      if (reduceMotion) return;
      timer = setInterval(() => step(1), 5200);
    };

    btnPrev?.addEventListener("click", () => step(-1));
    btnNext?.addEventListener("click", () => step(1));

    filters.forEach((btn) => {
      btn.addEventListener("click", () => {
        filter = btn.getAttribute("data-works-filter") || "all";
        filters.forEach((b) => {
          const on = b === btn;
          b.classList.toggle("is-active", on);
          b.setAttribute("aria-pressed", on ? "true" : "false");
        });
        index = 0;
        render();
        restartAutoplay();
      });
    });

    carousel.addEventListener("pointerenter", () => timer && clearInterval(timer));
    carousel.addEventListener("pointerleave", restartAutoplay);

    let touchX = null;
    carousel.addEventListener(
      "touchstart",
      (e) => {
        touchX = e.changedTouches[0].clientX;
      },
      { passive: true }
    );
    carousel.addEventListener(
      "touchend",
      (e) => {
        if (touchX == null) return;
        const dx = e.changedTouches[0].clientX - touchX;
        touchX = null;
        if (Math.abs(dx) < 40) return;
        step(dx < 0 ? 1 : -1);
      },
      { passive: true }
    );

    render();
    restartAutoplay();
  }

  /* Hero spray: restart class if reduced motion not preferred */
  const stage = document.querySelector(".hero__stage");
  if (stage && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    stage.classList.add("is-armed");
  }


  /* Magnetic buttons (desktop only) */
  if (
    window.matchMedia("(pointer: fine)").matches &&
    !window.matchMedia("(prefers-reduced-motion: reduce)").matches
  ) {
    document.querySelectorAll(".btn--primary, .btn--wa, .nav-cta").forEach((btn) => {
      btn.setAttribute("data-magnetic", "");
      btn.addEventListener("pointermove", (e) => {
        const r = btn.getBoundingClientRect();
        const x = e.clientX - (r.left + r.width / 2);
        const y = e.clientY - (r.top + r.height / 2);
        btn.style.transform = `translate(${x * 0.12}px, ${y * 0.18 - 2}px)`;
      });
      btn.addEventListener("pointerleave", () => {
        btn.style.transform = "";
      });
    });
  }

  /* Smooth active nav underline via IntersectionObserver sections */
  const sectionIds = [...document.querySelectorAll("main section[id]")].map((s) => s.id);
  if (sectionIds.length && "IntersectionObserver" in window) {
    const map = new Map(
      [...document.querySelectorAll('.nav-desktop a[href^="#"]')].map((a) => [
        a.getAttribute("href").slice(1),
        a,
      ])
    );
    const ioNav = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          map.forEach((el) => el.removeAttribute("aria-current"));
          map.get(entry.target.id)?.setAttribute("aria-current", "page");
        });
      },
      { rootMargin: "-40% 0px -50% 0px", threshold: 0.01 }
    );
    sectionIds.forEach((id) => {
      const el = document.getElementById(id);
      if (el) ioNav.observe(el);
    });
  }
  /* Brand micro-interaction: subtle shimmer on mark */
  const brand = document.querySelector(".brand");
  if (brand && window.matchMedia("(pointer: fine)").matches) {
    brand.addEventListener("pointermove", (e) => {
      const r = brand.getBoundingClientRect();
      const x = ((e.clientX - r.left) / r.width) * 100;
      const y = ((e.clientY - r.top) / r.height) * 100;
      brand.style.setProperty("--mx", `${x}%`);
      brand.style.setProperty("--my", `${y}%`);
    });
  }
})();
