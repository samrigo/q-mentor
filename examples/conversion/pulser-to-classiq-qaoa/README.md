# Pasqal/Pulser → Classiq optimization regression (README-10, mandatory)

Five-variable, ten-term QUBO defined by a Pulser register; separate from the six-bond demo fixture.

```text
source/ (Pulser 1.9.1)  ──main.py──▶ program_ir.json + canonical_problem.json + source_result.json
                                         │  (artifacts, not source text)
classiq/ (Classiq 1.32.0) ◀──────────────┘ ──▶ Qmod (p=1,2,4) + optimization_record.json
translation_record.json: route class R (reimplementation); analog schedule unsupported-exact
```

| Question | Answer (observed 2026-10-14) |
|---|---|
| Route | Rydberg analog → gate: **reimplementation** of the shared QUBO |
| Equivalence | Exported Qmod cost = canonical QUBO on all 32 states (error < 1e-9); schedule, noise, timing not carried over |
| Optimization | **not improved**: no variant's 95 % interval for the exact optimum probability lies above the p=1 baseline (0.062) at a fixed 60 000-shot budget per seed |
| Validation | Pulser source locally executed; Classiq model imported; variants on a local reference simulator; Classiq synthesis **unverified** (credentials) |

```bash
python scripts/validate_examples.py --only pulser-to-classiq-qaoa
```

Negative fixtures for this route (stale Pulser API, missing import, undefined name, credential-required synthesis,
energy-changing target, analog schedule labelled exact) live in `evals/conversion/`. The v2 walk-through in
`../pulser-to-classiq/` used `phase(+cost)` and interleaved angles; v3 follows the version-matched official
structure and sign instead.
