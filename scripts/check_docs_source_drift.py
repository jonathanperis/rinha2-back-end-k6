#!/usr/bin/env python3
"""Fail when public docs drift from the k6 source-of-truth facts.

This is intentionally lightweight and dependency-free so it can run in GitHub
Actions before the Astro Pages build.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def assert_in(text: str, needle: str, rel: str) -> None:
    if needle not in text:
        raise AssertionError(f"{rel} is missing expected marker: {needle!r}")


def assert_not_in(text: str, needle: str, rel: str) -> None:
    if needle in text:
        raise AssertionError(f"{rel} still contains stale marker: {needle!r}")


def main() -> None:
    k6 = read("test/stress-test/rinha-test.js")
    run_test = read("test/stress-test/run-test.sh")
    dockerfile = read("Dockerfile")
    release = read(".github/workflows/main-release.yml")

    scenario_names = re.findall(r"exec: '([^']+)'", k6)
    expected_scenarios = [
        "validacoes",
        "cliente_nao_encontrado",
        "debitos",
        "creditos",
        "extratos",
    ]
    if scenario_names != expected_scenarios:
        raise AssertionError(f"Unexpected scenario order/names: {scenario_names!r}")

    metrics = re.findall(r"new Trend\('([^']+)'", k6)
    expected_metrics = [
        "debitos_duration",
        "creditos_duration",
        "extratos_duration",
        "validacoes_duration",
        "cliente_nao_encontrado_duration",
    ]
    if metrics != expected_metrics:
        raise AssertionError(f"Unexpected Trend metrics: {metrics!r}")

    for rel in [
        "README.md",
        "AGENTS.md",
        ".agents/memory/test_design.md",
        "docs/wiki/home.md",
        "docs/wiki/test-scenarios.md",
        "docs/src/components/home/Dashboard.astro",
    ]:
        text = read(rel)
        for scenario in expected_scenarios:
            assert_in(text, scenario, rel)

    # Entrypoint/run-mode facts documented in README and wiki pages.
    assert_in(run_test, "k6 run rinha-test.js --quiet", "test/stress-test/run-test.sh")
    assert_in(run_test, "k6 run rinha-test.js -o xk6-influxdb", "test/stress-test/run-test.sh")
    for rel in ["README.md", "docs/wiki/getting-started.md", "docs/wiki/run-modes.md", "docs/wiki/configuration.md"]:
        text = read(rel)
        assert_in(text, "MODE=prod", rel)
        assert_in(text, "k6 run rinha-test.js --quiet", rel)
        assert_not_in(text, "HTML report output", rel)

    # Docker/runtime and release facts.
    assert_in(dockerfile, "FROM golang:1.25-alpine3.21 AS builder", "Dockerfile")
    assert_in(dockerfile, "FROM alpine:3.23", "Dockerfile")
    assert_in(release, "ghcr.io/jonathanperis/rinha2-back-end-k6:latest", ".github/workflows/main-release.yml")
    assert_in(release, "linux/amd64,linux/arm64/v8", ".github/workflows/main-release.yml")
    for rel in ["README.md", "docs/wiki/getting-started.md", "docs/wiki/ci-cd.md"]:
        text = read(rel)
        assert_in(text, "ghcr.io/jonathanperis/rinha2-back-end-k6:latest", rel)

    # Public homepage must not show unsupported historical/marketing numbers as facts.
    for rel in [
        "docs/src/pages/index.astro",
        "docs/src/layouts/BaseLayout.astro",
        "docs/src/components/home/Hero.astro",
        "docs/src/components/home/Dashboard.astro",
    ]:
        text = read(rel)
        for stale in [
            "30,000",
            "47k+",
            "0 -&gt; 500 VUs",
            "Executing scenario: default",
            "absolute chaos",
            "breaking point",
            "extreme load conditions",
            "across all Rinha de Backend implementations",
        ]:
            assert_not_in(text, stale, rel)

    print("Docs/source drift check passed")


if __name__ == "__main__":
    main()
