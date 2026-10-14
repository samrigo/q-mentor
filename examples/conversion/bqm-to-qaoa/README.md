# BQM / annealing → gate QAOA: same objective, different algorithm (class R)

- **Pins:** `dimod==0.12.22`, `qiskit==2.5.2`, `scipy==1.18.1`; CPython 3.13, x86_64 Linux.
- **What is proven:** the six-bond QUBO as a dimod `BinaryQuadraticModel` (offset included) and as a Qiskit Ising
  operator gives the canonical energy on all 64 bitstrings (error < 1e-9); `ExactSolver` returns `101010`.
- **Why R, not E:** annealing (or simulated annealing) and QAOA are different algorithms; their sample distributions,
  schedules, and costs are not comparable. `adapter.classify` returns E only when the algorithm is the same.
- **Negative fixture:** dropping the BQM offset keeps the argmin but shifts every energy by the constant; the test
  rejects it as non-equivalent.

```bash
uv venv && uv pip sync requirements.lock && python -m pytest -q
```

Sources: https://docs.dwavequantum.com/en/latest/ocean/api_ref_dimod/models.html,
https://qiskit-community.github.io/qiskit-optimization/tutorials/02_converters_for_quadratic_programs.html
