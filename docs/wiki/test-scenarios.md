# Test Scenarios

The test suite defines **5 scenarios** that run sequentially and in parallel, covering both correctness validation and high-throughput load generation. All scenarios target the same `BASE_URL` (default: `http://localhost:9999`).

## Scenario Overview

| Scenario | VUs | Iterations / Duration | Start Time | Purpose |
|----------|-----|----------------------|------------|---------|
| **validacoes** | 5 | 1 iter each | 0s | Edge-case validation (invalid inputs, 404, 422) |
| **cliente_nao_encontrado** | 1 | 1 iter | 0s | Validates 404 for unknown client IDs |
| **debitos** | 1 → 220 | 4 min ramp | 10s | High-concurrency debit transactions |
| **creditos** | 1 → 110 | 4 min ramp | 10s | High-concurrency credit transactions |
| **extratos** | 10 | 1 iter each | After load | Final balance/statement consistency check |

## validacoes

Runs 5 VUs concurrently, each executing 1 iteration of edge-case checks:

- Debit exceeding client limit → expects `422`
- Invalid transaction type → expects `422`
- Missing description field → expects `422`
- Description too long (>10 chars) → expects `422`
- Empty description → expects `422`

## cliente_nao_encontrado

Single VU, single iteration. Sends requests to client IDs `0`, `6`, and `999` — all of which must return `404 Not Found`.

## debitos

The primary load scenario. Ramps from **1 to 220 VUs** over 4 minutes, continuously posting debit transactions to randomly selected clients (IDs 1–5). After each debit, the response body is validated:

```js
// Balance must never go below the negative of the limit
check(res, {
  'debit balance valid': (r) => r.json().saldo >= r.json().limite * -1,
});
```

## creditos

Parallel to debitos. Ramps from **1 to 110 VUs** over 4 minutes, posting credit transactions to randomly selected clients. Credits cannot fail due to insufficient funds, so this scenario validates basic HTTP correctness (`200`) and response shape.

## extratos

Final consistency check. After the load scenarios complete, 10 VUs each request the account statement (`GET /clientes/{id}/extrato`) for one client. Validates that:

- Response is `200 OK`
- `saldo.total` is a number
- `ultimas_transacoes` is an array
- Balance is consistent with the limit (`saldo.total >= saldo.limite * -1`)

## Custom Trend Metrics

The test file defines **5 custom Trend metrics** to track p95/p99 latency broken down by operation type:

```js
const transacaoTrend    = new Trend('transacao_duration');
const extratoTrend      = new Trend('extrato_duration');
const validacaoTrend    = new Trend('validacao_duration');
const notFoundTrend     = new Trend('not_found_duration');
const consistencyTrend  = new Trend('consistency_duration');
```

These appear as separate metrics in Grafana and the HTML report, making it easy to identify which operation type is the bottleneck.
