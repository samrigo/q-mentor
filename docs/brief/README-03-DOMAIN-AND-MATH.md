# Domain, Research, and Math Contract

## The honest sequence

Q-Mentor must reason in this order:

1. Define the business decision and success measure.
2. Identify the mathematical kernel.
3. Build and run a classical baseline.
4. Choose an encoding and estimate resources.
5. Design a quantum or hybrid experiment only if it teaches something measurable.
6. Compare end to end, including data preparation, optimization loop, sampling, decoding, queue time, and cost.

Quantum is not the default. For small or routinely solved problems, the correct verdict is usually classical production plus an optional teaching experiment.

## Research evidence contract

`q-mentor-research` and `q-mentor-evaluate` must convert each material claim into an evidence card:

| Field | Required question |
|---|---|
| Claim | What exactly is asserted, without marketing language? |
| Source status | Peer-reviewed paper, preprint, official documentation, vendor result, or secondary source? |
| Boundary | Which problem, data, scale, hardware, algorithm, and metric were measured? |
| Baseline | Was the comparator current, strong, fairly tuned, and measured end to end? |
| Artifacts | Are code, data, parameters, seeds, and raw results available? |
| Limitations | What overhead, assumption, negative result, or omitted cost changes interpretation? |
| Replication | Independent, same-team only, attempted and failed, or unknown? |

Score evidence from `0–2` on source rigor, baseline strength, artifact completeness, scale relevance, and replication. The total helps triage reading; it does not turn weak evidence into a fact. New claims stay labeled `candidate` until a maintainer approves their use in a knowledge pack.

When live web/research tools are unavailable, require attached papers, URLs, or repository files. Never invent a citation from memory.

## Core representations

### Binary quadratic optimization

For binary decisions `x_i in {0,1}`, use a single canonical convention:

```text
minimize  E(x) = x^T Q x + c
```

Document whether off-diagonal terms appear once or twice. Convert to Ising spins with `x_i = (1 - s_i) / 2`, where `s_i in {-1,+1}`. Provider adapters must test this conversion rather than rely on visual inspection.

### Constraints as penalties

An equality `g(x) = 0` can become `A[g(x)]^2`. Choose `A` large enough that no infeasible improvement in the original objective can dominate the penalty, but not so large that coefficient scale harms hardware or numerical behavior. For small fixtures, enumerate every assignment and prove the chosen penalty separates feasible and infeasible optima.

Treat penalty selection as a tested modeling decision—not a magic constant.

### Mean-variance selection

Use the didactic Markowitz-style binary model:

```text
minimize  q x^T Sigma x - mu^T x
subject to  1^T x = B
```

`mu` is expected-return score, `Sigma` is a positive-semidefinite covariance or risk matrix, `q > 0` is risk aversion, and `B` is the number of selected assets. Real portfolios add prices, lot sizes, liquidity, turnover, taxes, limits, scenarios, and estimation uncertainty; the plugin must not imply the toy model is production-ready.

### QAOA

QAOA alternates a problem Hamiltonian and a mixer for `p` layers while a classical optimizer updates angles. It is a hybrid approximate method, sensitive to encoding, depth, optimizer, initialization, shots, noise, and seed. More layers can increase expressiveness and circuit cost. Do not state a general practical speedup.

### Annealing

Quantum annealers minimize an Ising/BQM energy through sampling and hardware-specific embedding or hybrid solvers. Report logical variables separately from physical qubits, chain strength, chain breaks, reads, embedding time, and post-processing. A hybrid solver result is not a pure-QPU benchmark.

## Provider-neutral translation

| Target | Native emphasis | Translation requirement |
|---|---|---|
| Qiskit | Quadratic program to operator; QAOA or sampling eigensolver; simulator or gate hardware | Pin Qiskit packages, transpilation, shots, seed, circuit depth, and qubits |
| Classiq | High-level model/Qmod, synthesis constraints, QAOA workflow, multiple execution targets | Preserve the objective, record synthesis choices, width/depth, and target |
| D-Wave Ocean | BQM/QUBO/Ising, constrained models, samplers, annealing/hybrid solvers | Record coefficient convention, embedding, reads, chain data, solver class, and timing |
| Pasqal/Pulser | Neutral-atom analog/digital pulse programs, local emulation, QAA and geometry-encoded interactions | Check sign, geometry, device, register, addressability, pulse, noise, and measurement constraints before claiming equivalence |
| PennyLane | Cross-platform differentiable circuit framework with local simulators and device plugins | Name the actual device, interface, gradient method, shots, optimizer, seed, and transformed Hamiltonian |

“Same problem” means the decoded feasible solutions and canonical energy agree. It does not mean the execution mechanism, hardware, or performance claims are interchangeable. PennyLane is not a hardware provider; it is an implementation framework. Pulser cannot represent an arbitrary dense QUBO merely because both use Ising-like notation: Rydberg interactions depend on atomic geometry and device capabilities.

For Pasqal/Pulser, emit a `CapabilityReport` before code. If the target QUBO requires negative or independently arbitrary couplings, non-embeddable distances, or unavailable local detuning/addressability, return `unsupported-exact` and propose a reformulation, higher-level Pasqal workflow, digital route, or different target. Approximation requires a separate error bound and result label.

## Classical baselines

Use at least one exact method on every small fixture: enumeration, branch-and-bound/MIP, or CP-SAT. Add a strong scalable heuristic when the quantum method is heuristic. Report:

- feasibility rate;
- best, median, and distribution of objective values;
- optimality gap when the optimum is known;
- wall-clock and solver/QPU time separately;
- preprocessing, embedding, compilation, and decoding time;
- repeated-seed stability;
- compute and monetary cost.

The baseline receives comparable tuning effort. Never compare a tuned quantum workflow only to naive random search.

## Implementation and test contract

`q-mentor-implement` may act only from an approved `ProblemSpec`, design, and acceptance tests. It pins supported versions, keeps provider dependencies optional, makes the smallest scoped change, records assumptions, and never opens a paid remote job by default.

`q-mentor-test` separates:

- deterministic formulation and decoding tests;
- cross-framework energy-equivalence tests;
- seeded statistical quality tests with confidence intervals;
- noise and resource-sensitivity tests;
- opt-in remote smoke tests with cost and credential gates.

Statistical failure is reported, not retried until it disappears. A test report includes attempts, seeds, shots, backend, versions, thresholds, and negative results.

## Quantum-fit evidence levels

1. **Formulated:** a valid encoding exists.
2. **Executable:** it runs on a simulator or target.
3. **Competitive on a toy:** it matches a baseline on a small case.
4. **Scales experimentally:** quality and cost remain credible across increasing instances.
5. **Advantage evidence:** a relevant strong classical baseline is beaten end to end under reproducible conditions.

Q-Mentor must name the achieved level. Levels 1–3 are not quantum advantage.

## PQC scan semantics

The scan inventories, locates, and classifies cryptographic use. It should flag RSA, finite-field Diffie–Hellman, and elliptic-curve key exchange/signatures for migration review; treat symmetric encryption and hashes separately; identify protocols, libraries, certificates, key lifetimes, and stored-data exposure; and link findings to current NIST guidance.

It must not silently replace algorithms, label a system “unsafe” from a text match, promise compliance, or claim that PQC migration is only a future concern. Every finding needs evidence, confidence, and a security-owner next step.

