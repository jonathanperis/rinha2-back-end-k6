# Docs

Astro static site deployed to GitHub Pages.

## Commands

Run from this directory (`docs/`):

| Command | Action |
|---|---|
| `bun install` | Install dependencies |
| `bun run dev` | Start dev server |
| `bun run build` | Build to `./out/` |
| `bun run preview` | Preview the generated `./out/` site locally |
| `bun run lint` | Run ESLint over the Astro docs source |
| `python3 ../scripts/check_docs_source_drift.py` | Verify docs copy against k6/workflow source facts |

## Environment

Copy `.env.example` to `.env` and fill in local values when needed. For local production-base smoke tests, run `NODE_ENV=production bun run build` before `bun run preview` so routes match `/rinha2-back-end-k6/`.

| Variable | Description |
|---|---|
| `PUBLIC_GA_ID` | Optional Google Analytics 4 Measurement ID |
