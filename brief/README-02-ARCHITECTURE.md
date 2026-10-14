# Architecture

## Design decision

Use a portable plugin with lazily loaded skills. Do not start with the Copilot SDK, MCP, retrieval infrastructure, or a hosted service. The core lifecycle is domain-neutral; finance, execution-target, and research packs are replaceable modules. Domain logic belongs in plain, reviewable files, while deterministic scripts validate the package, mappings, and demo.

## Target repository

```text
q-mentor/
├── plugin.json
├── README.md
├── CHANGELOG.md
├── com.github.copilot/
│   └── agents/q-mentor.agent.md
├── skills/
│   ├── q-mentor-orchestrate/SKILL.md
│   ├── q-mentor-help/SKILL.md
│   ├── q-mentor-learn/SKILL.md
│   ├── q-mentor-research/SKILL.md
│   ├── q-mentor-brainstorm/SKILL.md
│   ├── q-mentor-frame/SKILL.md
│   ├── q-mentor-verdict/SKILL.md
│   ├── q-mentor-design/SKILL.md
│   ├── q-mentor-translate/SKILL.md
│   ├── q-mentor-convert/SKILL.md
│   ├── q-mentor-evaluate/SKILL.md
│   ├── q-mentor-implement/SKILL.md
│   ├── q-mentor-test/SKILL.md
│   ├── q-mentor-review/SKILL.md
│   ├── q-mentor-pqc-scan/SKILL.md
│   ├── q-mentor-exec/SKILL.md
│   └── q-mentor-improve/SKILL.md
├── knowledge/
│   ├── INDEX.md
│   ├── quantum-basics.md
│   ├── optimization-math.md
│   ├── quantum-fit.md
│   ├── research-method.md
│   ├── providers-qiskit.md
│   ├── providers-classiq.md
│   ├── providers-dwave.md
│   ├── providers-pasqal-pulser.md
│   ├── framework-pennylane.md
│   ├── hardware-index.md
│   ├── hardware-superconducting.md
│   ├── hardware-ions-atoms.md
│   ├── hardware-photonic-spin.md
│   ├── hardware-nmr-helium.md
│   ├── recent-research.md
│   ├── conversion-atlas.md
│   ├── pqc.md
│   └── sources.yml
├── registry/
│   ├── skills.yml
│   ├── compatibility.yml
│   ├── backends.yml
│   └── conversion-edges.yml
├── schemas/
│   ├── response-v3.schema.json
│   ├── skill-registry.schema.json
│   ├── canonical-problem.schema.json
│   ├── program-ir.schema.json
│   ├── translation-record.schema.json
│   ├── conversion-edge.schema.json
│   ├── optimization-record.schema.json
│   └── result-record.schema.json
├── domains/
│   └── finance/
│       ├── INDEX.md
│       ├── portfolio-optimization.md
│       └── claims-and-limits.md
├── templates/
│   ├── frame.md
│   ├── verdict.md
│   ├── provider-design.md
│   ├── evidence-card.md
│   ├── experiment-record.md
│   ├── conversation-lesson.md
│   ├── executive-brief.md
│   └── responses/
│       ├── guide.md
│       ├── options.md
│       ├── evidence.md
│       ├── frame.md
│       ├── decision.md
│       ├── design.md
│       ├── mapping.md
│       ├── evaluation.md
│       ├── conversion.md
│       ├── code.md
│       ├── review.md
│       └── improvement.md
├── demo/bond-selection/
│   ├── README.md
│   ├── problem.json
│   └── expected.json
├── examples/
│   └── bond-selection/
│       ├── qiskit/
│       ├── classiq/
│       ├── dwave/
│       ├── pasqal-pulser/
│       ├── pennylane/
│       ├── cirq/
│       ├── bloqade/
│       ├── pytket/
│       └── perceval/
├── evals/
│   ├── routing/
│   ├── behavior/
│   ├── math/
│   ├── conversion/
│   ├── response-format/
│   ├── hardware/
│   ├── optimization/
│   └── incidents/
├── scripts/
│   ├── validate_package.py
│   ├── validate_math.py
│   ├── validate_responses.py
│   ├── validate_examples.py
│   ├── verify_sources.py
│   └── deploy_repo_local.py
└── .github/workflows/quality.yml
```

