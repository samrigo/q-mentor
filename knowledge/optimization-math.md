# Optimization Math (canonical conventions)

## Binary quadratic form

For binary decisions \(x_i \in \{0,1\}\):

\[
\min_x \; E(x) = x^T Q x + c
\]

Document whether off-diagonal terms appear once or twice. This repository uses the **full symmetric matrix** convention (cross terms appear twice when expanded).

## Ising conversion

\(x_i = (1 - s_i)/2\) with \(s_i \in \{-1,+1\}\). Adapters must test the conversion, not rely on visual inspection.

## Constraints as penalties

Equality \(g(x)=0\) → \(A[g(x)]^2\). Choose \(A\) large enough that no infeasible improvement in the original objective can dominate the penalty. For small fixtures, enumerate every assignment and prove separation.

## Mean-variance (didactic)

\[
\min_x \; q\, x^T \Sigma x - \mu^T x
\quad\text{s.t.}\quad
\mathbf{1}^T x = B
\]

Real portfolios add prices, lots, liquidity, turnover, taxes, limits, scenarios. The toy model is **not** production-ready.

## Six-bond demo energy

\[
E(x) = 1.5\, x^T \Sigma x - \mu^T x + 15(\sum x - 3)^2 + 0.25(d^T x - 15)^2
\]

See `demo/bond-selection/`.
