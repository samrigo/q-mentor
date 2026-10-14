---
name: q-mentor-review
description: Use when quantum work must be reviewed — 'review my QAOA code', 'check this QUBO formulation', 'sanity-check this quantum PoC', 'is the math right', 'review this diff before I merge', 'audit these claims' — returning findings only.
license: MIT
allowed-tools: read, search
---

# Q-Mentor · Review

Return findings only, highest severity first, covering math, code, hardware fit, claims, tests, and simpler classical alternatives.

## Shared files

Resolve from the plugin root (`../../` from this file) or, in repository mode, from `.github/q-mentor/`: registry `registry/skills.yml`, contract `templates/response-contract.md`, packs `knowledge/optimization-math.md`. If the registry is missing or invalid, answer `Status: blocked` naming the file; do not guess.

## Response template: `review`

For **every** user-facing answer, including clarification, error, and direct invocation, render `templates/responses/review.md` through `qmentor.response.v3`; preserve its lead, field order, status, uncertainty, and validation. Do not answer free-form or ask the user to invoke another skill.

## Input

Diff, files, artifacts, claims.

## Output

Up to three findings in the answer (severity · impact · evidence · fix/owner); more in a findings artifact. "No findings" names the scope reviewed.

## Procedure

1. Math: objective fidelity, units, bit order, matrix convention, penalty separation, Ising constants (`knowledge/optimization-math.md`).
2. Code: completeness, pins, stale APIs, undeclared names, network calls, credentials, decode independent of the sampler.
3. Hardware fit: family/model/backend/support level; geometry, postselection, dynamic-circuit needs.
4. Claims: advantage, `optimized`, `secure`; evidence level; baseline strength.
5. Tests: seeds, budgets, all-state equivalence, negative fixtures. Ask: can classical software do this more simply?
6. No patch unless the user asked for a fix.

## Stop when

Material risk lacks mitigation or owner (finding says so).

## Handoffs

`q-mentor-implement`/`q-mentor-test` for accepted fixes; `q-mentor-pqc-scan` when cryptography is in scope. The agent decides; do not ask the user to type another command unless approval or a material choice is needed.
