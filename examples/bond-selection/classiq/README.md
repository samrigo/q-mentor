# Six-bond selection — Classiq

- **SDK:** `classiq==1.32.0`
- **Model:** Python-Qmod QAOA, 2 layers: `hadamard_transform`, `phase(cost(x), gamma)`, `apply_to_all(RX(beta))`. `cost` is the canonical QUBO polynomial; the constant `c` is a global phase and is added back when reporting.
- **Native Qmod:** `bond_selection.qmod`, written by `write_qmod(..., symbolic_only=False, decimal_precision=10)`. With the default `symbolic_only=True`, helper functions were omitted from the file — a silent loss the test now catches.
- **Offline gate:** `create_model` runs locally. The tests extract the phase polynomial from both the serialized model and the native `.qmod` file and check it against the canonical energy on all 64 states.
- **Credentialed gate:** `synthesize` + `ExecutionSession.sample` run only with `QMENTOR_ALLOW_REMOTE=1` and `QMENTOR_CONFIRM_COST=yes` after `classiq.authenticate()`. **Unverified** in this repository: no credentials were used.

## Run

```bash
uv venv && uv pip sync requirements.lock
python main.py
python -m pytest -q
```

Validation state: `imported` (model creation and cost equivalence verified locally).

## Sources

- Classiq documentation: https://docs.classiq.io/
- Qmod reference: https://docs.classiq.io/qmod-reference
- Classiq library portfolio example: https://github.com/Classiq/classiq-library/tree/main/applications/finance/portfolio_optimization
