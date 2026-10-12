# Primary References

Use this list to build and maintain concise knowledge packs. Summarize sources; do not copy them. Prefer primary papers and official product documentation. Record pinned package versions and a `last_verified` date in the generated repository.

## GitHub Copilot construction

- [About GitHub Copilot plugins](https://docs.github.com/en/copilot/concepts/agents/about-plugins) — package choices, supported components, and distribution.
- [Creating a plugin for Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-creating) — Agent Plugins layout and local verification.
- [Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference) — manifest, locations, install/update behavior.
- [Adding agent skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills) — `SKILL.md`, discovery, and supported surfaces.
- [Customization feature comparison](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/comparing-cli-features) — when to use instructions, skills, agents, plugins, and tools.
- [Repository custom instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions) — small persistent repo guidance.
- [Best results with Copilot cloud agent](https://docs.github.com/en/copilot/tutorials/cloud-agent/get-the-best-results) — build/test context and scoped tasks.
- [Optimize AI usage and cost](https://docs.github.com/en/copilot/tutorials/optimize-ai-usage) — model selection, lean context, cache, limits, phased work, and deterministic guardrails.
- [Models and pricing](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing) and [budget controls](https://docs.github.com/en/copilot/concepts/billing-and-usage/organizations-and-enterprises/budgets) — dynamic cost source of truth.
- [Copilot SDK features](https://docs.github.com/en/copilot/how-tos/copilot-sdk/features) — future extension reference; not required for the MVP.

## Quantum-finance history

- [Markowitz, “Portfolio Selection” (1952)](https://doi.org/10.1111/j.1540-6261.1952.tb01525.x) — mean-variance portfolio theory.
- [Feynman, “Simulating Physics with Computers” (1982)](https://doi.org/10.1007/BF02650179) — foundational motivation for quantum simulation.
- [Deutsch, “Quantum theory, the Church–Turing principle…” (1985)](https://doi.org/10.1098/rspa.1985.0070) — universal quantum computation.
- [Shor, factoring and discrete logarithms (1994)](https://doi.org/10.1109/SFCS.1994.365700) and [Grover, database search (1996)](https://doi.org/10.1145/237814.237866) — the basis for distinct public-key and symmetric security impacts.
- [Farhi, Goldstone, and Gutmann, QAOA (2014)](https://arxiv.org/abs/1411.4028) — original approximate optimization algorithm.
- [Lucas, Ising formulations of NP problems (2014)](https://doi.org/10.3389/fphy.2014.00005) — mappings between combinatorial problems and Ising models.
- [Preskill, quantum computing in the NISQ era (2018)](https://arxiv.org/abs/1801.00862) — hardware-era framing and limits.
- [Egger et al., quantum computing for finance (2020)](https://arxiv.org/abs/2006.14510) — finance use-case survey and technical prospects.
- [Hoefler, Häner, and Troyer, practical quantum advantage (2023)](https://arxiv.org/abs/2307.00523) — criteria for separating useful speedups from overhead and hype.
- [Silvério et al., Pulser (2022)](https://doi.org/10.22331/q-2022-01-24-629) — pulse-level programming for programmable neutral-atom arrays.
- [Bergholm et al., PennyLane](https://arxiv.org/abs/1811.04968) — automatic differentiation for hybrid quantum-classical computation.

## Math and classical baselines

- [Qiskit Finance portfolio optimization tutorial](https://qiskit-community.github.io/qiskit-finance/tutorials/01_portfolio_optimization.html) — canonical binary mean-variance formulation and penalty mapping.
- [Qiskit Optimization](https://qiskit-community.github.io/qiskit-optimization/) — quadratic models, converters, quantum algorithms, and classical comparators.
- [Google OR-Tools CP-SAT](https://developers.google.com/optimization/cp/cp_solver) and [MIP guide](https://developers.google.com/optimization/mip) — classical integer baselines.
- [CVXPY documentation](https://www.cvxpy.org/) — convex modeling for applicable continuous baselines.

## Provider and framework SDKs

- [IBM quantum optimization tutorials](https://quantum.cloud.ibm.com/docs/en/tutorials/quantum-approximate-multi-objective-optimization) and [QAOA best-practices repository](https://github.com/qiskit-community/qopt-best-practices) — gate-model workflows, execution, and measurement.
- [Classiq documentation](https://docs.classiq.io/latest/) and [Classiq library portfolio example](https://github.com/Classiq/classiq-library/tree/main/applications/finance/portfolio_optimization) — high-level modeling, synthesis, and execution examples.
- [D-Wave model concepts](https://docs.dwavequantum.com/en/latest/concepts/models.html) and [Ocean workflow](https://docs.dwavequantum.com/en/latest/ocean/workflow.html) — BQM/QUBO/Ising conventions, sampling, and hybrid solvers.
- [Pasqal documentation](https://docs.pasqal.com/), [Pulser overview](https://docs.pasqal.com/pulser/), and [programming guide](https://docs.pasqal.com/pulser/programming/) — neutral-atom devices, registers, Hamiltonians, pulse sequences, and execution choices.
- [Pulser QUBO tutorial](https://docs.pasqal.com/pulser/tutorials/qubo/) and [noise models](https://docs.pasqal.com/pulser/noise_model/) — geometry-dependent Rydberg mappings, QAA, emulator behavior, and hardware limitations.
- [PennyLane documentation](https://docs.pennylane.ai/en/stable/), [QAOA module](https://docs.pennylane.ai/en/stable/code/qp_qaoa.html), and [gradients/training](https://docs.pennylane.ai/en/stable/introduction/interfaces.html) — device-independent circuits, hybrid optimization, automatic differentiation, and local/device-plugin execution.

PennyLane belongs in the framework layer, not the hardware-provider list. A PennyLane result is incomplete unless it names the concrete device or plugin. Pasqal/Pulser belongs in the neutral-atom provider path and requires a physical-capability check before translating a generic QUBO.

## Post-quantum cryptography

- [NIST PQC project and standards](https://csrc.nist.gov/Projects/Post-Quantum-Cryptography) — authoritative status and migration material.
- [FIPS 203: ML-KEM](https://csrc.nist.gov/pubs/fips/203/final), [FIPS 204: ML-DSA](https://csrc.nist.gov/pubs/fips/204/final), and [FIPS 205: SLH-DSA](https://csrc.nist.gov/pubs/fips/205/final) — finalized specifications.
- [NCCoE migration project](https://www.nccoe.nist.gov/crypto-agility-considerations-migrating-post-quantum-cryptographic-algorithms) — discovery, interoperability, and migration planning.

## Source policy

For claims that can change—Copilot packaging, billing, client support, provider APIs, hardware, or PQC status—official documentation overrides these summaries. For scientific claims, cite the original paper and state whether the claim is theoretical, simulated, hardware-demonstrated, peer reviewed, vendor reported, artifact-backed, or independently reproduced. Record contradictory and negative evidence rather than retaining only favorable results.

