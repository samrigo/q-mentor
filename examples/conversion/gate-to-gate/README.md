# Gate ↔ gate conversion (README-14 class E on a supported subset)

- **Pins:** `qiskit==2.5.2`, `pytket==2.18.5`, `pytket-qiskit==0.78.0`, `cirq-core==1.7.0` (+ `ply==3.11`, needed by
  `cirq.contrib.qasm_import` and not installed by cirq-core); CPython 3.13, x86_64 Linux.
- **Source:** Qiskit QAOA layer on a 3-variable slice (bonds A, B, C) of the six-bond QUBO, parameters bound.
- **Routes:** Qiskit → pytket through the maintained `pytket-qiskit` converter; Qiskit → Cirq through the OpenQASM 2
  subset. `pytket-cirq`, `pytket-pennylane`, `pytket-pyquil` are refused (Quantinuum lists them as unmaintained).

| Check | Observed (2026-10-14) |
|---|---|
| Operator equality | equal up to global phase after converting Qiskit little-endian to big-endian order |
| Bit order | ignoring it makes the operators differ (tested) |
| Symbolic parameters | `qiskit_to_tk` raises `ValueError` on an unbound `Parameter` in 0.78.0 → bind first |
| Dynamic circuits | `qasm2.dumps` raises `QASM2ExportError` on `if_test` → rejected for the Cirq route |
| Implicit swaps | after `DefaultMappingPass` onto a line, equality holds only with the initial and final qubit maps |

An interop import alone is not a semantic test: every claim above is an executed assertion in `test_example.py`.

```bash
uv venv && uv pip sync requirements.lock && python -m pytest -q
```

Sources: https://docs.quantinuum.com/tket/extensions/pytket-qiskit/api.html,
https://docs.quantinuum.com/tket/api-docs/extensions.html, https://quantumai.google/cirq/build/interop
