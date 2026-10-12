---
name: q-mentor-frame
description: >
  Convert a business problem into variables, objective, constraints, data requirements,
  and success measures. Use when the user describes a decision and needs a precise
  mathematical formulation. Maximum ~600 words.
---

# q-mentor-frame

## Workflow

1. Restate the business decision and success measure.
2. Identify decision variables and domains (prefer binary when a QUBO path is contemplated).
3. Write the objective and constraints in plain math.
4. List data sources, units, scaling, and provenance.
5. State assumptions and unknowns explicitly.
6. Propose a classical baseline method and a validation plan (enumeration for small n).
7. Output follows `templates/frame.md`.

## Shared answer rules

- Separate fact / assumption / estimate / unknown.
- Name a classical baseline.
- Use synthetic or public data by default.

## Knowledge links

- `knowledge/optimization-math.md`
- `domains/finance/portfolio-optimization.md`
- `templates/frame.md`
