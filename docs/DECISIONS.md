# Decision log

Assumptions and choices made while building v2.0.0 from the build kit, instead of silently inventing requirements.

| # | Decision | Why | Alternative rejected |
|---|---|---|---|
| D1 | Agent Plugins schema 1.0.0 | Kit default; Copilot CLI recognises 1.0.0 and 1.1.0; no 1.1 feature needed | 1.1.0 |
| D2 | Plugin `name: q-mentor`, published on branch `Claude-v2` of `samrigo/q-mentor` | Successor to the earlier `q-mentor` plugin; slash commands keep their names | New plugin name |
| D3 | Shared rules live in `templates/response-contract.md`; skills link it | Skills can be invoked without the agent and still need the rules; avoids repeating 12 rules × 15 | Duplicating rules in every skill |
| D4 | Skill `allowed-tools` use custom-agent aliases (`read`, `search`, `edit`, `web`) | Unknown names are ignored, so nothing is over-approved; no shell pre-approval | Pre-approving `shell` for test |
| D5 | Deterministic reference router (`scripts/route.py`) mirrors orchestrator rules | Lets routing evals test the registry offline; live routing is checked by behaviour evals | Only live evals |
| D6 | Six-bond on Pulser = `unsupported-exact`; a geometry-native 4-atom QUBO is the supported Pulser example | 15 couplings vs 9 geometric DoF; best-fit error ≈ 375 %; AnalogDevice is global-only | Shipping a fitted approximation as if equivalent |
| D7 | Pulser → Classiq = `reimplementation` of the shared QUBO; analog schedule `unsupported-exact` | Kit forbids line-by-line conversion; QAOA is a different algorithm | Generic QAOA labelled "converted" |
| D8 | Classiq validated to `imported` only | `create_model`/`write_qmod` run offline; synthesis needs credentials | Claiming synthesis passed |
| D9 | `write_qmod(symbolic_only=False)` | The default omitted helper functions from the native file (observed) | Default export |
| D10 | `QutipBackendV2` + `n_trajectories` | `QutipEmulator` and `NoiseModel(runs=...)` emit deprecation warnings in pulser 1.9.1 | Deprecated APIs |
| D11 | `qaoa_ansatz` function | `QAOAAnsatz` class path emits deprecation warnings in qiskit 2.5.2 | Deprecated class |
| D12 | Locks for CPython 3.13 / x86_64 Linux via `uv pip compile` | Environment available at build time; other platforms re-lock | Unpinned ranges |
| D13 | No hooks, MCP, SDK app, telemetry | Kit MVP scope; strict response hook deferred (opt-in later) | — |
| D14 | Source entries from the kit marked `verification: kit` until live-checked | Live fetches were not possible for every URL during the build | Marking all as verified |
