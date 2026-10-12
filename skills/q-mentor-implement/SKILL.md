---
name: q-mentor-implement
description: >
  Make the smallest approved repository change from an accepted design, with version
  pins and rollback. Use only after design acceptance. Produces a scoped diff.
---

# q-mentor-implement

## Preconditions

- An accepted design (or create one via `q-mentor-design` first).
- Explicit user approval for any write or credentialed action.
- No paid quantum job submission without separate confirmation.

## Workflow

1. Confirm the design artifacts (ProblemSpec, CanonicalQUBO, TargetPlan, tests).
2. Generate the smallest code change that realizes the approved plan.
3. Pin dependency versions.
4. Include a rollback note.
5. Prefer local simulators; never embed credentials.

## Knowledge links

- `knowledge/providers-qiskit.md`
- `knowledge/framework-pennylane.md`
- `demo/bond-selection/`
