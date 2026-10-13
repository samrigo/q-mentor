# Six-bond selection — Qiskit

- **SDK:** `qiskit==2.5.2`, `qiskit-optimization==0.7.0` (see `requirements.lock`)
- **Backend:** `qiskit.primitives.StatevectorSampler` — local, noiseless, seeded (`seed=7`, 4096 shots)
- **Algorithm:** QAOA via `qiskit.circuit.library.qaoa_ansatz`, `reps=2`, SciPy COBYLA (`maxiter=120`)
- **Mapping:** exact. `QuadraticProgram` keeps the cardinality equality as a constraint; `QuadraticProgramToQubo(penalty=15)` reproduces the canonical penalty, and `to_ising()` uses `x = (1 − z)/2`.
- **Bit order:** Qiskit labels are little-endian (qubit 0 rightmost); `adapter.decode_qiskit_bitstring` reverses them into canonical A..F order.

## Run

```bash
uv venv && uv pip sync requirements.lock
python main.py               # prints a ResultRecord JSON
python -m pytest -q          # all 64 states: QUBO and Ising energy == canonical; decode; smoke run
```

## Observed result (2026-10-13)

Exact enumeration: `101010` (A, C, E), energy `−9.3725`. QAOA best sample: `101010`;
optimum probability 0.070, feasibility rate 0.33. A uniform random guess hits the
optimum with probability 1/64 ≈ 0.016. Evidence level 2 (executable). This is not
quantum advantage: 64 states enumerate in microseconds.

## Sources

- Qiskit Optimization converters: https://qiskit-community.github.io/qiskit-optimization/tutorials/02_converters_for_quadratic_programs.html
- Portfolio formulation: https://qiskit-community.github.io/qiskit-finance/tutorials/01_portfolio_optimization.html
- QAOA (Farhi et al., 2014): https://arxiv.org/abs/1411.4028
