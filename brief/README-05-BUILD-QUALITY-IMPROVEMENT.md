# Build, Quality, and Improvement

## Build as small verified milestones

Copilot should complete one milestone, run its checks, and leave a reviewable commit before continuing.

| Milestone | Deliverable | Exit check |
|---|---|---|
| 1. Package | Manifest, agent, empty skill shells, install/remove docs | Plugin and frontmatter schemas validate; all skills are discoverable |
| 2. Contracts | Shared schemas, skill registry, generated help menu, mandatory v3 templates, guardrails, source registry | Registry DAG, help completeness, schema, format, and negative-behavior tests pass |
| 3. Math | Canonical QUBO/Ising utilities and six-bond exact baseline | All 64 states and stated optimum reproduce |
| 4. Lifecycle | Orchestrate, help, learn, research, brainstorm, frame, verdict, design, translate, convert, evaluate, implement, test, review, exec | Auto-handoff, help, cycle, routing, permission, and template evals pass |
| 5. Targets | README-11 hardware catalog plus complete Qiskit, Cirq, PennyLane, Classiq, D-Wave, Pulser, Bloqade, pytket, and Perceval local paths | Clean-environment syntax, import, local execution, capability, and equivalence/unsupported gates pass |
| 5b. Conversion quality | README-14 route atlas, sparse edge registry, representative cross-model fixtures, Pasqal/Pulser → Classiq regression, bounded QAOA variant harness | Every requested route classified; exact/conditional/reimplementation/approximation/unsupported proofs; fixed-budget quality/resource comparison; honest `not-improved` result allowed |
| 6. Research/security | Evidence cards, paper title/year/correction checks, SDK commits/issues/examples, review, and PQC inventory | All primary-paper metadata and source links classified; seeded claim, defect, and crypto fixtures pass |
| 7. Improvement | Opt-in lesson format, research-update path, eval-first workflow, changelog | Seeded failures are fixed without suite or cost regression |
| 8. Compatibility | Agent Plugins schema and supported Copilot surfaces | Discovery, tool, hook-free core, and response tests pass on the declared matrix |
| 9. Release | Offline CI, selectable repo-local deployment, version pins and checksum | Clean install, update, rollback, removal, and full lifecycle demo pass |

Use Python only where deterministic scripts add value. Markdown remains the source of behavior. Keep optional provider SDKs in separate dependency groups so the base install stays small.

## Test pyramid

### Deterministic checks

- JSON schema and plugin manifest validation.
- Skill name, description, path, size, and internal-link checks.
- Skill-registry schema, missing-edge, duplicate-edge, and cycle checks; every skill appears exactly once in the generated help menu.
- Per-skill `template_id` and response-file existence; lead-first field order, required content, maximum prose length, status-enum, audience-mode, and machine-JSON checks for **every** user-facing answer, not only successful final results.
- Hardware catalog/support-level schema and tests for named provider versus actual backend/model; reject code generation for `research-only` entries.
- Source entries include URL, owner, version/date, and `last_verified`.
- Math/property tests: symmetry, bit order, QUBO expansion, Ising conversion, penalty separation, energy equivalence, and target representability.
- Provider examples: reject ellipses, `TODO`, notebook-only state, undeclared names, stale imports, missing pins, missing entry points, and undocumented network calls; then compile, import, and smoke-test each clean environment.
- Optimization conversion: assert invariant objective/feasible set, basis-state phase and angle conventions, tested `@qperm`/`@qfunc` behavior, p=1/2/4 comparison where supported, identical shot/evaluation budget, feasible probability, gap, depth, runtime, and `not-improved` fallback.
- Cross-hardware conversion: verify README-14 model routing, maintained SDK and issue state, source/target pins, gate order and dynamic features, analog Hamiltonian/units/geometry, BQM offsets, photonic heralding success, NMR/cat backend limits, and explicit `U` for research-only targets. An interop import alone is not a passing semantic test.
- Check every cited DOI/arXiv title, publication year, correction/retraction status, and public SDK repository/example/commit/issue link; mark publisher 403 separately from a broken reference.
- Secret scanning, dependency audit, formatting, and unit tests.

### Behavioral evals

Use compact prompts with structural assertions rather than brittle golden prose. The suite must include:

- clear classical-only cases;
- plausible research cases;
- ambiguous requests that require assumptions;
- prompt-injection text inside a supplied document;
- requests containing prohibited data indicators;
- unsupported advantage claims;
- provider translation and version drift;
- one request spanning three skills, one direct skill invocation needing a prerequisite, one ambiguous handoff, one cycle attempt, and one unavailable skill;
- help-menu questions and a newly added skill that must appear automatically;
- terse, detailed, business, technical, and machine-format prompts for every skill and every relevant `complete`/`needs-input`/`blocked`/`unsupported`/`unverified` state; verbose drift, unstable headings, duplicate conclusions, invalid JSON, and truncated code;
- complete Pasqal/Pulser-to-Classiq conversion, analog-only unsupported conversion, missing-import code, stale API code, and code that compiles but changes the energy;
- gate↔gate conversion with implicit-swap and symbol pitfalls; Qiskit→Perceval dual-rail conversion with postselection rate; Pulser↔Bloqade/Braket AHS Hamiltonian mismatch; QUBO→D-Wave versus QAOA algorithm distinction; unsupported CV and research-only requests;
- Pasqal geometry/coupling/addressability failures and PennyLane device/gradient ambiguity;
- provider-matrix cases that distinguish physical modality, simulator, SDK, access layer, and unavailable QPU; archived SDK and research-only targets;
- QAOA code that compiles yet is worse than a simpler candidate, `RX(beta)`/`RX(2*beta)` convention drift, incorrect CVaR tail claim, and a four-layer run that still misses the exact optimum;
- papers with weak baselines, missing artifacts, conflicting results, or vendor-only evidence;
- RSA/ECC/DH, AES, hashing, and false-positive PQC fixtures;
- executive summaries whose input evidence is incomplete.

