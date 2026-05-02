# rinha2-back-end-k6

Grafana k6 load test suite for the Rinha de Backend 2024/Q1 challenge. Shared across all backend implementations to benchmark API performance under concurrent transactional workloads.

## Wiki Pages

| Page | Description |
|------|-------------|
| [Getting StartedL(Getting-Started.md) | Prerequisites, environment variables, and how to run |
| [Test ScenariosL(Test-Scenarios.md) | What scenarios are tested and how |
| [CI/CD PipelineL(CI-CD-Pipeline.md) | GitHub Actions workflows |

## Key Features

- Custom k6 binary with xk6-output-influxdb extension built from source
- Dual-mode execution: dev (InfluxDB export) and prod (HTML report)
- 5 test scenarios covering debits, credits, validations, statements, and error handling
- Multi-platform Docker image (amd64/arm64) published to GHCR
- Shared test suite across all rinha2 backend implementations

---

*[GitHubL(https://github.com/jonathanperis/rinha2-back-end-k6.md) · [Jonathan Peris](https://jonathanperis.github.io/)*
