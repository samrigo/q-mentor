# Decision log

Assumptions made while building from the brief, recorded instead of silently invented.

| # | Decision | Why | Revisit when |
|---|---|---|---|
| 1 | Plugin root = repository root; `plugin.json` uses the Agent Plugins **1.0.0** schema URL | Brief targets 1.0; Copilot CLI docs (checked 2026-10-12) accept 1.0.0 and 1.1.0 | A 1.1-only feature is needed |
| 2 | Agent tools: `read, search, edit, execute, web`; skills do not pre-approve tools | One agent hosts all skills; `implement`/`test` need edit/execute. The agent text restricts edit/execute to those skills after approval; Copilot then prompts per tool use | Clients support per-skill least-privilege tool lists |
| 3 | Skill descriptions are YAML double-quoted | Several contain `: `, which is invalid in plain YAML scalars | Never |
| 4 | Canonical QUBO stores a **full symmetric** Q (pairs counted twice); bit order variable 0 leftmost; Ising x = (1 - s)/2 | Matches the brief's demo convention and Pauli-Z on gate targets | Never without a migration and evals |
| 5 | Classiq offline adapter = Pyomo model evaluated on all states; no `classiq` SDK dependency | Synthesis needs authentication; the brief allows "model validation or mocked adapter" | A credential-free Classiq validation path exists |
| 6 | Classiq receives the **penalised** objective, not native constraints | Prevents Classiq choosing its own penalty and silently changing the objective | Constraint-native comparison is wanted (then re-run equivalence) |
| 7 | Pulser exactness = positive couplings + classical-MDS geometry test (rank <= device dimension) + local-detuning check + dynamic range | Deterministic and physically grounded; avoids optimiser-dependent "fits" | Pulser adds programmable couplings |
| 8 | Verdict cap: classical comparison = 0 -> `classical-now` regardless of total | The brief's demo must score classical now while being a well-formed problem; "no reason classical is insufficient" is the decisive fact | Weighting is recalibrated with real eval data |
| 9 | Simulated-annealing baseline uses flip + swap moves | Single flips get trapped by the cardinality penalty; the brief requires comparable tuning effort | Larger fixtures need tabu/MIP |
| 10 | Repo-local deployment puts shared files under `.github/q-mentor/` and rewrites skill links | Keeps `.github/` tidy and links valid without symlinks | Copilot supports skill-relative resource folders |
| 11 | Behavioral evals graded from captured responses with structural assertions | No model in CI; golden prose is brittle | A Copilot eval harness is available |
| 12 | PQC helper is a regex inventory with confidence levels and comment downgrades | Inventory-only by design; false positives handled by confidence and owner review | A maintained crypto-inventory tool is approved |
| 13 | QAOA tests assert seed reproducibility and decoding, not solution quality | Statistical quality is reported with intervals, never retried until it passes | Larger statistical suites are funded |
