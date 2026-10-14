# Recent research watchlist (2023–2026)

**Rule:** this list is discovery input, not product claims. Re-verify version, status, and corrections before citing; record what each source does **not** establish. Hardware-family papers live in `knowledge/hardware-*.md`.

| Source (id in `sources.yml`) | Status at the 2026-10-14 check | What it supports | What it does not show |
|---|---|---|---|
| Challenges and opportunities in quantum optimization, Nat. Rev. Phys. 2024 (`rr-challenges-quantum-optimization-2024`) | peer-reviewed review; not re-read | Benchmarking and scaling questions are open | Any specific application advantage |
| Towards Robust Benchmarking of Quantum Optimization Algorithms (`rr-robust-benchmarking-2024`) | preprint, v1 2024-05-13, no journal ref shown | Fair formulations, tuning parity, holistic metrics | Results on the user's problem |
| A review on QAOA and its variants, Phys. Rep. 2024 (`rr-qaoa-review-2024`) | peer-reviewed review; not re-read | Variants, limits, noise sensitivity | Practical speed-up |
| Hoefler, Häner & Troyer, Disentangling Hype from Practicality (`ref-hoefler-hype-2023`) | perspective; arXiv lists a CACM journal ref | I/O and overhead criteria for useful advantage | That no advantage is possible |
| Quantum error correction below the surface code threshold, Nature 2024 (`hw-google-below-threshold-2025`) | peer-reviewed; **Author Correction 2026-04-28** (Fig. 3a) | Logical error suppression with distance | Application advantage |
| Weighted-Graph Optimization on a Rydberg-Atom Array, PRX Quantum 2025 (`hw-rydberg-weighted-graph-2025`) | peer-reviewed, 2025-01-02 | Neutral-atom weighted-graph encodings on hardware | Dense arbitrary QUBOs |
| End-to-End Portfolio Optimization with Quantum Annealing (`rr-portfolio-annealing-e2e-2025`) | preprint v1 2025-04-10; **v2 2025-12-17 lists DOI 10.1002/qute.202500753** — read the journal version before citing | A complete finance pipeline to audit | Advantage over tuned classical solvers; separate classical allocation from quantum selection |
| Benchmarking quantum software for circuit creation and compilation, Nat. Comput. Sci. 2025 (`rr-sdk-benchmarking-2025`) | peer-reviewed; not re-read | Cross-SDK compile-time and quality comparisons | Hardware performance |

Changes found by the build check (not in the brief): the four-logical-qubit trapped-ion "preprint" is published (Phys. Rev. Lett. 133, 180601); the Helios 98-qubit paper has a Publisher Correction (2026-07-07). See `docs/SOURCE-CHECK.md`. Refresh at each minor release; prefer a shorter current list and keep negative or null results.
