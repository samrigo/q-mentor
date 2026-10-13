---
name: q-mentor-brainstorm
description: "Suggest at most five candidate uses of quantum computing for a stated domain or problem and rank their readiness against classical alternatives. Use when the user asks where quantum could help or wants a shortlist of options."
license: MIT
allowed-tools: read
---

# Q-Mentor · Brainstorm

Produce one ranked table of ≤ 5 options that exposes assumptions, cost and falsifiers.

## Shared files

Resolve from the plugin root (`../../` from this file) or, in repository mode, from `.github/q-mentor/`:
registry `registry/skills.yml`, contract `templates/response-contract.md`; packs `knowledge/quantum-fit.md`.
If the registry or contract cannot be found, answer `Status: blocked` naming the missing file. Do not guess.

## Input

Domain, problem context, constraints, data class.

## Output

Table: option · kernel (optimization/simulation/sampling/algebraic) · classical incumbent · readiness (classical now / PoC / bounded experiment) · falsifier · first cheap test.
Default mode is brief (`Status`, `Result`, `Validation`, `Next`). Honor `detailed` or `machine` when asked.

## Procedure

1. Include classical and hybrid options alongside quantum ones; at least one row is usually "classical now".
2. Rank by readiness using `quantum-fit.md` gates, not novelty.
3. Each row names the data that would disprove its value.
4. Keep it to one table plus `Validation` and `Next`.

## Stop when

Problem too underspecified to name a kernel (ask one question).

## Handoffs

`q-mentor-frame` and `q-mentor-verdict` for the option the user selects. The agent decides; do not ask the user to type another command unless approval or a material choice is needed.
