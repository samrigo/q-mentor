# Changelog

All notable changes follow [Keep a Changelog](https://keepachangelog.com/) and semantic versioning. Behavior changes must reference the eval that motivated them.

## [0.1.0] - 2026-10-12

### Added
- Agent Plugins 1.0 manifest, `q-mentor` Copilot agent (router), and 14 skills covering the full lifecycle.
- Knowledge packs (quantum basics, optimization math, quantum fit, research method, Qiskit, Classiq, D-Wave, Pasqal/Pulser, PennyLane, PQC) with a source registry.
- Finance domain pack and six-bond synthetic demo with exact baseline, penalty-separation proof, seeded heuristic, and executive brief generated from result records.
- Target adapters with all-state energy equivalence (Qiskit, PennyLane, Classiq model, D-Wave) and a Pasqal/Pulser capability gate that returns `unsupported-exact` with alternatives.
- JSON Schemas for ProblemSpec, CanonicalQUBO, TargetPlan, CapabilityReport, ResultRecord, BenchmarkRecord, EvidenceCard, LessonCandidate, EvalCase.
- Evals: routing (15), behavior (34), math (16, run offline), incidents (1 seeded); coverage enforced per lifecycle phase and target.
- `validate_package.py`, `validate_math.py`, `run_evals.py`, `deploy_repo_local.py` (dry-run, selective packs, no-overwrite, manifest, remove), offline CI.

### Known limits
- Behavioral and routing evals require captured Copilot responses; not yet run against every supported client.
- Classiq synthesis and all remote/hardware paths are intentionally not executed.
- Evidence level of the demo: competitive-on-a-toy. No advantage claim.
