# Classiq reimplementation of the Pulser-native QUBO

- **SDK:** `classiq==1.32.0`
- **Input:** `../canonical_problem.json`, extracted from the Pulser program by `../extract_ir.py`
- **Model:** 2-layer QAOA (`phase` cost + `RX` mixer) over 4 qubits; qubit k = atom k; `|1>` = Rydberg.
- **Status:** reimplementation of the objective. The analog adiabatic schedule is **unsupported-exact** (see `../translation_record.json`).
- **Validation state:** `imported` — `create_model` and the native Qmod cost polynomial are checked against the canonical energy for all 16 assignments. Synthesis needs Classiq credentials and is not run.

```bash
uv venv && uv pip sync requirements.lock
python main.py
python -m pytest -q
```

Expected: optimum `1001`, energy −11.974547 rad/µs (same as the Pulser source's canonical optimum).
Source: Qmod reference https://docs.classiq.io/qmod-reference
