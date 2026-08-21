# Stygia design notes

phpMyAdmin is a dense, all-day tool. Most “dark themes” for it are inverted light UIs: low contrast greys, leftover PNGs, and a syntax highlighter that paints every token the same accent. Stygia is a CSS/image-only theme for 6.x that tries to feel like a modern database product without touching phpMyAdmin JavaScript.

## Constraints

- No theme JS. phpMyAdmin owns the DOM.
- Icons are CSS `mask-image` over SVG so hover and semantic states can recolor a single asset.
- Compilation must work from a GitHub clone (`npm install && npm run build`), not only from inside a phpMyAdmin tree.

## Decisions

**Branding = both, different jobs.**

| Surface | What shows | Why |
| --- | --- | --- |
| Login / sidebar | River-mark badge + CSS lockup `phpMyAdmin · STYGIA` | User must know they are still in phpMyAdmin; Stygia is the skin |
| GitHub / README / OG | Stygia mark alone (`logo-mark.svg`) | You are selling the theme, not rebranding the host app |

Replacing the host logo entirely with “Stygia” looked like a fork. Showing only phpMyAdmin hid the theme authorship. The combined lockup fixes both.

phpMyAdmin may still inject an `<h1>phpMyAdmin</h1>` (especially after legacy PNG logos are gone). The in-app wordmark is therefore drawn with CSS (`::before` / `::after` on `a.logo`), and the host `<img>` / heading is clipped — not layered as a second `background-image` on the same `<img>`.

**Green is the accent, not every meaning.** Primary buttons use a deep green (`#006239`) so white label text stays AA. Success, info, strings and numbers get their own hues so SQL and alerts are scannable.

**Typed cells share the editor palette.** Browse `td[data-type]`, insert/edit inputs, structure Type labels, and CodeMirror all use [One Dark Pro](https://github.com/Binaryify/OneDark-Pro) classic tokens (`scss/_datatypes.scss`, `scss/_codemirror.scss`). An integer in a result grid and a number in SQL should read as the same family.

**Tokens are inspectable.** Sass tokens in `_variables.scss` are mirrored to `:root` as `--stygia-*` custom properties for DevTools debugging and future theming hooks.

**Weight is hierarchy, not decoration.** Body is 400. Paragraphs, helper text and small print are 300 (Inter 300 is bundled). Headings and table headers are 500. 600 is for brand lockups, not every label.

**Bundled fonts vs optional Nerd Font.** Inter and JetBrains Mono ship as woff2 so a clone works with no extra install. The stack *prefers* system `FiraCode Nerd Font` (Propo for UI, Mono for SQL) when present — a local trial, not a CDN. Remove those names in `_variables.scss` to force the bundled faces.

**Pill only for the verb.** Go/Save stay pill-shaped. phpMyAdmin’s `.nav-pills` (Browse / Structure / SQL / …) are underline tabs: transparent track, 2px accent underline, icons that follow the active color. Toolbars, icon buttons and DataTables use a 6px radius so dense chrome does not look like a marketing site.

**Console opens on purpose.** Expanding `#pma_console_container` on `:hover` made the query log jump while moving the pointer toward the bottom of the page. It now opens only with `.expanded`. Width is `left: $navi-width; right: 0` (not `calc(100% - 240px)`). Collapsed, the prompt ghost is hidden.

**Hit targets without inflating desktop.** Chrome and sidebar glyphs stay ~14px inside 28–32px flex boxes. Tree item controls (`.navItemControls`) stay hidden until hover/`focus-within` so the navi tree does not shout.

## Before / after (v1 → v2)

- Missing PNG/GIF icon maps → SVG set + mask coloring
- Inter/Space Mono declared but never loaded → local Inter + JetBrains Mono woff2
- `screen.png` was a solid green square → UI preview
- `author: "Personal"`, no LICENSE file → MIT + repo URL
- Bootstrap imported from `../../bootstrap` → npm `bootstrap@5.3.3`

## v2.1.0 (this release)

- 20 usability passes: responsive shell, contrast, forms flex, modal dedupe, asset cleanup
- Login/sidebar identity redraw (mark + lockup, no double wordmark)
- Underline tabs instead of green pills
- One Dark Pro colors on typed cells *and* CodeMirror
- Optional FiraCode Nerd Font; Inter 300 for light copy
- Orphan PMA PNGs removed from `img/`

## What this theme cannot do

phpMyAdmin does not let a theme add a skip link, swap the server-rendered logo file, or restyle jqPlot canvases beyond CSS around them. Those remain host-app limits, not unfinished CSS.
