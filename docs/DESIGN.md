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
| Sidebar / login | Single-line lockup `phpMyAdmin - Stygia` | User must know they are still in phpMyAdmin; Stygia is the skin |
| GitHub / README / OG | Stygia mark alone (`logo-mark.svg`) | You are selling the theme, not rebranding the host app |

Replacing the host logo entirely with “Stygia” looked like a fork. Showing only phpMyAdmin hid the theme authorship. The combined lockup fixes both.

**Green is the accent, not every meaning.** Primary buttons use a deep green (`#006239`) so white label text stays AA. Success, info, strings and numbers get their own hues so SQL and alerts are scannable.

**Pill only for the verb.** Go/Save stay pill-shaped. Toolbars, icon buttons and DataTables use an 6px radius so dense chrome does not look like a marketing site.

**Console opens on purpose.** Expanding `#pma_console_container` on `:hover` made the query log jump while moving the pointer toward the bottom of the page. It now opens only with `.expanded`.

## Before / after (v1 → v2)

- Missing PNG/GIF icon maps → SVG set + mask coloring
- Inter/Space Mono declared but never loaded → local Inter + JetBrains Mono woff2
- `screen.png` was a solid green square → UI preview
- `author: "Personal"`, no LICENSE file → MIT + repo URL
- Bootstrap imported from `../../bootstrap` → npm `bootstrap@5.3.3`

## What this theme cannot do

phpMyAdmin does not let a theme add a skip link, swap the server-rendered logo file, or restyle jqPlot canvases beyond CSS around them. Those remain host-app limits, not unfinished CSS.
