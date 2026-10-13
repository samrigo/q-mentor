---
name: q-mentor-implement
description: "Make the smallest approved repository change from an accepted design: complete files with pinned dependencies, seed, fixture, expected result and validation command. Use only after a design is accepted; produces a scoped diff."
license: MIT
allowed-tools: read, search, edit
---

# Q-Mentor · Implement

Complete, pinned, offline-first code. Diff plus a 5-line result.

## Shared files

Resolve from the plugin root (`../../` from this file) or, in repository mode, from `.github/q-mentor/`:
registry `registry/skills.yml`, contract `templates/response-contract.md`; the one `knowledge/providers-*.md` or `knowledge/framework-pennylane.md` pack for the target in use.
If the registry or contract cannot be found, answer `Status: blocked` naming the missing file. Do not guess.

## Input

Accepted `Design` (run `q-mentor-design` first if missing), `CapabilityReport`, test plan.

## Output

Complete files or a scoped diff, then: files changed · pins · validation command · highest observed state · rollback (revert the commit).
Default mode is brief (`Status`, `Result`, `Validation`, `Next`). Honor `detailed` or `machine` when asked.

## Procedure

1. Confirm the design is accepted and the target mapping is `exact` or approved `approximate`.
2. Follow the example contract: `README.md`, `requirements.in` + lock, `main.py`, `adapter.py`, `test_example.py`, `expected.json`. Mirror `examples/bond-selection/<target>/` in the Q-Mentor repository.
3. Load only the provider pack for the target in use.
4. Use only APIs confirmed in a version-matched official example or reference. Check `registry/compatibility.yml` `stale_apis`.
5. Keep provider dependencies optional; no network calls, credentials or paid jobs by default; remote paths sit behind explicit environment flags.
6. No placeholders. Code you could not run is labelled `draft` or `syntax-checked`.

## Stop when

Required dependency, permission or mapping is absent; design not accepted.

## Handoffs

Always `q-mentor-test`; then `q-mentor-review` for material code. The agent decides; do not ask the user to type another command unless approval or a material choice is needed.
