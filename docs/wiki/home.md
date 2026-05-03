# Home

**rinha2-back-end-k6** is the shared Grafana k6 stress test suite for the [Rinha de Backend 2024/Q1](https://github.com/jonathanperis) challenge. It validates correctness and measures throughput for all API implementations under extreme concurrency.

## What is Rinha de Backend?

Rinha de Backend is a Brazilian backend engineering challenge where participants build a fictional banking API that handles concurrent credit/debit transactions with strict resource constraints: **1.5 CPU** and **550MB RAM** total across all services.

This k6 suite is the single source of truth for stress testing — shared across all sibling implementations (Rust, Go, .NET, Python).

## Tech Stack

| Technology | Purpose |
|-----------|---------|
| `Grafana k6` | Load testing engine |
| `xk6` | Custom k6 build with InfluxDB output extension |
| `JavaScript (ES2015+)` | Test script language |
| `Docker / Alpine 3.23` | Container runtime |
| `InfluxDB` | Time-series metrics storage (dev mode) |
| `Grafana` | Real-time dashboard for metrics |

## Repository Structure

```text
rinha2-back-end-k6/
├── test/stress-test/
│   ├── rinha-test.js       # Main test file (~318 lines, 5 scenarios)
│   └── run-test.sh         # Helper script to invoke k6
├── Dockerfile              # Multi-stage: Go 1.25 + xk6 → Alpine 3.23
├── docker-compose.yml      # Dev stack (InfluxDB + Grafana)
└── .github/workflows/
    ├── main-release.yml    # Build + push multi-platform Docker image
    ├── deploy.yml          # GitHub Pages deployment
    └── codeql.yml          # Security analysis
```

## Docker Image

The test suite is published as a multi-platform Docker image (amd64 and arm64/v8) to the GitHub Container Registry:

```text
ghcr.io/jonathanperis/rinha2-back-end-k6:latest
```

Sibling repos pull this image in their `docker-compose.yml` to run the full stress test:

```sh
docker compose up k6 --build --force-recreate
```

## Key Design Patterns

- **SharedArray** — client data loaded once, shared across all VUs for efficiency
- **Custom Trend metrics** — 5 named Trend metrics track latency per endpoint type
- **Staggered start** — validation scenarios run at 0s; load scenarios ramp from 10s
- **Balance validation** — checks `saldo >= limite * -1` after each debit
- **Dual output mode** — `prod` generates an HTML report; `dev` streams to InfluxDB
