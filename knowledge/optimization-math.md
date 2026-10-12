# Optimization math (canonical conventions)

`last_verified: 2026-10-12` · sources: `lucas-2014`, `farhi-2014`, `markowitz-1952`, `qiskit-finance-portfolio`

## Operational rule

Every adapter preserves **one** canonical energy. Prove it by enumerating all assignments on toy sizes; never by visual inspection.

## Canonical QUBO

```text
E(x) = x^T Q x + c,   x_i in {0,1}
```

- `Q` is stored **full and symmetric**: off-diagonal couplings appear twice (Q_ij and Q_ji). Libraries that store a coupling once need `2 Q_ij`.
- Because x_i^2 = x_i, linear terms live on the diagonal.
- **Bit order:** variable 0 is the leftmost character of a bitstring.

## Ising conversion

`x_i = (1 - s_i)/2`, so s_i = +1 means x_i = 0 (matches Pauli-Z on |0>).

```text
E(s) = offset + sum_i h_i s_i + sum_{i<j} J_ij s_i s_j
h_i = -Q_ii/2 - sum_{j!=i} Q_ij/2;  J_ij = Q_ij/2;  offset = c + sum_i Q_ii/2 + sum_{i<j} Q_ij/2
```

D-Wave dimod uses s = 2x - 1 (opposite sign): flip h, keep J.

## Constraints as penalties

Equality g(x) = a^T x - b = 0 becomes A (a^T x - b)^2 = A[x^T(a a^T)x - 2b a^T x + b^2]. Choose A large enough that no infeasible state beats the best feasible one, but not so large that coefficient range harms hardware precision. **Test** separation by enumeration on small fixtures; treat A as a modeling decision, not a constant.

## Mean-variance selection

```text
minimize  q x^T Sigma x - mu^T x   subject to  1^T x = B
```

Sigma must be symmetric PSD, q > 0. Real portfolios add prices, lots, liquidity, turnover, taxes, limits, scenarios, and estimation error; the toy is didactic.

## QAOA

Alternate cost evolution exp(-i gamma H_C) and mixer exp(-i beta sum X) for p layers; a classical optimizer tunes angles. It is a hybrid **heuristic**, sensitive to encoding, depth, optimizer, initialization, shots, noise, and seed. No general practical speedup is established.

## Annealing

Samplers minimize an Ising/BQM energy. Report logical variables vs physical qubits, chain strength, chain breaks, reads, embedding time, and post-processing. Hybrid-solver results are not pure-QPU results.

## Classical baselines

Exact: enumeration (<= ~20 variables), MIP (branch-and-bound), CP-SAT. Heuristic: simulated annealing with problem-aware moves, tabu search. Give baselines comparable tuning effort.
