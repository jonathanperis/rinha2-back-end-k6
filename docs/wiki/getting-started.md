# Getting Started

## Prerequisites

- Docker

## Build

```bash
docker build -t rinha-k6 .
```

## Run

```bash
# Dev run (InfluxDB metrics) — this is the default mode
docker run --rm -e K6_INFLUXDB_ADDR=http://influxdb:8086 rinha-k6

# Production run (HTML report)
docker run --rm -e MODE=prod -e BASE_URL=http://api:9999 rinha-k6
```

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `MODE` | `dev` | Execution mode (`dev` or `prod`) |
| `BASE_URL` | `http://localhost:9999` | Target API endpoint |
| `K6_INFLUXDB_ADDR` | — | InfluxDB address (dev mode) |

## Modes

- **dev** (default): Exports metrics to InfluxDB for real-time monitoring in Grafana dashboards
- **prod**: Runs quietly and produces an HTML report

## Run with a Backend

The k6 service is included in each backend implementation's docker-compose.yml. Start any backend and k6 runs automatically:

```bash
# Example: run with the .NET implementation
cd rinha2-back-end-dotnet
docker compose up -d --build
```
