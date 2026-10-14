"""Six-bond selection on Qiskit: exact classical baseline + local seeded QAOA.

Offline only: StatevectorSampler (qiskit.primitives) on the local machine.
Run: python main.py   (from this directory, inside the pinned environment)
"""
from __future__ import annotations

import json
import time

import numpy as np
from qiskit.circuit.library import qaoa_ansatz
from qiskit.primitives import StatevectorSampler
from scipy.optimize import minimize

import adapter
import canonical

SEED = 7
SHOTS = 4096
REPS = 2


def exact_baseline(problem: dict) -> dict:
    start = time.perf_counter()
    result = canonical.exact_baseline(problem)
    result["wall_clock_s"] = round(time.perf_counter() - start, 6)
    return result


def run_qaoa(problem: dict) -> dict:
    operator, offset = adapter.build_ising(problem)
    ansatz = qaoa_ansatz(operator, reps=REPS)
    measured = ansatz.copy()
    measured.measure_all()
    sampler = StatevectorSampler(seed=SEED)
    # Normalise the cost so angles stay O(1); the optimiser sees expected energy.
    scale = float(np.max(np.abs(operator.coeffs)))

    def expected_energy(params: np.ndarray) -> float:
        counts = sampler.run([(measured, params)], shots=SHOTS).result()[0].data.meas.get_counts()
        total = sum(counts.values())
        return sum(c * adapter.operator_energy(adapter.decode_qiskit_bitstring(b), operator, offset)
                   for b, c in counts.items()) / total / scale

    rng = np.random.default_rng(SEED)
    x0 = rng.uniform(0, np.pi, ansatz.num_parameters)
    start = time.perf_counter()
    opt = minimize(expected_energy, x0, method="COBYLA", options={"maxiter": 120, "rhobeg": 0.5})
    counts = sampler.run([(measured, opt.x)], shots=SHOTS).result()[0].data.meas.get_counts()
    elapsed = time.perf_counter() - start

    samples = []
    for raw, count in counts.items():
        x = adapter.decode_qiskit_bitstring(raw)
        info = canonical.decode(x, problem)
        info["count"] = count
        samples.append(info)
    samples.sort(key=lambda s: s["energy"])
    feasible = [s for s in samples if s["feasible"]]
    optimum_bits = canonical.exact_baseline(problem)["optimum"]["bitstring"]
    hits = sum(s["count"] for s in samples if s["bitstring"] == optimum_bits)
    return {
        "algorithm": f"QAOA reps={REPS}, COBYLA maxiter=120",
        "backend": "qiskit.primitives.StatevectorSampler (local, noiseless)",
        "seed": SEED,
        "shots": SHOTS,
        "qubits": ansatz.num_qubits,
        "transpiled": False,
        "optimizer_evaluations": int(opt.nfev),
        "best_sampled": samples[0],
        "best_feasible_sampled": feasible[0] if feasible else None,
        "feasibility_rate": round(sum(s["count"] for s in feasible) / SHOTS, 4),
        "optimum_probability": round(hits / SHOTS, 4),
        "wall_clock_s": round(elapsed, 3),
    }


def main() -> dict:
    problem = canonical.load_problem()
    record = {
        "schema": "qmentor.result-record.v3",
        "target": "qiskit",
        "versions": {"qiskit": __import__("qiskit").__version__,
                     "qiskit-optimization": __import__("qiskit_optimization").__version__},
        "baseline": exact_baseline(problem),
        "quantum": run_qaoa(problem),
        "evidence_level": "executable (level 2); matching a 64-state toy is not quantum advantage",
    }
    print(json.dumps(record, indent=2))
    return record


if __name__ == "__main__":
    main()
