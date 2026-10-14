# Six-bond selection — Perceval (Quandela photonic, discrete-variable)

- **SDK:** `perceval-quandela==1.3.1` (see `requirements.lock`; CPython 3.13, x86_64 Linux)
- **Hardware family / model / backend / support level:** photonics (Quandela) / photonic-DV / `Processor("SLOS")` local, perfect source / `tested-local`. Quandela cloud QPUs are `profiled` and not used.

## Six-bond QUBO: conditional in principle, impractical

On dual-rail qubits every CNOT is probabilistic. One QAOA layer needs 15 ZZ terms = 30 CNOTs: 29 heralded (2/27
each, 58 ancilla photons) and one postselected (1/9). Unconditional success ≈ 1.8 × 10⁻³⁴ per run, so no code is
generated for the six-bond case (`adapter.six_bond_report`).

## Native program (supported)

Two-variable sub-problem from the same data: choose exactly one of bonds A and C (energies: `01` −3.425, `10`
−2.5, `11` 9.165, `00` 15.0). QAOA p=1 on two dual-rail qubits with one heralded and one postselected CNOT.
The conditional logical distribution equals the ideal gate-model distribution (total-variation distance 5 × 10⁻¹⁶);
the **unconditional success probability is 0.0082** (2/27 × 1/9), reported alongside it. p=1 cannot separate the
two feasible answers (0.478 vs 0.479): a correct conversion is not a good optimizer.

Conventions (tested): logical 0 = photon in the first mode of a pair; Perceval `BS.Rx(θ)` equals the standard
`RX(−θ)`, so the adapter builds `RX(θ)` as `BS.Rx(theta=−θ)`; `RZ(θ)` = `PS(−θ/2)`, `PS(θ/2)`.
`build_processor` is deprecated since Perceval 1.2; the adapter uses `build_experiment` and `pcvl.Experiment`.

## Run

```bash
uv venv && uv pip sync requirements.lock
python main.py
python -m pytest -q
```

## Sources

- Perceval docs and catalog: https://perceval.quandela.net/docs/ (repository https://github.com/Quandela/Perceval, tag v1.3.1)
