# Stygia — phpMyAdmin Dark Theme

A dark, elegant theme for [phpMyAdmin](https://www.phpmyadmin.net/) 6.x inspired by the mythological river Styx. Deep green accents, accessible contrast, RTL overrides, and a dense but calm admin UI.

[![phpMyAdmin](https://img.shields.io/badge/phpMyAdmin-6.x-3ecf8e?style=flat-square)](https://www.phpmyadmin.net/)
[![License: MIT](https://img.shields.io/badge/License-MIT-2e2e2e?style=flat-square)](LICENSE)
[![Contrast](https://img.shields.io/badge/contrast-WCAG%20AA-3ecf8e?style=flat-square)](docs/DESIGN.md)

![Stygia theme preview](screen.png)

<p align="center">
  <img src="docs/tour.gif" alt="Stygia login and browse tour" width="640">
</p>

## Features

- **Deep dark surfaces** — `#121212` body, stepped elevation for cards and popovers
- **Stygia green** — `#3ecf8e` accent with a darker primary button (`#006239`) that stays readable
- **Accessible** — `:focus-visible`, `prefers-reduced-motion`, `prefers-contrast`, `forced-colors`
- **RTL overrides** — compiled from SCSS tokens, not hardcoded hex
- **Typography** — Inter for UI, JetBrains Mono for SQL (local woff2, no CDN)
- **SQL editor** — CodeMirror highlighting with five distinct hues (keyword, string, number, comment, error)
- **Branding** — In-app: single-line `phpMyAdmin - Stygia`; portfolio: Stygia mark alone

## Requirements

- phpMyAdmin 6.0 or higher
- Modern browser (Chrome, Firefox, Safari, Edge)

## Installation

1. Download `stygia.zip` from [Releases](https://github.com/horaciodominguez/stygia/releases) or clone this repository
2. Place the `stygia` folder in your phpMyAdmin themes directory:

```
phpMyAdmin/
└── themes/
    └── stygia/
        ├── css/
        ├── fonts/
        ├── img/
        ├── scss/
        ├── theme.json
        └── screen.png
```

3. phpMyAdmin → Appearance Settings → Theme → **Stygia** → Save

## Build from source

The GitHub clone compiles without a phpMyAdmin tree:

```bash
npm install
npm run build
```

Watch mode:

```bash
npm run watch
```

Package a distributable zip:

```bash
npm run zip
```

## Theme structure

```
stygia/
├── css/                 # Compiled LTR + RTL + source maps
├── fonts/               # Inter + JetBrains Mono (OFL)
├── img/                 # SVG icons + logo
├── scss/
│   ├── theme.scss       # Entry
│   ├── _variables.scss  # Design tokens
│   ├── _fonts.scss
│   ├── _icons.scss
│   ├── _login.scss
│   ├── _console.scss
│   ├── _designer.scss
│   ├── _jquery-ui.scss
│   └── ...
├── docs/DESIGN.md       # Case study + contrast notes
├── theme.json
└── screen.png
```

## Customization

Edit `scss/_variables.scss`, then:

```bash
npm run build
```

| Token | Hex | Role |
| --- | --- | --- |
| `$accent-green` | `#3ecf8e` | Links, focus, active nav |
| `$accent-green-deep` | `#006239` | Primary buttons |
| `$bg-body` | `#121212` | Page background |
| `$bg-surface` | `#1a1a1a` | Cards / inputs |
| `$bg-popover` | `#242424` | Dropdowns / datepicker |
| `$text-primary` | `#fafafa` | Body text |
| `$text-secondary` | `#c4c4c4` | Secondary text |
| `$color-success` | `#5dd39e` | Success (not the same as primary) |
| `$color-danger` | `#f07178` | Errors |
| `$color-warning` | `#f5a623` | Warnings |
| `$color-info` | `#4ecdc4` | Info |

## Accessibility

Measured on `#121212` unless noted:

| Pair | Ratio | AA |
| --- | --- | --- |
| `#fafafa` on `#121212` | ~18:1 | Pass (normal) |
| `#c4c4c4` on `#121212` | ~11:1 | Pass (normal) |
| `#a3a3a3` on `#121212` | ~7.6:1 | Pass (normal) |
| `#3ecf8e` on `#121212` | ~9.4:1 | Pass (normal) |
| `#fafafa` on `#006239` | ~7.2:1 | Pass (normal) |
| `#8a8a8a` on `#121212` | ~6.3:1 | Pass (normal) |

Keyboard focus uses a 2px green outline (`:focus-visible`). Reduced motion disables console and hover transitions. This theme cannot inject a skip link into phpMyAdmin HTML; the `.skip-link` class is styled if the host page provides one.

## License

MIT — see [LICENSE](LICENSE). Fonts: SIL Open Font License (see [fonts/README.md](fonts/README.md)).

## Credits

Created by [Horacio Dominguez](https://github.com/horaciodominguez) for phpMyAdmin 6.x. Design notes: [docs/DESIGN.md](docs/DESIGN.md).
