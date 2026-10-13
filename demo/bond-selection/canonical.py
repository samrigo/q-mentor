"""Canonical six-bond model: energy, QUBO expansion, Ising conversion, enumeration.

Standard library only, so every target adapter and validator can import it in a
clean environment. Conventions are documented in problem.json:

* bit order: index k <-> bitstring character k (left to right) <-> variable A..F
* QUBO: E(x) = sum_i a_i x_i + sum_{i<j} b_ij x_i x_j + c  (each pair stored once)
* Ising: x_i = (1 - s_i) / 2, s_i in {-1, +1}
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

HERE = Path(__file__).resolve().parent
PROBLEM_PATH = HERE / "problem.json"

Linear = Dict[int, float]
Quadratic = Dict[Tuple[int, int], float]


def load_problem(path: Path | str = PROBLEM_PATH) -> dict:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def direct_energy(x: Sequence[int], problem: dict) -> float:
    """Evaluate the business objective exactly as written, without expansion."""
    data, par = problem["data"], problem["parameters"]
    mu, dur, sigma = data["mu"], data["duration"], data["sigma"]
    n = len(mu)
    risk = sum(sigma[i][j] * x[i] * x[j] for i in range(n) for j in range(n))
    ret = sum(mu[i] * x[i] for i in range(n))
    card = sum(x) - par["budget_B"]
    dev = sum(dur[i] * x[i] for i in range(n)) - par["duration_target"]
    return (par["risk_aversion_q"] * risk - ret
            + par["cardinality_penalty_A"] * card ** 2
            + par["duration_weight"] * dev ** 2)


def to_qubo(problem: dict) -> Tuple[Linear, Quadratic, float]:
    """Expand the objective into (linear, upper-triangular quadratic, constant)."""
    data, par = problem["data"], problem["parameters"]
    mu, dur, sigma = data["mu"], data["duration"], data["sigma"]
    q, budget = par["risk_aversion_q"], par["budget_B"]
    pen, w, target = par["cardinality_penalty_A"], par["duration_weight"], par["duration_target"]
    n = len(mu)
    linear: Linear = {}
    quad: Quadratic = {}
    for i in range(n):
        # x_i^2 = x_i for binaries
        linear[i] = (q * sigma[i][i] - mu[i]
                     + pen * (1 - 2 * budget)
                     + w * (dur[i] ** 2 - 2 * target * dur[i]))
    for i in range(n):
        for j in range(i + 1, n):
            quad[(i, j)] = (q * (sigma[i][j] + sigma[j][i])
                            + 2 * pen
                            + 2 * w * dur[i] * dur[j])
    const = pen * budget ** 2 + w * target ** 2
    return linear, quad, const


def qubo_energy(x: Sequence[int], linear: Linear, quad: Quadratic, const: float) -> float:
    return (const + sum(a * x[i] for i, a in linear.items())
            + sum(b * x[i] * x[j] for (i, j), b in quad.items()))


def qubo_matrix_upper(linear: Linear, quad: Quadratic, n: int) -> List[List[float]]:
    """Upper-triangular matrix Q with E = x^T Q x + c (diagonal = linear terms)."""
    mat = [[0.0] * n for _ in range(n)]
    for i, a in linear.items():
        mat[i][i] = a
    for (i, j), b in quad.items():
        mat[i][j] = b
    return mat


def to_ising(linear: Linear, quad: Quadratic, const: float) -> Tuple[Linear, Quadratic, float]:
    """Map QUBO to Ising with x_i = (1 - s_i)/2. Returns (h, J, offset)."""
    h: Linear = {i: -a / 2 for i, a in linear.items()}
    J: Quadratic = {}
    offset = const + sum(a / 2 for a in linear.values())
    for (i, j), b in quad.items():
        J[(i, j)] = b / 4
        h[i] -= b / 4
        h[j] -= b / 4
        offset += b / 4
    return h, J, offset


def ising_energy(s: Sequence[int], h: Linear, J: Quadratic, offset: float) -> float:
    return (offset + sum(v * s[i] for i, v in h.items())
            + sum(v * s[i] * s[j] for (i, j), v in J.items()))


def bits_to_spins(x: Sequence[int]) -> List[int]:
    return [1 - 2 * b for b in x]


def bitstring(x: Sequence[int]) -> str:
    return "".join(str(int(b)) for b in x)


def parse_bitstring(text: str) -> List[int]:
    return [int(ch) for ch in text]


def is_feasible(x: Sequence[int], problem: dict) -> bool:
    return sum(x) == problem["parameters"]["budget_B"]


def enumerate_all(problem: dict) -> List[Tuple[float, Tuple[int, ...]]]:
    n = len(problem["variables"])
    return sorted((direct_energy(x, problem), x) for x in itertools.product((0, 1), repeat=n))


def decode(x: Sequence[int], problem: dict) -> dict:
    data = problem["data"]
    n = len(x)
    chosen = [problem["variables"][i]["id"] for i in range(n) if x[i]]
    return {
        "bitstring": bitstring(x),
        "selected": chosen,
        "feasible": is_feasible(x, problem),
        "yield_score": round(sum(data["mu"][i] * x[i] for i in range(n)), 10),
        "risk": round(sum(data["sigma"][i][j] * x[i] * x[j] for i in range(n) for j in range(n)), 10),
        "duration": round(sum(data["duration"][i] * x[i] for i in range(n)), 10),
        "energy": round(direct_energy(x, problem), 10),
    }


def exact_baseline(problem: dict) -> dict:
    """Exhaustive enumeration: the classical exact baseline for the toy."""
    ranked = enumerate_all(problem)
    best_e, best_x = ranked[0]
    feasible = [(e, x) for e, x in ranked if is_feasible(x, problem)]
    infeasible = [(e, x) for e, x in ranked if not is_feasible(x, problem)]
    return {
        "method": "exhaustive enumeration",
        "states": len(ranked),
        "optimum": decode(best_x, problem),
        "unique": ranked[1][0] - best_e > 1e-9,
        "runner_up": decode(feasible[1][1], problem),
        "gap": round(feasible[1][0] - best_e, 10),
        "best_infeasible_energy": round(infeasible[0][0], 10),
    }


if __name__ == "__main__":
    print(json.dumps(exact_baseline(load_problem()), indent=2))
