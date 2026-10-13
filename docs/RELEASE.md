# Release checklist

Run on a clean checkout. Record results in `CHANGELOG.md` and `registry/compatibility.yml`.

1. `python scripts/validate_package.py` — manifest, skills, agent, registry DAG, schemas, coverage.
2. `python scripts/validate_math.py`, `python scripts/validate_routing.py`, `python scripts/validate_responses.py`.
3. `python scripts/validate_examples.py` — fresh per-target environments from locks.
4. `python scripts/verify_sources.py --live` — every URL reachable; update `last_verified` and set
   `verification: live` only for entries you actually checked; refresh `knowledge/recent-research.md`.
5. Copilot client matrix (needs a Copilot licence): `copilot plugin install ./`, `/agent`, `/skills list`,
   then capture the prompts in `evals/behavior/cases.yml` and run `python scripts/run_behavior_evals.py`.
   Test once with a strong reasoning model and once with an economical one; compare median tokens.
6. Disabled-plugin behaviour: uninstall and confirm no `q-mentor` skills remain.
7. Repository-local: `deploy_repo_local.py --dry-run`, deploy, re-deploy (no changes), modify a file
   (refusal), `--uninstall`.
8. Optional credentialed gates (Classiq synthesis, D-Wave QPU) only with budget approval; record as
   `target-validated` or leave `unverified`.
9. Tag `vX.Y.Z`; attach `SHA256SUMS` of the release archive; enable artifact attestations where available
   (`artifact-attestations` in `knowledge/sources.yml`).
