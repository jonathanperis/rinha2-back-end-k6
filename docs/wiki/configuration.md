# Configuration

The suite is configured through environment variables and the exported `options` object in `test/stress-test/rinha-test.js`. Keep operational values in code, not in the docs, then use this page as the readable map.

## Environment variables

| Variable | Default / required value | Description |
|----------|--------------------------|-------------|
| `BASE_URL` | `http://localhost:9999` | Base URL for the API under test, usually the NGINX/load-balancer endpoint. |
| `MODE` | empty value behaves like `dev` in `run-test.sh` | Run mode selector. Use `prod` for quiet CI/log runs or `dev` for InfluxDB export. |
| `K6_INFLUXDB_ADDR` | required by the xk6 output when using dev mode | InfluxDB endpoint, for example `http://influxdb:8086`. |

## Docker run examples

Build the local image:

```sh
docker build -t rinha-k6 .
```

Run against an API endpoint in production/CI mode:

```sh
docker run --rm \
  -e MODE=prod \
  -e BASE_URL=http://api:9999 \
  rinha-k6
```

Run with InfluxDB export in development mode:

```sh
docker run --rm \
  -e MODE=dev \
  -e BASE_URL=http://api:9999 \
  -e K6_INFLUXDB_ADDR=http://influxdb:8086 \
  rinha-k6
```

## Direct k6 invocation

If you have the custom k6 binary available locally, pass variables with `-e`:

```sh
k6 run \
  -e BASE_URL=http://localhost:9999 \
  test/stress-test/rinha-test.js
```

For dev output, include the xk6 InfluxDB output:

```sh
k6 run \
  -e MODE=dev \
  -e BASE_URL=http://localhost:9999 \
  -e K6_INFLUXDB_ADDR=http://localhost:8086 \
  -o xk6-influxdb \
  test/stress-test/rinha-test.js
```

## SharedArray client data

`rinha-test.js` defines five clients and their credit limits in cents. k6 loads this data through `SharedArray` so VUs share one read-only copy:

| Client | Limit |
|--------|-------|
| `1` | `100000` |
| `2` | `80000` |
| `3` | `1000000` |
| `4` | `10000000` |
| `5` | `500000` |

Those values drive the validation scenario and the balance-limit checks after debit and statement requests.

## Thresholds

The current script does **not** define hard k6 thresholds. It measures and reports behavior; sibling implementations or CI jobs can decide whether to fail a pipeline based on their own policy.

If thresholds are added later, keep the metric names aligned with the exported Trend metrics:

```js
export const options = {
  scenarios: { /* ... */ },
  thresholds: {
    debitos_duration: ['p(95)<500'],
    creditos_duration: ['p(95)<500'],
    extratos_duration: ['p(95)<200'],
    http_req_failed: ['rate<0.01'],
  },
};
```

## Entrypoint behavior

`run-test.sh` waits 15 seconds before starting k6 so a backend stack launched in the same Compose project can finish booting. It accepts only three effective states:

| `MODE` value | Command |
|--------------|---------|
| `prod` | `k6 run rinha-test.js --quiet` |
| `dev` | `k6 run rinha-test.js -o xk6-influxdb` |
| empty | same as `dev` |

Any other value exits with `Invalid MODE specified. Set MODE=dev or MODE=prod.`

## Resource boundaries

The Rinha challenge constrains the backend services, not the k6 runner. Treat k6 as the external pressure source. The API stack under test is responsible for staying inside the challenge budget.
