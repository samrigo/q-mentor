---
name: q-mentor-orchestrate
description: Internal Q-Mentor router. Use whenever a quantum-computing request spans more than one phase (e.g. 'analyze, design, implement and validate', 'convert this Pulser code to Classiq and test it', 'is this a quantum fit and if so build a PoC') or when another Q-Mentor skill is invoked without its prerequisite artifact. Selects and orders the minimum skills from the registry so users never name skills.
license: MIT
allowed-tools: read, search
user-invocable: false
disable-model-invocation: false
---

# Q-Mentor · Orchestrate (internal router)

Select and sequence the fewest Q-Mentor skills for the user's outcome. Emit a typed `PhasePlan`, never a user answer.

## Shared files

Resolve from the plugin root (`../../` from this file) or, in repository mode, from `.github/q-mentor/`: registry `registry/skills.yml`, contract `templates/response-contract.md`. If the registry is missing or invalid, answer `Status: blocked` naming the file; do not guess.

## Response template: none (internal)

Emit only a typed `PhasePlan`. The terminal skill of the chain renders the single user answer through its registered template and `qmentor.response.v3`.

## Input

User outcome; `registry/skills.yml`; artifacts already present (ProblemSpec, CanonicalProblem, Verdict, Design, ProgramIR, CapabilityReport, Implementation, ResultRecord …).

## Output

`PhasePlan`: ordered `skills_used`, artifacts passed between them, approvals needed, checkpoint (if any). The terminal skill renders the single user answer with its own template.

## Procedure

1. Read `registry/skills.yml`. Missing or unparsable → the terminal answer is `Status: blocked` naming the file. Never guess a skill list.
2. Pick ONE primary skill by `intents` and the requested outcome (help questions → `q-mentor-help`; code in another SDK/hardware → `q-mentor-convert`).
3. Add prerequisites only when an artifact in `requires` (or every artifact in `requires_any`) is missing or invalid. Reuse valid artifacts.
4. Topologically sort; reject cycles and running a skill twice in one turn.
5. Add a follow-on only if the stated outcome needs it ("…and validate" → `q-mentor-test`; "…and is it better" → optimization inside `q-mentor-convert`).
6. Cap: 5 skills per turn. Longer workflows end at a checkpoint artifact and name the phase that resumes.
7. Load one `SKILL.md` at a time and only the packs it names; pass artifacts, not prose. If the client cannot load a skill dynamically, read its file; never claim a slash command ran.
8. Stop for approval before paid, credentialed, remote, destructive, production, cryptographic, or non-public-data actions; stop for input only on a material choice.
9. Return one final answer in the terminal skill's template; record `skills_used` in order.

## Stop when

Registry missing; cycle; approval required; capability unavailable; material user choice open.

## Handoffs

Any skill listed in the registry, in dependency order. The reference implementation of these rules is `scripts/route.py` (tested by `evals/routing/cases.yml`). The agent decides; do not ask the user to type another command unless approval or a material choice is needed.
