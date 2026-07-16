from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOCK = (
    '\n  <script src="js/main.js?v=2" defer></script>\n'
    '  <script src="js/experience.js?v=2" defer></script>\n'
)

for p in ROOT.glob("*.html"):
    t = p.read_text(encoding="utf-8")
    # remove broken backtick-n litter and old script tags near end
    n = t.replace("`n", "\n")
    n = n.replace(
        '  <script src="js/experience.js?v=2" defer></script>\n'
        '  <script src="js/main.js?v=2" defer></script>',
        "",
    )
    n = n.replace(
        '  <script src="js/main.js?v=2" defer></script>\n'
        '  <script src="js/experience.js?v=2" defer></script>',
        "",
    )
    n = n.replace('  <script src="js/main.js" defer></script>', "")
    n = n.replace('  <script src="js/experience.js" defer></script>', "")
    if "</body>" not in n:
        raise SystemExit(f"no body in {p}")
    n = n.replace("</body>", BLOCK + "</body>", 1)
    p.write_text(n, encoding="utf-8")
    print("ok", p.name)
