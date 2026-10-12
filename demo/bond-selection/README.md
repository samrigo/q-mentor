# Six-Bond Selection Demo

Synthetic didactic problem. Not market data or investment advice.

## Problem

Select exactly three of six bonds. Balance expected yield, covariance risk, and closeness to target duration 15.0.

See `problem.json` and `expected.json`.

## Ground truth

Enumerate all \(2^6 = 64\) assignments. Unique optimum:

```
x*        = [1, 0, 1, 0, 1, 0]   # A, C, E
bitstring = 101010
energy    = -9.3725
```

Next-best feasible (A, D, E) energy = -9.1675; gap = 0.2050.

## Expected verdict

**classical now; quantum teaching PoC only** — 64 states are trivial to enumerate.
