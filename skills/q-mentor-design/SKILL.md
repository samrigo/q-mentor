---
name: q-mentor-design
description: >
  Produce a target-neutral design and a target-specific starter implementation plan.
  Use after a positive or teaching-PoC verdict. Maximum ~800 words.
---

# q-mentor-design

## Workflow

1. Confirm or create a `ProblemSpec` (variables, domains, objective, constraints, scaling, provenance).
2. Build the canonical QUBO / Ising representation with documented coefficient convention.
3. Select classical baseline (exact enumeration for toy sizes, strong heuristic otherwise).
4. Draft `TargetPlan`s for the requested providers/frameworks (default: local Qiskit + PennyLane).
5. Define result schema, seeds, version pins, and acceptance tests before any quantum code.
6. Output follows `templates/provider-design.md`.

## Canonical objects

- ProblemSpec
- CanonicalQUBO (matrix, constant, bit order, penalties)
- TargetPlan
- CapabilityReport

## Knowledge links

- `knowledge/optimization-math.md`
- `knowledge/providers-qiskit.md`
- `knowledge/framework-pennylane.md`
- `templates/provider-design.md`
