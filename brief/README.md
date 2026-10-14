# Q-Mentor Copilot Build Kit v3.1.1

Brief version: `3.1.1` · Last verified: `2026-10-14`

This folder is a construction brief for a GitHub Copilot plugin, not the plugin. Drop the folder into a new repository, open Copilot in Plan mode or Copilot CLI, and use the build prompt below. Earlier v2, v3.0, and v3.1.0 ZIPs remain separate archives.

## Product

Q-Mentor is a vendor-neutral quantum-computing guide inside GitHub Copilot. It teaches, researches, assesses fit, designs, converts, implements, tests, reviews, and explains results. The finance bond-selection example is its first end-to-end demo; the core works across domains.

## v3 changes

- A hardware catalog distinguishes superconducting gates and annealing, trapped ions, neutral atoms, photonics, silicon spins, diamond centers, and topological research. Every provider has an honest support level.
- `/q-mentor-help` explains each skill and when to use it; the agent still selects skills automatically for ordinary requests.
- `/q-mentor-convert` converts across supported computing models and benchmarks optimization quality, not merely syntax. The Pasqal/Pulser → Classiq regression is mandatory.
- Every skill follows one mandatory, audience-aware response template—even for clarifications, failures, and unsupported requests. Business results lead with the answer; runnable code remains complete.
- Primary papers from 2023 onward and public SDK repositories are mapped to documentation, examples, commits, and issues, with a release link check.
- V3.1 adds NMR and electron-on-helium research paths plus a cross-hardware conversion atlas. It routes every requested pair by execution model and checks maintained SDK bridges before emitting code.

## Build target

Use an **Agent Plugins portable skill pack** with one Copilot custom agent, plus repository-local `.github/skills/` deployment. No hosted service is required. Plugin release `3.1.1` is independent of the Agent Plugins manifest schema. The v2 brief recorded CLI support for schemas `1.0.0` and `1.1.0`; the builder must recheck client support and use the oldest schema that covers the needed features.

Load skills and knowledge packs only when required. The custom agent owns the registry and automatic handoffs; no portable direct skill-to-skill call API is assumed. Keep SDK dependencies optional by target. Local simulation and exact classical baselines are the default; remote jobs need explicit approval.

## Read in this order

1. [Product contract](README-01-PRODUCT.md) and [architecture](README-02-ARCHITECTURE.md)
2. [Domain and math](README-03-DOMAIN-AND-MATH.md) and [demo](README-04-DEMO.md)
3. [Build and evals](README-05-BUILD-QUALITY-IMPROVEMENT.md) and [cost/governance](README-06-COST-AND-GOVERNANCE.md)
4. [Core references](README-07-REFERENCES.md) and [coverage matrix](README-08-COVERAGE-MATRIX.md)
5. [Skill orchestration](README-09-ORCHESTRATION-AND-OUTPUTS.md) and [code conversion](README-10-CODE-CONVERSION.md)
6. [Hardware and recent research](README-11-HARDWARE-AND-RESEARCH.md), [SDK source map](README-12-SDK-SOURCE-MAP.md), [response templates](README-13-RESPONSE-TEMPLATES.md), and [cross-hardware conversion atlas](README-14-CONVERSION-ATLAS.md)

The lifecycle is **learn/research → explore → frame → verdict → design → translate/convert → evaluate → implement → test → review → communicate → improve**. Enter at any phase; the registry adds only the prerequisites needed for the requested outcome.

## Paste this into GitHub Copilot

```text
Build Q-Mentor using README.md and README-01 through README-14 as the source of truth. Index them first; open only the files needed for the current milestone rather than pasting the entire brief into each Copilot turn.

First produce a short implementation plan from README.md, README-01, README-02, and README-05. Map every lifecycle phase, hardware support level, SDK path, skill handoff, response template, safety rule, and acceptance criterion to files and tests; load the referenced detail files only when implementing those phases. Then build in the milestones of README-05, running the stated checks after each milestone. Stop and repair a failed gate before adding more scope.

Build an Agent Plugins package with one custom Q-Mentor agent, a small skill registry, lazily loaded skills including q-mentor-help and q-mentor-convert, versioned schemas, mandatory response templates, curated knowledge packs, a domain-neutral canonical problem model, the finance starter pack, the six-bond synthetic demo, and repository-local deployment. Follow README-11 for hardware coverage and support levels, and README-12 for official SDK sources, examples, commit histories, and issue histories.

Build the 12 response templates in README-13. Assign exactly one template to every user-facing skill and enforce it on every answer, including clarification, failure, unsupported, direct-invocation, business, technical, and machine-mode answers. Lead with the answer, preserve observed validation and uncertainty, and never shorten requested code to satisfy a prose cap.

Provide complete pinned offline examples for every target declared tested-local. For research-only and profiled providers, provide capability records and negative fixtures rather than invented runnable adapters. Apply README-14 to every source/target request: classify the execution-model route, check the current maintained SDK bridge and its issues, preserve the stated semantics, and prove exact/conditional/reimplementation/approximate claims with the corresponding fixture. Convert source -> canonical problem and program semantics -> capability report -> target implementation. In the Pasqal/Pulser -> Classiq optimization case, use the version-matched QAOA reference structure, test decorator and angle conventions, compare depth/optimizer/shot-budget candidates, and report whether the new code improves a fixed metric without changing the objective or feasible set. Never call code optimized based only on compilation.

Use a strong classical exact or well-tuned heuristic baseline. No paid hardware call, credentials, confidential data, autonomous production change, web service, database, telemetry vendor, or unreviewed conversation memory. Research and lessons enter through the opt-in, eval-first review loop. Do not claim quantum advantage without reproducible end-to-end comparison.

Completion requires valid packaging and skill discovery, automatic routing and q-mentor-help tests, every skill's mandatory v3 response template across all statuses and audiences, clean-environment example tests, README-14 route-classification and exact/conditional/approximate/unsupported fixtures, fair optimization benchmarks, the demo optimum, checked paper/source links, and a documented compatibility matrix. Record unsupported APIs and unresolved source access honestly.
```

## Acceptance in one pass

- A user can ask “What can Q-Mentor do?” and get a concise registry-derived skill guide; a normal task invokes the relevant skills without naming them.
- A business user gets a short decision, evidence, cost/risk, and next gate; a developer gets complete files/diffs and observed validation.
- The toy demo reproduces its classical optimum and proves exact target energy equivalence where supported.
- The Pasqal → Classiq case produces runnable, semantically faithful code and a measured optimization comparison; decorator, layer count, angle convention, and classical optimizer are explicit and tested.
- Other conversion families follow README-14: gate↔gate, analog↔analog, gate→photonic DV, and BQM reimplementations each have a source/target fixture; NMR and emerging helium/topological routes receive honest capability limits.
- Every hardware recommendation names the physical family, computing model, SDK, backend, and support level. A research-only system never receives fictional execution code.
- New research or conversation lessons change prompts or packs only through sanitized, reviewed, regression-tested updates.

Treat packaging, SDK APIs, provider availability, prices, and paper status as changeable. Pin tested versions and repeat the source and link checks before release.
