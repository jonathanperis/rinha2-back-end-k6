# CI/CD

The repository uses three GitHub Actions workflows covering Docker image release, GitHub Pages deployment, and security analysis.

## Workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| **main-release.yml** | Push to `main` | Build + push multi-platform Docker image to GHCR |
| **deploy.yml** | Push to `main` | Build Astro docs site and deploy to GitHub Pages |
| **codeql.yml** | Push / PR / weekly | CodeQL security and quality analysis |

## main-release.yml

Builds the xk6 Docker image for both `linux/amd64` and `linux/arm64/v8` using `docker buildx` and pushes to the GitHub Container Registry:

```
ghcr.io/jonathanperis/rinha2-back-end-k6:latest
ghcr.io/jonathanperis/rinha2-back-end-k6:{sha}
```

Sibling repos ([Rust](https://github.com/jonathanperis/rinha2-back-end-rust), [Go](https://github.com/jonathanperis/rinha2-back-end-go), [.NET](https://github.com/jonathanperis/rinha2-back-end-dotnet), [Python](https://github.com/jonathanperis/rinha2-back-end-python)) pull this image in their own CI/CD pipelines to run the full stress test after each release.

## deploy.yml

Builds the Astro docs site with `bun install && bun run build` and uploads the `docs/out/` directory to GitHub Pages:

```yaml
- uses: actions/setup-node@v6
  with:
    node-version: '22'
    cache: 'npm'
    cache-dependency-path: docs/package-lock.json

- name: Install dependencies
  run: bun install
  working-directory: docs

- name: Build
  run: bun run build
  working-directory: docs
  env:
    PUBLIC_GA_ID: ${{ secrets.PUBLIC_GA_ID }}

- uses: actions/upload-pages-artifact@v4
  with:
    path: docs/out/
```

## codeql.yml

Runs [GitHub CodeQL](https://codeql.github.com/) analysis on every push to `main`, on every pull request, and on a weekly schedule. It scans the JavaScript test code for security vulnerabilities and code quality issues.

## Branch Protection

All changes to `main` must go through a **pull request**. Direct pushes to `main` are disabled. PRs use **rebase merge only** (squash and merge commits are disabled).

## Docker Image Registry

The published image is publicly available at:

```
docker pull ghcr.io/jonathanperis/rinha2-back-end-k6:latest
```

No authentication is required to pull. The image is rebuilt and re-tagged on every push to `main`.
