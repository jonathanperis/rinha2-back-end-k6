# Configuration

The test suite is configured entirely through **environment variables**, making it easy to switch between local development and CI/CD production runs without modifying any test code.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MODE` | `prod` | Run mode: `prod` (HTML report) or `dev` (InfluxDB export) |
| `BASE_URL` | `http://localhost:9999` | Base URL of the API under test (NGINX load balancer endpoint) |
| `K6_INFLUXDB_ADDR` | — | InfluxDB address for dev mode (e.g. `http://influxdb:8086`) |

## Passing Variables

When running directly with k6:

```sh
k6 run \
  -e MODE=dev \
  -e BASE_URL=http://localhost:9999 \
  -e K6_INFLUXDB_ADDR=http://localhost:8086 \
  test/stress-test/rinha-test.js
```

When running via Docker Compose:

```sh
docker compose up k6 --build --force-recreate
```

The `docker-compose.yml` passes environment variables to the k6 container automatically. Override them with a `.env` file or inline exports.

## SharedArray — Client Data

Client data (IDs 1–5, with their credit limits) is loaded once at startup using k6's `SharedArray` to avoid redundant memory allocation across VUs:

```js
import { SharedArray } from 'k6/data';

const clients = new SharedArray('clients', function () {
  return [
    { id: 1, limite: 100000 },
    { id: 2, limite: 80000  },
    { id: 3, limite: 1000000 },
    { id: 4, limite: 10000000 },
    { id: 5, limite: 500000 },
  ];
});
```

## Thresholds

The suite does not enforce hard thresholds by default — it is designed to measure and report, not pass/fail CI. Each sibling implementation's own CI pipeline decides whether to treat threshold violations as failures.

Custom thresholds can be added to the `options` export in `rinha-test.js`:

```js
export const options = {
  scenarios: { /* ... */ },
  thresholds: {
    'transacao_duration': ['p(95)<500'],
    'extrato_duration':   ['p(95)<200'],
    http_req_failed:      ['rate<0.01'],
  },
};
```

## Resource Constraints

The k6 container itself is intentionally kept **outside** the 1.5 CPU / 550MB RAM budget. Only the API services (2x webapi + NGINX + PostgreSQL) are constrained.
