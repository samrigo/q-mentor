# Quantum fit: readiness score, gates, evidence levels

`last_verified: 2026-10-12` · sources: `hoefler-2023`, `preskill-2018`, `egger-2020`

## Operational rule

Quantum is never the default. Apply hard gates, then score, then name the classical alternative.

## Hard gates (any one blocks a "fit now" verdict)

No clear objective · no classical baseline · no resource estimate · prohibited data (stops the workflow) · unsupported advantage claim.

## Readiness score (fractions of each weight)

| Dimension | Weight | Question |
|---|---:|---|
| Problem structure | 25 | Precise optimization, simulation, sampling, or algebraic kernel? |
| Formulation quality | 20 | Variables, objective, constraints, encodings explicit? |
| Classical comparison | 20 | Strong baseline exists **and** a reason it may be insufficient? |
| Input/output fit | 15 | Can data loading and readout avoid erasing any gain? |
| Resource fit | 10 | Qubits, depth, shots, embedding, solver limits estimated? |
| Evidence | 10 | Claims reproducible, cited, measured end to end? |

Bands: 0-39 **classical now** · 40-64 **research or teaching PoC** · 65-79 **bounded experiment** with stop condition · 80-100 **candidate experiment** (not proof of advantage).

Cap: if a classical method already solves the production problem (classical comparison = 0), the verdict is classical now; a labeled teaching PoC may be offered.

## Kernels with plausible long-run interest

Quantum simulation of physical systems; some structured sampling; algebraic problems underlying public-key cryptography (Shor). Optimization claims remain heuristic and instance-dependent. End-to-end analyses (Hoefler et al. 2023) show that quadratic speedups are often erased by error-correction and I/O overheads; prefer problems with large (super-polynomial) speedups and small input/output.

## Evidence levels (name the one achieved)

1. **Formulated** - a valid encoding exists.
2. **Executable** - runs on a simulator or target.
3. **Competitive on a toy** - matches a baseline on a small case.
4. **Scales experimentally** - quality and cost stay credible as instances grow.
5. **Advantage evidence** - beats a relevant, strong classical baseline end to end, reproducibly.

Levels 1-3 are not quantum advantage.

## Typical "classical now" signals

State space small enough to enumerate; mature MIP/CP-SAT performance; data loading dominates; no measurable hypothesis; the request is quantum because someone asked for quantum.
