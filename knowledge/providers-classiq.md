# Classiq adapter

Tested: `classiq==1.32.0` (last_verified 2026-10-14). Version-matched reference: `Classiq/classiq-library`
`algorithms/search_and_optimization/QAOA/qaoa.ipynb` at `9e5b7bed123716274150e1221addb03e51a785e7`.

**Rule:** Classiq is a programming and synthesis layer, not hardware. Treat notebook, Python-Qmod and native Qmod as distinct artifacts; validate locally; gate synthesis and execution behind credentials and approval.

## QAOA structure (official pattern)

- Named `cost_layer` → `phase(-cost(v), gamma)`; `mixer_layer` → `apply_to_all(lambda q: RX(beta, q), v)`; `qaoa_ansatz` → `repeat(betas.len, …)`; `main(params: CArray[CReal, 2p])` slices `params[0:p]` (gammas) and `params[p:2p]` (betas).
- Optimise with `ExecutionSession.estimate_cost(cost_func, {"params": …})` inside SciPy COBYLA, or `variational_minimize` (server-side optimiser; not runnable offline). `minimize` is deprecated in 1.32.0.

## Conventions verified on 1.32.0

- `RX(θ) = exp(−iθX/2)` (SDK docstring). `RX(β)` and `RX(2β)` describe the same mixer family with different β ranges; never compare angles across conventions.
- `phase(expr, coefficient)` multiplies `|x⟩` by `exp(i · coefficient · expr(x))`; `phase(−C, γ)` is the cost unitary `exp(−iγC)`.
- `estimate_cost(..., quantile=q)` averages the **lowest** `q` fraction of sampled costs (`classiq.interface.executor.estimate_cost`): `quantile=0.3` = best 30 %. A CVaR objective is not the mean energy; never compare their values.
- `@qperm` is accepted for a phase-only layer and rejected for `RX` ("Non-permutation operation used in a permutation function"). No offline evidence of a synthesis benefit; keep `@qfunc` unless measured.
- `write_qmod(..., symbolic_only=False)` keeps helper functions; the exported expression may be simplified (`1.0·v_i·v_j` → `v_i and v_j`); evaluate what was written, on all states.
- Offline: `create_model` and `write_qmod` need no network. `synthesize` and `ExecutionSession` need `classiq.authenticate()`; report `unverified` until run.
- No `from __future__ import annotations` in Qmod files: Qmod inspects real type objects.

Worked examples: `examples/bond-selection/classiq/`, `examples/conversion/pulser-to-classiq-qaoa/classiq/`.
