# CI/CD Pipeline

## Workflows

This repository uses three GitHub Actions workflows:

### deploy.yml

- **Trigger:** Push to main branch or workflow dispatch
- **Steps:** Deploys documentation site to GitHub Pages using `actions/deploy-pages`
- **Purpose:** Publish project documentation for public viewing

### main-release.yml

- **Trigger:** Push to main branch
- **Steps:** Builds multi-platform Docker image (amd64/arm64) and pushes to GHCR
- **Image:** `ghcr.io/jonathanperis/rinha2-back-end-k6:latest`
- **Purpose:** Automated release of the load test container

### codeql.yml

- **Trigger:** Push to main branch, pull requests, and weekly schedule
- **Steps:** Runs CodeQL security and quality analysis for JavaScript
- **Purpose:** Automated vulnerability detection and code quality scanning
