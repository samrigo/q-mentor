# Changelog

## 2.0.0 — 2026-10-13

First release built from the Q-Mentor Copilot build kit v2.0.0.

### Added
- Agent Plugins 1.0.0 package: `plugin.json`, `com.github.copilot/agents/q-mentor.agent.md`, 15 skills.
- Skill registry with prerequisites, follow-ons, side effects and pack links; deterministic reference router.
- `qmentor.response.v2` contract (brief, detailed, machine) with a linter and fixtures.
- Schemas: response, skill registry, canonical problem, ProgramIR, translation record, result record, capability report.
- Knowledge packs (11) with a source registry; finance domain pack.
- Six-bond demo with exact ground truth, result records and a generated executive brief.
- Complete offline examples for Qiskit, PennyLane, D-Wave Ocean, Classiq, Pasqal/Pulser, plus a Pulser→Classiq conversion through ProgramIR.
- Evals: routing (17), math (4), response format (12), conversion (9), behaviour (18 live prompts), PQC fixtures.
- Repository-local deployment with dry run, conflict refusal, checksum manifest and uninstall.
- CI workflow with SHA-pinned actions and per-target fresh environments.

### Known limitations
- Copilot client discovery and live behaviour evals not yet run (`unverified`).
- Classiq synthesis and any remote/hardware path not run (`unverified`).
- Pasqal/Pulser cannot represent the six-bond QUBO exactly (`unsupported-exact`).
