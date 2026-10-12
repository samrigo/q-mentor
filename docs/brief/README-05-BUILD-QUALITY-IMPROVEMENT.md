# Build, Quality, and Improvement

## Build as small verified milestones

Copilot should complete one milestone, run its checks, and leave a reviewable commit before continuing.

| Milestone | Deliverable | Exit check |
|---|---|---|
| 1. Package | Manifest, agent, empty skill shells, install/remove docs | Plugin and frontmatter schemas validate; all skills are discoverable |
| 2. Contracts | Shared schemas, templates, guardrails, source registry | Schema and negative-behavior tests pass |
| 3. Math | Canonical QUBO/Ising utilities and six-bond exact baseline | All 64 states and stated optimum reproduce |
| 4. Lifecycle | Learn, research, brainstorm, frame, verdict, design, translate, evaluate, implement, test, review, exec | Coverage, routing, permission, and output-contract evals pass |
| 5. Targets | Qiskit/PennyLane local implementations; Classiq/D-Wave translations; Pasqal/Pulser capability gate | Equivalence or honest-unsupported tests pass |
| 6. Research/security | Evidence cards, source freshness, review, and PQC inventory | Seeded paper, claim, defect, and crypto fixtures pass |
| 7. Improvement | Opt-in lesson format, research-update path, eval-first workflow, changelog | Seeded failures are fixed without suite or cost regression |
| 8. Release | Offline CI, selectable repo-local deployment, version pins | Clean install and full lifecycle demo pass |

Use Python only where deterministic scripts add value. Markdown remains the source of behavior. Keep optional provider SDKs in separate dependency groups so the base install stays small.

## Test pyramid

### Deterministic checks

- JSON schema and plugin manifest validation.
- Skill name, description, path, size, and internal-link checks.
- Source entries include URL, owner, version/date, and `last_verified`.
- Math/property tests: symmetry, bit order, QUBO expansion, Ising conversion, penalty separation, energy equivalence, and target representability.
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
- Pasqal geometry/coupling/addressability failures and PennyLane device/gradient ambiguity;
- papers with weak baselines, missing artifacts, conflicting results, or vendor-only evidence;
- RSA/ECC/DH, AES, hashing, and false-positive PQC fixtures;
- executive summaries whose input evidence is incomplete.

Assertions should check fields and claims: lifecycle phase, verdict enum, classical alternative, capability status, evidence level and source type, uncertainty, citations, stop condition, tool permission, no forbidden action, and output length.

### Integration tests

Run offline/local tests on every change. PennyLane uses an explicit local device, and Pulser uses an emulator or capability-only test by default. Run remote provider smoke tests only on release candidates, behind environment flags, with fixed budgets and sanitized logs.

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

Use Copilot session-cost insights such as `/chronicle cost-tips` where available, but commit only stable, repository-specific lessons. A prompt change is accepted only if quality improves and median eval tokens do not rise materially without justification.

## Release gates

- All fixed evals pass on the supported Copilot clients.
- No high-severity dependency or secret finding is open.
- Source links and provider versions are checked.
- Every row in README-08 has a skill, template/schema, eval, and stop condition.
- The demo is reproducible from a clean environment.
- Known limitations and evidence level are visible in release notes.
- Security, legal, model-risk, and AI-use approvals required by the deploying organization are recorded outside the public plugin.

