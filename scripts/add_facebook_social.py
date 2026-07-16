from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FB = "https://www.facebook.com/intentando.coleccionar"
FB_LINK = f'<a href="{FB}" target="_blank" rel="noopener noreferrer">Facebook</a>'

FACEBOOK_CARD = f'''          <a class="social-card" href="{FB}" target="_blank" rel="noopener noreferrer" aria-label="Síguenos en Facebook">
            <svg viewBox="0 0 24 24" fill="#1877F2" aria-hidden="true"><path d="M14 13.5h2.5l.5-3H14v-2c0-.9.2-1.5 1.6-1.5H17V4.1C16.5 4 15.4 4 14.4 4 11.9 4 10 5.5 10 8.2V10.5H7.5v3H10V20h4v-6.5z"/></svg>
            <div>
              <div class="social-card__platform">Facebook</div>
              <div class="social-card__handle">intentando.coleccionar</div>
            </div>
          </a>
'''


def patch(html: str) -> str:
    # Footer contacto links: Instagram TikTok -> add Facebook before Instagram
    needle = (
        '<a href="https://www.instagram.com/intentando_coleccionar/" '
        'target="_blank" rel="noopener noreferrer">Instagram</a>'
    )
    if FB not in html and needle in html:
        html = html.replace(needle, FB_LINK + needle, 1)
        # Also footers that may appear once - replace remaining carefully if contact page has multiple
        # For pages with multiple Instagram footer links (rare), first is enough in footer-col

    # Index social-row: insert Facebook before TikTok card
    if 'class="social-row' in html and FB not in html.split('social-row')[1][:1200]:
        tiktok_card_start = html.find(
            '<a class="social-card" href="https://www.tiktok.com/@intentandocoleccionar"'
        )
        if tiktok_card_start != -1:
            html = html[:tiktok_card_start] + FACEBOOK_CARD + html[tiktok_card_start:]

    # Contacto page channel list
    if "Redes" in html or "Instagram" in html:
        block = (
            '              <p><a href="https://www.instagram.com/intentando_coleccionar/" '
            'target="_blank" rel="noopener noreferrer">@intentandocoleccionar</a></p>'
        )
        fb_block = (
            f'              <div class="channel">\n'
            f'                <p class="channel__label">Facebook</p>\n'
            f'                <p><a href="{FB}" target="_blank" rel="noopener noreferrer">'
            f"intentando.coleccionar</a></p>\n"
            f"              </div>\n"
        )
        # Only if contacto has channel pattern and facebook missing nearby
        if "channel__label" in html and FB not in html:
            # insert before Instagram channel if present
            ig = html.find(">Instagram</p>")
            if ig != -1:
                # find start of that channel div
                start = html.rfind('<div class="channel">', 0, ig)
                if start != -1:
                    html = html[:start] + fb_block + html[start:]

    # Bump experience cache
    html = html.replace("experience.js?v=2", "experience.js?v=3")
    html = html.replace("motion.css", "motion.css")  # noop keep
    return html


def main() -> None:
    for p in sorted(ROOT.glob("*.html")):
        old = p.read_text(encoding="utf-8")
        new = patch(old)
        # Ensure every footer has Facebook if it has Instagram
        if "intentandocoleccionar" in new and FB not in new:
            new = new.replace(
                '<a href="https://www.instagram.com/intentando_coleccionar/" target="_blank" rel="noopener noreferrer">Instagram</a>',
                FB_LINK
                + '<a href="https://www.instagram.com/intentando_coleccionar/" target="_blank" rel="noopener noreferrer">Instagram</a>',
            )
        # bump scripts on all
        new = new.replace("js/experience.js?v=2", "js/experience.js?v=3")
        new = new.replace('href="css/motion.css"', 'href="css/motion.css?v=3"')
        if new != old:
            p.write_text(new, encoding="utf-8")
            print("updated", p.name)
        else:
            print("unchanged", p.name)


if __name__ == "__main__":
    main()
