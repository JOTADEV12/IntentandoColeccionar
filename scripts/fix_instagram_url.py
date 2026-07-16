from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = "https://www.instagram.com/intentando_coleccionar/"
NEW = "https://www.instagram.com/intentando_coleccionar/"

for p in ROOT.rglob("*"):
    if p.suffix.lower() not in {".html", ".js", ".md", ".py", ".txt"}:
        continue
    if any(part.startswith(".") for part in p.parts):
        continue
    text = p.read_text(encoding="utf-8")
    updated = text.replace(OLD + "/", NEW).replace(OLD, NEW)

    # Instagram visible handles (not TikTok)
    updated = updated.replace(
        f'href="{NEW}" target="_blank" rel="noopener noreferrer">@intentandocoleccionar</a>',
        f'href="{NEW}" target="_blank" rel="noopener noreferrer">@intentando_coleccionar</a>',
    )
    updated = updated.replace(
        '<strong>Instagram</strong><span>@intentando_coleccionar</span>',
        '<strong>Instagram</strong><span>@intentando_coleccionar</span>',
    )

    # Social card handle under Instagram only: replace handle line that follows Instagram platform label
    if 'social-card__platform">Instagram</div>' in updated:
        updated = updated.replace(
            'social-card__platform">Instagram</div>\n'
            '              <div class="social-card__handle">@intentandocoleccionar</div>',
            'social-card__platform">Instagram</div>\n'
            '              <div class="social-card__handle">@intentando_coleccionar</div>',
        )

    if updated != text:
        p.write_text(updated, encoding="utf-8")
        print("updated", p.relative_to(ROOT))
