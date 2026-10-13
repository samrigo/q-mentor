# D-Wave Ocean adapter

Tested: `dimod==0.12.22`, `dwave-samplers==1.8.0` (last_verified 2026-10-13).

**Rule:** build the BQM from canonical coefficients and verify energies with `dimod.ExactSolver` before any sampler.

- `dimod.BinaryQuadraticModel(linear, quadratic, offset, dimod.BINARY)`; quadratic biases are per pair (stored once).
- SPIN convention is `x = (s + 1)/2` — the negation of the canonical spin.
- Local: `dimod.ExactSolver()` (exact, small only); `dwave.samplers.SimulatedAnnealingSampler().sample(bqm, num_reads=..., seed=...)` (classical heuristic).
- Single-flip annealing struggles with cardinality penalties: moves between feasible states cross the penalty. Consider CQM or swap moves, and say so.
- QPU/hybrid (`dwave-system`, Leap): opt-in only, with cost confirmation. Report logical variables, physical qubits, embedding, chain strength, chain-break fraction, reads, QPU access time vs wall clock. Hybrid solver results are not pure-QPU results.

Worked example: `examples/bond-selection/dwave/`.
