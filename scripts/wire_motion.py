from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BOOT = '  <script>document.documentElement.classList.add("is-booting");</script>\n'
MOTION_CSS = '  <link rel="stylesheet" href="css/motion.css"/>\n'
EXP_JS = (
    '  <script src="js/main.js?v=2" defer></script>\n'
    '  <script src="js/experience.js?v=2" defer></script>\n'
)


def patch(html: str) -> str:
    if 'href="css/motion.css"' not in html:
        if 'href="css/premium.css"/>' in html:
            html = html.replace(
                '  <link rel="stylesheet" href="css/premium.css"/>\n',
                '  <link rel="stylesheet" href="css/premium.css"/>\n' + MOTION_CSS,
                1,
            )
        elif 'href="css/works.css"/>' in html:
            html = html.replace(
                '  <link rel="stylesheet" href="css/works.css"/>\n',
                '  <link rel="stylesheet" href="css/works.css"/>\n' + MOTION_CSS,
                1,
            )
        else:
            html = html.replace("</head>", MOTION_CSS + "</head>", 1)

    if 'classList.add("is-booting")' not in html:
        html = html.replace("<head>\n", "<head>\n" + BOOT, 1)

    if 'src="js/experience.js"' not in html:
        if 'src="js/main.js"' in html:
            html = html.replace(
                '  <script src="js/main.js" defer></script>',
                EXP_JS.rstrip() + "\n  <script src=\"js/main.js\" defer></script>",
                1,
            )
        else:
            html = html.replace("</body>", EXP_JS + "</body>", 1)

    return html


def main() -> None:
    for fp in sorted(ROOT.glob("*.html")):
        old = fp.read_text(encoding="utf-8")
        new = patch(old)
        fp.write_text(new, encoding="utf-8")
        print(fp.name, "ok" if new != old else "already")


if __name__ == "__main__":
    main()
