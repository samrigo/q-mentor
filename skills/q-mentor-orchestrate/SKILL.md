---
name: q-mentor-orchestrate
description: "Internal router for Q-Mentor. Use for multi-phase quantum-computing requests (analyze and implement, convert and validate, end-to-end demo) to select and sequence the minimum Q-Mentor skills from the registry. Not user-invocable."
license: MIT
allowed-tools: read, search
user-invocable: false
disable-model-invocation: false
---

# Q-Mentor · Orchestrate

Turn a user outcome into the smallest safe, ordered chain of Q-Mentor skills and run it.

## Shared files

Resolve from the plugin root (`../../` from this file) or, in repository mode, from `.github/q-mentor/`:
registry `registry/skills.yml`, contract `templates/response-contract.md`.
If the registry or contract cannot be found, answer `Status: blocked` naming the missing file. Do not guess.

## Input

User goal; `registry/skills.yml`; existing artifacts in the conversation or repository.

## Output

`PhasePlan` (internal) then the final skill's answer in the response contract. Report `skills_used` in order.
Default mode is brief (`Status`, `Result`, `Validation`, `Next`). Honor `detailed` or `machine` when asked.

## Procedure

1. Read `registry/skills.yml`. Missing or unparsable → `Status: blocked`.
2. Pick ONE primary skill whose `intents` best match the requested outcome.
3. Add prerequisites only when an artifact in the skill's `requires` is missing or invalid. Reuse valid artifacts. For `requires_any`, one present artifact suffices; if none is present, stop with `needs-input` or `blocked` — never fabricate one.
4. Topologically sort. Reject cycles and duplicate runs of the same skill in a turn.
5. Add a follow-on only if the user's stated outcome needs it (e.g. "implement and validate" adds `q-mentor-test` after `q-mentor-implement`).
6. Cap: 5 skills per turn. Longer workflows: finish the current phase, write a checkpoint artifact (e.g. `ProblemSpec`, `Design`), and say which phase resumes next.
7. Load each `SKILL.md` in turn, passing artifacts (structured blocks or files), not prose summaries. If the client cannot load another skill dynamically, read its `SKILL.md` file; never claim a slash command ran.
8. Stop for approval before paid, credentialed, remote, destructive, production, cryptographic or non-public-data actions. Stop for input only when a missing choice materially changes the result.
9. Emit one final answer (brief mode unless asked otherwise), not one answer per skill.

## Stop when

Registry missing; cycle detected; approval required; required capability unavailable; material user choice open.

## Handoffs

Any skill listed under `follow_ons` in the registry. The agent decides; do not ask the user to type another command unless approval or a material choice is needed.
