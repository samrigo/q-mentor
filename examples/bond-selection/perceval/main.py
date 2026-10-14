"""Perceval (Quandela photonic DV): six-bond resource report + native two-variable QAOA with success rate.

Run: python main.py   (from this directory, inside the pinned environment). Local SLOS backend only.
"""
from __future__ import annotations

import json
import time

import numpy as np
import perceval as pcvl
from scipy.optimize import minimize

import adapter
import canonical

SEED = 7


def main() -> dict:
    problem = canonical.load_problem()
    sub = adapter.sub_problem(problem)
    energies = np.array([adapter.sub_energy(x, sub) for x in adapter.all_states()])
    scale = float(np.max(np.abs(energies)))
    ranked = sorted((adapter.sub_energy(x, sub), canonical.bitstring(x)) for x in adapter.all_states())
    start = time.perf_counter()

    def expected(params):
        dist = adapter.reference_distribution(sub, params[0], params[1], scale)
        return sum(dist[canonical.bitstring(x)] * adapter.sub_energy(x, sub) for x in adapter.all_states()) / scale

    rng = np.random.default_rng(SEED)
    best = min((minimize(expected, rng.uniform(0, np.pi / 2, 2), method="COBYLA", options={"maxiter": 200})
                for _ in range(4)), key=lambda r: r.fun)
    gamma, beta = float(best.x[0]), float(best.x[1])
    ideal = adapter.reference_distribution(sub, gamma, beta, scale)
    photonic, success = adapter.photonic_distribution(sub, gamma, beta, scale)
    elapsed = time.perf_counter() - start
    tvd = 0.5 * sum(abs(photonic.get(k, 0.0) - ideal[k]) for k in ideal)
    record = {
        "schema": "qmentor.result-record.v3",
        "target": "perceval",
        "versions": {"perceval-quandela": pcvl.__version__},
        "baseline": {"six_bond": canonical.exact_baseline(problem)["optimum"],
                     "sub_problem": {"labels": sub["labels"], "optimum": ranked[0][1],
                                     "energy": round(ranked[0][0], 6), "all": [[b, round(e, 6)] for e, b in ranked]}},
        "capability_report": adapter.six_bond_report(problem),
        "quantum": {
            "algorithm": "QAOA p=1 on two dual-rail qubits; heralded CNOT + postselected CNOT",
            "backend": "perceval Processor SLOS (local, perfect source)",
            "angles": {"gamma": round(gamma, 6), "beta": round(beta, 6)},
            "conditional_distribution": {k: round(v, 6) for k, v in sorted(photonic.items())},
            "ideal_gate_distribution": {k: round(v, 6) for k, v in sorted(ideal.items())},
            "total_variation_distance": tvd,
            "unconditional_success_probability": success,
            "optimum_conditional_probability": round(photonic.get(ranked[0][1], 0.0), 6),
            "wall_clock_s": round(elapsed, 3),
        },
        "evidence_level": "executable (level 2), conditional on postselection; not quantum advantage",
    }
    print(json.dumps(record, indent=2))
    return record


if __name__ == "__main__":
    main()
