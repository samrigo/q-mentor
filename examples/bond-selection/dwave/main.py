"""Six-bond selection on D-Wave Ocean, fully local.

* dimod.ExactSolver: exhaustive classical baseline over all 64 states.
* dwave.samplers.SimulatedAnnealingSampler: local classical heuristic with a seed.
No Leap/QPU call is made; see adapter.qpu_sampler_guarded for the opt-in path.
"""
from __future__ import annotations

import json
import time

import dimod
from dwave.samplers import SimulatedAnnealingSampler

import adapter
import canonical

SEED = 7
NUM_READS = 200


def main() -> dict:
    problem = canonical.load_problem()
    bqm = adapter.build_bqm(problem)

    start = time.perf_counter()
    exact = dimod.ExactSolver().sample(bqm)
    exact_s = time.perf_counter() - start
    best = adapter.sample_to_vector(exact.first.sample, problem)

    start = time.perf_counter()
    sa = SimulatedAnnealingSampler().sample(bqm, num_reads=NUM_READS, seed=SEED)
    sa_s = time.perf_counter() - start
    vectors = [adapter.sample_to_vector(s, problem) for s in sa.samples()]
    feasible = [v for v in vectors if canonical.is_feasible(v, problem)]
    opt_bits = canonical.bitstring(best)
    record = {
        "schema": "qmentor.result-record.v2",
        "target": "dwave-ocean",
        "versions": {"dimod": dimod.__version__,
                     "dwave-samplers": __import__("dwave.samplers", fromlist=["__version__"]).__version__},
        "logical_variables": bqm.num_variables,
        "physical_qubits": None,
        "baseline": {"method": "dimod.ExactSolver", "optimum": canonical.decode(best, problem),
                     "energy_from_bqm": round(float(exact.first.energy), 10), "wall_clock_s": round(exact_s, 6)},
        "heuristic": {
            "method": "dwave.samplers.SimulatedAnnealingSampler (classical, local)",
            "seed": SEED, "num_reads": NUM_READS,
            "best": canonical.decode(adapter.sample_to_vector(sa.first.sample, problem), problem),
            "feasibility_rate": round(len(feasible) / len(vectors), 4),
            "optimum_rate": round(sum(canonical.bitstring(v) == opt_bits for v in vectors) / len(vectors), 4),
            "wall_clock_s": round(sa_s, 6),
        },
        "qpu": "not run (requires explicit approval; no chain/embedding data)",
        "evidence_level": "executable classical toolchain; no quantum hardware used",
    }
    print(json.dumps(record, indent=2))
    return record


if __name__ == "__main__":
    main()
