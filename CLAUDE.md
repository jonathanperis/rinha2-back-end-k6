# Rinha de Backend K6 — Claude Code Guide

Grafana k6 load testing suite for the Rinha de Backend 2024/Q1 challenge. Shared across all backend implementations (Rust, .NET, Go, Python).

---

## Tech Stack

| Technology | Purpose |
|-----------|---------|
| k6 | Load testing framework |
| xk6-output-influxdb | InfluxDB metrics extension |
| Go 1.25 | Custom k6 binary builder |
| JavaScript (ES6) | Test scripts |
| Docker | Multi-stage build (Go → Alpine) |
| InfluxDB | Metrics storage (dev mode) |

---

## Run Commands

```sh
docker build -t rinha-k6 .                                      # Build
docker run --rm -e BASE_URL=http://api:9999 rinha-k6             # Run (prod mode)
docker run --rm -e MODE=dev -e K6_INFLUXDB_ADDR=http://influx:8086 rinha-k6  # Dev mode
```

---

## Test Scenarios

| Scenario | VUs | Duration | Purpose |
|----------|-----|----------|---------|
| Validacoes | 5 | 1 iteration each | Comprehensive workflow per client |
| Cliente Nao Encontrado | 1 | 1 iteration | 404 error handling |
| Debitos | 1→220 ramp | 4 minutes | Debit transactions + overdraft |
| Creditos | 1→110 ramp | 4 minutes | Credit transactions |
| Extratos | 10 | 1 iteration each | Statement retrieval |

---

## Execution Modes

| Mode | Output | Use Case |
|------|--------|----------|
| `prod` | HTML report (stdout) | CI/CD pipeline |
| `dev` | InfluxDB export | Real-time monitoring with Grafana |

---

## Key Patterns

- **SharedArray** for client data (read-only, shared across VUs)
- **Custom Trend metrics** (5): debitos, creditos, extratos, validacoes, cliente_nao_encontrado
- **Staggered start**: validations at 0s, load scenarios at 10s
- **Balance validation**: `saldo >= limite * -1` (overdraft protection)
- **Invalid request tests**: decimal valor, invalid tipo, oversized descricao, empty/null descricao

---

## Project Structure

```
rinha2-back-end-k6/
├── test/stress-test/
│   ├── rinha-test.js    # Main test suite (318 lines, 5 scenarios)
│   └── run-test.sh      # Mode dispatcher (dev/prod)
├── Dockerfile            # Multi-stage: Go 1.25 + xk6 → Alpine 3.23
├── .github/workflows/
│   ├── main-release.yml  # Docker build + push to GHCR
│   ├── main-build.yml    # Deploy docs to GitHub Pages
│   ├── deploy-docs.yml   # Wiki → HTML doc generation
│   └── codeql.yml        # Security scanning
├── docs/                 # Generated documentation site
└── wiki/                 # Source wiki pages
```

---

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `MODE` | `dev` | Execution mode (dev/prod) |
| `BASE_URL` | `http://localhost:9999` | Target API endpoint |
| `K6_INFLUXDB_ADDR` | — | InfluxDB address (dev mode) |

---

## CI/CD

- **Main:** Multi-platform Docker build (amd64/arm64) → push to GHCR
- **Image:** `ghcr.io/jonathanperis/rinha2-back-end-k6:latest`
- **Docs:** Wiki auto-converted to HTML → GitHub Pages

---

## Workflow & Conventions

- **All changes** must go through a **branch + PR** strategy (never push directly to main)
- **PRs are rebase only** — no merge commits, no squash merges
- **Use `gh` CLI** for all GitHub operations (repos, PRs, checks, merges, releases)
- **Repo-wide files** (SECURITY.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md, FUNDING.yml, etc.) live in the org-level `.github` repo — do not create them in this repository
