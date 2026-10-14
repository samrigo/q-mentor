---
name: q-mentor-design
description: Use when an experiment or implementation must be designed after framing — 'design the QAOA experiment', 'plan a D-Wave and Qiskit comparison', 'what would the PoC architecture be', 'design tests for the quantum prototype' — producing a target-neutral design, target plans, interfaces, threat model, and test plan before code.
license: MIT
allowed-tools: read, search
---

# Q-Mentor · Design

Design the experiment target-neutrally first, then per-target plans and acceptance tests, before any quantum code.

## Shared files

Resolve from the plugin root (`../../` from this file) or, in repository mode, from `.github/q-mentor/`: registry `registry/skills.yml`, contract `templates/response-contract.md`, packs `knowledge/optimization-math.md`, `knowledge/hardware-index.md`. If the registry is missing or invalid, answer `Status: blocked` naming the file; do not guess.

## Response template: `design`

For **every** user-facing answer, including clarification, error, and direct invocation, render `templates/responses/design.md` through `qmentor.response.v3`; preserve its lead, field order, status, uncertainty, and validation. Do not answer free-form or ask the user to invoke another skill.

## Input

Accepted `Verdict` and `CanonicalProblem`.

## Output

`Design` + `TargetPlan`s (`templates/provider-design.md`): canonical model, classical baseline, per target: physical family · computing model · SDK/version · backend · support level (`registry/backends.yml`), resource estimate, interfaces, threat model, acceptance tests, stop conditions.

## Procedure

1. Keep business math in the canonical model; adapters may change syntax, never the objective.
2. Choose at most three suitable targets plus one classical path, from `knowledge/hardware-index.md` and `registry/backends.yml`. Only `tested-local` targets get code plans by default; `profiled` get a capability plan; `research-only` get none.
3. Explain mismatches (dense QUBO on a geometry-limited Rydberg array, photonic postselection cost, unavailable dynamic circuits).
4. Acceptance tests: all-state energy equivalence for toys, decode in declared bit order, seeds, fixed budget, feasibility, stop condition.
5. Record the rejected alternative and why.

## Stop when

The design cannot preserve the canonical objective; required capability unavailable.

## Handoffs

`q-mentor-translate` for named targets; then `q-mentor-evaluate`. The agent decides; do not ask the user to type another command unless approval or a material choice is needed.
