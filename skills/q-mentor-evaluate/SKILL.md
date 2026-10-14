---
name: q-mentor-evaluate
description: Use when a paper, vendor claim, proposal, or experiment must be graded — 'evaluate this quantum paper', 'is this benchmark fair', 'score this PoC proposal', 'plan a fair comparison against Gurobi', 'review the vendor's advantage claim' — producing one scorecard on evidence, baseline, resources, reproducibility, cost, and stop conditions.
license: MIT
allowed-tools: read, search
---

# Q-Mentor · Evaluate

Grade one item on evidence, baseline, resources, reproducibility, and cost; name what the evidence cannot establish.

## Shared files

Resolve from the plugin root (`../../` from this file) or, in repository mode, from `.github/q-mentor/`: registry `registry/skills.yml`, contract `templates/response-contract.md`, packs `knowledge/research-method.md`, `knowledge/quantum-fit.md`. If the registry is missing or invalid, answer `Status: blocked` naming the file; do not guess.

## Response template: `evaluation`

For **every** user-facing answer, including clarification, error, and direct invocation, render `templates/responses/evaluation.md` through `qmentor.response.v3`; preserve its lead, field order, status, uncertainty, and validation. Do not answer free-form or ask the user to invoke another skill.

## Input

Paper, proposal, experiment, or result records; candidate metrics and budget.

## Output

Scorecard / `ExperimentPlan` (`templates/experiment-record.md`): same instances, seeds, budgets, metric definitions, confidence intervals, evidence level 1-5, stop condition.

## Procedure

1. Check the baseline is current, strong, fairly tuned, and measured end to end (data prep, compile, queue, decode).
2. Same instance, seeds, shot/evaluation budget for every arm; report variability. A CVaR objective and mean energy are different metrics.
3. Separate simulator, annealer, gate, analog, photonic, and hybrid-solver results; vendor-only evidence is labelled vendor result.
4. Name the achieved evidence level (formulated, executable, competitive on a toy, scales, advantage evidence). Levels 1-3 are not advantage.

## Stop when

The comparison would be unfair or underpowered (say so and give the fix).

## Handoffs

Back to `q-mentor-design` on failure; otherwise `q-mentor-implement` or `q-mentor-exec`. The agent decides; do not ask the user to type another command unless approval or a material choice is needed.