Assertions should check fields and claims: lifecycle phase, ordered `skills_used`, `template_id`, verdict enum, classical alternative, hardware support level, capability status, optimization status, evidence level and source type, uncertainty, citations, stop condition, tool permission, validation state, no forbidden action, heading order, and output length.

### Integration tests

Run offline/local tests on every change in fresh per-target environments. PennyLane uses an explicit local device, D-Wave uses an exact/local sampler, Qiskit/Cirq/pytket use local simulators, Classiq performs all locally available import/model validation, Pulser/Bloqade use emulators or capability-only tests, and Perceval uses a local photonic processor. Run credentialed synthesis and remote-provider smoke tests only on release candidates, behind environment flags, with fixed budgets and sanitized logs. Never upgrade an unavailable remote check to `passed`.

Run `copilot skill list --json` to confirm discovery. Where `gh skill` is available, run `gh skill publish --dry-run` for Agent Skills validation. Validate the chosen Agent Plugins schema locally and test both clean install and disabled-plugin behavior.

## Review checklist

Before accepting generated code or advice, ask:

1. Is the business objective represented faithfully?
2. Are units, bit order, matrix convention, scaling, and penalties explicit?
3. Is the classical baseline strong and fairly tuned?
4. Are feasibility and decoding tested independently of the sampler?
5. Are resource and cost measurements end to end?
6. Are seeds, versions, and backend metadata recorded?
7. Does the conclusion match the achieved evidence level?
8. Can the same result be obtained more simply with classical software?

## Safe self-improvement

Q-Mentor does not retrain itself or silently remember chats. It improves through a governed repository loop:

```text
opted-in conversation lesson, observed failure, or changed research
  -> sanitized candidate file
  -> failing eval added first
  -> smallest prompt/pack/code change
  -> full regression and cost comparison
  -> human-reviewed pull request
  -> versioned release and changelog
```

An incident or lesson records: explicit consent, prompt category, expected behavior, actual failure or correction, risk, sanitized evidence, affected skill, model/client/version, counterexample, proposed assertion, scope (`personal`, `repository`, or `plugin`), and retention decision. It must not contain raw transcripts, source code, or data the user is not authorized to retain.

At the end of a material workflow, Q-Mentor may ask once whether the user wants to save a sanitized lesson. Silence means no. The user sees and edits the candidate before any file write. Conversation-derived preferences remain personal unless the user explicitly promotes them; factual corrections require a source or reproducible test.

`q-mentor-improve` is maintainer-invoked. It may propose edits and a PR plan; it may not auto-merge, rewrite knowledge from one anecdote, store raw conversations, or spread one user's preference to others. Require at least one reproducible failure, approved lesson, or changed primary source.

For new research, `q-mentor-research` creates a candidate evidence card. A maintainer compares it with existing cards, adds contradiction and replication status, creates or updates evals, and only then promotes a compact claim into a knowledge pack. Retain negative and null results because they prevent repeated hype and wasted experiments.

Quarantine every conversation- or research-derived candidate. Strip embedded instructions, verify provenance, deduplicate it, and require either a reproducible failure or corroborating primary evidence. Promote through a canary eval set, then the full suite; record the exact rollback commit. A candidate that improves one case but harms routing, accuracy, privacy, format compliance, or token cost is rejected.

Use Copilot session-cost insights such as `/chronicle cost-tips` where available, but commit only stable, repository-specific lessons. A prompt change is accepted only if quality improves and median eval tokens do not rise materially without justification.

## Release gates

- All fixed evals pass on the supported Copilot clients.
- No high-severity dependency or secret finding is open.
- Source links and provider versions are checked.
- Every row in README-08 has a skill, template/schema, eval, and stop condition.
- Every registry edge is exercised, every response mode passes, and no auto-handoff cycle is possible.
- Every skill is present in registry-derived help, declares a valid v3 template, and passes direct and automatic routing evals.
- The hardware catalog covers all README-11 families and providers with an explicit support level; no profiled or research-only entry claims tested code.
- The conversion quality record shows fair, fixed-budget comparisons and reports `not-improved` when no candidate wins.
- Every claimed runnable provider example reaches its declared validation state from a clean lockfile.
- Supported Copilot clients, Agent Plugins schema, SDK versions, and last-verified dates are recorded in `registry/compatibility.yml`.
- The demo is reproducible from a clean environment.
- Known limitations and evidence level are visible in release notes.
- Security, legal, model-risk, and AI-use approvals required by the deploying organization are recorded outside the public plugin.

