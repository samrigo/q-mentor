# Repository instructions (Q-Mentor)

Build and test (offline, no credentials):

- `pip install -e ".[dev]"` (core) or `pip install -e ".[dev,all-targets]"` (all local targets)
- `python scripts/validate_package.py` - manifest, agent, skills, packs, sources, schemas, secrets
- `python scripts/run_evals.py` - eval schema, coverage, and the deterministic math suite
- `python -m pytest -m "not slow"` - fast tests; `python -m pytest` adds local QAOA runs
- `python -m qmentor.demo` - six-bond demo; writes result record and executive brief

Universal rules:

- Markdown skills are the source of behavior; Python exists only for deterministic checks.
- Synthetic or public data only. Never add secrets, client data, or credentials to fixtures, logs, or docs.
- Never run remote or paid quantum jobs, read provider tokens, or change cryptography without explicit approval.
- Never claim quantum advantage without a reproducible end-to-end benchmark against a strong classical baseline.
- Behavior changes start with a failing eval (see `docs/IMPROVEMENT.md`).
- Keep each `SKILL.md` under 120 lines and each knowledge pack under ~1,000 tokens.
