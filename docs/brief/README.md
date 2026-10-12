# Q-Mentor Copilot Build Kit

Brief version: `1.1` · Last verified: `2026-10-11`

This folder is a construction brief, not the plugin itself. Drop it into a new repository, open GitHub Copilot in Plan mode (or Copilot CLI), and give Copilot the build prompt below.

## Product in one sentence

Q-Mentor is an honest, vendor-neutral quantum-computing guide inside GitHub Copilot: it teaches concepts, researches evidence, screens problems, designs and implements experiments, tests results, and always names the strongest classical alternative. Finance is the first domain pack and reference demo, not a limit on the core architecture.

## Recommended build target

Build the MVP as an **Agent Plugins 1.0 skill pack** with one Copilot custom agent and no hosted runtime. Keep the same skills deployable to `.github/skills/` for repository-local use.

Why this target:

- Skills are loaded only when relevant, so unrelated prompts do not pay for the full knowledge base.
- The plugin serves Copilot CLI, the Copilot app, and cloud agent; the same skills serve supported IDE agent modes through the repository-local deployment.
- No API service, vector database, MCP server, or paid quantum job is required for the MVP.
- A future SDK or MCP layer can be added without rewriting the domain core.

## Read in this order

1. [Product contract](README-01-PRODUCT.md)
2. [Architecture](README-02-ARCHITECTURE.md)
3. [Domain and math](README-03-DOMAIN-AND-MATH.md)
4. [End-to-end demo](README-04-DEMO.md)
5. [Build, test, and improve](README-05-BUILD-QUALITY-IMPROVEMENT.md)
6. [Cost, security, and governance](README-06-COST-AND-GOVERNANCE.md)
7. [Primary references](README-07-REFERENCES.md)
8. [Coverage matrix](README-08-COVERAGE-MATRIX.md)

The required lifecycle is: **learn/research → explore → frame → verdict → design → translate → evaluate → implement → test → review → communicate → improve**.

## Paste this into GitHub Copilot

```text
Build Q-Mentor from the README files in this folder.

First, read README.md and README-01 through README-08. Produce a short implementation plan that maps every lifecycle phase, execution target, safety rule, and acceptance criterion to a file and a test. Do not write implementation code until the plan is complete.

Build only the documented MVP:
- an Agent Plugins 1.0 package;
- one custom Q-Mentor agent;
- the named, lazily loaded skills;
- a domain-neutral core with the finance starter pack;
- small cited knowledge packs and research-evidence cards;
- deterministic validation and evaluation fixtures;
- the six-bond synthetic demo;
- Qiskit, Classiq, D-Wave, Pasqal/Pulser, and PennyLane targets with explicit capability checks;
- repository-local deployment instructions.

Do not add a web service, database, MCP server, Copilot SDK application, telemetry vendor, or paid quantum-hardware execution. Do not use client, confidential, or production data. Use a classical exact baseline for every optimization demo. Never claim quantum advantage without reproducible end-to-end evidence. Do not persist raw conversations; only create a sanitized lesson candidate after explicit user opt-in and review.

Work in the milestones in README-05. At the end of each milestone, run its checks and stop if they fail. Prefer the simplest implementation that satisfies the acceptance tests. Record assumptions in a decision log instead of silently inventing requirements.

The build is complete only when the plugin manifest validates, Copilot discovers every skill, the full lifecycle is covered, the demo reproduces the stated classical optimum, exact target translations preserve the same objective, unsupported mappings fail honestly, all evals pass, and the docs explain installation, removal, limits, research updates, conversation learning, and governance.
```

## Definition of done

The generated repository must demonstrate all of the following:

- `/q-mentor-verdict` can recommend **classical now** without hedging or hype.
- Only the invoked skill and its referenced pack are brought into context.
- The toy demo goes from problem statement to formulation, classical baseline, provider design, code generation, tests, validation, and an executive summary.
- Qiskit, Classiq, D-Wave, and PennyLane outputs express the same canonical optimization problem where supported; Pasqal/Pulser produces either an equivalent encoding or a precise representability failure with alternatives.
- Quantum output is measured against an exact or strong classical baseline on feasibility, objective gap, runtime, resource use, and reproducibility.
- Research claims are graded by source type, baseline quality, artifact availability, scale relevance, and independent replication.
- “Self-improving” means opt-in, sanitized conversation lessons plus new-research evidence, converted into eval-driven, human-reviewed pull requests—not silent model training or unreviewed memory.
- Hardware submission, credential use, and non-public data always require explicit user approval and policy clearance.

## Maintenance rule

Treat external APIs, Copilot packaging, pricing, and provider SDKs as changeable. Pin tested versions, record a `last_verified` date, and check the official links in [README-07](README-07-REFERENCES.md) before release.

