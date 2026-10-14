---
name: q-mentor-frame
description: Use when a business problem must become a precise mathematical model — 'formulate this as a QUBO', 'frame my portfolio selection problem', 'what are the variables and constraints', 'model this scheduling problem', 'write the objective function' — producing a validated ProblemSpec and CanonicalProblem.
license: MIT
allowed-tools: read, search
---

# Q-Mentor · Frame

Produce a validated `ProblemSpec` and domain-neutral `CanonicalProblem` with units, signs, constraints, penalties, and success measures.

## Shared files

Resolve from the plugin root (`../../` from this file) or, in repository mode, from `.github/q-mentor/`: registry `registry/skills.yml`, contract `templates/response-contract.md`, packs `knowledge/optimization-math.md`, `domains/finance/portfolio-optimization.md`. If the registry is missing or invalid, answer `Status: blocked` naming the file; do not guess.

## Response template: `frame`

For **every** user-facing answer, including clarification, error, and direct invocation, render `templates/responses/frame.md` through `qmentor.response.v3`; preserve its lead, field order, status, uncertainty, and validation. Do not answer free-form or ask the user to invoke another skill.

## Input

Objective, data (public or synthetic), constraints, success metric.

## Output

`ProblemSpec` + `CanonicalProblem` (`schemas/canonical-problem.schema.json`): variables and domains, objective with units, constraints, penalty weights with a separation proof, bit order, coefficient convention (`x^T Q x + c`, off-diagonals stated once or twice), provenance.

## Procedure

1. Define the decision and success measure before any math; refuse confidential/client/production data without an approved workflow (`blocked`).
2. Write variables, objective, constraints; keep domain logic in the domain pack (`domains/finance/portfolio-optimization.md`), lifecycle math in `knowledge/optimization-math.md`.
3. Convert equality constraints to penalties `A·g(x)^2`; for ≤ 20 binary variables, enumerate all states to prove the penalty separates feasible and infeasible optima.
4. Record bit order, matrix convention, and the Ising map `x = (1 - s)/2`.
5. Leave one unresolved assumption visible rather than inventing data.

## Stop when

Contradictory or missing requirements; prohibited data.

## Handoffs

`q-mentor-verdict`; `q-mentor-design` only when the verdict justifies it. The agent decides; do not ask the user to type another command unless approval or a material choice is needed.
