# Coverage matrix (implemented)

Generated from `evals/`; `scripts/run_evals.py` fails CI if any phase or target loses a positive or adversarial case. Brief: [README-08](brief/README-08-COVERAGE-MATRIX.md).

## Lifecycle

| Phase | Skill | Template | Schema | Positive evals | Adversarial evals | Stop condition |
|---|---|---|---|---|---|---|
| learn | `q-mentor-learn` | — | — | `behavior-learn-qubo`, `route-learn` | `behavior-learn-ambiguous` | Ambiguous goal or prerequisite gap |
| research | `q-mentor-research` | evidence-card.md | evidence-card.schema.json | `behavior-research-positive`, `route-research` | `behavior-research-no-sources`, `behavior-prompt-injection`, `behavior-conflicting`, `math-evidence-vendor` | No adequate or accessible source |
| explore | `q-mentor-brainstorm` | — | — | `behavior-brainstorm-classical`, `route-brainstorm` | `behavior-brainstorm-advice` | Problem too underspecified |
| frame | `q-mentor-frame` | frame.md | problem-spec.schema.json | `behavior-frame-positive`, `math-sigma-psd`, `math-penalty-separation`, `route-frame` | `behavior-prohibited-data`, `route-ambiguous` | Contradictory/missing requirements; non-public data |
| verdict | `q-mentor-verdict` | verdict.md | — (qmentor.verdict) | `behavior-demo-verdict`, `math-verdict-demo`, `route-verdict` | `behavior-csv-sort`, `incident-quantum-because-asked`, `math-verdict-csv` | No measurable advantage hypothesis |
| design | `q-mentor-design` | provider-design.md | target-plan.schema.json | `behavior-design-positive`, `route-design` | `behavior-design-no-verdict` | Cannot preserve canonical objective |
| translate | `q-mentor-translate` | provider-design.md | capability-report.schema.json | `behavior-translate-dwave`, `math-ising`, `math-equivalence-qiskit`, `math-equivalence-pennylane`, `math-equivalence-classiq`, `math-equivalence-dwave`, `math-pulser-geometry-exact`, `route-translate` | `behavior-pulser-unsupported`, `behavior-pennylane-device`, `behavior-classiq-auth`, `math-pulser-unsupported` | Target cannot represent model exactly |
| evaluate | `q-mentor-evaluate` | experiment-record.md | benchmark-record.schema.json | `behavior-evaluate-positive`, `route-evaluate` | `behavior-vendor-only` | Unfair or underpowered comparison |
| implement | `q-mentor-implement` | provider-design.md | target-plan.schema.json | `behavior-implement-positive`, `route-implement` | `behavior-version-drift`, `behavior-implement-no-design` | Dependency, permission, or mapping absent |
| test | `q-mentor-test` | experiment-record.md | result-record.schema.json | `behavior-test-positive`, `math-demo-optimum`, `route-test` | `behavior-test-flaky`, `math-tamper-detected` | Flaky, cherry-picked, irreproducible |
| review | `q-mentor-review / q-mentor-pqc-scan` | — | — (qmentor.pqc) | `behavior-pqc-mixed`, `route-review`, `route-pqc` | `behavior-review-baseline`, `behavior-pqc-false-positive`, `math-pqc-fixtures` | Material risk lacks mitigation or owner |
| communicate | `q-mentor-exec` | executive-brief.md | result-record.schema.json | `behavior-exec-positive`, `route-exec` | `behavior-advantage-claim`, `behavior-exec-incomplete`, `behavior-exec-no-records` | Results not decision-ready |
| improve | `q-mentor-improve` | conversation-lesson.md | lesson-candidate.schema.json | `behavior-improve-positive`, `route-improve` | `behavior-improve-no-consent`, `math-lesson-schema` | Consent, evidence, scope, or gain absent |

## Execution targets

| Target | Adapter | Offline path | Positive evals | Adversarial evals |
|---|---|---|---|---|
| qiskit | `qmentor/targets/qiskit_target.py` | StatevectorSampler | `behavior-translate-dwave`, `math-equivalence-qiskit` | `behavior-version-drift` |
| classiq | `qmentor/targets/classiq_target.py` | Pyomo model validation | `math-equivalence-classiq` | `behavior-classiq-auth` |
| dwave | `qmentor/targets/dwave_target.py` | dimod.ExactSolver | `behavior-translate-dwave`, `math-equivalence-dwave` | `behavior-implement-no-design` |
| pasqal-pulser | `qmentor/targets/pulser_target.py` | capability analysis | `math-pulser-geometry-exact` | `behavior-pulser-unsupported`, `behavior-design-no-verdict`, `math-pulser-unsupported` |
| pennylane | `qmentor/targets/pennylane_target.py` | default.qubit | `behavior-implement-positive`, `math-equivalence-pennylane` | `behavior-pennylane-device` |

Every row also has: version and `last_verified` metadata in `knowledge/sources.yml`, offline default with optional dependencies, and explicit approval for remote cost.
