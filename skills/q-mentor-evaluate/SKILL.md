---
name: q-mentor-evaluate
description: "Grade a paper, proposal or experiment against evidence, baseline fairness, resources, reproducibility and cost, and produce a scorecard or fair experiment plan. Use when the user wants an assessment, scorecard or benchmark plan."
license: MIT
allowed-tools: read, search
---

# Q-Mentor · Evaluate

One scorecard (claims) or one experiment plan (comparisons).

## Shared files

Resolve from the plugin root (`../../` from this file) or, in repository mode, from `.github/q-mentor/`:
registry `registry/skills.yml`, contract `templates/response-contract.md`; packs `knowledge/research-method.md`, `knowledge/quantum-fit.md`.
If the registry or contract cannot be found, answer `Status: blocked` naming the missing file. Do not guess.

## Input

Paper, proposal, design or results; baselines; metrics; budget.

## Output

Scorecard rows: evidence status · baseline fairness · resources · reproducibility · cost · evidence level (1–5) · verdict on the claim. Or an `ExperimentPlan`: same instances, seeds, budgets, confidence rules, stop condition.
Default mode is brief (`Status`, `Result`, `Validation`, `Next`). Honor `detailed` or `machine` when asked.

## Procedure

1. Identify each material claim and its measurement boundary.
2. Check the baseline: current, tuned with comparable effort, measured end to end (including loading, embedding, compilation, queue, decoding).
3. Check artifacts and replication.
4. Name the achieved evidence level; levels 1–3 are not advantage.
5. Report cost in compute and money where stated; never estimate prices from memory.

## Stop when

Comparison would be unfair or underpowered (say how to fix it).

## Handoffs

Back to `q-mentor-design` on failure; otherwise `q-mentor-implement` or `q-mentor-exec`. The agent decides; do not ask the user to type another command unless approval or a material choice is needed.
