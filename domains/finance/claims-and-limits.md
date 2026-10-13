# Quantum-finance claims and limits

**Rule:** a finance "quantum" result counts only with a named classical baseline, the same instances and budgets, and end-to-end timing.

## Typical claim types and what to ask
| Claim | Ask |
|---|---|
| "Quantum portfolio optimization beats classical" | Which solver, tuned how, on how many assets, with which constraints? End to end including embedding and queue time? |
| "Quantum Monte Carlo gives a quadratic speed-up for pricing" | Theoretical amplitude-estimation result; needs fault-tolerant depth and efficient state loading — what resources were assumed? |
| "Hybrid solver found better portfolios" | Hybrid ≠ QPU. What did the classical part do? Same runtime budget as the baseline? |
| "Ran on real hardware" | How many variables, which share were embedded, chain-break rate, readout mitigation? |

## Hard limits for this plugin
No investment recommendations, live trading, client or position data, or production credentials. Outputs are teaching and engineering artefacts.

## Evidence anchors
- Survey of finance use cases and prospects: `egger-2020`.
- Overhead and I/O criteria for useful advantage: `hoefler-2023`.
- An end-to-end annealing portfolio pipeline to audit against these questions: `rr-e2e-portfolio-annealing` (preprint).
