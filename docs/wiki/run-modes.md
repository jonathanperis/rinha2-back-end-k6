# Run Modes

The suite supports two output modes controlled by the `MODE` environment variable. Both modes run the same 5 scenarios — only the output destination differs.

## prod — HTML Report

The default mode. k6 runs the full test suite and generates a self-contained **HTML report** at the end. This is used in CI/CD workflows where the report is archived as a build artifact or published to GitHub Pages.

```sh
# Run with prod mode (default)
docker compose up k6 --build --force-recreate

# Or directly:
k6 run -e MODE=prod test/stress-test/rinha-test.js
```

The HTML report includes:

- Request rate, VU count, and iteration timeline
- HTTP response time percentiles (p50, p90, p95, p99)
- Per-scenario breakdown
- Custom Trend metric charts (all 5 named metrics)
- Check pass/fail counts

## dev — InfluxDB + Grafana

Development mode streams all metrics in real time to **InfluxDB**, which is visualised in **Grafana** via a pre-configured dashboard. This is ideal for iterative tuning — you can watch latency graphs live as you adjust the API under test.

```sh
# Start the full dev stack (k6 + InfluxDB + Grafana)
MODE=dev docker compose up --build

# Or pass variables explicitly:
k6 run \
  -e MODE=dev \
  -e K6_INFLUXDB_ADDR=http://localhost:8086 \
  test/stress-test/rinha-test.js
```

## Dev Stack Services

| Service | Port | Purpose |
|---------|------|---------|
| **k6** | — | Runs test scenarios, streams metrics to InfluxDB |
| **InfluxDB** | 8086 | Time-series storage for k6 metrics |
| **Grafana** | 3000 | Real-time dashboards (k6 + system metrics) |

## run-test.sh

A convenience shell script at `test/stress-test/run-test.sh` wraps the `k6 run` invocation with the correct flags, handling both modes and setting `BASE_URL` from the first argument (defaulting to `http://localhost:9999`):

```sh
./test/stress-test/run-test.sh http://localhost:9999
```

## Docker Image

The Dockerfile uses a **multi-stage build**:

1. **Stage 1** — `golang:1.25-alpine`: builds xk6 with the InfluxDB output extension
2. **Stage 2** — `alpine:3.23`: copies the compiled `k6` binary and test scripts

The final image is minimal (~30MB) and published as:

```
ghcr.io/jonathanperis/rinha2-back-end-k6:latest
```

Supported platforms: `linux/amd64`, `linux/arm64/v8`.
