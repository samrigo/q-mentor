---
name: q-mentor-exec
description: Use when the user wants a leadership-ready summary of quantum work — 'write an executive brief', 'one-pager for the steering committee', 'summarize the PoC results for leadership', 'decision memo on quantum readiness' — built only from result records or a verdict.
license: MIT
allowed-tools: read
---

# Q-Mentor · Executive brief

Convert measured evidence into one decision with limits, cost, risk, and the next gate.

## Shared files

Resolve from the plugin root (`../../` from this file) or, in repository mode, from `.github/q-mentor/`: registry `registry/skills.yml`, contract `templates/response-contract.md`. If the registry is missing or invalid, answer `Status: blocked` naming the file; do not guess.

## Response template: `decision`

For **every** user-facing answer, including clarification, error, and direct invocation, render `templates/responses/decision.md` through `qmentor.response.v3`; preserve its lead, field order, status, uncertainty, and validation. Do not answer free-form or ask the user to invoke another skill.

## Input

`ResultRecord`s or a `Verdict` (required; plans are not evidence).

## Output

`ExecutiveBrief` (`templates/executive-brief.md`); numbers reconcile with the records; regenerated report: `scripts/build_report.py`.

## Procedure

1. If no result records or verdict exist → `Status: blocked`; `Next gate` names the run or verdict needed. Never manufacture conclusions from a plan.
2. Lead with the decision; one measured fact against a named classical baseline; evidence level.
3. Cost/risk: the one factor most likely to change the decision; separate AI-credit and hardware spend.
4. Matching a toy optimum is not advantage; say so when relevant.

## Stop when

Results not decision-ready (blocked).

## Handoffs

`q-mentor-improve` only after explicit opt-in. The agent decides; do not ask the user to type another command unless approval or a material choice is needed.
