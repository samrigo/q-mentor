---
name: q-mentor-verdict
description: "Decide classical now, research/teaching PoC, bounded experiment or candidate experiment for a framed problem, with hard gates, a 100-point score, the classical alternative and a revisit trigger. Use when the user asks whether to use quantum or whether quantum fits."
license: MIT
allowed-tools: read
---

# Q-Mentor · Verdict

Give an honest go/no-go in ≤ 300 words. Recommending **classical now** without hedging is a correct outcome.

## Shared files

Resolve from the plugin root (`../../` from this file) or, in repository mode, from `.github/q-mentor/`:
registry `registry/skills.yml`, contract `templates/response-contract.md`; packs `knowledge/quantum-fit.md`.
If the registry or contract cannot be found, answer `Status: blocked` naming the missing file. Do not guess.

## Input

`ProblemSpec` (run `q-mentor-frame` first if missing), baselines, target constraints.

## Output

`templates/verdict.md`.
Default mode is brief (`Status`, `Result`, `Validation`, `Next`). Honor `detailed` or `machine` when asked.

## Procedure

1. Apply hard gates: objective, baseline, resource estimate, data class, advantage claims. Any failure → no "fit now".
2. Score the six dimensions; map 0–39 classical now, 40–64 PoC, 65–79 bounded experiment, 80–100 candidate experiment.
3. Name the classical method you would ship today and why.
4. If an experiment is justified, state the smallest useful one and its stop condition.
5. Give a measurable revisit trigger (problem size, hardware metric, new evidence).
6. Do not soften the verdict because the user asked for quantum.

## Stop when

No measurable advantage hypothesis (verdict is classical now); missing ProblemSpec that frame cannot build.

## Handoffs

`q-mentor-design` for an approved experiment; `q-mentor-exec` for a decision-only brief. The agent decides; do not ask the user to type another command unless approval or a material choice is needed.
