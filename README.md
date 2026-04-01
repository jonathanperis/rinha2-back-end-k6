# rinha2-back-end-k6

> Grafana k6 load test suite for the Rinha de Backend 2024/Q1 challenge with custom xk6-output-influxdb binary and dual-mode execution

[![CI](https://github.com/jonathanperis/rinha2-back-end-k6/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/jonathanperis/rinha2-back-end-k6/actions/workflows/deploy-pages.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## About

The shared load test suite used across all Rinha de Backend 2024/Q1 implementations. Simulates transactional scenarios (debits, credits, client validations, error handling, account statements) against the fictional bank API. Built with a custom k6 binary that includes the xk6-output-influxdb extension, supporting both dev mode (real-time InfluxDB + Grafana dashboards) and prod mode (HTML report output).

## Tech Stack

| Technology | Version | Purpose |
|-----------|---------|---------|
| Grafana k6 | - | Load and stress testing |
| xk6-output-influxdb | - | Custom k6 extension for InfluxDB metrics export |
| Go | 1.23 | Builds custom k6 binary with xk6 |
| Docker | - | Multi-stage build (Go builder + Alpine runner) |
| InfluxDB | - | Metrics storage (dev mode) |
| GitHub Actions | - | CI/CD for Docker image and GitHub Pages |

## Features

- Dual-mode execution: dev (InfluxDB export) and prod (HTML report)
- Custom k6 binary with xk6-output-influxdb extension built from source
- Test scenarios covering debits, credits, validations, and error handling
- Dockerized for consistent execution across environments
- Shared test suite across all rinha2 backend implementations

## Getting Started

### Prerequisites

- Docker

### Quick Start

```bash
docker build -t rinha-k6 .
# Production run (HTML report)
docker run --rm rinha-k6
# Dev run (InfluxDB metrics)
docker run --rm -e MODE=dev -e K6_INFLUXDB_ADDR=http://influxdb:8086 rinha-k6
```

## Project Structure

```
rinha2-back-end-k6/
├── Dockerfile                  — Multi-stage: Go builder + Alpine runner
├── test/stress-test/
│   ├── rinha-test.js           — k6 test scenarios
│   └── run-test.sh             — Entrypoint (dev vs prod mode)
└── .github/workflows/          — CI/CD pipelines
```

## CI/CD

Two GitHub Actions workflows: `deploy-pages.yml` deploys test results to GitHub Pages, and `main-release.yml` builds and publishes the Docker image on the main branch.

## License

MIT — see [LICENSE](LICENSE)
