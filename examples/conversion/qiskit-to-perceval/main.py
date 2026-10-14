"""Gate -> photonic DV conversion fixture: conditional distributions and unconditional success rates.
Run: python main.py   (inside the pinned environment; local SLOS only)
"""
from __future__ import annotations

import importlib.metadata as md
import json

import adapter
import canonical


def main() -> dict:
    problem = canonical.load_problem()
    gamma, beta = adapter.best_angles(problem)
    rows = {}
    for name, qc in {"qaoa_A_C": adapter.qaoa_circuit(problem, gamma, beta), "ghz2": adapter.ghz_circuit(2),
                     "ghz3": adapter.ghz_circuit(3)}.items():
        ideal = adapter.gate_distribution(qc)
        photonic, success, resources = adapter.photonic_distribution(qc)
        rows[name] = {"tvd_conditional_vs_gate": adapter.tvd(ideal, photonic),
                      "unconditional_success_probability": success, **resources,
                      "conditional_distribution": {k: round(v, 6) for k, v in sorted(photonic.items())}}
    record = {
        "schema": "qmentor.translation-record.v3",
        "edge_id": "qiskit-to-perceval-dual-rail",
        "route_class": "C",
        "source": {"framework": "qiskit", "version": md.version("qiskit")},
        "target": {"framework": "perceval-quandela + perceval-interop",
                   "version": f"{md.version('perceval-quandela')} / {md.version('perceval-interop')}"},
        "overall_status": "conditional",
        "unconditional_success_probability": rows["qaoa_A_C"]["unconditional_success_probability"],
        "circuits": rows,
        "angles": {"gamma": gamma, "beta": beta},
        "losses": ["deterministic execution (postselection)", "loss and source imperfections on hardware"],
        "validation": {"observed_state": "locally-executed", "commands": ["python -m pytest -q"]},
    }
    print(json.dumps(record, indent=2))
    return record


if __name__ == "__main__":
    main()
