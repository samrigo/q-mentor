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
│   ├── q-mentor-learn/SKILL.md
│   ├── q-mentor-research/SKILL.md
│   ├── q-mentor-brainstorm/SKILL.md
│   ├── q-mentor-frame/SKILL.md
│   ├── q-mentor-verdict/SKILL.md
│   ├── q-mentor-design/SKILL.md
│   ├── q-mentor-translate/SKILL.md
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
│   ├── pqc.md
│   └── sources.yml
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
│   └── executive-brief.md
├── demo/bond-selection/
│   ├── README.md
│   ├── problem.json
│   └── expected.json
├── evals/
│   ├── routing/
│   ├── behavior/
│   ├── math/
│   └── incidents/
├── scripts/
│   ├── validate_package.py
│   ├── validate_math.py
│   └── deploy_repo_local.py
└── .github/workflows/quality.yml
```

`plugin.json` should use the current supported Agent Plugins schema. At the time this brief was checked, GitHub documented `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json`; verify before release. Put Copilot-specific agents under `com.github.copilot/agents/` and immediate skill directories under `skills/`.

## Runtime flow

```text
user intent
  -> Q-Mentor agent selects one skill
  -> skill reads only the indexed knowledge it needs
  -> skill emits a structured answer or a scoped repo plan
  -> deterministic checks evaluate math, format, and claims
  -> human approves any code, credentialed action, or policy decision
```

The custom agent is a thin router. It must not preload every knowledge file. Each `SKILL.md` contains its workflow, output contract, stop conditions, and links to no more than three small knowledge packs. Analysis skills should be read-only; `implement` and `test` receive write/execute capability only when the active Copilot client supports an explicit least-privilege tool list.

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

Target adapters may change syntax, but not the canonical objective. Test exact adapters by evaluating all 64 assignments in the toy case and comparing energy after documented constant and sign conventions. A target that cannot express the objective exactly must return `unsupported` or a separately labeled approximation; it must never pass the equivalence test by changing the problem silently.

PennyLane is a framework target: default to a local simulator and name the actual device plugin separately. Pasqal is a provider ecosystem: Pulser targets neutral-atom pulse programs, whose geometry, interaction signs, device limits, and addressability constrain which QUBOs are physically representable.

## Knowledge-pack rules

- One question per pack; target under 1,000 tokens.
- Lead with the operational rule, then math, limitations, and sources.
- Put version-specific APIs only in execution-target packs.
- Keep generic lifecycle rules out of domain packs; a new chemistry, logistics, or security pack should plug into the same schemas.
- Give every factual entry `source`, `source_date`, and `last_verified` metadata in `sources.yml`.
- Do not copy papers or vendor documentation into the repository. Summarize and link.
- Keep organization-specific lessons in a separately approved private pack; never mix them into the public plugin.

## Repository-local mode

The deployment script copies the canonical skills to `.github/skills/` and the agent to `.github/agents/` in a target repository. It must support `--dry-run`, refuse to overwrite changed files, let the installer select domain and execution-target packs, and write a manifest of copied versions. Avoid symlinks because client and cloud environments differ.

Repository-wide `.github/copilot-instructions.md` should contain only build/test commands and universal safety rules. Domain detail belongs in skills because persistent instructions are included much more often.

## Deferred extensions

Add these only after the MVP evals show a need:

- Copilot SDK: custom UI, session telemetry, or programmatic orchestration.
- MCP: a required external tool or data source with an approved trust boundary.
- Remote retrieval: a knowledge corpus too large for curated packs.
- Paid hardware automation: approved identity, budgets, audit, and explicit user confirmation.

Each extension needs an architecture decision record with benefit, token cost, security surface, rollback, and a cheaper alternative.

