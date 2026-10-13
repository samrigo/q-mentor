# Repository instructions (kept short on purpose)

Build and test:
- `python scripts/validate_package.py` — manifest, skills, agent, registry DAG, schemas, sources, links.
- `python scripts/validate_math.py` — six-bond fixture, QUBO/Ising conversions, penalty separation.
- `python scripts/validate_responses.py` — response-contract linter against evals/response-format.
- `python scripts/validate_routing.py` — routing fixtures in evals/routing against the registry.
- `python scripts/validate_examples.py` — clean per-target environments from lockfiles; `--static` for the scan only.

Universal rules:
- Behaviour lives in Markdown (`skills/`, `knowledge/`, `templates/`); scripts only validate.
- Synthetic or public data only. No credentials, paid jobs or network calls in default tests.
- Change behaviour eval-first: add a failing eval, then the smallest change.
