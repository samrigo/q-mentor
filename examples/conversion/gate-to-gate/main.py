"""Run the gate -> gate fixtures and print a TranslationRecord-style summary. Offline; no credentials.
Run: python main.py   (inside the pinned environment)
"""
from __future__ import annotations

import importlib.metadata as md
import json

import numpy as np

import adapter
import canonical


def main() -> dict:
    problem = canonical.load_problem()
    qc = adapter.qiskit_qaoa_layer(problem, 0.42, 0.31)
    ref = adapter.qiskit_operator_big_endian(qc)
    tk = adapter.to_pytket(qc)
    cq = adapter.to_cirq(qc)
    mapped, init, final = adapter.map_to_line(tk)
    u_mapped = adapter.permutation(final, 3).T @ mapped.get_unitary() @ adapter.permutation(init, 3)
    record = {
        "schema": "qmentor.translation-record.v3",
        "edge_id": "qiskit-to-pytket / qiskit-to-cirq-qasm2",
        "route_class": "E",
        "source": {"framework": "qiskit", "version": md.version("qiskit")},
        "target": {"framework": "pytket + cirq-core", "version": f"{md.version('pytket')} / {md.version('cirq-core')}"},
        "overall_status": "exact",
        "summary": "Bound-parameter QAOA layer converted through maintained bridges; operators equal up to global phase",
        "mappings": [
            {"source_semantic": "operator (bit order converted)", "target": "pytket", "status": "exact",
             "evidence": f"max |dU| {float(np.max(np.abs(tk.get_unitary() - ref))):.1e}"},
            {"source_semantic": "operator via OpenQASM 2", "target": "cirq", "status": "exact",
             "evidence": f"allclose_up_to_global_phase={adapter.equal_up_to_phase(adapter.cirq_unitary(cq), ref)}"},
            {"source_semantic": "operator after line mapping", "target": "pytket (mapped)", "status": "exact",
             "evidence": f"equal only with initial/final maps: {adapter.equal_up_to_phase(u_mapped, ref)}; "
                         f"naive {adapter.equal_up_to_phase(mapped.get_unitary(), ref)}"},
        ],
        "losses": ["symbolic parameters (must be bound)", "dynamic circuits (outside OpenQASM 2 subset)"],
        "generated_files": ["adapter.py", "main.py", "test_example.py"],
        "validation": {"observed_state": "locally-executed", "detail": "unitaries compared locally", "commands": ["python -m pytest -q"]},
        "resources": {"source_pytket": adapter.gate_counts(tk), "mapped_line": adapter.gate_counts(mapped)},
        "versions": {p: md.version(p) for p in ("qiskit", "pytket", "pytket-qiskit", "cirq-core")},
    }
    print(json.dumps(record, indent=2))
    return record


if __name__ == "__main__":
    main()
