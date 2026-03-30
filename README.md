# rinha2-back-end-k6

Grafana **k6** stress tests for the **Rinha de Backend** challenge (2nd Edition, 2024/Q1) — Dockerized with InfluxDB metrics export.

---

## About

Stress test suite used across all Rinha de Backend implementations. Simulates transactional scenarios (debits, credits, client validations, error handling, account statements) to benchmark backend performance under load.

This test suite is used by:

- [rinha2-back-end-dotnet](https://github.com/jonathanperis/rinha2-back-end-dotnet) — C# / .NET
- [rinha2-back-end-go](https://github.com/jonathanperis/rinha2-back-end-go) — Go
- [rinha2-back-end-rust](https://github.com/jonathanperis/rinha2-back-end-rust) — Rust
- [rinha2-back-end-python](https://github.com/jonathanperis/rinha2-back-end-python) — Python

## Tech Stack

| Technology | Purpose |
|---|---|
| k6 (Grafana) | Load/stress testing |
| Go 1.23 | Builds custom k6 binary with xk6-output-influxdb |
| Docker | Multi-stage build (Go builder + Alpine runner) |
| InfluxDB | Metrics export (dev mode) |
| GitHub Actions | CI/CD for Docker image builds |

## Modes

- **Dev mode** (`MODE=dev`) — Exports metrics to InfluxDB for real-time monitoring in Grafana
- **Prod mode** (`MODE=prod`) — Runs quietly and produces an HTML report

## Getting Started

### Build

```bash
docker build -t rinha-k6 .
```

### Run

```bash
# Production mode (HTML report)
docker run --rm rinha-k6

# Dev mode (InfluxDB export)
docker run --rm -e MODE=dev -e K6_INFLUXDB_ADDR=http://influxdb:8086 rinha-k6
```

## Project Structure

```
rinha2-back-end-k6/
├── Dockerfile                 # Multi-stage: Go builder + Alpine runner
├── test/stress-test/
│   ├── rinha-test.js          # k6 test scenarios
│   └── run-test.sh            # Entrypoint (dev vs prod mode)
└── .github/workflows/         # CI/CD pipeline
```

## License

Licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
