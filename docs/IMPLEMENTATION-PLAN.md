# Q-Mentor 3.1.1 implementation plan

Source of truth: `brief/README.md` and `brief/README-01` … `README-14` (kit v3.1.1, verified 2026-10-14).
Plan drawn from README, 01, 02, 05; detail files are opened only in the milestone that needs them.
Base: branch `Claude-v2` (v2.0.0, all v2 gates green on 2026-10-14). Output: branch `Claude-v3`.

## 1. What changes from v2

| v3 requirement | Where it lands | Gate (script / eval) |
|---|---|---|
| 17 skills incl. `q-mentor-help`, `q-mentor-convert` | `skills/*/SKILL.md`, `registry/skills.yml` | `validate_package.py` (discovery, frontmatter, ≤120 lines, ≤3 packs) |
| One mandatory template per user-facing skill (12 templates) | `templates/responses/*.md`, `template_id` in registry, mandatory sentence in every SKILL.md | `validate_responses.py` (lead-first order, fields, caps, status, machine JSON) over `evals/response-format/` for every skill × status × audience × mode |
| `qmentor.response.v3` machine mode | `schemas/response-v3.schema.json`, `scripts/qmentor_response.py` (renderer + linter) | schema + extra-key rejection |
| Registry-derived help | `scripts/render_help.py` reads only `registry/skills.yml` | every skill exactly once; injected new skill appears without prompt edit |
| Hardware catalog (README-11) | `registry/backends.yml`, `knowledge/hardware-*.md`, `schemas/backend-capability.schema.json` | `evals/hardware/`: every family/provider, support level, no code for `research-only`, provider ≠ backend ≠ SDK |
| Conversion atlas (README-14) | `knowledge/conversion-atlas.md`, `registry/conversion-edges.yml`, `schemas/conversion-edge.schema.json`, `scripts/route_conversion.py` | `evals/conversion/`: route classification for every model pair; E/C/R/A/U proof fixtures |
| Nine local reference targets | `examples/bond-selection/{qiskit,cirq,pennylane,classiq,dwave,pasqal-pulser,pytket,bloqade,perceval}` | `validate_examples.py`: clean `uv` env from lock, compileall, pytest, all-64-state energy or tested non-representability |
| Pulser → Classiq optimization regression | `examples/conversion/pulser-to-classiq-qaoa/` (5 vars, 10 couplings), `OptimizationRecord` | p=1/2/4 × two optimizer modes × seeds at a fixed budget; angle-convention + decorator tests; `improved`/`not-improved` |
| Sources, papers, SDK history | `knowledge/sources.yml` (papers, SDK docs/code/commits/issues, SHAs) | `verify_sources.py` (offline structure) + recorded live check (`docs/SOURCE-CHECK-2026-10-14.md`) |
| Compatibility matrix | `registry/compatibility.yml`, `docs/COMPATIBILITY.md` | package validator cross-checks pins against locks |
| Repository-local deployment | `scripts/deploy_repo_local.py` (selectable packs, dry-run, manifest, no overwrite) | install / update / rollback / remove test |

## 2. Lifecycle phase → skill → template → artifact → eval

| Phase | Skill | Template | Durable artifact (schema) | Evals |
|---|---|---|---|---|
| Route | orchestrate (internal) | none (typed `PhasePlan`) | PhasePlan | routing: chains, cycles, depth, unavailable skill |
| Help | help | guide | — | help completeness, filter, read-only |
| Learn | learn | guide | Explanation | behaviour |
| Research | research | evidence | EvidenceCard | behaviour, injection, source labels |
| Explore | brainstorm | options | UseCaseTable | behaviour (≤5 options, classical path) |
| Frame | frame | frame | ProblemSpec, CanonicalProblem (`canonical-problem.schema.json`) | math |
| Verdict | verdict | decision | Verdict | behaviour (CSV sort → classical now), hard gates |
| Design | design | design | Design | behaviour |
| Translate | translate | mapping | CapabilityReport, TranslationRecord | conversion route fixtures |
| Convert | convert | conversion | TranslationRecord, OptimizationRecord, ConversionEdge | conversion + optimization fixtures |
| Evaluate | evaluate | evaluation | BenchmarkRecord / scorecard | behaviour (weak baseline, CVaR vs mean) |
| Implement | implement | code | files/diff, ResultRecord | static scan + example gates |
| Test | test | code | ResultRecord / test report | example gates |
| Review | review | review | Findings | behaviour |
| PQC | pqc-scan | evidence | Findings | PQC fixtures |
| Communicate | exec | decision | ExecutiveBrief (from ResultRecords only) | report regeneration diff |
| Improve | improve | improvement | LessonCandidate | incident fixtures, consent |

