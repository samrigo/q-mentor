# Target: Classiq (high-level modeling and synthesis)

`last_verified: 2026-10-12` · sources: `classiq-docs`, `classiq-portfolio-example`

## Operational rule

Classiq synthesizes circuits from a high-level model (Qmod / Python SDK). Preserve the canonical objective at the **model** level, then record every synthesis choice. Synthesis and execution need a Classiq account: offline work stops at model validation.

## Mapping

- Combinatorial problems are expressed as a **Pyomo** model (binary variables, objective, constraints) and handed to Classiq's combinatorial-optimization / QAOA workflow; check the API name for the pinned SDK version.
- To keep energies identical, pass the **penalised canonical objective** (linear Q_ii, quadratic 2 Q_ij, constant c). If hard constraints are passed as Pyomo constraints, Classiq applies its own penalty: label that as a different objective and re-run equivalence.
- Equivalence offline: evaluate the Pyomo objective on all 2^n assignments.

## Record when synthesis is approved

SDK version, synthesis preferences and constraints (max width/depth, optimization target), resulting width, depth, gate counts, execution backend (simulator or hardware provider), shots, seed, decode order.

## Limits

- The synthesized circuit and its resources are unknown until synthesis runs; do not estimate them as facts.
- Classiq routes execution to third-party hardware; hardware claims belong to that provider and need their own capability check.
- Never call `authenticate()` or read credentials without explicit approval.
