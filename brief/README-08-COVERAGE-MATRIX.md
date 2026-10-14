# Coverage Matrix

Use this file as the build checklist. A lifecycle phase is complete only when its skill has the required input, emits the named artifact, passes its gate, and stops safely when evidence is insufficient.

## Lifecycle coverage

| Phase | Skill | Required input | Durable output | Deterministic gate | Stop condition |
|---|---|---|---|---|---|
| Route | `q-mentor-orchestrate` | User outcome, registry, available tools | Ordered bounded skill chain | Prerequisites satisfied; no cycles; minimal relevant skills only | Approval, missing capability, or material user choice |
| Help | `q-mentor-help` | Live skill registry, user goal if supplied | Short menu or task-filtered skill explanation | Every registered skill appears once; trigger and output agree with registry | Registry is missing or invalid |
| Learn | `q-mentor-learn` | Goal, current knowledge, domain pack | Short explanation, example, misconception check | User can restate the concept or pass a tiny check | Ambiguous goal or prerequisite gap |
| Research | `q-mentor-research` | Question, date, source policy | `EvidenceCard[]` with links and confidence | Claims trace to primary sources; conflicts remain visible | No adequate source or inaccessible evidence |
| Explore | `q-mentor-brainstorm` | Problem context and constraints | Ranked classical, hybrid, and quantum options | Options expose assumptions, cost, and falsifiers | Problem is too underspecified |
| Frame | `q-mentor-frame` | Objective, data, constraints, metrics | Validated `ProblemSpec` | Units, domains, signs, feasibility, and leakage checks pass | Contradictory or missing requirements |
| Verdict | `q-mentor-verdict` | `ProblemSpec`, baselines, target constraints | `Verdict` with go/no-go and confidence | Classical baseline and smallest useful experiment are explicit | No measurable advantage hypothesis |
| Design | `q-mentor-design` | Accepted verdict and canonical model | Architecture, interfaces, threat model, test plan | Every component has a contract and failure mode | Design cannot preserve the canonical objective |
| Translate | `q-mentor-translate` | Canonical model, `ProgramIR`, and target | Target mapping plus `CapabilityReport` and `TranslationRecord` | Exact semantic/energy equivalence, or labeled approximation | Target cannot represent the source semantics exactly |
| Convert | `q-mentor-convert` | Parsed source, canonical problem, capability report, target SDK | Complete target files, `TranslationRecord`, and `OptimizationRecord` for optimization tasks | Clean import/run, semantic equivalence, and fair quality/resource comparison | Missing SDK, unsupported mapping, or unverified optimization claim |
| Evaluate | `q-mentor-evaluate` | Candidates, baselines, metrics, budget | Experiment plan and comparison report | Same instances, seeds, budgets, and confidence rules | Comparison would be unfair or underpowered |
| Implement | `q-mentor-implement` | Accepted design, target report, test plan | Complete files or scoped diff | No placeholders; pinned imports, entry point, fixture, and validation commands exist | Required dependency, permission, or mapping is absent |
| Test | `q-mentor-test` | Implementation and fixtures | Reproducible test/eval report and validation state | Syntax, import, local execution, property, equivalence, statistical, and regression gates pass | Flaky, cherry-picked, incomplete, or irreproducible result |
| Review | `q-mentor-review` / `q-mentor-pqc-scan` | Diff, artifacts, security context | Findings with severity and evidence | Correctness, privacy, supply-chain, and cryptography checks pass | Material risk lacks mitigation or owner |
| Communicate | `q-mentor-exec` | Validated results and audience | Decision brief with limits and next action | Numbers reconcile with artifacts; uncertainty is stated | Results are not decision-ready |
| Improve | `q-mentor-improve` | Failure, changed source, or opted-in lesson | Sanitized `LessonCandidate`, eval, proposed update | User approves retention; regression proves the update | Consent, evidence, scope, or measurable gain is absent |

## Target capability coverage

| Target | Role | Offline-first path | Required capability gate |
|---|---|---|---|
| Qiskit | Gate-model SDK | Local simulator | Operator order, QUBO-to-Ising constants, bit order, shots, seed, optimizer, and decoded energy agree |
| Classiq | High-level modeling and synthesis platform | Model validation or mocked adapter | Objective, constraints, synthesis settings, credentials, and generated-circuit limits are explicit |
| D-Wave Ocean | BQM/CQM and annealing stack | Exact/local sampler | Linear/quadratic bias conventions, offsets, embedding, chain strength, sampler, and decode rules agree |
| Pasqal/Pulser | Neutral-atom pulse and analog workflow | Capability analysis and local emulation | Coupling signs, geometry, register/device limits, addressability, pulses, noise, and measurement support the claim |
| PennyLane | Cross-platform differentiable framework | Named local device such as `default.qubit` | Actual device/plugin, wire order, interface, differentiation method, shots, optimizer, seed, and Hamiltonian agree |
| Cirq | Gate-circuit framework | Local simulator | Grid/coupling choice, gate decomposition, measurement keys, and bit order agree |
| pytket | Compiler and circuit SDK; Quantinuum bridge | Local circuit/simulator | Pre/post compilation semantics and resource counts agree; Nexus access remains gated |
| Bloqade | QuEra neutral-atom programming | Local analog simulator | Geometry, Hamiltonian, schedule, and measurement match supported analog model |
| Perceval | Quandela photonic circuit SDK | Local processor | Modes, photon number, loss/postselection, detection, and decoding are explicit |

PennyLane is not itself a hardware provider. Pasqal/Pulser is not a generic QUBO compiler. The plugin must preserve these distinctions in prompts, schemas, UI text, and tests.

[README-11](README-11-HARDWARE-AND-RESEARCH.md) extends this table to profiled pyQuil, IQM, OQC, IonQ, AQT, Qristal, SpinQit, and research-only silicon, electron-on-helium, and topological paths. Store every backend's support level. These rows are reference SDK paths, not a claim of live access to every provider's hardware. [README-14](README-14-CONVERSION-ATLAS.md) classifies conversions between these physical families by computing model and proof obligation.

## Completeness audit

For every lifecycle phase and target, require:

- one discoverable skill with concise activation and stop rules;
- one mandatory `template_id` from [README-13](README-13-RESPONSE-TEMPLATES.md), tested for every answer in business/technical modes and all relevant statuses;
- one typed schema or reusable template for durable output;
- declared prerequisites and follow-ons in the registry, with an automatic-handoff eval;
- one positive fixture and at least one adversarial or unsupported fixture;
- an offline path, optional dependencies, and explicit remote-cost approval;
- one complete version-pinned example for each `tested-local` target, or a precise capability/negative fixture for a `profiled` or `research-only` path;
- one `ConversionEdge` with semantic classification, maintained source, and test for every shipped bridge; no unverified all-pairs promise;
- version and source-freshness metadata for external claims;
- privacy, security, and token-budget bounds;
- brief, detailed, business, technical, and machine response-contract tests;
- regression coverage before a learned lesson or research update is promoted.

## Adding a domain pack

A new pack supplies vocabulary, canonical models, units, domain-specific failure modes, fixtures, and primary references. It may refine teaching examples and verdict criteria, but must not fork the lifecycle schemas, provider contracts, consent rules, or evidence policy. This keeps the core broad while letting finance, chemistry, logistics, machine learning, and future domains evolve independently.

The pack is ready only when one toy problem runs from learning and research through verdict, design, evaluation, implementation, testing, communication, and opt-in improvement without remote services by default.
