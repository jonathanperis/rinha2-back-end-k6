# Test Scenarios

## Overview

The k6 test script (`test/stress-test/rinha-test.js`) simulates transactional workloads against the API. The entrypoint (`test/stress-test/run-test.sh`) selects dev or prod mode based on the `MODE` environment variable.

## Scenarios

### Validations (validacoes)

- **Executor:** per-vu-iterations — 5 VUs, 1 iteration each
- **Start time:** 0s
- Verifies initial balance is 0 and limit matches expected value per client
- Posts a credit then a debit and verifies balance/limit consistency
- Checks transaction ordering in statements (most recent first)
- Tests invalid requests: decimal `valor`, invalid `tipo`, oversized `descricao`, empty `descricao`, null `descricao`

### Client Not Found (cliente_nao_encontrado)

- **Executor:** per-vu-iterations — 1 VU, 1 iteration
- **Start time:** 0s
- Queries non-existent client (ID 6) — expects 404

### Debit Transactions (debitos)

- **Executor:** ramping-vus — 1 to 220 VUs over 4 minutes
- **Start time:** 10s
- Creates debit transactions (`tipo: "d"`) for random clients (IDs 1-5)
- Validates 200 or 422 responses and balance/limit consistency

### Credit Transactions (creditos)

- **Executor:** ramping-vus — 1 to 110 VUs over 4 minutes
- **Start time:** 10s
- Creates credit transactions (`tipo: "c"`) for random clients (IDs 1-5)
- Validates 200 responses and balance/limit consistency

### Account Statements (extratos)

- **Executor:** per-vu-iterations — 10 VUs, 1 iteration each
- **Start time:** 10s
- Fetches statements (`GET /clientes/{id}/extrato`) for random clients
- Validates response structure (saldo, ultimas_transacoes) and balance consistency
