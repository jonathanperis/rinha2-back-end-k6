# rinha2-back-end-k6

> Grafana k6 load test suite for the Rinha de Backend 2024/Q1 challenge with a custom xk6-output-influxdb binary and dual-mode execution

[![Deploy](https://github.com/jonathanperis/rinha2-back-end-k6/actions/workflows/deploy.yml/badge.svg)](https://github.com/jonathanperis/rinha2-back-end-k6/actions/workflows/deploy.yml) [![Main Release](https://github.com/jonathanperis/rinha2-back-end-k6/actions/workflows/main-release.yml/badge.svg)](https://github.com/jonathanperis/rinha2-back-end-k6/actions/workflows/main-release.yml) [![CodeQL](https://github.com/jonathanperis/rinha2-back-end-k6/actions/workflows/codeql.yml/badge.svg)](https://github.com/jonathanperis/rinha2-back-end-k6/actions/workflows/codeql.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**[Live demo →](https://jonathanperis.github.io/rinha2-back-end-k6/)** | **[Documentation →](https://jonathanperis.github.io/rinha2-back-end-k6/docs/)**

---

## About

The shared load test suite used across all Rinha de Backend 2024/Q1 implementations. Simulates transactional scenarios (debits, credits, client validations, error handling, account statements) against the fictional bank API. Built with a custom k6 binary that includes the xk6-output-influxdb extension, supporting both dev mode (real-time InfluxDB/Grafana streams) and prod mode (quiet k6 CLI output for CI logs).

## Tech Stack

| Technology | Version | Purpose |
|-----------|---------|---------|
| Grafana k6 | - | Load and stress testing |
| xk6-output-influxdb | - | Custom k6 extension for InfluxDB metrics export |
| Go | 1.25 on Alpine 3.21 | Builds custom k6 binary with xk6 |
| Docker | - | Multi-stage build (Go 1.25 Alpine 3.21 builder → Alpine 3.23 runner) |
| InfluxDB | - | Metrics storage (dev mode) |
| GitHub Actions | - | CI/CD for Docker image and GitHub Pages |

## Features

- Dual-mode execution: dev (InfluxDB export) and prod (quiet k6 CLI run)
- Custom k6 binary with xk6-output-influxdb extension built from source
- 5 source-backed k6 scenarios: `validacoes`, `cliente_nao_encontrado`, `debitos`, `creditos`, and `extratos`
- Multi-platform Docker image (amd64/arm64) published to GHCR
- Shared test suite across all rinha2 backend implementations

## Getting Started

### Prerequisites

- Docker

### Quick Start

Use the published image when you only need to run the shared load suite:

```bash
docker pull ghcr.io/jonathanperis/rinha2-back-end-k6:latest

# Production/CI run (quiet k6 output)
docker run --rm \
  -e MODE=prod \
  -e BASE_URL=http://api:9999 \
  ghcr.io/jonathanperis/rinha2-back-end-k6:latest
```

Build locally when changing this repository:

```bash
docker build -t rinha-k6 .
docker run --rm -e MODE=prod -e BASE_URL=http://api:9999 rinha-k6
```

Use dev mode only when an InfluxDB endpoint is available. Empty `MODE` is treated as dev mode by `run-test.sh`:

```bash
docker run --rm \
  -e MODE=dev \
  -e BASE_URL=http://api:9999 \
  -e K6_INFLUXDB_ADDR=http://influxdb:8086 \
  ghcr.io/jonathanperis/rinha2-back-end-k6:latest
```

## Project Structure

```
rinha2-back-end-k6/
├── Dockerfile                  — Multi-stage: Go 1.25 Alpine 3.21 builder + Alpine 3.23 runner
├── test/stress-test/
│   ├── rinha-test.js           — k6 test scenarios (5 scenarios, 5 Trend metrics)
│   └── run-test.sh             — Entrypoint (dev vs prod mode, 15s startup delay)
├── .github/workflows/
│   ├── main-release.yml        — Docker build + push to GHCR
│   ├── deploy.yml              — Deploy docs to GitHub Pages
│   └── codeql.yml              — Security scanning
├── docs/wiki/                  — Source Markdown for the public docs routes
└── docs/                       — Astro documentation site
```

## Docker Compose Service Example

Sibling backend repositories can wire the published image into their Compose stack and point `BASE_URL` at the API gateway/load balancer:

```yaml
services:
  k6:
    image: ghcr.io/jonathanperis/rinha2-back-end-k6:latest
    environment:
      MODE: prod
      BASE_URL: http://nginx:9999
    depends_on:
      - nginx
```

Switch to `MODE=dev` and add `K6_INFLUXDB_ADDR` only when the Compose stack also provides InfluxDB.

## CI/CD

Four GitHub Actions workflows:

- **Main Release** — builds a multi-platform Docker image (`linux/amd64`, `linux/arm64/v8`) and pushes `ghcr.io/jonathanperis/rinha2-back-end-k6:latest`
- **Deploy** — deploys documentation site to GitHub Pages
- **CodeQL** — security and quality scanning for the JavaScript k6 script
- **Docs Drift** — verifies README, agent notes, and Pages docs against source-backed k6/workflow facts

## Source-backed audit notes

This README was checked against the current `Dockerfile`, `test/stress-test/rinha-test.js`, `test/stress-test/run-test.sh`, and `.github/workflows/*.yml`. Current non-obvious facts:

- `MODE=prod` runs `k6 run rinha-test.js --quiet`; it does not create an HTML file by itself.
- empty `MODE` is treated as dev mode and runs `k6 run rinha-test.js -o xk6-influxdb`.
- the release workflow currently publishes the `latest` GHCR tag only for `linux/amd64` and `linux/arm64/v8`.
- the docs workflow delegates to the shared Pages workflow and builds from `docs/` with Bun.
- `scripts/check_docs_source_drift.py` guards public docs against stale scenario names, run modes, image tags, platforms, and homepage metrics.

## License

MIT — see [LICENSE](LICENSE)
