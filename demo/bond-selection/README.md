# Demo: six-bond selection

Synthetic, normalized scores — not market data or investment advice.

Select exactly three of six bonds, balancing yield score `μ`, covariance risk `Σ`, and closeness
to a target total duration of 15.0:

`E(x) = 1.5·xᵀΣx − μᵀx + 15·(Σx − 3)² + 0.25·(dᵀx − 15)²` (full symmetric `Σ`).

- `problem.json` — the CanonicalProblem (bit order: A..F left to right).
- `canonical.py` — standard-library energy, QUBO expansion, Ising map, enumeration, decoding.
- `expected.json` — ground truth: `101010` (A, C, E), yield 11.9, risk 1.67, duration 14.7, energy −9.3725; runner-up A, D, E at −9.1675; gap 0.2050; best infeasible 5.1275 (penalty separates).

```bash
python demo/bond-selection/canonical.py
python scripts/validate_math.py
```

## The one-prompt path

Ask Copilot (q-mentor agent): *"Analyze, design, implement, and validate the six-bond example across the supported targets."*
The orchestrator runs frame → verdict → design → implement → test in the first turn (five-skill cap),
checkpoints, then continues with translate/evaluate/review/exec. Expected verdict: **classical now;
quantum teaching PoC only** — 64 states are trivial to enumerate. Target results are in `examples/`.

Second verdict fixture: *"Use quantum computing to sort a 200-row CSV"* → classical now (`evals/behavior/cases.yml`).
