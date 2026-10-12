#!/usr/bin/env python3
"""Deterministic validation of the six-bond demo energy and optimum."""

from __future__ import annotations

import json
import itertools
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROBLEM = ROOT / "demo" / "bond-selection" / "problem.json"
EXPECTED = ROOT / "demo" / "bond-selection" / "expected.json"


def energy(x, mu, Sigma, d, q, card, A_card, d_target, A_dur):
    n = len(x)
    risk = 0.0
    for i in range(n):
        for j in range(n):
            risk += x[i] * Sigma[i][j] * x[j]
    yield_term = sum(mu[i] * x[i] for i in range(n))
    card_pen = A_card * (sum(x) - card) ** 2
    dur = sum(d[i] * x[i] for i in range(n))
    dur_pen = A_dur * (dur - d_target) ** 2
    return q * risk - yield_term + card_pen + dur_pen


def main() -> int:
    with open(PROBLEM) as f:
        p = json.load(f)
    with open(EXPECTED) as f:
        e = json.load(f)

    mu = p["mu"]
    Sigma = p["Sigma"]
    d = p["duration"]
    q = p["risk_aversion"]
    card = p["cardinality"]
    A_card = p["cardinality_penalty"]
    d_target = p["duration_target"]
    A_dur = p["duration_penalty"]
    tol = e["tolerance"]

    n = len(mu)
    for i in range(n):
        for j in range(n):
            assert abs(Sigma[i][j] - Sigma[j][i]) < tol, f"Sigma not symmetric at {i},{j}"

    best_e = float("inf")
    best_x = None
    for bits in itertools.product([0, 1], repeat=n):
        en = energy(bits, mu, Sigma, d, q, card, A_card, d_target, A_dur)
        if en < best_e - tol:
            best_e = en
            best_x = list(bits)

    exp = e["optimum"]
    assert best_x == exp["x"], f"optimum x mismatch: got {best_x}"
    assert abs(best_e - exp["energy"]) < tol, f"energy mismatch: got {best_e}"

    print("validate_math: PASS")
    print(f"  optimum x = {best_x}")
    print(f"  energy    = {best_e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
