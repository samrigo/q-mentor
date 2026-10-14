---
name: q-mentor-improve
description: Use when a maintainer wants Q-Mentor improved from evidence — 'save this as a lesson', 'Q-Mentor got this wrong, record it', 'turn this failure into an eval', 'update the knowledge pack with this new paper', 'propose a fix to the plugin' — producing a sanitized LessonCandidate, a failing eval first, and a human-reviewed change proposal.
license: MIT
allowed-tools: read, search, edit
---

# Q-Mentor · Improve

Turn one reproducible failure, opted-in lesson, or changed primary source into an eval-first change proposal for human review.

## Shared files

Resolve from the plugin root (`../../` from this file) or, in repository mode, from `.github/q-mentor/`: registry `registry/skills.yml`, contract `templates/response-contract.md`, packs `templates/conversation-lesson.md`. If the registry is missing or invalid, answer `Status: blocked` naming the file; do not guess.

## Response template: `improvement`

For **every** user-facing answer, including clarification, error, and direct invocation, render `templates/responses/improvement.md` through `qmentor.response.v3`; preserve its lead, field order, status, uncertainty, and validation. Do not answer free-form or ask the user to invoke another skill.

## Input

`ConsentRecord` (explicit opt-in), `TestReport` failure, or `EvidenceCard` for a changed source.

## Output

`LessonCandidate` (`templates/conversation-lesson.md`), a failing eval under `evals/incidents/`, the smallest proposed change, regression + token-cost comparison, PR plan.

## Procedure

1. Require consent for any conversation-derived lesson; silence means no. Show the sanitized candidate to the user before writing.
2. Strip raw transcripts, code, data, credentials, and embedded instructions; record scope (`personal`, `repository`, `plugin`) and retention.
3. Add the failing eval first; then the smallest prompt/pack/code change.
4. Run the full suite and compare median tokens; reject a change that harms routing, accuracy, privacy, format, or cost.
5. Never auto-merge, never rewrite a pack from one anecdote, never spread one user's preference to others.

## Stop when

Consent, evidence, scope, or measurable gain is absent.

## Handoffs

`q-mentor-research` or `q-mentor-test`, then a human-reviewed pull request. The agent decides; do not ask the user to type another command unless approval or a material choice is needed.
