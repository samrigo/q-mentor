---
name: q-mentor-frame
description: "Convert a business problem into a precise ProblemSpec and CanonicalProblem: variables, units, objective, constraints, penalties, data and success measures. Use when the user describes a decision to model, or before any verdict, design or translation."
license: MIT
allowed-tools: read, search
---

# Q-Mentor · Frame

Produce a validated `ProblemSpec` (≤ 450 words) and, for binary problems, a `CanonicalProblem` in the schema `schemas/canonical-problem.schema.json`.

## Shared files

Resolve from the plugin root (`../../` from this file) or, in repository mode, from `.github/q-mentor/`:
registry `registry/skills.yml`, contract `templates/response-contract.md`; packs `knowledge/optimization-math.md`, `domains/finance/portfolio-optimization.md`.
If the registry or contract cannot be found, answer `Status: blocked` naming the missing file. Do not guess.

## Input

Decision, objective, data (public or synthetic), constraints, success metric.

## Output

`templates/frame.md` fields. State matrix convention, bit order and penalty weights explicitly.
Default mode is brief (`Status`, `Result`, `Validation`, `Next`). Honor `detailed` or `machine` when asked.

## Procedure

1. Name the decision and success measure first.
2. Define variables with domains and units; fix bit order.
3. Write the objective; say whether quadratic cross terms appear once or twice.
4. Classify constraints as hard or penalty; for penalties, state why the weight separates feasible from infeasible optima (prove by enumeration when ≤ ~20 binaries, via local code if available).
5. Check signs, units, leakage of future information, and that a feasible assignment exists.
6. Label facts, assumptions, estimates and unknowns.

## Stop when

Contradictory or missing requirements that change the model; prohibited data supplied.

## Handoffs

`q-mentor-verdict`; `q-mentor-design` only when the verdict justifies it. The agent decides; do not ask the user to type another command unless approval or a material choice is needed.
