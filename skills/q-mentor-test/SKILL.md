---
name: q-mentor-test
description: "Create or run deterministic, equivalence, statistical, noise and cross-target tests in a clean pinned environment and report the observed validation state without hiding failures. Use after implement, or when asked to validate or verify results."
license: MIT
allowed-tools: read, search, edit
---

# Q-Mentor · Test

Evidence, not reassurance. ≤ 120 words on success; focused diagnostics on failure.

## Shared files

Resolve from the plugin root (`../../` from this file) or, in repository mode, from `.github/q-mentor/`:
registry `registry/skills.yml`, contract `templates/response-contract.md`.
If the registry or contract cannot be found, answer `Status: blocked` naming the missing file. Do not guess.

## Input

Implementation and fixtures (run `q-mentor-implement` first if no code exists).

## Output

`TestReport` and `ResultRecord` (`schemas/result-record.schema.json`): commands, attempts, seeds, shots, backend, versions, thresholds, pass/fail, negative results, highest observed validation state.
Default mode is brief (`Status`, `Result`, `Validation`, `Next`). Honor `detailed` or `machine` when asked.

## Procedure

1. Prefer the repository scripts: `python scripts/validate_math.py`, `python scripts/validate_examples.py`, `python -m pytest -q` inside the target folder. Shell commands need the user's confirmation; they are not pre-approved.
2. Order: syntax → import → local execution → exact energy equivalence on all enumerable states → seeded statistics → noise sensitivity.
3. Statistical failure is reported once with its seed; never re-run until it passes.
4. Credentialed or remote checks are opt-in and stay `unverified` when not run — never `passed`.
5. On failure: first failing command, smallest diagnostic, one repair.

## Stop when

Flaky, cherry-picked, incomplete or irreproducible result; missing environment (report `unverified`).

## Handoffs

`q-mentor-implement` for a scoped repair; `q-mentor-review` on pass; `q-mentor-exec` for results. The agent decides; do not ask the user to type another command unless approval or a material choice is needed.
