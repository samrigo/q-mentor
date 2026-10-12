# Target: Qiskit (gate-model SDK)

`last_verified: 2026-10-12` · tested: `qiskit 2.5.2`, `qiskit-optimization 0.7.0` · sources: `qiskit-optimization-docs`, `ibm-qaoa-tutorial`, `qopt-best-practices`

## Operational rule

Map QUBO -> Ising -> `SparsePauliOp`; run locally with seeded primitives; decode bitstrings by **reversing** them (Qiskit is little-endian: qubit 0 is the rightmost character).

## Mapping

- Qubit i holds canonical variable i. Z_i for h_i, Z_i Z_j for J_ij, plus the scalar offset.
- `SparsePauliOp.from_sparse_list([("Z",[i],h_i), ("ZZ",[i,j],J_ij)], n)`.
- Cross-check: `QuadraticProgram.to_ising()` returns `(operator, offset)`; pass linear = Q_ii and quadratic = 2 Q_ij so energies match.
- `qiskit_optimization` converters (`QuadraticProgramToQubo`) choose their own penalty; if used, re-run all-state equivalence.

## Offline execution

`QAOAAnsatz(op, reps=p)` from `qiskit.circuit.library`; `StatevectorEstimator(seed=...)` for the cost, a classical optimizer (e.g. SciPy COBYLA), then `StatevectorSampler(seed=...)` for samples. Record reps, optimizer, iterations, shots, seed.

## Hardware path (approval required)

IBM hardware uses `qiskit-ibm-runtime` (SamplerV2/EstimatorV2) with an account token, transpilation via a preset pass manager, and optional error mitigation. Record backend name, transpiled depth and two-qubit gate count, shots, queue time, and job IDs. Never run without explicit approval and a cost estimate.

## Limits

- Statevector simulation scales as 2^n memory; ~30 qubits is a practical ceiling on a laptop.
- Dense QUBOs need all-to-all ZZ terms; on hardware, routing adds SWAPs and depth.
- QAOA at low p is a heuristic; report distributions, not a lucky best sample.
