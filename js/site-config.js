/* Config del sitio — Intentando Coleccionar
 *
 * SITE_ORIGIN: URL canónica del sitio (www.intentandocoleccionar.autos)
 *
 * Analítica — se visualiza en Vercel → proyecto → Analytics:
 *   VERCEL_ANALYTICS: true = Web Analytics (visitas / páginas / referrers)
 *   VERCEL_SPEED_INSIGHTS: true = métricas de velocidad (LCP, CLS, etc.)
 *   Actívalos en el dashboard: Analytics → Enable (y Speed Insights)
 *
 * GA_MEASUREMENT_ID: opcional, ID tipo G-XXXXXXXXXX de analytics.google.com
 * GOOGLE_SITE_VERIFICATION: código de Search Console (meta HTML tag).
 *   Inyéctalo en las páginas con: python scripts/set_gsc_verification.py CODIGO
 */
window.IC_SITE = Object.freeze({
  SITE_ORIGIN: "https://www.intentandocoleccionar.autos",
  WA: "573115152006",
  OG_IMAGE: "assets/img/hero-tag-brick.webp",
  GA_MEASUREMENT_ID: "",
  GOOGLE_SITE_VERIFICATION: "",
  VERCEL_ANALYTICS: true,
  VERCEL_SPEED_INSIGHTS: true,
});
