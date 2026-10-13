# Portfolio optimization (binary, didactic)

**Rule:** the toy model teaches formulation and translation; it is not a production portfolio model.

## Model
`minimize q·xᵀΣx − μᵀx` subject to `1ᵀx = B`, `x ∈ {0,1}ⁿ`.
- `μ`: expected-return (or yield) score; `Σ`: positive-semidefinite covariance/risk matrix; `q > 0`: risk aversion; `B`: number of selected assets.
- Extra soft terms are allowed if stated, e.g. duration targeting `w·(dᵀx − T)²`.
- Cardinality becomes the penalty `A·(1ᵀx − B)²`; prove separation by enumeration on small instances.

## What production adds (and the toy omits)
Prices and weights (not just in/out), lot sizes, liquidity, turnover and transaction costs, taxes, regulatory and client limits, scenario/stress risk, estimation error in `μ` and `Σ`, rebalancing horizon.

## Classical baselines
- ≤ ~25 assets binary: exhaustive enumeration.
- Larger: MIP or CP-SAT with the same constraints; continuous relaxations via convex solvers (e.g. CVXPY) for weights.
- Report the optimality gap of any heuristic against an exact or bounded solution.

## Six-bond reference values
Optimum A, C, E (`101010`): yield 11.9, risk 1.67, duration 14.7, energy −9.3725. Runner-up A, D, E at −9.1675. Verdict: classical now; quantum teaching PoC only.

## Sources
`markowitz-1952`, `qiskit-finance-portfolio`, `cvxpy` in `knowledge/sources.yml`.
