# Six-bond selection — Bloqade (QuEra analog)

- **SDK:** `bloqade-analog==0.16.9` with `numpy==2.2.6`, `scipy==1.15.3` (see `requirements.lock`; CPython 3.13, x86_64 Linux). numpy ≥ 2.3 fails at run time inside bloqade-analog's pydantic v1 models (`RuntimeError: error checking inheritance of NDArray`, observed 2026-10-14), so numpy is pinned to 2.2.6.
- **Hardware family / model / backend / support level:** neutral atoms (QuEra) / analog Rydberg / bloqade python emulator, noiseless / `tested-local`. Aquila via Amazon Braket AHS is `profiled` and not used.

## Six-bond QUBO: `unsupported-exact`

Rydberg couplings are `C6/r^6` (C6 = `RB_C6` = 5.42 × 10⁶ rad·µm⁶/µs) and fixed by geometry. The QUBO needs
15 independent couplings; six atoms in 2-D have 9 geometric degrees of freedom. The most generous fit (free
global scale, 20 seeded restarts) still misses a coupling by 375 %, so no exact program exists. Use a gate or
annealing target for this QUBO; this matches the Pulser report in `../pasqal-pulser/`.

## Native program (supported)

Five atoms on a line, 6.1 µm apart. The final classical Hamiltonian `E(n) = −δ_f Σ n_i + Σ C6/r_ij⁶ n_i n_j`
(δ_f = 16 rad/µs) is defined by the geometry; its classical ground state is `10101` (energy −44.6865). An adiabatic
sweep (Ω 0 → 15.7 → 0 rad/µs, δ −16 → +16 rad/µs, 4.0 µs) puts 0.516 probability on `10101` in the exact
emulator state; 2000 seeded shots give 0.505.

Bit convention: Bloqade reports `0` for Rydberg; the adapter reads the emulator state via `run_callback` and
returns canonical strings with `1` = Rydberg, atom k = character k (tested with a single-atom π pulse).

## Run

```bash
uv venv && uv pip sync requirements.lock
python main.py
python -m pytest -q
```

Evidence level 2 for the native problem; matching a 32-state classical ground state is not quantum advantage.

## Sources

- Bloqade analog docs: https://www.bloqade.quera.com/vendored/bloqade-analog/ (repository https://github.com/QuEraComputing/bloqade-analog)
- Aquila AHS on Braket: https://docs.aws.amazon.com/braket/latest/developerguide/braket-quera-submitting-analog-program-aquila.html