`plugin.json` should use the newest Agent Plugins schema proven across the supported-client matrix. At this brief's verification date, Copilot CLI recognized `1.0.0` and `1.1.0`; use `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json` as the compatibility baseline. An Agent Plugins manifest has a closed top-level schema: do not add legacy component-path fields such as `skills`, `agents`, `hooks`, or `mcpServers`. Put Copilot-specific agents under `com.github.copilot/agents/` and immediate skill directories under `skills/`.

## Runtime flow

```text
user intent
  -> Q-Mentor agent reads the small skill registry
  -> orchestrator selects a bounded dependency chain
  -> each skill reads only its indexed knowledge and prior typed artifact
  -> skill emits a versioned artifact or response block
  -> deterministic checks evaluate math, format, claims, and hardware support
  -> human approves any code, credentialed action, or policy decision
```

The custom agent is a thin orchestrator. It must not preload every skill or knowledge file. `registry/skills.yml` records each skill's intents, inputs, outputs, prerequisites, suggested follow-ons, allowed side effects, `template_id`, and maximum chain depth. `q-mentor-help` renders the registry; it never maintains a separate skill list. Each `SKILL.md` repeats only its local contract and links to no more than three small packs.

Skill chaining is agent-owned because skill discovery does not guarantee a portable skill-to-skill call primitive. The agent loads the next `SKILL.md` named by the registry, passes artifacts rather than conversational summaries, records `skills_used`, and rejects cycles. Default maximum: five skills per turn. A longer lifecycle uses checkpointed phases and resumes from artifacts instead of retaining the full chat.

Agent frontmatter must enumerate required tools rather than use `tools: ["*"]`. Read-only skills receive no write or shell preapproval. Research alone receives web tools. `implement` and `test` may request scoped edit/execute permission, but their `allowed-tools` must not pre-approve arbitrary `shell` or `bash`; GitHub warns that doing so removes confirmation for terminal commands.

## Canonical model, target adapters

Keep business math independent of SDKs:

1. `ProblemSpec`: variables, domains, objective, constraints, scaling, provenance.
2. `CanonicalQUBO`: matrix, constant, bit order, coefficient convention, penalties.
3. `TargetPlan`: provider or framework, algorithm, device/backend/simulator, encoding, resource estimate, version pins.
4. `CapabilityReport`: exact, approximate, unsupported, or unknown mapping; required hardware features and lost semantics.
5. `ResultRecord`: samples, feasibility, energy, decoded decision, runtime, cost, seed, provider metadata.
6. `BenchmarkRecord`: exact/heuristic classical result and comparison metrics.
7. `EvidenceCard`: claim, source type, problem scale, baseline, hardware, metric, artifacts, limitations, replication status.
8. `LessonCandidate`: explicit consent, sanitized failure or preference, scope, counterexample, proposed eval, and retention decision.
9. `ProgramIR`: source semantics, mathematical operators, register/wire model, controls/pulses, measurements, constraints, and unsupported features—never raw source alone.
10. `TranslationRecord`: source/target versions, semantic mappings, losses, capability status, generated files, validation commands, and observed results.
11. `ResponseEnvelope`: contract version, status, mode, answer blocks, evidence, assumptions, skills used, validation, and next action.
12. `BackendCapability`: physical modality, computing model, provider, SDK, concrete backend, native operations, geometry/connectivity, measurement/noise, access, and support level.
13. `OptimizationRecord`: identical objective and feasible set, baseline, variant parameters, seed/shots/evaluations, feasible probability, best feasible energy, expected energy, depth/two-qubit gates, runtime/cost, confidence interval, and selection reason.
14. `ConversionEdge`: source and target concrete backends, physical/model classes, source and target pinned SDKs/SHAs, classification (`E`/`C`/`R`/`A`/`U`), preserved semantics, losses, proof fixture, success probability or approximation error where relevant, and validation state.

