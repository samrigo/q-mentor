# Executive brief — six-bond selection (generated from result records)

Status: complete

Result
**Decision: classical now; quantum is a teaching PoC only.** Exact enumeration finds the unique optimum
`101010` (A, C, E), energy -9.3725, in under a millisecond.
No quantum or hybrid run improved on it, and none can at 64 states. Evidence level ≤ 2 everywhere: not quantum advantage.

Validation
| Target | Versions | Observed outcome | Evidence level |
|---|---|---|---|
| classiq | classiq 1.32.0 | Model built; cost error 1.3e-13 on 64 states; synthesis not run | formulated (level 1); no quantum hardware used; not quantum advantage |
| dwave | dimod 0.12.22, dwave-samplers 1.8.0 | ExactSolver optimum `101010`; SA optimum rate 0.145 (classical) | executable classical toolchain; no quantum hardware used |
| pasqal-pulser | pulser 1.9.1 | Six-bond: **unsupported-exact**; native 4-atom toy P(optimum) 0.461 noiseless, 0.3895 with SPAM | executable on a local emulator; geometry-native toy only; not quantum advantage |
| pennylane | pennylane 0.45.1 | QAOA best sample `101010`; P(optimum) 0.0098; feasible 0.3894 | executable on a local simulator; not a hardware result and not quantum advantage |
| qiskit | qiskit 2.5.2, qiskit-optimization 0.7.0 | QAOA best sample `101010`; P(optimum) 0.0703; feasible 0.3333 | executable (level 2); matching a 64-state toy is not quantum advantage |

Source: `demo/bond-selection/result-records/*.json` (5 records, recorded 2026-10-13).
Uncertainty: single seed per target; simulators only; no hardware, queue or cost data.

Next
Use enumeration (or MIP/CP-SAT beyond ~25 assets) in production; revisit quantum only with a decision-scale instance and a tuned classical baseline.
