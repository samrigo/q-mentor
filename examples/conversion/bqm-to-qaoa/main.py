"""BQM -> QAOA reimplementation fixture. Run: python main.py (offline)."""
from __future__ import annotations

import importlib.metadata as md
import json

import adapter
import canonical


def main() -> dict:
    problem = canonical.load_problem()
    bqm = adapter.to_bqm(problem)
    op, off = adapter.to_qiskit_operator(problem)
    e_bqm = adapter.max_error(problem, lambda x: bqm.energy(dict(enumerate(x))))
    e_op = adapter.max_error(problem, lambda x: adapter.operator_energy(x, op, off))
    best = adapter.lowest(adapter.exact_samples(bqm))
    record = {
        "schema": "qmentor.translation-record.v3",
        "edge_id": "dwave-bqm-to-qiskit-qaoa",
        "route_class": adapter.classify("quantum annealing / BQM sampling", "QAOA", e_bqm < 1e-9 and e_op < 1e-9,
                                        best == canonical.exact_baseline(problem)["optimum"]["bitstring"]),
        "overall_status": "reimplementation",
        "source": {"framework": "dimod", "version": md.version("dimod")},
        "target": {"framework": "qiskit", "version": md.version("qiskit")},
        "max_energy_error": {"bqm": e_bqm, "qiskit_operator": e_op},
        "bqm_offset": bqm.offset,
        "exact_solver_optimum": best,
        "losses": ["annealing schedule, embedding and chain behaviour", "sampling distribution and runtime"],
        "validation": {"observed_state": "locally-executed", "commands": ["python -m pytest -q"]},
    }
    print(json.dumps(record, indent=2))
    return record


if __name__ == "__main__":
    main()
