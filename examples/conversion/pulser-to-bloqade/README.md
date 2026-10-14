# Pulser ↔ Bloqade: Rydberg analog Hamiltonian translation (README-14)

- **Pins:** `pulser==1.9.1` (+ simulation, qutip 5.3.1), `bloqade-analog==0.16.9`, `numpy==2.2.6` (bloqade needs < 2.3),
  `scipy==1.15.3`; CPython 3.13, x86_64 Linux. No SDK bridge exists; the translation goes through the canonical
  time-dependent Hamiltonian.
- **Program:** 3 atoms on a line, Ω ramp 0 → 2π·0.6 rad/µs (0.2 µs), hold 1.6 µs, ramp down 0.2 µs; Δ −4 → +4 rad/µs
  during the hold; Pulser on `AnalogDevice` (`QutipBackendV2`), Bloqade python emulator; exact final-state probabilities.

| Check | Observed (2026-10-14) |
|---|---|
| C6 | Pulser AnalogDevice 865 723 vs Bloqade `RB_C6` 5 420 441 rad·µm⁶/µs — different device models |
| Matched Hamiltonian | Bloqade coordinates × (C6_b/C6_p)^(1/6) = 1.3576; interactions equal to 4 × 10⁻¹⁵; final distributions TVD 2.8 × 10⁻⁴ → class **E** (tolerance 10⁻³, ODE/time-grid differences) |
| Same µm coordinates | TVD 0.083 → class **A** with that measured error, never "exact" |
| Signs and units | positive final Δ favours Rydberg in both (most probable `101`); Pulser ns vs Bloqade µs converted explicitly |

A shared "Ising" label is insufficient: equality is proven by the executed distributions in `test_example.py`.

```bash
uv venv && uv pip sync requirements.lock && python -m pytest -q
```

Sources: https://docs.pasqal.com/pulser/pulses/, https://www.bloqade.quera.com/vendored/bloqade-analog/
