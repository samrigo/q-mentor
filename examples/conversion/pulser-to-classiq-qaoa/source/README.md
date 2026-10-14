# Source side — Pulser program (5 atoms, 10 couplings)

- **SDK:** `pulser==1.9.1` (+ `pulser-simulation` 1.9.1, `qutip` 5.3.1), `scipy==1.18.1`; CPython 3.13, x86_64 Linux.
- **Family / model / backend / level:** neutral atom (Pasqal) / analog Rydberg / `AnalogDevice` + `QutipBackendV2` noiseless / `tested-local`.
- **Program:** five atoms in a zig-zag (µm: (0,0) (7,0) (14,0) (3.3,6.6) (10.9,6.4), centred), global Rydberg
  channel, 4 µs adiabatic sweep: Ω 0 → 2π·0.8 → 0 rad/µs, δ −6 → 0 → +6 rad/µs.
- **Extracted problem:** final classical Hamiltonian `E(x) = −6 Σ x_i + Σ_{i<j} C6/r_ij⁶ x_i x_j` with all ten pair
  terms positive; unique optimum `10110` (−12.3030), runner-up `10100` (−11.8850).

`python main.py` writes `../program_ir.json`, `../canonical_problem.json`, `../source_result.json`. The Classiq side
reads only those artifacts. Observed (2026-10-14): QAA puts 0.194 probability on the optimum (exact final state).
