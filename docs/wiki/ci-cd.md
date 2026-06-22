# CI/CD

The repository uses GitHub Actions for the k6 image, the GitHub Pages documentation site, CodeQL analysis, and docs/source drift checks.

## Workflow map

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `main-release.yml` | Push to `main`, manual dispatch | Build and publish the multi-platform k6 image to GHCR. |
| `deploy.yml` | Push to `main`, manual dispatch | Call the shared Pages deploy workflow for the Astro docs site. |
| `codeql.yml` | Push, pull request, weekly schedule | Run JavaScript CodeQL analysis. |
| `docs-drift.yml` | Push and pull request paths that touch code/docs facts | Verify README, agent notes, and Pages docs against source-backed k6/workflow facts. |

## Release workflow

`main-release.yml` builds the Docker image and publishes it to GitHub Container Registry. The current workflow publishes this tag:

```text
ghcr.io/jonathanperis/rinha2-back-end-k6:latest
```

Sibling backend implementations can pull the same image so comparisons use the same stress-test profile. No SHA tag is configured in `main-release.yml` today. The workflow publishes `linux/amd64` and `linux/arm64/v8` platforms.

## Pages deploy workflow

`deploy.yml` delegates publishing to the shared workflow:

```yaml
jobs:
  deploy:
    uses: jonathanperis/.github/.github/workflows/pages-docs-deploy.yml@main
    secrets: inherit
    with:
      package-manager: bun
```

That workflow builds the Astro 7 static site under `docs/` with Bun and publishes it to GitHub Pages after changes land on `main`. Astro 7's Rust compiler, default Rust/Sätteri Markdown pipeline, Vite 8/Rolldown bundling, and queued rendering are adopted by the framework upgrade. Route caching, CDN cache providers, and `src/fetch.ts` advanced routing are not configured because this repository publishes static Pages output rather than an SSR/edge runtime.

Public documentation route:

```text
https://jonathanperis.github.io/rinha2-back-end-k6/docs/
```

## Docs drift check

`docs-drift.yml` runs `python3 scripts/check_docs_source_drift.py`. The script checks the documented scenario names, Trend metrics, run modes, Docker image tag, release platforms, and homepage metric copy against the current source files.

## CodeQL

`codeql.yml` scans the JavaScript test code on pull requests, pushes to `main`, and a weekly Monday 03:00 UTC schedule. Treat CodeQL failures as blocking unless the finding is understood and explicitly waived.

## Branch protection

The repository is configured for rebase merges and required status checks on `main`. Operationally, changes should go through pull requests before landing on `main`, then GitHub Pages deploys from the updated branch.

## Deployment checklist

Before merging docs or test-profile changes:

1. Build locally from `docs/` with Bun.
2. Smoke-check `/docs/` and the section routes: `/docs/getting-started/`, `/docs/configuration/`, `/docs/run-modes/`, `/docs/test-scenarios/`, and `/docs/ci-cd/`.
3. Confirm Docs Drift, CodeQL, and review-bot status are clean.
4. Merge through the PR.
5. Watch the Pages deploy run for the merge commit.
6. Fetch the live `/docs/` route and verify a distinctive updated phrase.