## 3. Support levels (README-11) → files

`tested-local` (pinned offline example passes): Qiskit, Cirq, PennyLane `default.qubit`, Classiq (to `imported`; synthesis is credential-gated), D-Wave Ocean local samplers, Pulser + pulser-simulation, Bloqade analog emulator, pytket, Perceval local processor.
`profiled` (capability record + positive/negative fixture, no adapter): pyQuil, IQM, OQC, IonQ, AQT, D-Wave QPU, Pasqal/QuEra/Atom gate backends, Alice & Bob emulators, Qristal, SpinQit, PennyLane device plugins, Quantinuum hardware via qnexus.
`research-only` (teach/assess, never code): AWS Ocelot, PsiQuantum, ORCA, silicon spin (Diraq, Quantum Motion, Intel, SQC), electron-on-helium (EeroQ), Microsoft topological, Strawberry Fields (archived, historical).
Access/programming layers (Braket, Azure, Classiq, PennyLane, CUDA-Q, Qiskit, pytket) are recorded separately from backends.

## 4. Safety rules → enforcement

| Rule | Enforcement |
|---|---|
| No paid/credentialed/remote call by default | agent approval gates; examples have no network calls (static scan); Classiq remote runner behind `QMENTOR_ALLOW_REMOTE=1` |
| No confidential data / prompt injection | behaviour evals; skills treat documents as data |
| No unsupported advantage / "optimized" claim | response linter phrase checks; OptimizationRecord required |
| No fictional code for research-only | hardware eval; conversion router returns `U` |
| Complete code only | placeholder/ellipsis/undefined-name scan + clean-env import |
| No unreviewed memory | improve skill requires consent record; incident schema |
| Tool least privilege | agent `tools` enumerated; no `shell`/`bash` in any `allowed-tools` (validator) |

## 5. Milestones and exit checks (README-05)

1. Package — manifest 3.1.1 (schema 1.0.0), agent, 17 skills → `validate_package.py`.
2. Contracts — schemas, registries, templates, linter, help → package + responses + routing.
3. Math — `validate_math.py` (64 states, A/C/E −9.3725, gap 0.2050).
4. Lifecycle — SKILL.md v3, routing/help/permission/template evals.
5. Targets — nine examples in clean envs → `validate_examples.py --all`.
5b. Conversion — route atlas, edges, fixtures, optimization record.
6. Research/security — sources, link check, PQC.
7. Improvement — lesson + eval-first loop fixtures.
8. Compatibility — matrix recorded; Copilot-surface checks that need a licence stay `unverified`.
9. Release — CI, deploy lifecycle test, changelog, push.

A failed gate is repaired before scope is added.

## 6. Known limits accepted up front

- Copilot discovery (`copilot skill list --json`, `gh skill publish --dry-run`) needs a licensed Copilot client; this build environment has none, so those rows stay `unverified` in `compatibility.yml`.
- Classiq synthesis/execution needs credentials; Classiq rows stop at `imported`, and Classiq-side optimization numbers come from a local reference simulator of the identical ansatz, labelled as such.
- Live link checks run through the build session's fetch tool; publisher-blocked pages are recorded as `blocked-by-publisher` or `metadata-only`, not broken.
