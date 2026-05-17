# Run Modes

`test/stress-test/run-test.sh` selects the k6 output path from the `MODE` environment variable. The scenario profile is the same in both modes; only the output destination changes.

<div class="mode-grid" aria-label="run mode comparison">
  <div>
    <span class="signal-label">prod</span>
    <strong>quiet CI/log run</strong>
    <p>Use in CI, release jobs, and repeatable local checks where lower-noise k6 logs matter more than live telemetry.</p>
  </div>
  <div>
    <span class="signal-label">dev</span>
    <strong>InfluxDB stream</strong>
    <p>Use while tuning an implementation and watching latency or throughput in Grafana.</p>
  </div>
</div>

## `prod`: quiet CI/log run

Set `MODE=prod` to run k6 quietly through the bundled entrypoint:

```sh
docker run --rm \
  -e MODE=prod \
  -e BASE_URL=http://api:9999 \
  rinha-k6
```

The entrypoint executes:

```sh
k6 run rinha-test.js --quiet
```

Use this mode when the caller is collecting stdout or CI logs outside the container. The current entrypoint does not create an HTML report file; it only passes `--quiet` to k6.

## `dev`: InfluxDB export

Set `MODE=dev`, or leave `MODE` empty, to stream k6 metrics through the `xk6-output-influxdb` extension:

```sh
docker run --rm \
  -e MODE=dev \
  -e BASE_URL=http://api:9999 \
  -e K6_INFLUXDB_ADDR=http://influxdb:8086 \
  rinha-k6
```

The entrypoint executes:

```sh
k6 run rinha-test.js -o xk6-influxdb
```

Use this mode when an InfluxDB target is available and you want Grafana-style feedback during a tuning loop.

## Mode behavior

| `MODE` value | Behavior |
|--------------|----------|
| `prod` | Runs `k6 run rinha-test.js --quiet`. |
| `dev` | Runs `k6 run rinha-test.js -o xk6-influxdb`. |
| empty | Treated as dev mode by `run-test.sh`. |
| anything else | Fails fast with `Invalid MODE specified. Set MODE=dev or MODE=prod.` |

## Startup delay

The entrypoint prints `Tests will start in 15 seconds...` and sleeps before launching k6. That delay gives the API stack under test time to finish booting when k6 is started alongside other services.

## Docker image shape

The Dockerfile uses two stages:

1. `golang:1.25-alpine3.21` builds a custom k6 binary with `github.com/grafana/xk6-output-influxdb`.
2. `alpine:3.23` copies the binary, `rinha-test.js`, and `run-test.sh` into `/app`.

The Dockerfile creates `/reports`, but the current script does not write report files there. The image entrypoint is:

```text
/app/run-test.sh
```

Published image:

```text
ghcr.io/jonathanperis/rinha2-back-end-k6:latest
```

Supported platforms are published by the release workflow as `linux/amd64` and `linux/arm64/v8`.
