# Target: D-Wave Ocean (BQM / CQM, annealing, hybrid)

`last_verified: 2026-10-12` · tested: `dimod 0.12.22` · sources: `dwave-models`, `dwave-workflow`

## Operational rule

Build a `BinaryQuadraticModel` in BINARY vartype; verify energies with `dimod.ExactSolver` offline. Report logical variables separately from physical qubits and never present hybrid-solver output as a pure-QPU result.

## Mapping and conventions

- linear[v_i] = Q_ii; quadratic[(v_i, v_j)] = **2 Q_ij** (dimod counts each pair once); offset = c.
- dimod SPIN uses **s = 2x - 1** (s = +1 means x = 1), the opposite of the canonical x = (1 - s)/2: when comparing Ising forms, flip the sign of h; J is unchanged.
- Constraint-native modeling: a CQM keeps constraints explicit for hybrid CQM solvers; that is a different object from the penalised BQM and needs its own feasibility check.

## Offline samplers

`ExactSolver` (exhaustive; toy sizes), simulated annealing from `dwave-samplers`. Both are classical.

## QPU / hybrid path (approval required)

QPU: `DWaveSampler` + `EmbeddingComposite` (minor-embedding). Record solver name, topology, embedding (chain lengths), chain strength, chain-break fraction, num_reads, annealing time, QPU access time vs total wall-clock, and post-processing. Hybrid (Leap) solvers: record solver class and time limit; results are hybrid. A Leap API token is a credential: never read it without approval.

## Limits

Dense problems need long chains; chain breaks and coefficient precision degrade quality. Embedding time and queue time belong in end-to-end comparisons.
