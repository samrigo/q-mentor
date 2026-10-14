---
name: q-mentor-brainstorm
description: Use when the user wants ideas for where quantum computing could apply — 'where could quantum help our business', 'brainstorm quantum use cases for asset management', 'what logistics problems suit quantum', 'give me options' — returning at most five ranked classical, hybrid, and quantum options.
license: MIT
allowed-tools: read
---

# Q-Mentor · Brainstorm

Offer at most five ranked options, at least one classical, each with readiness, assumption, cost, and falsifier.

## Shared files

Resolve from the plugin root (`../../` from this file) or, in repository mode, from `.github/q-mentor/`: registry `registry/skills.yml`, contract `templates/response-contract.md`, packs `knowledge/quantum-fit.md`. If the registry is missing or invalid, answer `Status: blocked` naming the file; do not guess.

## Response template: `options`

For **every** user-facing answer, including clarification, error, and direct invocation, render `templates/responses/options.md` through `qmentor.response.v3`; preserve its lead, field order, status, uncertainty, and validation. Do not answer free-form or ask the user to invoke another skill.

## Input

Business context and constraints.

## Output

`UseCaseTable` (≤ 5 rows: option · paradigm · readiness · key assumption · falsifier · cost).

## Procedure

1. Identify mathematical kernels (optimization, simulation, sampling, algebraic) in the context; ignore buzzwords.
2. Rank with `knowledge/quantum-fit.md`; a classical option is always present and usually first for small or routine problems.
3. Name what would falsify each quantum option (instance size, baseline gap, data loading cost).
4. No advantage language; readiness is evidence level 1-5, not a promise.

## Stop when

Problem too underspecified (needs-input with one question).

## Handoffs

`q-mentor-frame` and `q-mentor-verdict` for the option the user selects. The agent decides; do not ask the user to type another command unless approval or a material choice is needed.
