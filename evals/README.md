# Evals

| Suite | Runs where | How it is graded |
|---|---|---|
| `math/` | CI, offline | Deterministic checks in `scripts/run_evals.py` (no model) |
| `routing/` | Copilot with the plugin installed | Captured response's first line `skill: <name>` |
| `behavior/` | Copilot with the plugin installed | Structural assertions: verdict enum, capability status, required/forbidden phrases, word limit, forbidden actions |
| `incidents/` | Both | Eval written **before** the fix (see `docs/IMPROVEMENT.md`) |

Every case validates against `schemas/eval-case.schema.json`. `run_evals.py` also enforces coverage: each lifecycle phase and each execution target needs a positive and an adversarial case, and every skill needs a routing case.

## Grading captured responses

```bash
mkdir -p captured
# For each case id, run its prompt (with attachments) in Copilot and save the answer to captured/<id>.md.
# Routing cases: put "skill: <skill used>" on the first line.
python scripts/run_evals.py --responses captured
```

Record the client, model, and plugin version alongside each capture. Assertions check fields and claims, not prose, so equivalent wording passes.
