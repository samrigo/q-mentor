# Classiq adapter

Tested: `classiq==1.32.0` (last_verified 2026-10-13).

**Rule:** treat notebook, Python-Qmod and native Qmod as distinct artifacts; validate locally, gate synthesis behind credentials and approval.

- Python-Qmod: `@qfunc` functions with `QArray[QBit, N]`, `allocate`, `hadamard_transform`, `phase(expr, theta)`, `apply_to_all`, `repeat`.
- Do not use `from __future__ import annotations` in Qmod files: Qmod inspects real type objects.
- Offline: `create_model(main)` serialises the model without network access. `write_qmod(main, name, symbolic_only=False, decimal_precision=...)` writes native Qmod; with the default `symbolic_only=True`, generated helper functions were omitted.
- Credentialed: `synthesize(main)` and `ExecutionSession(qprog, num_shots=..., random_seed=...)` require `classiq.authenticate()`; report as `unverified` until run.
- Global constants in the cost only add a phase; add them back when reporting energies.
- Record: synthesis constraints/preferences, width, depth, backend.

Worked example: `examples/bond-selection/classiq/`.
