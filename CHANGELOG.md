# Changelog

## 3.1.1 — 2026-10-14 (branch `Claude-v3`)

Built from the v3.1.1 build kit (`brief/`). Highlights:

- **Skills:** 17 (new `q-mentor-help`, `q-mentor-convert`); each user-facing skill has exactly one mandatory
  `qmentor.response.v3` template, cited in its `SKILL.md`.
- **Response contract:** 12 templates as data, a renderer/linter for text, machine JSON and code-only answers,
  56 template answers × 4 modes plus 31 negative fixtures.
- **Routing:** registry-intent selection, 37 routing fixtures, all 46 declared handoff edges exercised; help menu
  derived from the registry.
- **Hardware:** 37 backend records across 12 physical families (9 tested-local, 18 profiled, 10 research-only),
  each non-local record with a negative fixture.
- **Targets:** Cirq, pytket, Bloqade, Perceval added; all nine six-bond targets pass in clean environments.
- **Conversion:** README-14 atlas, 12 conversion edges (E, C, R, U) with proof and negative fixtures; gate↔gate,
  gate→photonic, analog↔analog, BQM→QAOA, and the Pasqal/Pulser→Classiq optimization regression
  (result: **not-improved** at a fixed budget).
- **Sources:** every brief link registered; 29 papers re-read, 34 repository HEADs and tag SHAs recorded; corrections
  found that the brief lacks.
- **Compatibility:** Copilot CLI 1.0.97 plugin and repository-mode discovery observed; deployment lifecycle
  (install, conflict, update with backup, rollback, removal) tested.

Not verified in this build: agent invocation and behaviour evals in a licensed Copilot session; Classiq synthesis and
execution; live remote providers; `gh skill publish --dry-run` (not available in gh 2.89.0).

## 2.0.0 — 2026-10-13 (branch `Claude-v2`)

Initial Copilot plugin from the v2 build kit: 15 skills, five targets, six-bond demo, Pulser→Classiq walk-through.
