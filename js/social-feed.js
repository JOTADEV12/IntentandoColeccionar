(() => {
  "use strict";

  const JSON_PATH = "data/social-embeds.json";
  const TIKTOK_SRC = "https://www.tiktok.com/embed.js";
  const IG_SRC = "https://www.instagram.com/embed.js";
  const LABELS = {
    tiktok: "TikTok",
    instagram: "Instagram",
    facebook: "Facebook",
  };

  let dataPromise = null;
  const scripts = {
    tiktok: { loading: null, loaded: false },
    instagram: { loading: null, loaded: false },
  };

  const platformLabel = (platform) => LABELS[platform] || platform || "Redes";

  const trackClick = (platform, id) => {
    try {
      if (typeof window.IC_track === "function") {
        window.IC_track("social_embed_click", { platform: platform, id: id || "" });
      }
    } catch (_) {}
  };

  const tiktokVideoId = (url) => {
    const match = String(url || "").match(/\/video\/(\d+)/);
    return match ? match[1] : "";
  };

  const bindOpenLink = (anchor, item) => {
    if (!anchor) return;
    anchor.addEventListener("click", () => trackClick(item.platform, item.id));
  };

  const fallbackCard = (item) => {
    const safe = item || {};
    const article = document.createElement("article");
    article.className = "social-embed social-embed--fallback";
    article.setAttribute("data-social-id", safe.id || "");
    article.setAttribute("data-platform", safe.platform || "");

    const platform = document.createElement("p");
    platform.className = "social-card__platform";
    platform.textContent = platformLabel(safe.platform);

    const frame = document.createElement("div");
    frame.className = "social-embed__frame social-embed__frame--fallback";

    const title = document.createElement("h3");
    title.className = "social-embed__title";
    title.textContent = safe.title || "Ver publicación";

    const link = document.createElement("a");
    link.className = "social-embed__open";
    link.href = safe.url || "#";
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.textContent = "Ver en " + platformLabel(safe.platform);
    bindOpenLink(link, safe);

    frame.append(title, link);
    article.append(platform, frame);
    return article;
  };

  const makeCardShell = (item) => {
    const article = document.createElement("article");
    article.className = "social-embed" + (item.featured ? " social-embed--featured" : "");
    article.setAttribute("data-social-id", item.id || "");
    article.setAttribute("data-platform", item.platform || "");

    const platform = document.createElement("p");
    platform.className = "social-card__platform";
    platform.textContent = platformLabel(item.platform);

    const frame = document.createElement("div");
    frame.className = "social-embed__frame";

    article.append(platform, frame);
    return { article, frame };
  };

  const tiktokCard = (item) => {
    const videoId = tiktokVideoId(item.url);
    if (!videoId) return fallbackCard(item);

    const { article, frame } = makeCardShell(item);
    const quote = document.createElement("blockquote");
    quote.className = "tiktok-embed";
    quote.setAttribute("cite", item.url);
    quote.setAttribute("data-video-id", videoId);

    const section = document.createElement("section");
    const link = document.createElement("a");
    link.href = item.url;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.textContent = item.title || "Ver en TikTok";
    bindOpenLink(link, item);
    section.appendChild(link);
    quote.appendChild(section);
    frame.appendChild(quote);
    return article;
  };

  const instagramCard = (item) => {
    if (!item.url) return fallbackCard(item);

    const { article, frame } = makeCardShell(item);
    const quote = document.createElement("blockquote");
    quote.className = "instagram-media";
    quote.setAttribute("data-instgrm-permalink", item.url);
    quote.setAttribute("data-instgrm-version", "14");

    const link = document.createElement("a");
    link.href = item.url;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.textContent = "Ver en Instagram";
    bindOpenLink(link, item);
    quote.appendChild(link);
    frame.appendChild(quote);
    return article;
  };

  const renderItem = (item) => {
    if (!item || !item.url) return fallbackCard(item || {});
    if (item.platform === "tiktok") return tiktokCard(item);
    if (item.platform === "instagram") return instagramCard(item);
    return fallbackCard(item);
  };

  const loadScript = (src, id) =>
    new Promise((resolve, reject) => {
      const existing = document.getElementById(id);
      if (existing) {
        if (existing.getAttribute("data-ic-loaded") === "1") return resolve();
        if (existing.getAttribute("data-ic-error") === "1") return reject(new Error(src));
        existing.addEventListener("load", () => resolve(), { once: true });
        existing.addEventListener("error", () => reject(new Error(src)), { once: true });
        return;
      }
      const script = document.createElement("script");
      script.id = id;
      script.async = true;
      script.src = src;
      script.onload = () => {
        script.setAttribute("data-ic-loaded", "1");
        resolve();
      };
      script.onerror = () => {
        script.setAttribute("data-ic-error", "1");
        reject(new Error(src));
      };
      document.body.appendChild(script);
    });

  const processInstagram = () => {
    try {
      if (window.instgrm && window.instgrm.Embeds && typeof window.instgrm.Embeds.process === "function") {
        window.instgrm.Embeds.process();
      }
    } catch (_) {}
  };

  const fallbackEmpty = (root, items, platform) => {
    window.setTimeout(() => {
      root.querySelectorAll('.social-embed[data-platform="' + platform + '"]').forEach((card) => {
        if (card.classList.contains("social-embed--fallback")) return;
        if (card.querySelector("iframe")) return;
        const id = card.getAttribute("data-social-id");
        const item = items.find((entry) => entry.id === id);
        if (item) card.replaceWith(fallbackCard(item));
      });
    }, 10000);
  };

  const ensureTikTok = (root, items) => {
    if (scripts.tiktok.loaded) return;
    if (!scripts.tiktok.loading) {
      scripts.tiktok.loading = loadScript(TIKTOK_SRC, "ic-tiktok-embed-js")
        .then(() => {
          scripts.tiktok.loaded = true;
        })
        .catch(() => {
          root.querySelectorAll('.social-embed[data-platform="tiktok"]').forEach((card) => {
            const id = card.getAttribute("data-social-id");
            const item = items.find((entry) => entry.id === id);
            if (item) card.replaceWith(fallbackCard(item));
          });
        });
    }
    scripts.tiktok.loading.then(() => fallbackEmpty(root, items, "tiktok"));
  };

  const ensureInstagram = (root, items) => {
    const after = () => {
      processInstagram();
      fallbackEmpty(root, items, "instagram");
    };
    if (scripts.instagram.loaded) {
      after();
      return;
    }
    if (!scripts.instagram.loading) {
      scripts.instagram.loading = loadScript(IG_SRC, "ic-ig-embed-js")
        .then(() => {
          scripts.instagram.loaded = true;
          processInstagram();
        })
        .catch(() => {
          root.querySelectorAll('.social-embed[data-platform="instagram"]').forEach((card) => {
            const id = card.getAttribute("data-social-id");
            const item = items.find((entry) => entry.id === id);
            if (item) card.replaceWith(fallbackCard(item));
          });
        });
    }
    scripts.instagram.loading.then(after);
  };

  const lazyLoadEmbeds = (root, items, needs) => {
    const run = () => {
      if (needs.tiktok) ensureTikTok(root, items);
      if (needs.instagram) ensureInstagram(root, items);
    };

    if (!("IntersectionObserver" in window)) {
      run();
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        if (entries.some((entry) => entry.isIntersecting)) {
          observer.disconnect();
          run();
        }
      },
      { rootMargin: "240px 0px", threshold: 0.01 }
    );
    observer.observe(root);
  };

  const loadData = () => {
    if (!dataPromise) {
      dataPromise = fetch(JSON_PATH, { credentials: "same-origin" }).then((res) => {
        if (!res.ok) throw new Error("social-embeds");
        return res.json();
      });
    }
    return dataPromise;
  };

  const mountError = (el) => {
    el.classList.add("social-feed");
    el.replaceChildren();
    const note = document.createElement("p");
    note.className = "social-feed__error";
    note.textContent = "Los videos no se pudieron cargar ahora. Puedes verlos en nuestras redes.";
    el.appendChild(note);
  };

  const mount = (el, data) => {
    const compact = el.getAttribute("data-social-feed") === "compact";
    const limit = compact ? 3 : 6;
    const items = Array.isArray(data.items) ? data.items.slice(0, limit) : [];

    el.classList.add("social-feed");
    if (compact) el.classList.add("social-feed--compact");
    el.replaceChildren();

    const needs = { tiktok: false, instagram: false };
    items.forEach((item) => {
      try {
        if (item.platform === "tiktok") needs.tiktok = true;
        if (item.platform === "instagram") needs.instagram = true;
        el.appendChild(renderItem(item));
      } catch (_) {
        try {
          el.appendChild(fallbackCard(item));
        } catch (__) {
          /* keep the rest of the grid */
        }
      }
    });

    if (!items.length) {
      mountError(el);
      return;
    }

    lazyLoadEmbeds(el, items, needs);
  };

  const boot = () => {
    const hosts = document.querySelectorAll("[data-social-feed]");
    if (!hosts.length) return;

    loadData()
      .then((data) => {
        hosts.forEach((el) => {
          try {
            mount(el, data);
          } catch (_) {
            mountError(el);
          }
        });
      })
      .catch(() => {
        hosts.forEach(mountError);
      });
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot, { once: true });
  } else {
    boot();
  }
})();
