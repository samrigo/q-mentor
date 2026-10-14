---
name: q-mentor-verdict
description: Use when the user asks whether quantum computing is a fit — 'should we use quantum for this', 'is this a good quantum use case', 'quantum or classical', 'go/no-go on a quantum PoC', 'quantum readiness score', 'use quantum to sort this CSV' — returning Classical now, Research/teaching PoC, Bounded experiment, or Candidate experiment.
license: MIT
allowed-tools: read
---

# Q-Mentor · Verdict

Decide plainly — including "classical now" — with a score, hard gates, the classical alternative, and when to revisit.

## Shared files

Resolve from the plugin root (`../../` from this file) or, in repository mode, from `.github/q-mentor/`: registry `registry/skills.yml`, contract `templates/response-contract.md`, packs `knowledge/quantum-fit.md`. If the registry is missing or invalid, answer `Status: blocked` naming the file; do not guess.

## Response template: `decision`

For **every** user-facing answer, including clarification, error, and direct invocation, render `templates/responses/decision.md` through `qmentor.response.v3`; preserve its lead, field order, status, uncertainty, and validation. Do not answer free-form or ask the user to invoke another skill.

## Input

`ProblemSpec` (frame runs first if missing), baselines, target constraints.

## Output

`Verdict` (`templates/verdict.md`): hard gates, six scores (structure 25, formulation 20, classical comparison 20, I/O fit 15, resources 10, evidence 10), verdict band, classical method to ship, smallest useful experiment and stop condition, revisit trigger.

## Procedure

1. Apply hard gates first: clear objective, baseline, resource estimate, data class, no unsupported advantage claim. Any failure → no "fit now".
2. Score and map: 0-39 classical now; 40-64 research/teaching PoC; 65-79 bounded experiment with stop condition; 80-100 candidate experiment (not proof of advantage).
3. Name the classical method you would ship today (exact enumeration, MIP/CP-SAT, tuned heuristic) and why it may be preferable.
4. If an experiment is justified, state the smallest one and its stop condition; name target family, model, SDK, backend, and support level.
5. Give a measurable revisit trigger. Do not soften the verdict because the user asked for quantum.

## Stop when

No measurable advantage hypothesis (decision is classical now); ProblemSpec cannot be built.

## Handoffs

`q-mentor-design` for an approved experiment; `q-mentor-exec` for a decision-only request. The agent decides; do not ask the user to type another command unless approval or a material choice is needed.
