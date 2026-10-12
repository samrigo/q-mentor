# Q-Mentor

**An honest, vendor-neutral quantum-computing guide inside GitHub Copilot.** Q-Mentor teaches concepts, researches evidence, screens problems, designs and implements experiments, tests results, and always names the strongest classical alternative. Finance is the first domain pack and reference demo, not a limit on the core.

It is an [Agent Plugins 1.0](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json) skill pack: one Copilot custom agent, fourteen lazily loaded skills, small cited knowledge packs, and deterministic checks. No hosted service, database, MCP server, telemetry, or paid quantum job.

> Q-Mentor is a guide and engineering assistant, not an autonomous decision system, financial adviser, vulnerability scanner, or quantum-compute broker.

## Skills

| Skill | Job | Default output |
|---|---|---|
| `/q-mentor-learn` | Explain one concept with analogy, formula, misconception, source | <= 300 words |
| `/q-mentor-research` | Evidence cards from primary sources; contradictions and gaps | 1 evidence table |
| `/q-mentor-brainstorm` | At most five use cases ranked by readiness | 1 table |
| `/q-mentor-frame` | Business problem -> variables, objective, constraints, success measures | <= 600 words |
| `/q-mentor-verdict` | Classical now / research PoC / bounded experiment / candidate | <= 450 words |
| `/q-mentor-design` | Target-neutral design and starter implementation plan | <= 800 words |
| `/q-mentor-translate` | Canonical problem -> targets, with a capability report first | 1 comparison table |
| `/q-mentor-evaluate` | Scorecard: evidence, baseline, resources, reproducibility, cost | 1 scorecard |
| `/q-mentor-implement` | Smallest approved change, version pins, rollback | Scoped diff |
| `/q-mentor-test` | Deterministic, equivalence, statistical, noise tests | Test report |
| `/q-mentor-review` | Math, code, hardware fit, claims, simpler alternatives | Findings only |
| `/q-mentor-pqc-scan` | Inventory quantum-vulnerable cryptography | Findings only |
| `/q-mentor-exec` | One-page leadership brief from result records | 1 page |
| `/q-mentor-improve` | Failure or opted-in lesson -> eval-first PR plan | 1 PR plan |

Lifecycle: **learn/research -> explore -> frame -> verdict -> design -> translate -> evaluate -> implement -> test -> review -> communicate -> improve**. Enter at any phase; prerequisites are enforced (`implement` needs a design, `exec` needs result records, `improve` needs a failure, approved lesson, or changed source).

## Install

### Copilot CLI (plugin)

```bash
copilot plugin marketplace add samrigo/q-mentor          # registers marketplace "samrigo-q-mentor"
copilot plugin install q-mentor@samrigo-q-mentor
copilot plugin list                                       # confirm q-mentor is installed
```

Direct install also works (`copilot plugin install samrigo/q-mentor`), but Copilot CLI marks direct installs as deprecated in favor of `plugin@marketplace`. Verified with Copilot CLI 1.0.95: the plugin installs with 14 skills and the `q-mentor` agent.

Then use the `q-mentor` agent or call a skill directly, e.g. `/q-mentor-verdict Should we use quantum for ...`.

### Repository-local (Copilot agent mode in supported IDEs, cloud agent)

```bash
git clone https://github.com/samrigo/q-mentor
python q-mentor/scripts/deploy_repo_local.py /path/to/your-repo --dry-run
python q-mentor/scripts/deploy_repo_local.py /path/to/your-repo \
    --domains finance --targets qiskit,pennylane,dwave,classiq,pasqal-pulser
```

This copies skills to `.github/skills/`, the agent to `.github/agents/`, and the knowledge, domain, template, and schema files to `.github/q-mentor/`, then writes `.github/q-mentor/MANIFEST.json`. It never symlinks, never overwrites a file you changed (use `--force` only after review), and installs only the target packs you select.

### Remove

```bash
copilot plugin uninstall q-mentor                                  # CLI plugin (add @samrigo-q-mentor if installed from the marketplace)
python q-mentor/scripts/deploy_repo_local.py /path/to/your-repo --remove   # repo-local; keeps files you edited
```

## Run the checks and the demo (offline)

