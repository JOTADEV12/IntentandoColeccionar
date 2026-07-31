/**
 * Analítica de visitas — Intentando Coleccionar
 *
 * Visualización (después del deploy en Vercel):
 *   Proyecto → Analytics → Web Analytics
 *   (visitas, páginas, países, referrers)
 *
 * Activación:
 *   1) Vercel → Analytics → Enable Web Analytics (+ Speed Insights opcional)
 *   2) Redeploy (para crear /_vercel/insights/*)
 *   3) Opcional: GA_MEASUREMENT_ID en js/site-config.js
 */
(function () {
  "use strict";

  var cfg = window.IC_SITE || {};
  var gaId = (cfg.GA_MEASUREMENT_ID || "").trim();

  function trackEvent(name, data) {
    try {
      if (typeof window.va === "function") {
        window.va("event", Object.assign({ name: name }, data || {}));
      }
    } catch (_) {}
    try {
      if (typeof window.gtag === "function" && gaId) {
        window.gtag("event", name, data || {});
      }
    } catch (_) {}
  }

  window.IC_track = trackEvent;

  /* —— Google Analytics 4 (opcional) —— */
  if (gaId && /^G-[A-Z0-9]+$/i.test(gaId)) {
    window.dataLayer = window.dataLayer || [];
    function gtag() {
      window.dataLayer.push(arguments);
    }
    window.gtag = gtag;
    gtag("js", new Date());
    gtag("config", gaId, {
      anonymize_ip: true,
      send_page_view: true,
    });

    var s = document.createElement("script");
    s.async = true;
    s.src =
      "https://www.googletagmanager.com/gtag/js?id=" +
      encodeURIComponent(gaId);
    document.head.appendChild(s);
  }

  /* —— Vercel Web Analytics (sitio estático HTML) —— */
  if (cfg.VERCEL_ANALYTICS !== false) {
    window.va =
      window.va ||
      function () {
        (window.vaq = window.vaq || []).push(arguments);
      };

    var vs = document.createElement("script");
    vs.defer = true;
    vs.src = "/_vercel/insights/script.js";
    document.head.appendChild(vs);
  }

  /* —— Vercel Speed Insights (rendimiento) —— */
  if (cfg.VERCEL_SPEED_INSIGHTS !== false) {
    window.si =
      window.si ||
      function () {
        (window.siq = window.siq || []).push(arguments);
      };

    var ss = document.createElement("script");
    ss.defer = true;
    ss.src = "/_vercel/speed-insights/script.js";
    document.head.appendChild(ss);
  }

  /* —— Eventos útiles: clics a WhatsApp / cotizar —— */
  document.addEventListener(
    "click",
    function (e) {
      var a = e.target && e.target.closest ? e.target.closest("a[href]") : null;
      if (!a) return;
      var href = a.getAttribute("href") || "";
      if (/wa\.me|whatsapp\.com/i.test(href)) {
        trackEvent("whatsapp_click", {
          path: location.pathname || "/",
        });
      }
    },
    true
  );
})();
