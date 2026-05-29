# DESIGN.md

## Design Intent

The public site should feel like an operator-grade load-test console for the Rinha de Backend challenge. Preserve the current CRT terminal aesthetic, but make the system more disciplined: fewer fake signals, more source-backed data, stronger accessibility, and clearer developer paths.

The target feel is **controlled failure lab**, not generic hacker theater.

## Register

brand

The homepage is a brand surface for a developer tool. It can be visually intense and memorable, but every metric, scenario, and command should earn trust.

## Physical Scene Sentence

A backend developer is staring at a dark monitor late at night, comparing a Rinha implementation against a reproducible k6 load profile, with terminal output and Grafana nearby. This scene supports a dark interface with high-contrast green instrumentation, warning accents, and restrained motion.

## Visual Anchors

Use these as directional references, not as copies:

- CRT terminal boot screens and old monochrome monitors.
- Grafana/k6 performance instrumentation, especially panels that make load, latency, and scenario state readable.
- Operator consoles and lab instrumentation, where visual drama is secondary to confidence in the reading.
- Rinha challenge culture: adversarial, resource-constrained, backend-focused, and direct.

## Current Aesthetic to Preserve

- Dark green-black background.
- Neon terminal green as the main brand signal.
- Monospace UI language.
- CRT scanline texture, used carefully.
- Warning amber and error red/pink accents.
- Large punchy developer headline.
- Terminal panels, scenario panels, command blocks, and metric readouts.

## Color Strategy

**Committed dark terminal palette.** Green carries the identity across more than 10% of the surface, but it should feel like instrumentation, not decoration.

Use OKLCH for new or refactored tokens. Existing hex colors may remain during migration, but new design work should prefer semantic OKLCH tokens.

Recommended semantic palette:

```css
:root {
  color-scheme: dark;

  --color-bg-deep: oklch(12% 0.025 145);
  --color-bg-surface: oklch(16% 0.035 145);
  --color-bg-panel: oklch(18% 0.045 145);

  --color-text-primary: oklch(88% 0.11 145);
  --color-text-secondary: oklch(72% 0.09 145);
  --color-text-muted: oklch(58% 0.075 145);

  --color-signal-green: oklch(86% 0.28 145);
  --color-signal-green-dim: oklch(62% 0.18 145);
  --color-warning: oklch(82% 0.18 82);
  --color-danger: oklch(68% 0.24 18);
  --color-info: oklch(76% 0.17 230);

  --color-border-subtle: oklch(72% 0.12 145 / 0.18);
  --color-border-strong: oklch(82% 0.23 145 / 0.58);
  --color-glow-green: oklch(86% 0.28 145 / 0.35);
}
```

Never use pure `#000` or pure `#fff`. Neutrals should stay slightly green-tinted.

## Typography

The brand can remain monospace-forward because the product is a k6 terminal-oriented developer tool. Use monospace deliberately, not as a generic technical costume.

Recommended role split:

- Display and UI chrome: current terminal monospace direction.
- Code, commands, metric names: monospace required.
- Longer explanatory paragraphs: either a readable mono with generous line-height or a restrained sans if readability suffers.

Current imported fonts include Fira Code, Inter, and JetBrains Mono. The CSS currently references `Share Tech Mono` without importing it, so either import it explicitly or remove the reference during redesign.

Rules:

- Keep body line length around 65 to 75 characters.
- Avoid all-caps paragraphs.
- Use uppercase for short labels, terminal chrome, and CTA flavor only.
- Make display text huge when needed, but reduce glitch/shadow intensity enough to preserve legibility.

## Layout Principles

- Lead with one decisive hero message and one clear developer action.
- Put a real command or quick-start path above the first major scroll.
- Prefer dashboard rows, scenario matrices, command panels, and terminal readouts over generic feature cards.
- Avoid identical card grids unless the data is genuinely tabular and the repeated shape helps comparison.
- Avoid thick side-tab borders. Use full terminal borders, labeled rows, numeric indexes, background tints, or corner brackets instead.
- Consolidate repeated GitHub/docs links into a clear CTA hierarchy.

Recommended homepage order:

