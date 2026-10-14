# Six-bond selection — Cirq

- **SDK:** `cirq-core==1.7.0`, `scipy==1.18.1` (see `requirements.lock`; CPython 3.13, x86_64 Linux)
- **Hardware family / model / backend / support level:** superconducting gate (Google Quantum AI family) / gate / `cirq.Simulator` local statevector, seeded / `tested-local`. No QPU is used; Google hardware is `profiled` in `registry/backends.yml`.
- **Algorithm:** QAOA p=2; cost `exp(-i γ H_C / s)` with `s` = largest Ising coefficient, mixer `rx(2β)` = `exp(-i β X)`; COBYLA (`maxiter=150`, 4 seeded starts) on the exact expectation; 4096 seeded shots.
- **Mapping:** exact. `cirq.PauliSum` built from the canonical Ising map `x = (1 − s)/2`; tests prove the energy of all 64 basis states and that the cost layer equals `diag(exp(−iγE(x)))` up to global phase.
- **Bit order:** `LineQubit(k)` = variable k; Cirq state vectors and the measurement key `x` are big-endian in qubit order, so bitstrings read A..F left to right with no reversal.

## Run

```bash
uv venv && uv pip sync requirements.lock
python main.py               # prints a ResultRecord JSON
python -m pytest -q          # energies, phase convention, mixer convention, bit order, smoke run
```

## Observed result (2026-10-14)

Exact enumeration: `101010` (A, C, E), energy `−9.3725`. QAOA best sample `101010`; feasibility rate 0.90,
optimum probability 0.045 — about the 1/20 a uniform choice among the 20 feasible portfolios would give, so the
circuit learned feasibility, not the optimum. Evidence level 2 (executable); not quantum advantage.

## Sources

- Cirq gates and simulators: https://quantumai.google/cirq (repository https://github.com/quantumlib/Cirq, tag v1.7.0)
- QAOA (Farhi et al., 2014): https://arxiv.org/abs/1411.4028
