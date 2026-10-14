# Conversion atlas: route classes by computing model

**Rule:** resolve source program → source semantics → canonical problem or operator → target capability → target implementation. A shared language, QASM file, or cloud is not hardware equivalence. Shipped edges live in `registry/conversion-edges.yml`; an unlisted pair gets a capability report before any code.

## Classes

`E` exact logical computation on a supported subset · `C` equal **conditional** distribution after heralding/postselection (report unconditional success) · `R` same classical objective reimplemented with a different algorithm · `A` quantified approximation to evolution · `U` unsupported / no verified route. `E` never means equal noise, success probability, time, or cost.

| Source ↓ / target → | Gate | Rydberg analog | BQM/anneal | Photonic DV | Photonic CV | Research-only |
|---|---|---|---|---|---|---|
| Gate | E (subset) | A or R | R if objective recovered | C (dual-rail subset) | U | U |
| Rydberg analog | A or R | E only if Hamiltonian/control match | R if objective recovered | U | U | U |
| BQM/anneal | R | R if geometry permits | E energy model | R with explicit encoding | U | U |
| Photonic DV | C with verified inverse encoding | U | R if objective recovered | E on optical model | U | U |
| Photonic CV | U | U | U | U | E matched CV model | U |
| Research-only | U | U | U | U | U | U |

## Recipes and proof obligations

- **Gate ↔ gate:** maintained `pytket-qiskit` (`qiskit_to_tk`/`tk_to_qiskit`), `pytket-braket`, or a tested Cirq OpenQASM 2 subset. Prove operator equality up to global phase with stated bit order; check measurements, classical control, symbolic parameters, implicit swaps. `pytket-cirq`, `pytket-pennylane`, `pytket-pyquil` are unmaintained — never default.
- **Gate → photonic DV:** pinned `perceval-interop` Qiskit converter. Report the conditional distribution **and** the unconditional (postselected/heralded) success rate; never present postselected fidelity as deterministic.
- **Rydberg ↔ Rydberg (Pulser, Bloqade, Braket AHS):** translate the time-dependent Hamiltonian: coordinates, `C6/r^6` (different devices use different C6), units, signs, Ω(t), δ(t), phase, addressing, time grid. If C6 or controls differ, report `A` with error or `U`. Qadence→Pulser is a legacy, unmaintained bridge.
- **Analog ↔ gate:** only a documented decomposition or Hamiltonian simulation is `A` (report Trotter error); re-expressing a shared QUBO as QAOA is `R` (Pulser → Classiq).
- **BQM ↔ others:** dimod offsets and QUBO↔Ising transforms; prove every bitstring's canonical energy. Annealing, QAOA, analog, and photonic sampling are different algorithms on the same objective (`R`). A general circuit has no BQM inverse.
- **CV photonics, electrons on helium, topological, unverified spin devices:** capability report only — no executable code.

Every claimed `E/C/R/A` edge needs complete pinned files plus a negative fixture; every `U` needs a negative fixture and the nearest valid alternative. Recheck SDK docs, changelog, commit SHA, and issues before pinning (`sdk-pytket-extensions-status`, `sdk-perceval-interop`, `sdk-qadence` in `sources.yml`).
