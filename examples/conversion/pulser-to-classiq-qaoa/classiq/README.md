# Target side — Classiq QAOA reimplementation and optimization record

- **SDK:** `classiq==1.32.0`, `numpy==2.5.4`, `scipy==1.18.1`; CPython 3.13, x86_64 Linux.
- **Route:** Rydberg analog → gate = **reimplementation** of the shared QUBO. The adiabatic schedule, device noise and
  pulse timing are not carried over (they have no exact circuit equivalent).
- **Structure (version-matched):** the official `Classiq/classiq-library` QAOA notebook at
  `9e5b7bed123716274150e1221addb03e51a785e7` (2026-10-14): named `cost_layer` (`phase(-cost(v), gamma)`),
  `mixer_layer` (`RX(beta, q)`), `qaoa_ansatz` (`repeat`), `params[0:p]` / `params[p:2p]`, COBYLA on `estimate_cost`.

## Tested conventions (classiq 1.32.0)

| Item | Observed |
|---|---|
| `RX(θ)` | `exp(−iθX/2)` (SDK docstring); `RX(β)` ≠ `RX(2β)`, angles are relabelled, never reused across conventions |
| Cost layer | `phase(−C/s, γ)` = `exp(−iγC/s)`, `s` = max coefficient; exported Qmod expression equals the canonical QUBO on all 32 states (the SDK rewrites `1.0·v_i·v_j` as `v_i and v_j`) |
| `@qperm` | accepted for the phase-only cost layer; **rejected** for the RX mixer (“Non-permutation operation used in a permutation function”). No synthesis benefit is measurable offline, so `@qfunc` (official pattern) is kept |
| `quantile` | `estimate_cost(..., quantile=q)` averages the **lowest** `q` fraction of sampled costs (`quantile=0.3` = best 30 %, not "drop the best 70 %") |

## Optimization comparison (`../optimization_record.json`)

Fixed: QUBO (sha256 recorded), feasible set (all 32), initial state `H^⊗5`, decode, total budget 60 000 shots per seed,
seeds 7/11/13. Variants: p = 1, 2 (stage 1) and p = 4 (stage 2, run because stage-1 optimum probability < 0.5);
objectives mean (`quantile=1.0`) and CVaR (`quantile=0.3`); a shot-split variant 4000 × 15 vs 1000 × 60.
Primary metric: exact optimum probability at the final angles. Cap: ≤ 80 two-qubit gates.

**Result (2026-10-14): `not-improved`.** Baseline p1-mean 0.062 (95 % CI 0.013–0.110). Best mean is p2-cvar 0.106, but
its interval overlaps the baseline's; p = 4 (80 two-qubit gates) reached 0.075 and does not find the optimum
reliably. The simpler variant is kept. For reference, the source QAA reached 0.194 on the same objective, and
exhaustive enumeration finds `10110` exactly in microseconds. Nothing here is an advantage claim.

Classiq synthesis/execution needs credentials and was **not run**: variants were evaluated on `adapter.statevector`,
a local reference simulator of the identical ansatz. `run_remote.py` repeats the comparison on Classiq's simulator
only with `QMENTOR_ALLOW_REMOTE=1` after approval.

```bash
uv venv && uv pip sync requirements.lock
python main.py           # model build + Qmod export (p=1,2,4) + fixed-budget comparison
python -m pytest -q
```
