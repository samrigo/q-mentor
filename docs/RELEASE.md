# Release checklist

Run on a clean checkout; record results in `CHANGELOG.md`, `registry/compatibility.yml`, `docs/COMPATIBILITY.md`.

1. Contracts: `python scripts/validate_package.py --live-schema`, `validate_math.py`, `validate_routing.py`,
   `validate_responses.py`, `validate_hardware.py`, `score_evidence.py`, `validate_incidents.py`,
   `run_behavior_evals.py --check-cases`.
2. Examples: `python scripts/validate_examples.py` — every folder in a fresh environment from its lock.
3. Optimization regression: confirm `examples/conversion/pulser-to-classiq-qaoa/optimization_record.json` regenerates
   with the same `status` and objective hash; never edit it by hand.
4. Sources: `python scripts/verify_sources.py --live` (Crossref per DOI, arXiv abstract pages, `git ls-remote` for
   repositories); review `docs/SOURCE-CHECK.md`. Publisher 403/429 are `blocked-by-publisher`/`rate-limited`, not
   broken. Re-read SDK changelogs and issues for every pinned bridge (README-12 procedure) and update tag SHAs.
5. Copilot: `QMENTOR_COPILOT_BIN=$(which copilot) python scripts/test_copilot_discovery.py` and
   `python scripts/test_deploy.py`. With a licensed session, capture the prompts in `evals/behavior/cases.yml` and
   run `python scripts/run_behavior_evals.py` once with a strong and once with an economical model; compare
   median answer length and retries.
6. Optional credential gates (Classiq synthesis via `run_remote.py`, D-Wave QPU) only with a budget approval;
   record `target-validated` or leave `unverified`.
7. `python scripts/build_report.py` and commit the regenerated brief.
8. Tag `vX.Y.Z`; attach `SHA256SUMS` of the archive; enable artifact attestations where available.
