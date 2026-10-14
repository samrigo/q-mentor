# Primary References

Use this list for cross-cutting history and methods; [README-11](README-11-HARDWARE-AND-RESEARCH.md) holds hardware papers since 2023, [README-12](README-12-SDK-SOURCE-MAP.md) holds SDK code/commit/issue/example links, and [README-14](README-14-CONVERSION-ATLAS.md) connects current interop documentation to conversion proofs. Summarize sources; do not copy them. Prefer primary papers and official product documentation. Record pinned package versions and a `last_verified` date in the generated repository.

## GitHub Copilot construction

- [About GitHub Copilot plugins](https://docs.github.com/en/copilot/concepts/agents/about-plugins) — package choices, supported components, and distribution.
- [Creating a plugin for Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-creating) — Agent Plugins layout and local verification.
- [Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference) — manifest, locations, install/update behavior.
- [Agent Plugins specification](https://agent-plugins.org/specification) and [schemas](https://agent-plugins.org/schemas) — portable manifest, skill discovery, MCP configuration, versioning, and failure boundaries.
- [Adding agent skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills) — `SKILL.md`, discovery, and supported surfaces.
- [Copilot CLI command reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference) — current skill and custom-agent frontmatter, discovery priority, and management commands.
- [Custom agents](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-custom-agents) — agent routing, tools, and subagent behavior.
- [Hooks reference](https://docs.github.com/en/copilot/reference/hooks-reference) — optional deterministic lifecycle enforcement and surface-specific behavior.
- [Tool permissions](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/allowing-tools) — available, allowed, and denied tool boundaries.
- [Customization feature comparison](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/comparing-cli-features) — when to use instructions, skills, agents, plugins, and tools.
- [Repository custom instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions) — small persistent repo guidance.
- [Best results with Copilot cloud agent](https://docs.github.com/en/copilot/tutorials/cloud-agent/get-the-best-results) — build/test context and scoped tasks.
- [Optimize AI usage and cost](https://docs.github.com/en/copilot/tutorials/optimize-ai-usage) — model selection, lean context, cache, limits, phased work, and deterministic guardrails.
- [Models and pricing](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing) and [budget controls](https://docs.github.com/en/copilot/concepts/billing-and-usage/organizations-and-enterprises/budgets) — dynamic cost source of truth.
- [Copilot SDK features](https://docs.github.com/en/copilot/how-tos/copilot-sdk/features) — future extension reference; not required for the MVP.
- [Artifact attestations](https://docs.github.com/en/actions/concepts/security/artifact-attestations) — optional release provenance and SBOM evidence.

## Quantum-finance history

- [Markowitz, “Portfolio Selection” (1952)](https://doi.org/10.1111/j.1540-6261.1952.tb01525.x) — mean-variance portfolio theory.
- [Feynman, “Simulating Physics with Computers” (1982)](https://doi.org/10.1007/BF02650179) — foundational motivation for quantum simulation.
- [Deutsch, “Quantum theory, the Church–Turing principle…” (1985)](https://doi.org/10.1098/rspa.1985.0070) — universal quantum computation.
- [Shor, factoring and discrete logarithms (1994)](https://doi.org/10.1109/SFCS.1994.365700) and [Grover, database search (1996)](https://doi.org/10.1145/237814.237866) — the basis for distinct public-key and symmetric security impacts.
- [Farhi, Goldstone, and Gutmann, QAOA (2014)](https://arxiv.org/abs/1411.4028) — original approximate optimization algorithm.
- [Lucas, Ising formulations of NP problems (2014)](https://doi.org/10.3389/fphy.2014.00005) — mappings between combinatorial problems and Ising models.
- [Preskill, quantum computing in the NISQ era (2018)](https://arxiv.org/abs/1801.00862) — hardware-era framing and limits.
- [Egger et al., quantum computing for finance (2020)](https://arxiv.org/abs/2006.14510) — finance use-case survey and technical prospects.
- [Hoefler, Häner, and Troyer, “Disentangling Hype from Practicality: On Realistically Achieving Quantum Advantage” (2023)](https://arxiv.org/abs/2307.00523) — criteria for separating useful speedups from overhead and hype.
- [Silvério et al., Pulser (2022)](https://quantum-journal.org/papers/q-2022-01-24-629/) — pulse-level programming for programmable neutral-atom arrays.
- [Bergholm et al., PennyLane](https://arxiv.org/abs/1811.04968) — automatic differentiation for hybrid quantum-classical computation.

## Math and classical baselines

- [Qiskit Finance portfolio optimization tutorial](https://qiskit-community.github.io/qiskit-finance/tutorials/01_portfolio_optimization.html) — canonical binary mean-variance formulation and penalty mapping.
- [Qiskit Optimization](https://qiskit-community.github.io/qiskit-optimization/) — quadratic models, converters, quantum algorithms, and classical comparators.
- [Google OR-Tools CP-SAT](https://developers.google.com/optimization/cp/cp_solver) and [MIP guide](https://developers.google.com/optimization/mip) — classical integer baselines.
- [CVXPY documentation](https://www.cvxpy.org/) — convex modeling for applicable continuous baselines.

## Provider and framework SDKs

- Qiskit: [optimization source](https://github.com/qiskit-community/qiskit-optimization), [overview](https://qiskit-community.github.io/qiskit-optimization/), [tutorial catalog](https://qiskit-community.github.io/qiskit-optimization/tutorials/index.html), [QuadraticProgram](https://qiskit-community.github.io/qiskit-optimization/tutorials/01_quadratic_program.html), [converters](https://qiskit-community.github.io/qiskit-optimization/tutorials/02_converters_for_quadratic_programs.html), [minimum-eigen/QAOA workflow](https://qiskit-community.github.io/qiskit-optimization/tutorials/03_minimum_eigen_optimizer.html), [release notes](https://qiskit-community.github.io/qiskit-optimization/release_notes.html), and [best practices](https://github.com/qiskit-community/qopt-best-practices).
- Classiq: [documentation](https://docs.classiq.io/), [Qmod reference](https://docs.classiq.io/qmod-reference), [SDK reference](https://docs.classiq.io/sdk-reference), [Classiq library](https://github.com/Classiq/classiq-library), and [portfolio example](https://github.com/Classiq/classiq-library/tree/main/applications/finance/portfolio_optimization). Treat notebook, native Qmod, and Python-Qmod formats distinctly.
- D-Wave: [official example repositories](https://github.com/dwave-examples), [Ocean SDK](https://docs.dwavequantum.com/en/latest/ocean/), [package/API index](https://docs.dwavequantum.com/en/latest/ocean/packages.html), [model concepts](https://docs.dwavequantum.com/en/latest/concepts/models.html), [formulation workflow](https://docs.dwavequantum.com/en/latest/ocean/workflow.html), [local and QPU workflow](https://docs.dwavequantum.com/en/latest/quantum_research/workflow.html), and [SampleSet semantics](https://docs.dwavequantum.com/en/latest/concepts/samplesets.html).
- [Pasqal documentation](https://docs.pasqal.com/), [Pulser overview](https://docs.pasqal.com/pulser/), and [programming guide](https://docs.pasqal.com/pulser/programming/) — neutral-atom devices, registers, Hamiltonians, pulse sequences, and execution choices.
- Pasqal/Pulser: [source repository](https://github.com/pasqal-io/Pulser), [QUBO/QAA tutorial](https://docs.pasqal.com/pulser/tutorials/qubo/), [devices and registers](https://docs.pasqal.com/pulser/programming/), and [noise models](https://docs.pasqal.com/pulser/noise_model/). Examples must preserve geometry and pulse/device constraints.
- PennyLane: [source repository](https://github.com/PennyLaneAI/pennylane), [documentation](https://docs.pennylane.ai/en/stable/), [QAOA module](https://docs.pennylane.ai/en/stable/code/qp_qaoa.html), [QUBO demo](https://pennylane.ai/demos/tutorial_QUBO), [QAOA demo](https://pennylane.ai/demos/tutorial_qaoa_intro), [devices](https://docs.pennylane.ai/en/stable/code/qp_devices.html), [interfaces and gradients](https://docs.pennylane.ai/en/stable/introduction/interfaces.html), and [demo catalog](https://www.pennylane.ai/demonstrations).

PennyLane belongs in the framework layer, not the hardware-provider list. A PennyLane result is incomplete unless it names the concrete device or plugin. Pasqal/Pulser belongs in the neutral-atom provider path and requires a physical-capability check before translating a generic QUBO. For all new targets, use the public repository, exact examples, commits, and issues in [README-12](README-12-SDK-SOURCE-MAP.md).

## Recent research watchlist: 2023–2026

These sources inform evals and research prompts; they do not become product claims automatically.

- [“Challenges and opportunities in quantum optimization” (Nature Reviews Physics, 2024)](https://www.nature.com/articles/s42254-024-00770-9) — complexity, scaling, benchmarking, and application boundaries.
- [“Towards Robust Benchmarking of Quantum Optimization Algorithms” (preprint, 2024)](https://arxiv.org/abs/2405.07624) — fair formulations, hard instances, holistic metrics, and comparable tuning.
- [“A review on Quantum Approximate Optimization Algorithm and its variants” (Physics Reports, 2024)](https://www.sciencedirect.com/science/article/pii/S0370157324001078) — QAOA variants, limitations, noise, and open performance questions.
- [“Hybrid quantum programming with PennyLane Lightning on HPC platforms” (preprint, 2024)](https://arxiv.org/abs/2403.02512) — simulator architecture and scaling evidence for hybrid workflows.
- [“Machine learning for practical quantum error mitigation” (Nature Machine Intelligence, 2024)](https://www.nature.com/articles/s42256-024-00927-2) — artifact-backed mitigation methods and their additional-runtime tradeoff.
- [“Demonstration of Weighted-Graph Optimization on a Rydberg-Atom Array Using Local Light Shifts” (PRX Quantum, 2025)](https://doi.org/10.1103/PRXQuantum.6.010301) — neutral-atom weighted-graph optimization and hardware-specific evidence.
- [“Benchmarking the performance of quantum computing software for quantum circuit creation, manipulation and compilation” (Nature Computational Science, 2025)](https://www.nature.com/articles/s43588-025-00792-y) — uniform cross-SDK benchmarking and reproducibility.
- [“Quantum error correction below the surface code threshold” (Nature, 2025)](https://doi.org/10.1038/s41586-024-08449-y) — logical-memory evidence, with a [2026 correction](https://doi.org/10.1038/s41586-026-10559-8); not proof of application advantage.
- [“End-to-End Portfolio Optimization with Quantum Annealing” (preprint, 2025)](https://arxiv.org/abs/2504.08843) — an end-to-end finance case to evaluate against the plugin's baseline, overhead, and artifact criteria.

Refresh this watchlist and the modality-specific [paper catalog](README-11-HARDWARE-AND-RESEARCH.md) at every minor release. Record publication status, version, artifacts, corrections, contradictory evidence, and the exact claim affected. Prefer a shorter current list over accumulating stale papers.

## Post-quantum cryptography

- [NIST PQC project and standards](https://csrc.nist.gov/Projects/Post-Quantum-Cryptography) — authoritative status and migration material.
- [FIPS 203: ML-KEM](https://csrc.nist.gov/pubs/fips/203/final), [FIPS 204: ML-DSA](https://csrc.nist.gov/pubs/fips/204/final), and [FIPS 205: SLH-DSA](https://csrc.nist.gov/pubs/fips/205/final) — finalized specifications.
- [NCCoE migration project](https://www.nccoe.nist.gov/crypto-agility-considerations-migrating-post-quantum-cryptographic-algorithms) — discovery, interoperability, and migration planning.

## Source policy

For claims that can change—Copilot packaging, billing, client support, provider APIs, hardware, or PQC status—official documentation overrides these summaries. Generate SDK code only from a version-matched official example or API reference and record the source URL plus tested version; never reconstruct an API from memory. For scientific claims, cite the original paper and state whether the claim is theoretical, simulated, hardware-demonstrated, peer reviewed, vendor reported, artifact-backed, or independently reproduced. Record contradictory and negative evidence rather than retaining only favorable results. The release source check must resolve every DOI/arXiv record to a matching title/year, check corrections or retractions, and record publisher blocks separately from broken links; GitHub SDK links must identify repository state, commit SHA, issue availability, and a version-matched example.

