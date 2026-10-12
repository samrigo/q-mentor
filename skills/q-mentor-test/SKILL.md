---
name: q-mentor-test
description: >
  Create or run deterministic, statistical, noise, and cross-provider tests.
  Report failures without hiding them. Use after implement or when validating math.
---

# q-mentor-test

## Test categories

1. **Deterministic** – enumeration of all 64 assignments for the six-bond fixture; energy match.
2. **Property** – Sigma symmetry, positive-definiteness, penalty separation, bit-order consistency.
3. **Equivalence** – exact target encodings match canonical energy after documented conversion.
4. **Statistical** – sampled results decoded in declared bit order; feasibility marked.
5. **Capability** – Pasqal/Pulser representability gate; PennyLane device naming.

## Rules

- Default suite is offline and credential-free.
- Live-provider tests are opt-in, budget-capped, and require explicit confirmation.
- Never hide a failing assertion.

## Knowledge links

- `demo/bond-selection/`
- `evals/math/`
- `scripts/validate_math.py`
