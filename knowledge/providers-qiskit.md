# Qiskit adapter

Tested: `qiskit==2.5.2`, `qiskit-optimization==0.7.0` (last_verified 2026-10-13). Re-check release notes before changing pins.

**Rule:** build a `QuadraticProgram`, convert with an explicit penalty, and compare every enumerated state against the canonical energy.

- Model: `QuadraticProgram` with `binary_var`, `minimize(constant, linear, quadratic)`, `linear_constraint(..., "==", rhs)`.
- QUBO: `QuadraticProgramToQubo(penalty=A).convert(qp)`; pass the canonical `A` rather than relying on the automatic penalty.
- Ising: `qubo.to_ising()` returns `(SparsePauliOp, offset)` with `x = (1 − z)/2`.
- Bit order: Qiskit bitstrings are little-endian (qubit 0 rightmost). Reverse before decoding.
- Local execution: `qiskit.primitives.StatevectorSampler(seed=...)`; ansatz `qiskit.circuit.library.qaoa_ansatz(op, reps=p)` (the `QAOAAnsatz` class is deprecated since 2.1).
- Removed: `from qiskit import execute` (Qiskit 1.0).
- Record: qubits, reps, transpilation, shots, seed, optimizer, iterations.

Worked example: `examples/bond-selection/qiskit/`.
