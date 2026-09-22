"""Normalize Stygia icons from Lucide and audit the mask catalog.

``scripts/icon_map.json`` is the source of truth. This script copies Lucide
SVGs (ISC) into ``img/``, keeps aliases identical, and refuses hand-drawn
geometry. Run ``npm run icons:generate`` to write and ``npm run icons:check``
to audit without writing.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMG = ROOT / "img"
ICONS_SCSS = ROOT / "scss" / "_icons.scss"
CATALOG = ROOT / "docs" / "icons.html"
MAP_PATH = ROOT / "scripts" / "icon_map.json"
LUCIDE_DIR = ROOT / "node_modules" / "lucide-static" / "icons"

STROKE = "#b4b4b4"
GEOM = {"path", "rect", "circle", "ellipse", "line", "polyline", "polygon"}
HEADER = (
    "<!-- Adapted from Lucide (https://lucide.dev), ISC License. "
    "Copyright (c) Lucide Contributors. Portions Copyright (c) Cole Bemis "
    "2013-2023 (Feather, MIT). -->\n"
)


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def load_map() -> list[dict]:
    data = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    icons = data.get("icons")
    if not isinstance(icons, list) or not icons:
        raise SystemExit("icon_map.json: missing icons array")
    return icons


def referenced_assets() -> set[str]:
    source = ICONS_SCSS.read_text(encoding="utf-8")
    return set(
        re.findall(
            r'(?:url|icon-mask)\(["\']?\.\./img/([^"\')]+)',
            source,
        )
    )


def index_entries(entries: list[dict]) -> dict[str, dict]:
    by_file: dict[str, dict] = {}
    for entry in entries:
        name = entry.get("file")
        if not name or name in by_file:
            raise SystemExit(f"icon_map.json: duplicate or empty file {name!r}")
        by_file[name] = entry
    return by_file


def resolve_source(name: str, by_file: dict[str, dict]) -> str:
    seen: list[str] = []
    current = name
    while True:
        entry = by_file.get(current)
        if entry is None:
            raise SystemExit(f"{name}: alias chain leaves the map at {current}")
        alias = entry.get("aliasOf")
        if not alias:
            return current
        if current in seen:
            raise SystemExit(f"{name}: alias cycle {' -> '.join(seen)}")
        seen.append(current)
        current = alias


def attr_escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
    )


def child_attrs(el: ET.Element, *, filled: bool) -> list[tuple[str, str]]:
    name = local(el.tag)
    attrs: list[tuple[str, str]] = []
    for key, value in el.attrib.items():
        if key in {"class", "style"} or key.startswith("{"):
            continue
        if key == "stroke" and value == "currentColor":
            continue
        if key == "fill" and value == "none" and not filled:
            continue
        if key == "fill" and value == "currentColor":
            value = STROKE
        attrs.append((key, value))
    if filled and name in GEOM:
        attrs = [(key, value) for key, value in attrs if key != "fill"]
        attrs.append(("fill", STROKE))
    return attrs


def render_element(el: ET.Element, *, filled: bool, root: bool = False) -> str:
    name = local(el.tag)
    if name in {"filter", "image", "style", "script", "text"}:
        raise ValueError(f"forbidden <{name}>")
    if "transform" in el.attrib:
        raise ValueError("transform attribute")
    if root:
        view_box = el.attrib.get("viewBox")
        if view_box != "0 0 24 24":
            raise ValueError(f"expected Lucide viewBox 0 0 24 24, got {view_box!r}")
        attrs = [
            ("xmlns", "http://www.w3.org/2000/svg"),
            ("width", "24"),
            ("height", "24"),
            ("viewBox", "0 0 24 24"),
            ("fill", "none"),
            ("stroke", STROKE),
            ("stroke-width", "2"),
            ("stroke-linecap", "round"),
            ("stroke-linejoin", "round"),
        ]
    else:
        attrs = child_attrs(el, filled=filled)
    attr_text = "".join(f' {key}="{attr_escape(value)}"' for key, value in attrs)
    inner = "".join(render_element(child, filled=filled) for child in list(el))
    if inner:
        return f"<{name}{attr_text}>{inner}</{name}>"
    return f"<{name}{attr_text}/>"


def render_lucide(icon_id: str, *, filled: bool) -> str:
    path = LUCIDE_DIR / f"{icon_id}.svg"
    if not path.is_file():
        raise SystemExit(f"missing Lucide icon: {icon_id}")
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S).strip()
    try:
        root = ET.fromstring(text)
        body = render_element(root, filled=filled, root=True)
    except (ET.ParseError, ValueError) as exc:
        raise SystemExit(f"{icon_id}: {exc}") from exc
    return HEADER + body + "\n"


def source_label(entry: dict, by_file: dict[str, dict]) -> str:
    if entry.get("preserve"):
        return "preserve"
    if entry.get("aliasOf"):
        return f"alias {entry['aliasOf']}"
    label = entry.get("lucide", "")
    if entry.get("fill"):
        label += " filled"
    return label


def catalog_html(entries: list[dict], by_file: dict[str, dict]) -> str:
    referenced = referenced_assets()
    cards = []
    for name in sorted(referenced):
        entry = by_file.get(name, {})
        label = html.escape(source_label(entry, by_file))
        src = html.escape(name)
        icons = "".join(
            f'<i class="icon {size}{extra}" style="--src:url(../img/{src})"></i>'
            for size, extra in (
                ("s12", ""),
                ("s16", ""),
                ("s20", ""),
                ("s24", ""),
                ("s16 is-disabled", ""),
            )
        )
        cards.append(
            f"<figure><div class=\"sizes\">{icons}</div>"
            f"<figcaption>{src}<small>{label}</small></figcaption></figure>"
        )
    return (
        """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>Stygia icon catalog</title><style>
