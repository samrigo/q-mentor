# Executive brief - six-bond selection (synthetic)

_Generated from `result-record.json` (2026-10-12T14:25:20+00:00). Synthetic data; not investment advice._

**Decision:** classical-now (score 48/100, band research-or-teaching-poc; capped: classical baseline sufficient). Use exact classical enumeration; keep quantum as a teaching exercise.

## Evidence
- Exact enumeration of 64 states found A, C, E (bits `101010`), energy -9.3725, in 0.9 ms.
- Seeded simulated annealing reached the optimum in 5/5 seeds.
- qiskit: exact; energies match on all 64 states.
- pennylane: exact; energies match on all 64 states.
- classiq: exact; energies match on all 64 states.
- dwave: exact; energies match on all 64 states.
- pasqal-pulser: unsupported-exact; non-uniform linear terms need local detuning addressability, which this device lacks; required interaction distances are not realisable in 2D (MDS rank 5, negative eigenvalues: False).
- qiskit QAOA (StatevectorSampler (local, noiseless), seed 7, 4096 shots): feasible 42%, best gap 0.0000, P(optimum) 0.024 (95% CI 0.020-0.029).
- pennylane QAOA (default.qubit, seed 7, 4096 shots): feasible 67%, best gap 0.0000, P(optimum) 0.034 (95% CI 0.029-0.040).

## Evidence level
competitive-on-a-toy. Matching a 64-state toy optimum is **not** quantum advantage.

## Limits
- Toy mean-variance model: no prices, lots, liquidity, turnover, taxes, or estimation error.
- Simulators are noiseless; no hardware, queue time, or provider cost measured.

## Next gate
Revisit only with a problem class where a tuned classical solver (MIP/CP-SAT) measurably struggles and an end-to-end benchmark plan is approved.