1. Hero with headline, exact subhead, primary action, secondary action.
2. Quick-start terminal with prod and dev commands.
3. Scenario matrix with all five scenarios.
4. Mode split for prod vs dev.
5. Custom Trend metrics panel.
6. CI, GHCR, docs, and source proof row.
7. Footer.

## Component Direction

### Hero

Keep the headline: “IT WORKED ON YOUR MACHINE. NOT ON OURS.”

Supporting copy should be precise:

- Mention Grafana k6.
- Mention Rinha de Backend 2024/Q1.
- Mention debit, credit, statement, validation, and missing-client scenarios.
- Mention custom Trend metrics only if it fits naturally.

### CTA System

Primary CTA should describe the real action.

Preferred labels:

- `Run the suite`
- `Read quick start`
- `Copy Docker command`

Avoid making the primary CTA sound like it performs an action when it only opens docs.

### Terminal Panels

Terminal panels should show real commands, real mode names, real scenario names, or clearly labeled sample output. Avoid fake live telemetry unless it is visibly decorative.

Good terminal content:

```sh
MODE=prod BASE_URL=http://api:9999 /app/run-test.sh
scenario: debitos target=220VUs
trend: debitos_duration
```

### Scenario Matrix

Use the canonical five scenarios:

| Scenario | Shape | Purpose |
|---|---|---|
| `validacoes` | 5 VUs, one iteration | Client validation workflow |
| `cliente_nao_encontrado` | 1 VU, one iteration | 404 behavior |
| `debitos` | ramping to 220 VUs | Debit transactions and overdraft checks |
| `creditos` | ramping to 110 VUs | Credit transactions |
| `extratos` | 10 VUs, one iteration | Statement reads |

### Mode Split

Use a two-panel comparison:

- `prod`: quiet k6 CLI output for CI logs and repeatable runs.
- `dev`: InfluxDB export for Grafana dashboards.

### Metrics Panel

Show the five custom Trend metrics as real instrumentation:

- `debitos_duration`
- `creditos_duration`
- `extratos_duration`
- `validacoes_duration`
- `cliente_nao_encontrado_duration`

## Motion

Motion should feel like terminal boot or instrumentation coming online, not arcade effects.

Allowed:

- One page-load reveal for hero/terminal content.
- Cursor blink in terminal surfaces.
- Subtle scanline texture.
- Small hover transitions on links and buttons.

Avoid:

- Constant global flicker.
- Large repeated transforms.
- Layout-property animation.
- Motion that affects long-reading sections.

Required:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    scroll-behavior: auto !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Accessibility Standards

- Maintain WCAG AA contrast at minimum, preferably higher because the palette is dark and neon.
- Provide visible `:focus-visible` states for all links and buttons.
- Do not rely on color alone for status. Pair color with text such as `WARN`, `ERR`, `OK`, or icons with accessible names.
- Keep interactive target sizes comfortable on mobile.
- Do not place scanlines or flicker over long-form reading content if it reduces legibility.
- External links should be clear in context when they open GitHub or CI pages.

## Copy Standards

- Every claim should be source-backed or explicitly labeled.
- Prefer exact scenario and metric names over adjectives.
- Keep the punchy headline, then make supporting copy operational.
- Avoid generic hype words: “extreme”, “massive”, “absolute chaos”, “breaking point”, “seamless”, “powerful”.
- Avoid em dashes in user-facing copy.

## Known Current Issues to Address in Redesign

- Keep homepage numbers source-backed whenever the k6 script changes.
- `.stat-box` uses a thick left border accent, which should be replaced.
- CRT flicker and scanlines are global and always-on.
- The final stress-test panel has softer rounded styling than the sharper terminal system.
- Design tokens contain legacy names such as `--rust-orange` for green values.
- `Share Tech Mono` is referenced but not imported.

## Quality Bar

A strong redesign should pass these checks:

1. Could a skeptical Rinha participant verify every metric against the script?
2. Can a developer identify the run command within 10 seconds?
3. Does the page still feel like a hostile terminal for fragile backends?
4. Is the visual noise controlled enough for sustained reading?
5. Would the page look custom even if all decorative animations were disabled?
