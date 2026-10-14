"""Six-bond selection on pytket: exact baseline, QAOA p=2, compilation pass with semantic check.

Offline only: pytket's exact statevector (Circuit.get_statevector) plus seeded numpy sampling of 4096 shots.
Quantinuum hardware (via qnexus) is profiled, not used.
Run: python main.py   (from this directory, inside the pinned environment)
"""
from __future__ import annotations

import json
import time

import numpy as np
import pytket
from scipy.optimize import minimize

import adapter
import canonical

SEED = 7
SHOTS = 4096
P = 2


def run_qaoa(problem: dict) -> dict:
    energies = adapter.all_energies(problem)
    scale = float(np.max(np.abs(energies)))

    def expected(params: np.ndarray) -> float:
        sv = adapter.qaoa_circuit(problem, params[:P], params[P:]).get_statevector()
        return float(np.abs(sv) ** 2 @ energies) / scale

    rng = np.random.default_rng(SEED)
    start = time.perf_counter()
    best = None
    for _ in range(4):
        opt = minimize(expected, rng.uniform(0, np.pi / 2, 2 * P), method="COBYLA",
                       options={"maxiter": 150, "rhobeg": 0.3})
        if best is None or opt.fun < best.fun:
            best = opt
    source = adapter.qaoa_circuit(problem, best.x[:P], best.x[P:])
    compiled, compile_report = adapter.compile_circuit(source)
    probs = np.abs(compiled.get_statevector()) ** 2
    shots = rng.choice(len(probs), size=SHOTS, p=probs / probs.sum())
    elapsed = time.perf_counter() - start
    counts = np.bincount(shots, minlength=len(probs))
    samples = []
    for index in np.nonzero(counts)[0]:
        info = canonical.decode(adapter.decode_index(int(index)), problem)
        info["count"] = int(counts[index])
        samples.append(info)
    samples.sort(key=lambda s: s["energy"])
    feasible = [s for s in samples if s["feasible"]]
    optimum = canonical.exact_baseline(problem)["optimum"]["bitstring"]
    return {
        "algorithm": f"QAOA p={P}, COBYLA maxiter=150, 4 seeded starts, exact expectation",
        "backend": "pytket Circuit.get_statevector (local exact) + numpy seeded sampling",
        "seed": SEED,
        "shots": SHOTS,
        "qubits": adapter.N,
        "resources_source": adapter.resources(source),
        "compilation": compile_report,
        "best_sampled": samples[0],
        "best_feasible_sampled": feasible[0] if feasible else None,
        "feasibility_rate": round(sum(s["count"] for s in feasible) / SHOTS, 4),
        "optimum_probability": round(int(counts[int(optimum, 2)]) / SHOTS, 4),
        "wall_clock_s": round(elapsed, 3),
    }


def main() -> dict:
    problem = canonical.load_problem()
    start = time.perf_counter()
    baseline = canonical.exact_baseline(problem)
    baseline["wall_clock_s"] = round(time.perf_counter() - start, 6)
    record = {
        "schema": "qmentor.result-record.v3",
        "target": "pytket",
        "versions": {"pytket": pytket.__version__},
        "baseline": baseline,
        "quantum": run_qaoa(problem),
        "evidence_level": "executable (level 2); matching a 64-state toy is not quantum advantage",
    }
    print(json.dumps(record, indent=2))
    return record


if __name__ == "__main__":
    main()
