# Q-Mentor for GitHub Copilot

[![quality](https://github.com/samrigo/q-mentor/actions/workflows/quality.yml/badge.svg?branch=Claude-v3)](https://github.com/samrigo/q-mentor/actions/workflows/quality.yml?query=branch%3AClaude-v3)

An honest, vendor-neutral quantum-computing guide inside GitHub Copilot. It teaches, researches, screens problems,
designs, converts code across hardware families, implements, tests, reviews, and **always names the strongest
classical alternative**. "Classical now" is a first-class answer.

- **Version:** 3.1.1, built from the Q-Mentor Copilot build kit v3.1.1 (kept verbatim in [`brief/`](brief/)).
- **Package:** Agent Plugins `1.0.0` manifest, one Copilot custom agent, 17 lazily loaded skills, a small registry.
- **No runtime:** no web service, database, MCP server, telemetry, credentials, or paid quantum job by default.
- **Observed:** Copilot CLI 1.0.97 installs it and discovers all 17 skills (plugin and repository mode).

## Install

```bash
git clone -b Claude-v3 https://github.com/samrigo/q-mentor.git
copilot plugin install ./q-mentor
```

Then ask "What can Q-Mentor do?" or just describe the outcome you want. Repository-local deployment for the cloud
agent, Copilot app, or IDE agent mode, plus update, rollback, and removal: [docs/INSTALL.md](docs/INSTALL.md).

## Use it

| Ask | What happens |
|---|---|
| "What can Q-Mentor do?" | `help` renders the menu from `registry/skills.yml` (no second, hand-kept menu) |
| "Should we use quantum to pick 3 of these 6 bonds?" | frame → verdict: **classical now**, with score, hard gates, revisit trigger |
| "Run the six-bond QUBO on Pasqal." | capability report: **unsupported-exact** (geometry), with alternatives |
| "Convert this Pulser program to Classiq and tell me if it got better." | translate → convert: **reimplementation**, verified cost on all states, fixed-budget p=1/2/4 comparison → **not improved** |
| "Port my Qiskit circuit to Perceval." | **conditional**: exact postselected distribution *and* the unconditional success rate |
| "Write code for an electron-on-helium computer." | **unsupported**: research-only, capability report, no fictional code |
| "Inventory post-quantum risk in this repo." | public-key findings vs symmetric/hash notes, routed to a security owner |

Every answer uses its skill's mandatory `qmentor.response.v3` template: the answer first, then `Status`, then fixed
fields (for a decision: Why, Cost / risk, Next gate). Business answers avoid jargon; technical answers keep the same
fields and link artifacts; `machine` mode is JSON; `code-only` is code plus a manifest. Requested code is never cut.

## What is inside

| Path | Contents |
|---|---|
| `skills/` (17) | `SKILL.md` per skill; each cites its one response template |
| `com.github.copilot/agents/` | the `q-mentor` custom agent (thin orchestrator) |
| `registry/` | `skills.yml` (routing + help), `backends.yml` (37 backends, 12 families, support levels), `conversion-edges.yml` (README-14 classes), `compatibility.yml` |
| `templates/responses/` | the 12 response templates as data |
| `schemas/` | response, registry, canonical problem, ProgramIR, translation, conversion edge, optimization and result records, backend capability |
| `knowledge/`, `domains/finance/` | curated packs (< 1,000 tokens each) and the source registry with link-check results |
| `examples/bond-selection/` | nine `tested-local` targets: Qiskit, Cirq, pytket, PennyLane, Classiq, D-Wave, Pulser, Bloqade, Perceval |
| `examples/conversion/` | gate↔gate, gate→photonic, analog↔analog, BQM→QAOA, and the Pulser→Classiq optimization regression |
| `evals/` | routing, response-format, hardware, conversion, research, behaviour (live), incidents |
| `scripts/` | deterministic gates, help renderer, routers, linter, deployment |

## Quality gates

```bash
python scripts/validate_package.py      # manifest, skills, templates, registries, schemas, help, coverage, pins
python scripts/validate_math.py         # six-bond: 64 states, optimum 101010 at -9.3725, gap 0.2050
python scripts/validate_routing.py      # intent selection, chains, cycles, every handoff edge
python scripts/validate_responses.py    # every skill x status x audience x mode, plus negative fixtures
python scripts/validate_hardware.py     # support levels; no code for profiled or research-only targets
python scripts/validate_examples.py     # every example in a fresh environment from its lock
python scripts/verify_sources.py        # source registry; --live re-checks DOIs, arXiv, repositories
```

Results on 2026-10-14 and what remains unverified (live Copilot behaviour evals, Classiq synthesis, remote
providers): [docs/COMPATIBILITY.md](docs/COMPATIBILITY.md), [CHANGELOG.md](CHANGELOG.md). Design choices:
[docs/DECISIONS.md](docs/DECISIONS.md). Build plan: [docs/IMPLEMENTATION-PLAN.md](docs/IMPLEMENTATION-PLAN.md).

## Boundaries

Not an investment adviser, scientific authority, security scanner of record, or compute broker. Public or synthetic
data only. Remote, paid, credentialed, cryptographic, or production actions need explicit approval. Matching a toy
optimum is not quantum advantage. MIT licence.