```bash
pip install -e ".[dev]"                  # core: numpy + PyYAML (+ pytest, jsonschema)
pip install -e ".[dev,all-targets]"      # optional: Qiskit, PennyLane, dimod, Pyomo, pulser-core
python scripts/validate_package.py       # manifest, agent, skills, packs, sources, schemas, secret scan
python scripts/run_evals.py              # eval schema + lifecycle/target coverage + math suite
python -m pytest -m "not slow"           # fast tests; drop the marker to include local QAOA runs
python -m qmentor.demo                   # six-bond demo -> results/result-record.json + executive-brief.md
```

The [six-bond demo](demo/bond-selection/README.md) reproduces the unique optimum A, C, E (`101010`, energy -9.3725), shows that Qiskit, PennyLane, Classiq (Pyomo model), and D-Wave encodings match the canonical energy on all 64 assignments, and shows Pasqal/Pulser refusing an exact mapping with a precise reason. Verdict: **classical now; teaching PoC only.**

Provider SDKs are optional extras with lazy imports. Missing SDKs produce explicit skips, never silent passes. Tested versions are in [`requirements-lock.txt`](requirements-lock.txt).

## Execution targets

| Target | Role | Offline path | Capability gate |
|---|---|---|---|
| Qiskit | Gate-model SDK | `StatevectorSampler` (seeded) | Operator order, Ising constants, little-endian decode |
| Classiq | High-level modeling and synthesis | Pyomo model validation (no authentication) | Objective preserved; synthesis choices recorded when approved |
| D-Wave Ocean | BQM/CQM, annealing, hybrid | `dimod.ExactSolver` | Pair-bias counting, spin-sign flip, embedding and chains on QPU |
| Pasqal/Pulser | Neutral-atom pulse/analog | Capability analysis, then emulation if exact | Positive couplings, geometry (MDS rank), local detuning, dynamic range |
| PennyLane | Differentiable framework (not a provider) | `default.qubit` | Named device, interface, diff method, optimizer, shots, seed |

## Limits

- Toy models are didactic. Real portfolios add prices, lots, liquidity, turnover, taxes, limits, scenarios, and estimation error.
- Simulator results say nothing about hardware noise, queue time, or cost. Matching a toy optimum is **not** quantum advantage.
- Behavioral evals need a model: they are graded from captured Copilot responses (see [evals/README.md](evals/README.md)). The deterministic suites run in CI.
- SDK APIs, Copilot packaging, and pricing change. Every pack carries `last_verified`; re-check [sources](knowledge/sources.yml) before release.

## Research updates and conversation learning

- New research becomes a **candidate** evidence card via `/q-mentor-research`; a maintainer compares, adds contradiction and replication status, adds evals, and only then promotes a compact claim into a pack.
- Q-Mentor does not retrain itself or remember chats. At the end of a material workflow it may ask once whether to save a **sanitized lesson** (no transcript, no code, no client data). Silence means no; you see and edit the candidate before any file write. `/q-mentor-improve` turns it into a failing eval first, then a human-reviewed pull request.

Details: [docs/IMPROVEMENT.md](docs/IMPROVEMENT.md).

## Governance

Public or synthetic data only. Explicit approval is required before remote provider execution, paid usage, credentials, production or cryptographic changes, organization-wide deployment, or non-public data. If your organization has not approved Copilot custom agents/plugins for the data class, stop and route to your AI-governance and security owners. See [docs/GOVERNANCE.md](docs/GOVERNANCE.md).

## Repository map

```text
plugin.json                         Agent Plugins 1.0 manifest
com.github.copilot/agents/          q-mentor.agent.md (thin router)
skills/<name>/SKILL.md              14 skills (lazy, <=120 lines, <=3 packs each)
knowledge/                          small cited packs + sources.yml
domains/finance/                    first domain pack
templates/  schemas/                durable output formats and JSON Schemas
demo/bond-selection/                problem, expected optimum, runner output
qmentor/                            deterministic helpers (canonical math, baselines, targets, verdict, evidence, PQC)
evals/                              routing, behavior, math, incidents
scripts/                            validate_package, validate_math, run_evals, deploy_repo_local
docs/                               coverage, decisions, governance, improvement, original build brief
```

Built from the construction brief in [docs/brief/](docs/brief/README.md). License: MIT.
