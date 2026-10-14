---
name: q-mentor-help
description: Use when the user asks what Q-Mentor can do, which skill fits a task, or how to start — 'what can you do?', 'which skill should I use to convert Pulser code?', 'how do I use Q-Mentor?', 'list all skills'. Renders the live skill registry; read-only.
license: MIT
allowed-tools: read
user-invocable: true
disable-model-invocation: false
---

# Q-Mentor · Help

Explain the available skills from the live registry so the user can state an outcome instead of a skill itinerary.

## Shared files

Resolve from the plugin root (`../../` from this file) or, in repository mode, from `.github/q-mentor/`: registry `registry/skills.yml`, contract `templates/response-contract.md`. If the registry is missing or invalid, answer `Status: blocked` naming the file; do not guess.

## Response template: `guide`

For **every** user-facing answer, including clarification, error, and direct invocation, render `templates/responses/guide.md` through `qmentor.response.v3`; preserve its lead, field order, status, uncertainty, and validation. Do not answer free-form or ask the user to invoke another skill.

## Input

Optional user goal. Reads ONLY `registry/skills.yml` (not other SKILL.md files).

## Output

Best 1-3 skills for the goal with use-when, input/prerequisite, and output; on "all skills" one row per registry entry: `skill | use when | prerequisite | output` (≤ 20 rows / 350 words). Deterministic reference: `scripts/render_help.py`.

## Procedure

1. Read `registry/skills.yml`; if missing → `Status: blocked`, `Next` names the file to restore.
2. No goal or "all skills" → list every `user_invocable: true` entry exactly once, using its `summary`/`use_when`/`output` text. Never add, rename, or omit a skill; never keep a second menu.
3. With a goal → match it to registry `intents`; show the best 1-3 skills and the prerequisite that would run automatically.
4. If nothing matches, `needs-input` with one question about the outcome.
5. Stay read-only. If the user asks to act ("do it"), hand the chosen skill to the orchestrator; never make the user type a slash command to continue.

## Stop when

Registry missing or invalid (blocked).

## Handoffs

The skill the user chooses, only when the user asks to run it (via `q-mentor-orchestrate`). The agent decides; do not ask the user to type another command unless approval or a material choice is needed.
