# Portfolio Optimization (didactic)

Binary selection of assets under a Markowitz-style objective plus cardinality and duration-style constraints. See `demo/bond-selection/` for the concrete six-bond fixture.

\[
\min_x \; q\, x^T \Sigma x - \mu^T x
\quad\text{s.t.}\quad
\mathbf{1}^T x = B
\]

Real portfolios require prices, lot sizes, liquidity, turnover, taxes, scenario analysis, and estimation uncertainty. This pack is for teaching formulation and provider translation only.
