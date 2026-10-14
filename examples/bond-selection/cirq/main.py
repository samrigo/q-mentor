"""Six-bond selection on Cirq: exact classical baseline + local seeded QAOA (p=2).

Offline only: cirq.Simulator on the local machine, seed 7, 4096 repetitions.
Run: python main.py   (from this directory, inside the pinned environment)
"""
from __future__ import annotations

import json
import time

import cirq
import numpy as np
from scipy.optimize import minimize

import adapter
import canonical

SEED = 7
SHOTS = 4096
P = 2


def exact_baseline(problem: dict) -> dict:
    start = time.perf_counter()
    result = canonical.exact_baseline(problem)
    result["wall_clock_s"] = round(time.perf_counter() - start, 6)
    return result


def run_qaoa(problem: dict) -> dict:
    energies = np.array([canonical.direct_energy([int(b) for b in format(k, "06b")], problem) for k in range(64)])
    scale = float(np.max(np.abs(energies)))
    sim = cirq.Simulator(seed=SEED)

    def expected(params: np.ndarray) -> float:
        circuit = adapter.qaoa_circuit(problem, params[:P], params[P:], measure=False)
        probs = np.abs(sim.simulate(circuit, qubit_order=adapter.QUBITS).final_state_vector) ** 2
        return float(probs @ energies) / scale

    rng = np.random.default_rng(SEED)
    start = time.perf_counter()
    best = None
    for _ in range(4):  # seeded multi-start, fixed budget
        x0 = rng.uniform(0, np.pi / 2, 2 * P)
        opt = minimize(expected, x0, method="COBYLA", options={"maxiter": 150, "rhobeg": 0.3})
        if best is None or opt.fun < best.fun:
            best = opt
    gammas, betas = best.x[:P], best.x[P:]
    result = sim.run(adapter.qaoa_circuit(problem, gammas, betas), repetitions=SHOTS)
    elapsed = time.perf_counter() - start
    counts: dict = {}
    for row in result.measurements["x"]:
        key = canonical.bitstring(adapter.decode_measurement(row))
        counts[key] = counts.get(key, 0) + 1
    samples = []
    for bits, count in counts.items():
        info = canonical.decode(canonical.parse_bitstring(bits), problem)
        info["count"] = count
        samples.append(info)
    samples.sort(key=lambda s: s["energy"])
    feasible = [s for s in samples if s["feasible"]]
    optimum_bits = canonical.exact_baseline(problem)["optimum"]["bitstring"]
    return {
        "algorithm": f"QAOA p={P}, COBYLA maxiter=150, 4 seeded starts, exact expectation",
        "backend": "cirq.Simulator (local, noiseless)",
        "seed": SEED,
        "shots": SHOTS,
        "qubits": len(adapter.QUBITS),
        "circuit_depth": len(adapter.qaoa_circuit(problem, gammas, betas)),
        "angles": {"gammas": [round(float(g), 6) for g in gammas], "betas": [round(float(b), 6) for b in betas]},
        "best_sampled": samples[0],
        "best_feasible_sampled": feasible[0] if feasible else None,
        "feasibility_rate": round(sum(s["count"] for s in feasible) / SHOTS, 4),
        "optimum_probability": round(counts.get(optimum_bits, 0) / SHOTS, 4),
        "wall_clock_s": round(elapsed, 3),
    }


def main() -> dict:
    problem = canonical.load_problem()
    record = {
        "schema": "qmentor.result-record.v3",
        "target": "cirq",
        "versions": {"cirq-core": cirq.__version__},
        "baseline": exact_baseline(problem),
        "quantum": run_qaoa(problem),
        "evidence_level": "executable (level 2); matching a 64-state toy is not quantum advantage",
    }
    print(json.dumps(record, indent=2))
    return record


if __name__ == "__main__":
    main()
