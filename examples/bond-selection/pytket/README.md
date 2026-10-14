# Six-bond selection — pytket

- **SDK:** `pytket==2.18.5`, `scipy==1.18.1` (see `requirements.lock`; CPython 3.13, x86_64 Linux)
- **Hardware family / model / backend / support level:** trapped-ion (Quantinuum TKET compiler) / gate / pytket exact statevector (`Circuit.get_statevector`) + seeded numpy sampling / `tested-local`. Quantinuum hardware via `qnexus` is `profiled` and not used.
- **Algorithm:** QAOA p=2 in pytket half-turn angles (`Rz`, `ZZPhase`, `Rx`); COBYLA (`maxiter=150`, 4 seeded starts); 4096 seeded shots.
- **Compilation:** two pass sequences to `{ZZPhase, PhasedX, Rz}` are compared; both preserve the unitary (error < 1e-14). `FullPeepholeOptimise` doubled the two-qubit count (30 → 60) and depth (20 → 130) on this circuit, so the plain rebase is kept. A pass is not an optimization until its resources are measured.
- **Bit order:** ILO-BE — qubit 0 is the most significant bit, so basis indices read A..F left to right.

## Run

```bash
uv venv && uv pip sync requirements.lock
python main.py
python -m pytest -q          # conventions, all-64-state cost phases, compiled-unitary equality, bit order, smoke
```

## Observed result (2026-10-14)

Exact enumeration: `101010`, `−9.3725`. QAOA best sample `101010`; feasibility 0.90, optimum probability 0.046
(about uniform over the 20 feasible portfolios). Evidence level 2; not quantum advantage.

## Sources

- TKET passes and conventions: https://github.com/Quantinuum/tket (docs: https://github.com/Quantinuum/pytket-docs)
- Quantinuum device access moved to qnexus at pytket-quantinuum 0.56.0: https://docs.quantinuum.com/tket/extensions/pytket-quantinuum/
