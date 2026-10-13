# Optimization math

**Rule:** fix one convention and test it on every enumerable assignment; never trust visual inspection of coefficients.

## Canonical QUBO
`E(x) = Σ_i a_i x_i + Σ_{i<j} b_ij x_i x_j + c`, `x_i ∈ {0,1}`. Each pair is stored once.
From a symmetric matrix form `x^T M x`, `a_i = M_ii` and `b_ij = M_ij + M_ji`. State which form you use.

## Ising map
`x_i = (1 − s_i)/2`, `s_i ∈ {−1,+1}` (|0> ↔ s = +1). Then
`h_i = −a_i/2 − Σ_{j≠i} b_ij/4`, `J_ij = b_ij/4`, `offset = c + Σ a_i/2 + Σ b_ij/4`.
Warning: dimod's SPIN vartype uses `x = (s+1)/2`; its spins are the negation of ours.

## Penalties
Equality `g(x) = 0` → `A·g(x)^2`. Choose `A` so that no infeasible assignment beats the feasible optimum (prove by enumeration on small fixtures), but not so large that the objective is lost in coefficient scale or hardware precision.

## QAOA
Alternate `exp(−iγ H_C)` and `exp(−iβ Σ X)` for `p` layers; a classical optimizer tunes angles. Heuristic, hybrid, sensitive to depth, initialization, shots, noise and seed. No general practical speed-up is established.

## Annealing
Samples low-energy states of an Ising/BQM model after minor embedding. Report logical vs physical qubits, chain strength, chain breaks, reads, and embedding time.

## Classical baselines (always)
Exact: enumeration (≤ ~25 binaries), MIP/branch-and-bound, CP-SAT. Heuristic: simulated annealing, tabu, local search with problem-aware moves. Tune baselines with comparable effort.

## Sources
Lucas 2014; Farhi et al. 2014; OR-Tools CP-SAT docs — see `sources.yml`.
