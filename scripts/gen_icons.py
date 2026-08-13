from pathlib import Path

img = Path(__file__).resolve().parents[1] / "img"


def svg(inner: str, w: int = 16, h: int = 16) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" fill="none" stroke="#b4b4b4" stroke-width="1.5" '
        f'stroke-linecap="round" stroke-linejoin="round">{inner}</svg>'
    )


icons = {
    "print.svg": (
        '<rect x="4" y="6" width="8" height="6" rx="1"/>'
        '<path d="M5 12v3h6v-3"/>'
        '<path d="M5 6V3h6v3"/>'
        '<circle cx="11" cy="9" r="0.4" fill="#b4b4b4" stroke="none"/>'
    ),
    "export.svg": (
        '<path d="M8 10V3"/>'
        '<polyline points="5 6 8 3 11 6"/>'
        '<path d="M3 12v1a1 1 0 001 1h8a1 1 0 001-1v-1"/>'
    ),
    "import.svg": (
        '<path d="M8 3v7"/>'
        '<polyline points="5 7 8 10 11 7"/>'
        '<path d="M3 12v1a1 1 0 001 1h8a1 1 0 001-1v-1"/>'
    ),
    "col-move.svg": (
        '<rect x="3" y="3" width="4" height="10" rx="0.5"/>'
        '<rect x="9" y="3" width="4" height="10" rx="0.5"/>'
        '<path d="M7 8h2"/>'
    ),
    "firstpage.svg": '<path d="M4 3v10"/><polyline points="12 3 7 8 12 13"/>',
    "lastpage.svg": '<path d="M12 3v10"/><polyline points="4 3 9 8 4 13"/>',
    "nextpage.svg": '<polyline points="6 3 11 8 6 13"/>',
    "prevpage.svg": '<polyline points="10 3 5 8 10 13"/>',
    "chevron-left.svg": '<polyline points="10 3 5 8 10 13"/>',
    "chevron-right.svg": '<polyline points="6 3 11 8 6 13"/>',
    "col-drop.svg": (
        '<rect x="3" y="3" width="10" height="4" rx="0.5"/>'
        '<rect x="3" y="8" width="6" height="5" rx="0.5"/>'
        '<line x1="11" y1="10" x2="14" y2="10"/>'
    ),
    "sync.svg": (
        '<path d="M13 8a5 5 0 01-8.5 3.5"/>'
        '<polyline points="13 11 13 8 10 8"/>'
        '<path d="M3 8a5 5 0 018.5-3.5"/>'
        '<polyline points="3 5 3 8 6 8"/>'
    ),
    "eye.svg": (
        '<path d="M1.5 8s2.5-4.5 6.5-4.5S14.5 8 14.5 8 12 12.5 8 12.5 1.5 8 1.5 8z"/>'
        '<circle cx="8" cy="8" r="2"/>'
    ),
    "spinner.svg": (
        '<circle cx="8" cy="8" r="6" stroke-dasharray="22 12">'
        '<animateTransform attributeName="transform" type="rotate" from="0 8 8" '
        'to="360 8 8" dur="0.8s" repeatCount="indefinite"/>'
        "</circle>"
    ),
}

for name, inner in icons.items():
    (img / name).write_text(svg(inner), encoding="utf-8")
    print("wrote", name)

src = img / "field-index-uinique.svg"
dst = img / "field-index-unique.svg"
if src.exists():
    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    print("copied unique")
