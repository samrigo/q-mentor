# Six-bond selection — PennyLane

PennyLane is a **framework**, not a hardware provider. This example names its device explicitly.

- **SDK:** `pennylane==0.45.1`
- **Device:** `default.qubit` (local). Analytic device for training; seeded finite-shot device (`seed=7`, 4096 shots via `qml.set_shots`) for sampling.
- **Interface / gradient:** autograd, `diff_method="backprop"`
- **Optimizer:** `qml.AdamOptimizer(stepsize=0.05)`, 80 steps, 2 QAOA layers (`qml.qaoa.cost_layer`, `x_mixer`)
- **Mapping:** exact. Cost Hamiltonian `Σ h_i Z_i + Σ J_ij Z_i Z_j` from the canonical Ising form; the constant offset is added back when reporting.
- **Wire order:** wire k = variable k; sample rows are already in canonical A..F order.

## Run

```bash
uv venv && uv pip sync requirements.lock
python main.py
python -m pytest -q          # <x|H|x> + offset == canonical energy for all 64 basis states
```

## Observed result (2026-10-13)

Best sample `101010`, energy `−9.3725`; optimum probability 0.010 (below the
1/64 uniform baseline), feasibility 0.39. Shallow QAOA on a penalty-dominated
landscape concentrates on feasible states but not on the optimum. Exact
enumeration remains the right tool.

## Sources

- PennyLane QAOA module: https://docs.pennylane.ai/en/stable/code/qp_qaoa.html
- Devices: https://docs.pennylane.ai/en/stable/code/qp_devices.html
- Interfaces and gradients: https://docs.pennylane.ai/en/stable/introduction/interfaces.html
