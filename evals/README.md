# Evals

| Folder | What | Runner | Offline |
|---|---|---|---|
| `routing/` | Skill selection, prerequisites, follow-ons, cap, cycles, unavailable skills | `scripts/validate_routing.py` | yes |
| `math/` | Penalty separation, optimum shifts, bit-order errors | `scripts/validate_math.py` | yes |
| `response-format/` | Brief/detailed/machine contract, verbosity, headings, praise, duplicates, advantage claims, placeholders, JSON | `scripts/validate_responses.py` | yes |
| `conversion/` | Stale/deprecated sources, missing import, undefined name, partial code, ungated credentials, energy-changing target, translation record | `scripts/validate_examples.py --static` | yes |
| `behavior/` | Live prompts with structural assertions (classical-only, research, injection, prohibited data, Pulser, PennyLane, PQC, exec, remote gate, modes) | `scripts/run_behavior_evals.py` on captured answers | needs Copilot |
| `behavior/pqc-fixtures/` | RSA/ECC/DH, AES, SHA, false positive | `scripts/pqc_inventory.py` (checked by `validate_package.py`) | yes |
| `incidents/` | Sanitized, consented lesson candidates | reviewed by maintainers | — |
