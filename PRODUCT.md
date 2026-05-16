# PRODUCT.md

## Product

`rinha2-back-end-k6` is the shared Grafana k6 load-testing suite for the Rinha de Backend 2024/Q1 fictional bank API challenge. It packages the official-style stress profile as source code, documentation, and a Docker image so backend implementations can be tested consistently across languages and environments.

## Register

brand

The public website is a brand and documentation landing surface. It must create confidence, explain the tool quickly, and route developers to the exact run commands and docs. Design is part of the product impression, but the product value is operational correctness.

## Product Purpose

Help Rinha participants and maintainers run a reproducible k6 suite that stresses debit transactions, credit transactions, statement reads, validation flows, and missing-client behavior. The site should make the suite feel sharp, adversarial, and developer-native while staying precise about the actual load profile.

## Primary Users

- **Rinha participants** validating a backend before comparing results or submitting evidence.
- **Backend engineers** adopting the suite as a reusable benchmark harness.
- **Repository maintainers** checking that docs, landing copy, scripts, Docker image, and CI remain aligned.
- **Reviewers and technical observers** who need to understand what the suite tests without reading the full source first.

## User State of Mind

Visitors are usually technical, impatient, and skeptical. They want proof, commands, exact numbers, and fast orientation. They may be debugging a backend that already failed locally or in CI. They will punish vague marketing claims and reward source-backed details.

## Core Value Propositions

- Five k6 scenarios aligned with the Rinha banking API: `validacoes`, `cliente_nao_encontrado`, `debitos`, `creditos`, and `extratos`.
- Custom Trend metrics per scenario: `debitos_duration`, `creditos_duration`, `extratos_duration`, `validacoes_duration`, and `cliente_nao_encontrado_duration`.
- Dual-mode execution:
  - `prod`: HTML report output for CI and shareable runs.
  - `dev`: InfluxDB export for Grafana observability.
- Docker-first usage with a custom k6 binary that includes `xk6-output-influxdb`.
- Multi-platform GHCR image and GitHub Actions publishing.

## Canonical Facts for Design and Copy

Source-backed numbers should come from `test/stress-test/rinha-test.js` unless explicitly labeled as historical run output.

- `validacoes`: 5 VUs, 1 iteration each, starts at 0s.
- `cliente_nao_encontrado`: 1 VU, 1 iteration, starts at 0s.
- `debitos`: ramping VUs from 1 to 220, 2m ramp plus 2m hold, starts at 10s.
- `creditos`: ramping VUs from 1 to 110, 2m ramp plus 2m hold, starts at 10s.
- `extratos`: 10 VUs, 1 iteration each, starts at 10s.
- Default `BASE_URL`: `http://localhost:9999`.
- Production run example: `docker run --rm -e BASE_URL=http://api:9999 rinha-k6`.
- Dev run example: `docker run --rm -e MODE=dev -e K6_INFLUXDB_ADDR=http://influxdb:8086 rinha-k6`.

## Brand Voice

Concrete voice words:

- **Adversarial:** the suite is here to make weak assumptions fail.
- **Instrumented:** every claim should feel measured, sourced, and reproducible.
- **Terminal-native:** copy can sound like CLI output, but it should not fake live telemetry.

The strongest existing line is: “IT WORKED ON YOUR MACHINE. NOT ON OURS.” Preserve that attitude. Supporting copy should become more exact and less theatrical.

## Copy Principles

- Prefer exact operational claims over generic intensity words.
- Keep humor sharp but subordinate to trust.
- Use scenario names, commands, metric names, and mode names as proof.
- If a metric is illustrative or historical, label it as such.
- Avoid vague phrases like “absolute chaos”, “extreme duress”, “breaking point”, or “validated across all implementations” unless backed by specific evidence.
- Avoid em dashes in user-facing copy.

## Anti-References

Do not make the site feel like:

- Generic SaaS landing page with pastel gradients and rounded feature cards.
- Cyberpunk cosplay that sacrifices source-backed accuracy.
- Fake live observability dashboard with unsourced telemetry.
- Documentation site that hides the run command below several marketing sections.
- Terminal aesthetic where everything glows, blinks, and shouts at once.

## Desired Website Experience

A visitor should understand within 30 seconds:

1. This is a k6 suite for Rinha de Backend 2024/Q1.
2. It tests five concrete banking API scenarios.
3. It can run in prod or dev mode.
4. The quickest next action is running or reading the quick start.
5. The visual attitude is hostile to fragile backends, not hostile to the reader.

## Current Design Direction to Preserve

The existing dark CRT terminal, Matrix-green palette, monospace identity, warning/error accents, and developer humor are valuable. Future redesigns should preserve that aesthetic but make it more credible, accessible, and source-of-truth driven.