Target adapters may change syntax, but not the canonical objective. Cross-target conversion first extracts `ProgramIR`, then produces a capability report and target plan; it never rewrites APIs line by line. Test exact adapters by evaluating all 64 assignments in the toy case and comparing energy after documented constant and sign conventions. A target that cannot express the source semantics exactly must return `unsupported-exact` or a separately labeled approximation; it must never pass by dropping pulses, constraints, offsets, measurements, or decoding rules.

PennyLane is a framework target: default to a local simulator and name the actual device plugin separately. Pasqal is a provider ecosystem: Pulser targets neutral-atom pulse programs, whose geometry, interaction signs, device limits, and addressability constrain which QUBOs are physically representable.

`registry/backends.yml` starts from [README-11](README-11-HARDWARE-AND-RESEARCH.md). Only `tested-local` adapters generate code by default; `profiled` entries explain capability and direct the user to a versioned official example; `research-only` entries teach or assess, with no execution claim. The nine local examples in the tree are reference implementations, not nine interchangeable hardware backends. Backend-specific bridges are added only when a clean test and source record exist. The source map in [README-12](README-12-SDK-SOURCE-MAP.md) supplies versioned code provenance.

`registry/conversion-edges.yml` is a sparse, reviewed set of shipped bridges and negative routes. Its candidate classifications and proof requirements come from [README-14](README-14-CONVERSION-ATLAS.md); the registry does not claim that every hardware-family pair is executable. For an unlisted request, `q-mentor-convert` builds a capability report before code and cannot label an edge supported without the corresponding fixture.

## Knowledge-pack rules

- One question per pack; target under 1,000 tokens.
- Lead with the operational rule, then math, limitations, and sources.
- Put version-specific APIs only in execution-target packs.
- Keep generic lifecycle rules out of domain packs; a new chemistry, logistics, or security pack should plug into the same schemas.
- Give every factual entry `source`, `source_date`, and `last_verified` metadata in `sources.yml`.
- Keep paper and SDK change histories as small metadata records. Read only the selected provider pack and source entry during a user task.
- Classify sources as `volatile`, `active`, or `stable`. Verify volatile SDK, packaging, hardware, pricing, and availability claims during every release; do not say “latest” without a live check.
- Do not copy papers or vendor documentation into the repository. Summarize and link.
- Keep organization-specific lessons in a separately approved private pack; never mix them into the public plugin.

## Repository-local mode

The deployment script copies canonical skills to `.github/skills/`, the agent to `.github/agents/`, and shared registries, schemas, templates, and selected knowledge packs to `.github/q-mentor/`. Skills resolve shared files from the plugin root in plugin mode and `.github/q-mentor/` in repository mode; a missing registry is a visible routing failure, never permission to guess. The script must support `--dry-run`, refuse to overwrite changed files, let the installer select domain and execution-target packs, and write a manifest of copied versions and checksums. Avoid symlinks because client and cloud environments differ.

Repository-wide `.github/copilot-instructions.md` should contain only build/test commands and universal safety rules. Domain detail belongs in skills because persistent instructions are included much more often.

## Deferred extensions

Add these only after the MVP evals show a need:

- Copilot SDK: custom UI, session telemetry, or programmatic orchestration.
- MCP: a required external tool or data source with an approved trust boundary.
- Remote retrieval: a knowledge corpus too large for curated packs.
- Paid hardware automation: approved identity, budgets, audit, and explicit user confirmation.
- Strict response hook: an opt-in `agentStop` hook that runs the format linter and may request one repair turn. Keep it off by default because hooks vary by Copilot surface, consume another turn, and must avoid transcript retention.

Each extension needs an architecture decision record with benefit, token cost, security surface, rollback, and a cheaper alternative.

