# Executive brief — six-bond selection (generated from result records)

**Decision:** Classical now; keep the quantum versions as a teaching exercise only.

Status: complete

**Why:** Checking all 64 choices with ordinary software finds the unique best set A, C, E (score -9.3725) in under a millisecond; 9 quantum and classical tools reproduced or could not represent it, and none improved on it (confidence high).

**Cost / risk:** More quantum work at this size costs staff time and cannot show a speed or quality gain.

**Next gate:** Reopen only for a decision-scale problem where a tuned classical solver misses its time budget.

Evidence (from `demo/bond-selection/result-records/*.json`, 9 records, recorded 2026-10-14; simulators only, single seed per target):

| Target | Versions | Observed outcome | Evidence level |
|---|---|---|---|
| bloqade | bloqade-analog 0.16.9, numpy 2.2.6 | Six-bond: **unsupported-exact**; native 5-atom program P(ground state) 0.516 | executable (level 2) for the native problem; the six-bond QUBO is unsupported-exact here |
| cirq | cirq-core 1.7.0 | QAOA best sample `101010`; P(optimum) 0.0449; feasible 0.9004 | executable (level 2); matching a 64-state toy is not quantum advantage |
| classiq | classiq 1.32.0 | Model built; cost error 1.3e-13 on 64 states; synthesis not run | formulated (level 1); no quantum hardware used; not quantum advantage |
| dwave | dimod 0.12.22, dwave-samplers 1.8.0 | ExactSolver optimum `101010`; simulated annealing optimum rate 0.145 (classical heuristic) | executable classical toolchain; no quantum hardware used |
| pasqal-pulser | pulser 1.9.1 | Six-bond: **unsupported-exact**; native 4-atom toy P(optimum) 0.461 noiseless, 0.3895 with SPAM | executable on a local emulator; geometry-native toy only; not quantum advantage |
| pennylane | pennylane 0.45.1 | QAOA best sample `101010`; P(optimum) 0.0098; feasible 0.3894 | executable on a local simulator; not a hardware result and not quantum advantage |
| perceval | perceval-quandela 1.3.1 | Six-bond: **conditional-impractical** (success 1.8e-34); native 2-qubit conditional match TVD 5e-16, success 0.0082 | executable (level 2), conditional on postselection; not quantum advantage |
| pytket | pytket 2.18.5 | QAOA best sample `101010`; P(optimum) 0.0459; feasible 0.9031 | executable (level 2); matching a 64-state toy is not quantum advantage |
| qiskit | qiskit 2.5.2, qiskit-optimization 0.7.0 | QAOA best sample `101010`; P(optimum) 0.0703; feasible 0.3333 | executable (level 2); matching a 64-state toy is not quantum advantage |
