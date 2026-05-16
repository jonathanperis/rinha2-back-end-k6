# Test Scenarios

The suite defines **5 source-backed k6 scenarios**. They all target `BASE_URL`, which defaults to `http://localhost:9999` in `rinha-test.js`.

## Scenario overview

| Scenario | Executor | VUs / stages | Start | Purpose |
|----------|----------|--------------|-------|---------|
| `validacoes` | `per-vu-iterations` | 5 VUs, 1 iteration each | `0s` | Baseline statement, credit, debit, recent-transaction order, and invalid-request checks |
| `cliente_nao_encontrado` | `per-vu-iterations` | 1 VU, 1 iteration | `0s` | `GET /clientes/6/extrato` must return `404` |
| `debitos` | `ramping-vus` | 1 to 220 VUs over 2m, then hold 220 for 2m | `10s` | High-concurrency debit transactions with overdraft validation |
| `creditos` | `ramping-vus` | 1 to 110 VUs over 2m, then hold 110 for 2m | `10s` | High-concurrency credit transactions |
| `extratos` | `per-vu-iterations` | 10 VUs, 1 iteration each | `10s` | Statement reads and balance-limit consistency |

## `validacoes`

Runs one virtual user per configured client in `saldosIniciaisClientes`. Each VU checks the full client workflow:

1. `GET /clientes/{id}/extrato`, expecting status `200`, the configured limit, and initial balance `0`.
2. `POST /clientes/{id}/transacoes` with credit `{ valor: 1, tipo: 'c', descricao: 'toma' }`.
3. `POST /clientes/{id}/transacoes` with debit `{ valor: 1, tipo: 'd', descricao: 'devolve' }`.
4. `GET /clientes/{id}/extrato`, expecting recent transactions in the debit-then-credit order.
5. Invalid transaction requests, expecting `422` or `400` depending on implementation behavior.

Invalid request cases:

| Payload issue | Expected status |
|---------------|-----------------|
| Decimal `valor` | `422` or `400` |
| Invalid `tipo` | `422` or `400` |
| Description longer than 10 characters | `422` or `400` |
| Empty description | `422` or `400` |
| `null` description | `422` or `400` |

## `cliente_nao_encontrado`

Runs a single statement request against client `6`:

```http
GET /clientes/6/extrato
```

The expected result is `404`. This keeps missing-client behavior visible as a separate metric instead of hiding it inside the general validation flow.

## `debitos`

The debit workload ramps from **1 to 220 VUs**, holds that target, and posts random debit transactions to clients `1` through `5`.

```js
stages: [
  { duration: '2m', target: 220 },
  { duration: '2m', target: 220 },
]
```

Accepted response statuses are `200` or `422`, because debit operations can be rejected when a client would exceed the overdraft limit. Successful debit responses are checked with:

```js
saldo >= limite * -1
```

## `creditos`

The credit workload ramps from **1 to 110 VUs**, holds that target, and posts random credit transactions to clients `1` through `5`.

```js
stages: [
  { duration: '2m', target: 110 },
  { duration: '2m', target: 110 },
]
```

Credits are expected to return `200` and preserve the same balance-limit consistency contract.

## `extratos`

Runs 10 VUs, one iteration each, against:

```http
GET /clientes/{id}/extrato
```

The response must be `200`, and `saldo.total` must still respect the configured limit:

```js
saldo.total >= saldo.limite * -1
```

## Custom Trend metrics

The script exports five Trend metrics. These names are the canonical labels to use in reports and dashboards:

| Metric | Scenario |
|--------|----------|
| `debitos_duration` | `debitos` |
| `creditos_duration` | `creditos` |
| `extratos_duration` | `extratos` |
| `validacoes_duration` | `validacoes` |
| `cliente_nao_encontrado_duration` | `cliente_nao_encontrado` |

Each request path adds its observed duration to the scenario-specific Trend so Grafana and HTML reports can separate bottlenecks by operation type.
