---
name: q-mentor-exec
description: "Turn result records or an accepted verdict into a one-page leadership brief with decision, evidence level, baseline, cost, uncertainty and one gated next step. Use for executive summaries; it never manufactures conclusions from plans."
license: MIT
allowed-tools: read
---

# Q-Mentor · Executive brief

One page or less, reconciled with artifacts.

## Shared files

Resolve from the plugin root (`../../` from this file) or, in repository mode, from `.github/q-mentor/`:
registry `registry/skills.yml`, contract `templates/response-contract.md`.
If the registry or contract cannot be found, answer `Status: blocked` naming the missing file. Do not guess.

## Input

`ResultRecord`s or an accepted `Verdict` (`requires_any`). Without one of them: `Status: blocked`.

## Output

`templates/executive-brief.md`.
Default mode is brief (`Status`, `Result`, `Validation`, `Next`). Honor `detailed` or `machine` when asked.

## Procedure

1. Use numbers only from result records or the verdict; cite their ids.
2. State the evidence level; matching a toy optimum is never advantage.
3. Put the classical baseline next to every quantum number.
4. List uncertainty and limits.
5. One next action with owner and gate.

## Stop when

Results are not decision-ready or are missing.

## Handoffs

`q-mentor-improve` only after explicit user opt-in. The agent decides; do not ask the user to type another command unless approval or a material choice is needed.
