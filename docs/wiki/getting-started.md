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

# Production/CI run (quiet k6 output)
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
- **prod**: Runs `k6 run rinha-test.js --quiet` for a quieter CI/log path. The entrypoint does not write an HTML artifact by itself.

## Run with a Backend

Sibling backend implementations can include this image as their k6 service in `docker-compose.yml`. Start a backend stack that wires `BASE_URL` to its API/load-balancer endpoint:

```bash
# Example: run with the .NET implementation
cd rinha2-back-end-dotnet
docker compose up -d --build
```
