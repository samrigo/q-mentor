"""Math gates: fixture properties, exact optimum, QUBO/Ising equivalence, penalty separation."""
from __future__ import annotations

import copy
import itertools
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "demo" / "bond-selection"))
import canonical  # noqa: E402

TOL = 1e-9


def cholesky_ok(m) -> bool:
    n = len(m)
    low = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = m[i][j] - sum(low[i][k] * low[j][k] for k in range(j))
            if i == j:
                if s <= 0:
                    return False
                low[i][j] = s ** 0.5
            else:
                low[i][j] = s / low[j][j]
    return True


def separates(problem: dict) -> bool:
    ranked = canonical.enumerate_all(problem)
    best_feasible = min(e for e, x in ranked if canonical.is_feasible(x, problem))
    best_infeasible = min(e for e, x in ranked if not canonical.is_feasible(x, problem))
    return best_infeasible > best_feasible + TOL


def main() -> int:
    errors = []
    problem = canonical.load_problem()
    expected = json.loads((ROOT / "demo" / "bond-selection" / "expected.json").read_text())
    sigma = problem["data"]["sigma"]
    n = len(sigma)

    if any(abs(sigma[i][j] - sigma[j][i]) > TOL for i in range(n) for j in range(n)):
        errors.append("Sigma is not symmetric")
    if not cholesky_ok(sigma):
        errors.append("Sigma is not positive definite")

    base = canonical.exact_baseline(problem)
    opt = base["optimum"]
    if opt["bitstring"] != expected["optimum"]["bitstring"]:
        errors.append(f"optimum {opt['bitstring']} != {expected['optimum']['bitstring']}")
    for key in ("energy", "yield_score", "risk", "duration"):
        if abs(opt[key] - expected["optimum"][key]) > 1e-9:
            errors.append(f"optimum {key} {opt[key]} != {expected['optimum'][key]}")
    if not base["unique"]:
        errors.append("optimum is not unique")
    if base["runner_up"]["bitstring"] != expected["runner_up"]["bitstring"] or abs(base["gap"] - expected["gap"]) > 1e-9:
        errors.append("runner-up or gap mismatch")

    linear, quad, const = canonical.to_qubo(problem)
    h, J, offset = canonical.to_ising(linear, quad, const)
    for x in itertools.product((0, 1), repeat=n):
        e = canonical.direct_energy(x, problem)
        if abs(canonical.qubo_energy(x, linear, quad, const) - e) > TOL:
            errors.append(f"QUBO expansion mismatch at {x}")
        if abs(canonical.ising_energy(canonical.bits_to_spins(x), h, J, offset) - e) > TOL:
            errors.append(f"Ising conversion mismatch at {x}")
    if not separates(problem):
        errors.append("reference penalty does not separate feasible and infeasible optima")

    cases = yaml.safe_load((ROOT / "evals" / "math" / "cases.yml").read_text())["cases"]
    for case in cases:
        p = copy.deepcopy(problem)
        p["parameters"].update(case.get("override", {}))
        exp = case["expect"]
        if "penalty_separates" in exp and separates(p) != exp["penalty_separates"]:
            errors.append(f"{case['id']}: penalty separation expected {exp['penalty_separates']}")
        best = canonical.bitstring(canonical.enumerate_all(p)[0][1])
        if "optimum_bitstring" in exp and best != exp["optimum_bitstring"]:
            errors.append(f"{case['id']}: optimum {best}")
        if "optimum_bitstring_not" in exp and best == exp["optimum_bitstring_not"]:
            errors.append(f"{case['id']}: optimum unexpectedly {best}")
        if "reversed_probe" in case:
            rev = canonical.parse_bitstring(case["reversed_probe"][::-1])
            if not canonical.direct_energy(rev, p) > opt["energy"] + TOL:
                errors.append(f"{case['id']}: reversed bit order not detectable")
        print(f"case {case['id']}: checked")

    for err in errors:
        print("FAIL", err)
    print("math: OK" if not errors else f"math: {len(errors)} failure(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
