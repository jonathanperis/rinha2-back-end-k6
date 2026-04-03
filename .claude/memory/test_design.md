---
name: K6 Test Suite Design
description: 5 test scenarios, custom metrics, validation rules, dual execution modes, SharedArray pattern
type: project
---

## Test Scenario Design

The test suite (`test/stress-test/rinha-test.js`, 318 lines) implements 5 scenarios with staggered execution:

**Immediate start (0s):**
- **Validacoes** (5 VUs, 1 iter each): Full workflow per client — GET statement, POST credit, POST debit, GET verify, 5 invalid requests
- **Cliente Nao Encontrado** (1 VU): Tests 404 for non-existent client ID 6

**Delayed start (10s, after validations):**
- **Debitos** (ramp 1→220 VUs over 2min, sustain 2min): Debit transactions with overdraft testing
- **Creditos** (ramp 1→110 VUs over 2min, sustain 2min): Credit transactions
- **Extratos** (10 VUs, 1 iter each): Statement retrieval

**Why:** Validation scenarios run first to confirm API correctness, then load scenarios stress the system.

## Custom Metrics (5 Trend objects)

`debitosTrend`, `creditosTrend`, `extratosTrend`, `validacoesTrend`, `clienteNaoEncontradoTrend` — each records response duration in milliseconds.

## Key Validation Rules

- **Balance consistency**: `saldo >= limite * -1` (never exceed negative limit)
- **Transaction ordering**: Last 10 transactions returned in descending order by ID
- **Invalid request tests**: Decimal valor (1.2), invalid tipo ('x'), >10 char descricao, empty descricao, null descricao → all must return 422

## Dual Execution Modes

- **dev mode**: `k6 run -o xk6-influxdb` — exports real-time metrics to InfluxDB for Grafana dashboards
- **prod mode**: `k6 run --quiet` — generates HTML report for CI/CD artifacts

## SharedArray Pattern

Client data stored in `SharedArray` — read-only, shared across all VUs without memory duplication. Important for the 220 VU ramp scenario.
