# CI/CD

The repository uses GitHub Actions for the k6 image, the GitHub Pages documentation site, and CodeQL analysis.

## Workflow map

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `main-release.yml` | Push to `main`, manual dispatch | Build and publish the multi-platform k6 image to GHCR. |
| `deploy.yml` | Push to `main`, manual dispatch | Call the shared Pages deploy workflow for the Astro docs site. |
| `codeql.yml` | Push, pull request, weekly schedule | Run JavaScript CodeQL analysis. |

## Release workflow

`main-release.yml` builds the Docker image and publishes it to GitHub Container Registry. The current workflow publishes this tag:

```text
ghcr.io/jonathanperis/rinha2-back-end-k6:latest
```

Sibling backend implementations can pull the same image so comparisons use the same stress-test profile. No SHA tag is configured in `main-release.yml` today.

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

That workflow builds the Astro site under `docs/` and publishes it to GitHub Pages after changes land on `main`.

Public documentation route:

```text
https://jonathanperis.github.io/rinha2-back-end-k6/docs/
```

## CodeQL

`codeql.yml` scans the JavaScript test code on pull requests, pushes to `main`, and a weekly Monday 03:00 UTC schedule. Treat CodeQL failures as blocking unless the finding is understood and explicitly waived.

## Branch protection

Changes to `main` go through pull requests. The repository uses rebase merge for PR completion, then GitHub Pages deploys from the updated `main` branch.

## Deployment checklist

Before merging docs or test-profile changes:

1. Build locally from `docs/` with Bun.
2. Smoke-check `/docs/` and the section routes: `/docs/getting-started/`, `/docs/configuration/`, `/docs/run-modes/`, `/docs/test-scenarios/`, and `/docs/ci-cd/`.
3. Confirm PR checks and review-bot status are clean.
4. Merge through the PR.
5. Watch the Pages deploy run for the merge commit.
6. Fetch the live `/docs/` route and verify a distinctive updated phrase.
