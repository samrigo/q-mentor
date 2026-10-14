# Decision log

Choices made while building 3.1.1 from the v3.1.1 build kit (`brief/`), on top of v2.0.0 (`Claude-v2`).

| # | Decision | Why | Alternative rejected |
|---|---|---|---|
| D1 | Agent Plugins schema 1.0.0 | Oldest schema covering the needed fields; Copilot CLI 1.0.97 installs it | 1.1.0 |
| D2 | Branch `Claude-v3` of `samrigo/q-mentor`, plugin name `q-mentor` | Same pattern as `Claude-v2`; `main` untouched | New repository |
| D3 | Templates are data (frontmatter in `templates/responses/*.md`), one linter for text, JSON and code-only | README-13 table becomes testable; no second copy of field orders | Prose-only template advice |
| D4 | Template matrix evals render realistic answers per skill × status × audience × mode | Deterministic proof every skill's template works in every mode; live model behaviour is a separate, recorded `not-run` suite | Golden prose |
| D5 | Help menu rendered only from `registry/skills.yml` (`scripts/render_help.py`) | README-09: no second menu; a new skill appears automatically (tested) | Hand-written menu |
| D6 | Router treats only `present` artifacts as available; `requires_any` can trigger prerequisites | v2 counted every user-suppliable artifact as present | Implicit artifacts |
| D7 | 37 backend records; `backend_kind` separates simulators/emulators from QPUs | README-11 forbids inferring QPU support from a simulator | Provider-level records |
| D8 | Nine `tested-local` targets exactly as README-11; Alice & Bob, SpinQit, Qristal stay `profiled` | No pinned clean build was produced for them in 3.1.1 | Promoting on import alone |
| D9 | Six-bond on Bloqade = `unsupported-exact`, on Perceval = `conditional-impractical`; each ships a native program instead | Measured: 375 % coupling-fit error; 1.8e-34 success | Approximations labelled equivalent |
| D10 | Bloqade pins numpy 2.2.6 | Observed run-time failure with numpy 2.5.4 | Import-only gate |
| D11 | perceval-interop: bridge-matched qiskit 2.1.2 and a submodule import workaround with a test that detects the upstream fix | Declared `qiskit~=2.1.2`; package import defect without `myqlm` | Installing myqlm only to import the package |
| D12 | Pulser→Classiq regression uses the official Classiq QAOA structure (SHA 9e5b7bed) and a local reference simulator of the identical ansatz | Classiq synthesis needs credentials; semantics are tested offline, execution marked unverified | Claiming Classiq-side numbers |
| D13 | Optimization decision rule: primary metric's 95 % interval must clear the baseline's, within a two-qubit cap | README-10 "improved only on a predeclared metric"; honest `not-improved` | Best mean wins |
| D14 | pytket compilation keeps the cheaper of two verified pass sequences | FullPeepholeOptimise doubled two-qubit gates here | Assuming a pass optimizes |
| D15 | Source registry keeps `not-checked` when a publisher blocks or rate-limits | README-12: a 403 is not a broken DOI | Marking unread links verified |
| D16 | No hooks, MCP, SDK app, telemetry | Kit MVP scope; strict response hook stays a deferred, opt-in extension | — |
