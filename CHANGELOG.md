# Changelog

## 2.0.0 — 2026-08-13

Standalone, portfolio-ready release of Stygia for phpMyAdmin 6.x.

- Compile with `npm install && npm run build` (Bootstrap 5.3.3 via npm)
- Replace missing PNG/GIF icon maps with SVG + `mask-image`
- Load Inter and JetBrains Mono as local woff2
- Semantic colors distinct from the accent (success, info, SQL hues)
- Branded login, SVG mark, real `screen.png`
- In-app logo is single-line **phpMyAdmin - Stygia**; portfolio mark alone for GitHub/docs
- jQuery UI, designer, charts, and RTL compiled from tokens
- Console expands only when `.expanded` (no hover trap)
- WCAG AA contrast pass for body, links, and primary buttons
- MIT `LICENSE`, GitHub Actions zip, design notes in `docs/DESIGN.md`

## 1.0.0

Initial dark theme (tokens + PMA overrides).
