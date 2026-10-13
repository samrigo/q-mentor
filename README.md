# Q-Mentor for GitHub Copilot

[![quality](https://github.com/samrigo/q-mentor/actions/workflows/quality.yml/badge.svg?branch=Claude-v2)](https://github.com/samrigo/q-mentor/actions/workflows/quality.yml?query=branch%3AClaude-v2)

An honest, vendor-neutral quantum-computing guide inside GitHub Copilot. It teaches concepts, researches
evidence, screens problems, designs and implements experiments, tests results, and **always names the
strongest classical alternative**. "Classical now" is a first-class answer.

Finance is the first domain pack and reference demo; the lifecycle, schemas and evals are domain-neutral.

- **Package:** Agent Plugins `1.0.0` manifest (`plugin.json`), one Copilot custom agent, 15 lazily loaded skills.
- **No runtime:** no web service, database, MCP server, telemetry or paid quantum job.
- **Version:** 2.0.0 (built from the Q-Mentor Copilot build kit v2.0.0).

## Install

This v2 build lives on the `Claude-v2` branch of `samrigo/q-mentor`. Install it from a clone of that branch:

```bash
git clone -b Claude-v2 https://github.com/samrigo/q-mentor.git
copilot plugin install ./q-mentor
```

Then pick the **q-mentor** agent (`/agent`) or just ask a quantum question. For the cloud agent, Copilot app
or IDE agent mode, deploy into a repository:

```bash
python scripts/deploy_repo_local.py --target /path/to/repo --targets qiskit dwave --domains finance
```

Update, removal, pinning and limits: [docs/INSTALL.md](docs/INSTALL.md).

## Use it

Describe the outcome; Q-Mentor picks the skills.

| Ask | What happens |
|---|---|
| "Should we use quantum to pick 3 of these 6 bonds?" | frame → verdict: **classical now**, with the score, hard gates and a revisit trigger |
| "Analyze, design, implement and validate the six-bond example." | frame → verdict → design → implement → test, then a checkpoint and the next phase |
| "Run the six-bond QUBO on Pasqal." | capability report: **unsupported-exact**, with reasons and alternatives |
| "Convert this Pulser program to Classiq." | ProgramIR → per-semantic status → reimplementation of the shared QUBO; analog schedule unsupported |
| "Inventory post-quantum risk in this repo." | RSA/ECC/DH findings vs symmetric/hash review items, handed to a security owner |

Answers follow `qmentor.response.v2`: `Status`, `Result`, `Validation`, `Next`, under 180 words.
Ask for **detailed** or **machine** (JSON) mode when you need it.

## Skills

| Skill | Job |
|---|---|
| `q-mentor-orchestrate` (internal) | Pick and order the minimum skills from `registry/skills.yml`; ≤ 5 per turn, no cycles |
| `q-mentor-learn` | One concept: analogy, formula, misconception, source |
| `q-mentor-research` | Evidence cards from primary sources; contradictions kept |
| `q-mentor-brainstorm` | ≤ 5 ranked options, classical included |
| `q-mentor-frame` | ProblemSpec + CanonicalProblem |
| `q-mentor-verdict` | Classical now / PoC / bounded / candidate experiment |
| `q-mentor-design` | Target-neutral design and target plans |
| `q-mentor-translate` | Semantic translation with CapabilityReport and TranslationRecord |
| `q-mentor-evaluate` | Scorecard or fair experiment plan |
| `q-mentor-implement` | Smallest complete, pinned change |
| `q-mentor-test` | Deterministic, equivalence, statistical and noise tests; observed validation state |
| `q-mentor-review` | Findings only |
| `q-mentor-pqc-scan` | Crypto inventory, never migration |
| `q-mentor-exec` | One-page brief from result records only |
| `q-mentor-improve` | Opt-in, eval-first change proposals |

Lifecycle: learn/research → explore → frame → verdict → design → translate → evaluate → implement → test → review → communicate → improve.

## Reference demo: six-bond selection

Synthetic data. Exact enumeration finds **A, C, E** (`101010`, energy −9.3725) among 64 states; the verdict is
**classical now; quantum teaching PoC only**. All five targets express the same canonical problem where they can:

| Target | Status | Observed (2026-10-13) |
|---|---|---|
| Qiskit 2.5.2 | exact; `locally-executed` | QAOA p=2 best sample `101010`, P(optimum) 0.07 |
| PennyLane 0.45.1 (`default.qubit`) | exact; `locally-executed` | best sample `101010`, P(optimum) 0.01 |
| D-Wave Ocean (dimod 0.12.22) | exact; `locally-executed` | ExactSolver optimum; SA hits it 14.5 % (penalty landscape) |
| Classiq 1.32.0 | exact objective; `imported` | model + native Qmod verified on 64 states; synthesis unverified (credentials) |
| Pasqal/Pulser 1.9.1 | six-bond **unsupported-exact** | 15 couplings vs 9 geometric DoF, ≈375 % fit error, global-only detuning; geometry-native 4-atom toy runs on the emulator |

Generated brief: [demo/bond-selection/REPORT.md](demo/bond-selection/REPORT.md). Details: [examples/](examples/).

## Develop and verify

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_package.py      # manifest, agent, skills, registry DAG, schemas, coverage, PQC fixture
python scripts/validate_math.py         # 64-state ground truth, QUBO/Ising, penalty separation
python scripts/validate_routing.py      # 17 routing cases
python scripts/validate_responses.py    # response-contract linter fixtures
python scripts/validate_examples.py     # fresh env per target from locks; --static for scans only
python scripts/verify_sources.py        # source registry; --live before releases
```

Live Copilot behaviour (needs a Copilot licence): capture the prompts in `evals/behavior/cases.yml` and run
`python scripts/run_behavior_evals.py`. Release steps: [docs/RELEASE.md](docs/RELEASE.md).

## Governance

Q-Mentor pauses for explicit approval before remote or paid execution, credentials, production or cryptographic
changes, organisation-wide deployment, or non-public data. It keeps no conversation history; lessons are opt-in,
sanitized and reviewed as pull requests. See [docs/GOVERNANCE.md](docs/GOVERNANCE.md),
[docs/IMPROVEMENT.md](docs/IMPROVEMENT.md) and the [decision log](docs/DECISIONS.md).

## Known limits

- Copilot client checks (CLI, cloud agent, IDE) are recorded as `unverified` in `registry/compatibility.yml` until run with a licence.
- Nothing is `target-validated`: no hardware, cloud simulator or credentials were used.
- Locks are for CPython 3.13 on x86_64 Linux.
- Most source entries were taken from the build kit and are marked `verification: kit` until a live check.
- Not investment advice; not a security certification.

## Layout

```text
plugin.json                      Agent Plugins 1.0.0 manifest
com.github.copilot/agents/       q-mentor custom agent
skills/                          15 SKILL.md files
registry/                        skill registry, compatibility and stale-API matrix
schemas/                         response, registry, canonical problem, ProgramIR, translation, result, capability
knowledge/ domains/finance/      small cited packs + sources.yml
templates/                       response contract and output templates
demo/bond-selection/             fixture, canonical model, expected values, result records, report
examples/                        five targets + Pulser→Classiq conversion
evals/                           routing, math, response-format, conversion, behaviour, incidents
scripts/                         validators, router, PQC inventory, deploy, report
```

MIT licensed.
