# Getting Started

## Prerequisites

- Docker

## Use the published image

For most backend implementations, pull the shared GHCR image and run it against your API gateway:

```bash
docker pull ghcr.io/jonathanperis/rinha2-back-end-k6:latest

docker run --rm \
  -e MODE=prod \
  -e BASE_URL=http://api:9999 \
  ghcr.io/jonathanperis/rinha2-back-end-k6:latest
```

## Build locally

Build locally when changing this repository or testing an unpublished image:

```bash
docker build -t rinha-k6 .
docker run --rm -e MODE=prod -e BASE_URL=http://api:9999 rinha-k6
```

## Dev mode with InfluxDB

Dev mode is the default when `MODE` is empty, and it requires an InfluxDB output target:

```bash
docker run --rm \
  -e MODE=dev \
  -e BASE_URL=http://api:9999 \
  -e K6_INFLUXDB_ADDR=http://influxdb:8086 \
  ghcr.io/jonathanperis/rinha2-back-end-k6:latest
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

## Run with a backend

Sibling backend implementations can include this image as their k6 service in `docker-compose.yml`. Point `BASE_URL` at the service name and port used by the API gateway or load balancer:

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

Start the backend stack, then run the k6 service using that implementation's Compose workflow.
