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
| Go | 1.25 | Builds custom k6 binary with xk6 |
| Docker | - | Multi-stage build (Go builder → Alpine runner) |
| InfluxDB | - | Metrics storage (dev mode) |
| GitHub Actions | - | CI/CD for Docker image and GitHub Pages |

## Features

- Dual-mode execution: dev (InfluxDB export) and prod (quiet k6 CLI run)
- Custom k6 binary with xk6-output-influxdb extension built from source
- 5 test scenarios covering debits, credits, validations, statements, and error handling
- Multi-platform Docker image (amd64/arm64) published to GHCR
- Shared test suite across all rinha2 backend implementations

## Getting Started

### Prerequisites

- Docker

### Quick Start

```bash
docker build -t rinha-k6 .
# Production/CI run (quiet k6 output)
docker run --rm -e MODE=prod -e BASE_URL=http://api:9999 rinha-k6
# Dev run (InfluxDB metrics)
docker run --rm -e MODE=dev -e BASE_URL=http://api:9999 -e K6_INFLUXDB_ADDR=http://influxdb:8086 rinha-k6
```

## Project Structure

```
rinha2-back-end-k6/
├── Dockerfile                  — Multi-stage: Go 1.25 Alpine builder + Alpine 3.23 runner
├── test/stress-test/
│   ├── rinha-test.js           — k6 test scenarios (5 scenarios, 318 lines)
│   └── run-test.sh             — Entrypoint (dev vs prod mode, 15s startup delay)
├── .github/workflows/
│   ├── main-release.yml        — Docker build + push to GHCR
│   ├── deploy.yml              — Deploy docs to GitHub Pages
│   └── codeql.yml              — Security scanning
├── docs/wiki/                  — Source Markdown for the public docs routes
└── docs/                       — Astro documentation site
```

## CI/CD

Three GitHub Actions workflows:

- **Main Release** — builds a multi-platform Docker image (`linux/amd64`, `linux/arm64/v8`) and pushes `ghcr.io/jonathanperis/rinha2-back-end-k6:latest`
- **Deploy** — deploys documentation site to GitHub Pages
- **CodeQL** — security and quality scanning for the JavaScript k6 script

## Source-backed audit notes

This README was checked against the current `Dockerfile`, `test/stress-test/rinha-test.js`, `test/stress-test/run-test.sh`, and `.github/workflows/*.yml`. Current non-obvious facts:

- `MODE=prod` runs `k6 run rinha-test.js --quiet`; it does not create an HTML file by itself.
- empty `MODE` is treated as dev mode and runs `k6 run rinha-test.js -o xk6-influxdb`.
- the release workflow currently publishes the `latest` GHCR tag only.
- the docs workflow delegates to the shared Pages workflow and builds from `docs/` with Bun.

## License

MIT — see [LICENSE](LICENSE)
