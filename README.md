# Stygia — phpMyAdmin Dark Theme

A dark, elegant theme for phpMyAdmin 6.x inspired by the mythological river Styx. Features a deep green accent palette, enhanced accessibility, and a clean, modern UI.

## Features

- **Deep Dark Mode** — Easy on the eyes for long database sessions
- **Stygia Green Palette** — Calming deep green accents that reduce eye strain
- **Accessibility First** — Keyboard navigation support, focus indicators, reduced motion support
- **RTL Support** — Full right-to-left language compatibility
- **Clean Typography** — Inter font for UI, Source Code Pro for code
- **Modern UI** — Subtle shadows, rounded corners, smooth transitions

## Requirements

- phpMyAdmin 6.0 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)

## Installation

1. Download the `stygia.zip` package or clone this repository
2. Extract the `stygia` folder to your phpMyAdmin themes directory:
   ```
   phpMyAdmin/
   └── themes/
       └── stygia/
           ├── css/
           ├── scss/
           ├── theme.json
           └── screen.png
   ```
3. Go to phpMyAdmin → Appearance Settings → Theme
4. Select "Stygia" from the dropdown
5. Click "Save"

## Theme Structure

```
stygia/
├── css/
│   ├── theme.css          # Compiled styles (LTR)
│   ├── theme.css.map      # Source map
│   └── theme.rtl.css      # RTL overrides
├── scss/
│   ├── theme.scss         # Main entry point
│   ├── _variables.scss    # Design tokens
│   ├── _common.scss       # Core overrides
│   ├── _navigation.scss   # Sidebar navigation
│   ├── _forms.scss        # Form elements
│   ├── _tables.scss       # Data tables
│   ├── _buttons.scss      # Buttons
│   ├── _navbar.scss       # Top navbar
│   ├── _card.scss         # Cards
│   ├── _alert.scss        # Alerts
│   ├── _codemirror.scss   # SQL editor
│   ├── _reboot.scss       # Base styles
│   ├── _print.scss        # Print styles
│   └── _icons.scss        # Icon styles
├── theme.json             # Theme metadata
└── screen.png             # Screenshot preview
```

## Customization

The theme uses SCSS variables for easy customization. Edit `scss/_variables.scss` to change:

- **Colors**: `$accent-green`, `$bg-body`, `$text-primary`, etc.
- **Typography**: `$font-family-base`, `$font-size-base`, etc.
- **Border radius**: `$border-radius`, `$border-radius-lg`, etc.
- **Shadows**: `$shadow-sm`, `$shadow-md`, `$shadow-lg`

After editing SCSS files, recompile with:

```bash
cd scss
sass theme.scss ../css/theme.css --style=compressed
```

## Color Reference

| Variable | Hex | Usage |
|----------|-----|-------|
| `$accent-green` | `#3ecf8e` | Primary accent, links, focus |
| `$bg-body` | `#121212` | Page background |
| `$bg-surface` | `#181818` | Card/input backgrounds |
| `$text-primary` | `#FAFAFA` | Main text |
| `$text-secondary` | `#b4b4b4` | Muted text |
| `$border-default` | `#2e2e2e` | Borders |

## Accessibility

- `:focus-visible` outlines for keyboard navigation
- `prefers-reduced-motion` media query support
- Skip link for screen reader users
- Color contrast ratios meeting WCAG AA standards

## License

MIT License — Free to use, modify, and distribute.

## Credits

Created for phpMyAdmin 6.x. Inspired by mythological darkness and modern database tooling aesthetics.
