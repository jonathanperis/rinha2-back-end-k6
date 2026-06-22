# Docs

Astro 7 static site deployed to GitHub Pages. The site uses Astro's default Rust-powered compiler/Markdown pipeline and keeps the deployment target static, so SSR-only route caching/CDN providers and `src/fetch.ts` are intentionally not configured.

## Commands

Run from this directory (`docs/`):

| Command | Action |
|---|---|
| `bun install` | Install dependencies |
| `bun run dev` | Start foreground dev server |
| `bun run dev:bg` | Start Astro 7's managed background dev server for agent-friendly local checks |
| `bun run dev:status` | Show the managed dev server URL/PID/uptime |
| `bun run dev:logs` | Print managed background dev server logs |
| `bun run dev:stop` | Stop the managed background dev server |
| `bun run build` | Build to `./out/` |
| `bun run preview` | Preview the generated `./out/` site locally |
| `bun run lint` | Run ESLint over the Astro docs source |
| `python3 ../scripts/check_docs_source_drift.py` | Verify docs copy against k6/workflow source facts |

## Environment

Copy `.env.example` to `.env` and fill in local values when needed. Astro 7 requires Node.js `>=22.12.0`; use Node 22+ for local builds/previews and keep Bun as the dependency manager. For local production-base smoke tests, run `NODE_ENV=production bun run build` before `bun run preview` so routes match `/rinha2-back-end-k6/`.

| Variable | Description |
|---|---|
| `PUBLIC_GA_ID` | Optional Google Analytics 4 Measurement ID |
