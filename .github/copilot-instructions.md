# Repository instructions (kept short on purpose)

Build and test:
- `python scripts/validate_package.py` — manifest, skills, agent, templates, registries (skills, backends, conversion edges, compatibility), schemas, help, coverage.
- `python scripts/validate_math.py` · `validate_routing.py` · `validate_responses.py` · `validate_hardware.py` · `score_evidence.py` · `validate_incidents.py` · `verify_sources.py`.
- `python scripts/validate_examples.py` — every example folder in a fresh environment from its lock; `--static` for the scan only.
- `python scripts/test_deploy.py` — repository-local install/update/rollback/removal.

Universal rules:
- Behaviour lives in Markdown (`skills/`, `knowledge/`, `templates/`); scripts validate.
- Synthetic or public data only. No credentials, paid jobs, or network calls in default tests.
- Change behaviour eval-first: add a failing eval, then the smallest change.
