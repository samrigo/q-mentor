---
name: q-mentor-review
description: >
  Check math, code, hardware fit, claims, tests, and simpler classical alternatives.
  Output findings only. Use before accepting generated code or advice.
---

# q-mentor-review

## Checklist

1. Is the business objective represented faithfully?
2. Are units, bit order, matrix convention, scaling, and penalties explicit?
3. Is the classical baseline strong and fairly tuned?
4. Are feasibility and decoding tested independently of the sampler?
5. Are resource and cost measurements end-to-end?
6. Are seeds, versions, and backend metadata recorded?
7. Does the conclusion match the achieved evidence level?
8. Can the same result be obtained more simply with classical software?

## Output

Findings only (no soft-pedaling). Severity: blocker / major / minor / note.

## Knowledge links

- `knowledge/optimization-math.md`
- `knowledge/quantum-fit.md`
- `domains/finance/claims-and-limits.md`