:root{color-scheme:dark;font:14px/1.4 Inter,Segoe UI,sans-serif;background:#121212;color:#fafafa}
body{margin:0;padding:24px}h1{font-size:20px;margin:0 0 8px}p{color:#b0b0b0;margin:0 0 24px}
main{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:8px}
figure{margin:0;padding:14px;display:flex;align-items:center;gap:12px;background:#1a1a1a;border:1px solid #2e2e2e;border-radius:8px}
.sizes{display:flex;align-items:flex-end;gap:8px;flex:none}
.icon{display:block;background:#c8c8c8;mask:var(--src) center/contain no-repeat;-webkit-mask:var(--src) center/contain no-repeat}
.s12{width:12px;height:12px}.s16{width:16px;height:16px}.s20{width:20px;height:20px}.s24{width:24px;height:24px}
.is-disabled{background:#6e6e6e;opacity:.72}
figure:hover .icon:not(.is-disabled){background:#3ecf8e}
figcaption{font:11px/1.3 "JetBrains Mono",Consolas,monospace;overflow-wrap:anywhere}
small{display:block;color:#8d8d8d;font-size:10px}
</style></head><body><h1>Stygia icon catalog</h1>
<p>Lucide icons normalized for CSS masks. Each card shows 12, 16, 20 and 24 px, then 16 px disabled. Hover tints the active sizes. 16 px is the in-app glyph.</p>
<main>"""
        + "\n".join(cards)
        + "</main></body></html>\n"
    )


def expected_svg(entry: dict, by_file: dict[str, dict], rendered: dict[str, str]) -> str | None:
    if entry.get("preserve"):
        return None
    if entry.get("aliasOf"):
        source = resolve_source(entry["file"], by_file)
        return rendered[source]
    return rendered[entry["file"]]


def build_rendered(entries: list[dict], by_file: dict[str, dict]) -> dict[str, str]:
    if not LUCIDE_DIR.is_dir():
        raise SystemExit("lucide-static is not installed; run npm install")
    rendered: dict[str, str] = {}
    for entry in entries:
        if entry.get("preserve") or entry.get("aliasOf"):
            continue
        icon_id = entry.get("lucide")
        if not icon_id:
            raise SystemExit(f"{entry['file']}: needs lucide, aliasOf, or preserve")
        rendered[entry["file"]] = render_lucide(icon_id, filled=bool(entry.get("fill")))
    for entry in entries:
        if not entry.get("aliasOf"):
            continue
        source = resolve_source(entry["file"], by_file)
        if source not in rendered:
            raise SystemExit(f"{entry['file']}: alias target {source} is not generated")
        rendered[entry["file"]] = rendered[source]
    return rendered


def validate_map(entries: list[dict], by_file: dict[str, dict]) -> list[str]:
    errors: list[str] = []
    for entry in entries:
        name = entry["file"]
        modes = [bool(entry.get("lucide")), bool(entry.get("aliasOf")), bool(entry.get("preserve"))]
        if sum(modes) != 1:
            errors.append(f"{name}: set exactly one of lucide, aliasOf, preserve")
        if entry.get("fill") and not entry.get("lucide"):
            errors.append(f"{name}: fill requires lucide")
        tier = entry.get("tier")
        if tier not in {"universal", "domain", "brand"}:
            errors.append(f"{name}: tier must be universal, domain, or brand")
    return errors


def audit(entries: list[dict], by_file: dict[str, dict], rendered: dict[str, str]) -> list[str]:
    errors = validate_map(entries, by_file)
    refs = referenced_assets()
    svg_files = {path.name: path for path in IMG.glob("*.svg")}

    for missing in sorted(refs - set(by_file)):
        errors.append(f"SCSS references {missing} but it is not in icon_map.json")
    for name in sorted(set(by_file) - set(svg_files)):
        errors.append(f"mapped SVG missing on disk: {name}")
    for orphan in sorted(set(svg_files) - set(by_file)):
        errors.append(f"SVG not in icon_map.json: {orphan}")

    catalog = catalog_html(entries, by_file)
    if not CATALOG.is_file() or CATALOG.read_text(encoding="utf-8") != catalog:
        errors.append("generated icon catalog is stale: docs/icons.html")

    hashes: defaultdict[str, set[str]] = defaultdict(set)
    for name, path in sorted(svg_files.items()):
        entry = by_file.get(name)
        if entry is None or not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        expected = expected_svg(entry, by_file, rendered)
        if expected is not None and text != expected:
            errors.append(f"generated SVG is stale: {name}")
            continue
        if entry.get("preserve"):
            continue
        try:
            root = ET.fromstring(re.sub(r"<!--.*?-->", "", text, flags=re.S).strip())
        except ET.ParseError as exc:
            errors.append(f"{name}: invalid XML: {exc}")
            continue
        if root.attrib.get("viewBox") != "0 0 24 24":
            errors.append(f"{name}: expected viewBox 0 0 24 24")
        if "<image" in text or "<filter" in text or "transform=" in text:
            errors.append(f"{name}: image, filter, or transform is not mask-safe")
        normalized = re.sub(r"\s+", " ", text).strip()
        hashes[hashlib.sha256(normalized.encode()).hexdigest()].add(name)

    for names in hashes.values():
        if len(names) < 2:
            continue
        roots = {resolve_source(name, by_file) for name in names}
        if len(roots) != 1:
            errors.append("undeclared duplicate SVGs: " + ", ".join(sorted(names)))
    return errors


def generate() -> None:
    entries = load_map()
    by_file = index_entries(entries)
    rendered = build_rendered(entries, by_file)
    for name, text in rendered.items():
        (IMG / name).write_text(text, encoding="utf-8")
    CATALOG.write_text(catalog_html(entries, by_file), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="audit without writing")
    args = parser.parse_args()
    entries = load_map()
    by_file = index_entries(entries)
    if not args.check:
        generate()
    rendered = build_rendered(entries, by_file)
    errors = audit(entries, by_file, rendered)
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1
    print(
        f"icon audit passed: {len(list(IMG.glob('*.svg')))} SVG, "
        f"{len(referenced_assets())} mapped assets"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
