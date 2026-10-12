# Portfolio and bond selection (binary mean-variance)

`last_verified: 2026-10-12` · sources: `markowitz-1952`, `qiskit-finance-portfolio`, `egger-2020`

## Operational rule

Use the binary mean-variance model to **teach** encodings and provider translation. Solve it classically first; at toy scale, exact enumeration is the production answer.

## Model

```text
minimize  q x^T Sigma x - mu^T x + A (1^T x - B)^2 [+ soft targets]
x_i in {0,1}: select asset i
```

- `mu`: expected-return score vector (units stated); `Sigma`: symmetric PSD covariance/risk matrix; `q > 0`: risk aversion; `B`: number of assets.
- Soft targets (e.g. total duration close to D*) add w (d^T x - D*)^2. They are preferences, not feasibility rules.
- Check: Sigma symmetric and PSD; units consistent; penalty A separates feasible from infeasible states by enumeration.

## Six-bond demo (synthetic)

Select exactly 3 of 6 bonds; q = 1.5, A = 15, duration target 15.0 with weight 0.25. Unique optimum A, C, E (`101010`), energy -9.3725; next feasible A, D, E at -9.1675. Expected verdict: **classical now; teaching PoC only**.

## What real portfolios add

Prices and budgets, lot sizes, integer holdings, liquidity, turnover and transaction costs, taxes, regulatory and issuer limits, scenario/CVaR risk, and estimation error in mu and Sigma (often dominant). Each changes the encoding (more variables, slack bits, larger coefficient ranges).

## Classical baselines

Exact: MIP/MIQP (branch-and-bound), CP-SAT for integer formulations; continuous relaxations via convex solvers. Heuristics: simulated annealing with swap moves, tabu search. These scale to realistic sizes today.

## Domain failure modes

Treating synthetic scores as market data · forgetting that cardinality penalty sets coefficient scale · comparing a quantum sampler to random search · calling a toy match "advantage" · drifting into investment advice.
