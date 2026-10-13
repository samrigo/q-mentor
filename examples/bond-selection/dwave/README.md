# Six-bond selection — D-Wave Ocean

- **SDK:** `dimod==0.12.22`, `dwave-samplers==1.8.0`
- **Solvers:** `dimod.ExactSolver` (classical exact, all 64 states); `dwave.samplers.SimulatedAnnealingSampler` (classical heuristic, `seed=7`, 200 reads)
- **QPU:** not run. `adapter.qpu_sampler_guarded()` refuses unless `QMENTOR_ALLOW_REMOTE=1` and `QMENTOR_CONFIRM_COST=yes`, and needs the optional `dwave-system` package plus a Leap token from an approved secret store.
- **Coefficient convention:** BINARY linear = canonical `a_i`, quadratic = upper-triangular `b_ij`, offset = `c`.
- **Sign convention:** dimod SPIN uses `x = (s + 1)/2`, the opposite of the canonical `x = (1 − s)/2`; the test proves `s_dimod = −s_canonical`.

## Run

```bash
uv venv && uv pip sync requirements.lock
python main.py
python -m pytest -q
```

## Observed result (2026-10-13)

ExactSolver: `101010`, `−9.3725`. Simulated annealing: 100 % feasible reads, but
only 14.5 % hit the optimum — single-bit-flip moves cannot travel between
feasible states without crossing the cardinality penalty. Retuning the beta
range made it worse (6 %). A swap-move heuristic or CP-SAT would be the fair
scalable baseline; for six variables, enumeration wins.

Logical variables: 6. Physical qubits, chain strength and chain breaks: not
applicable (no QPU embedding was performed).

## Sources

- Ocean SDK: https://docs.dwavequantum.com/en/latest/ocean/
- Models (BQM/CQM): https://docs.dwavequantum.com/en/latest/concepts/models.html
- SampleSet semantics: https://docs.dwavequantum.com/en/latest/concepts/samplesets.html
