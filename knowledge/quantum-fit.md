# Quantum fit

**Rule:** apply hard gates first; a high score cannot override a failed gate. "Classical now" is a complete, valid answer.

## Hard gates (any failure → no "fit now")
No clear objective · no classical baseline · no resource estimate · prohibited or non-public data · an advantage claim without reproducible end-to-end evidence.

## Score (100)
| Dimension | Pts |
|---|---:|
| Problem structure (precise optimization/simulation/sampling/algebraic kernel) | 25 |
| Formulation quality (variables, objective, constraints, encoding explicit) | 20 |
| Classical comparison (strong baseline and why it may fall short) | 20 |
| Input/output fit (loading and readout do not erase the gain) | 15 |
| Resource fit (qubits, depth, shots, embedding estimated) | 10 |
| Evidence (reproducible, cited, end to end) | 10 |

0–39 classical now · 40–64 research/teaching PoC · 65–79 bounded experiment with stop condition · 80–100 candidate experiment (still not proof).

## Evidence levels
1 formulated · 2 executable · 3 competitive on a toy · 4 scales experimentally · 5 beats a strong classical baseline end to end. Levels 1–3 are not advantage.

## Red flags
Tiny instances (brute force wins) · data loading of large classical datasets · "quantum because we asked" · comparisons against random search · hybrid-solver results reported as QPU results.

## Sources
Hoefler, Häner & Troyer 2023; "Challenges and opportunities in quantum optimization" (Nature Reviews Physics 2024) — see `sources.yml`.
