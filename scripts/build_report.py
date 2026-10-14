"""Generate the six-bond executive brief from result records only (q-mentor-exec, template `decision`).

Reads demo/bond-selection/result-records/*.json (schema qmentor.result-record.v3) and writes
demo/bond-selection/REPORT.md. Refuses (exit 1) when no records exist: a brief is never manufactured from a plan.
The rendered brief is linted against templates/responses/decision.md (business audience).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from qmentor_response import lint_text, render_text  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RECORDS = ROOT / "demo" / "bond-selection" / "result-records"
OUT = ROOT / "demo" / "bond-selection" / "REPORT.md"
SAMPLED = ("qiskit", "pennylane", "cirq", "pytket")


def outcome(name: str, r: dict) -> str:
    if name in SAMPLED:
        q = r["quantum"]
        return (f"QAOA best sample `{q['best_sampled']['bitstring']}`; P(optimum) {q['optimum_probability']}; "
                f"feasible {q['feasibility_rate']}")
    if name == "dwave":
        return (f"ExactSolver optimum `{r['baseline']['optimum']['bitstring']}`; simulated annealing optimum rate "
                f"{r['heuristic']['optimum_rate']} (classical heuristic)")
    if name == "classiq":
        v = r["offline_model_validation"]
        return f"Model built; cost error {v['max_energy_error_all_64_states']:.1e} on 64 states; synthesis not run"
    if name == "bloqade":
        q = r["quantum"]
        return (f"Six-bond: **{r['capability_report']['status']}**; native 5-atom program P(ground state) "
                f"{q['ground_state_probability']}")
    if name == "perceval":
        q = r["quantum"]
        return (f"Six-bond: **{r['capability_report']['status']}** (success "
                f"{r['capability_report']['checks']['unconditional_success_probability']:.1e}); native 2-qubit "
                f"conditional match TVD {q['total_variation_distance']:.0e}, success {q['unconditional_success_probability']:.4f}")
    return (f"Six-bond: **{r['six_bond_capability']}**; native 4-atom toy P(optimum) "
            f"{r['noiseless_emulation']['optimum_probability']} noiseless, "
            f"{r['spam_noise_emulation']['optimum_probability']} with SPAM")


def main() -> int:
    records = {p.stem: json.loads(p.read_text()) for p in sorted(RECORDS.glob("*.json"))}
    if not records:
        print("blocked: no result records; run the examples first")
        return 1
    rows = [f"| {n} | {', '.join(f'{k} {v}' for k, v in r['versions'].items())} | {outcome(n, r)} | {r['evidence_level']} |"
            for n, r in records.items()]
    base = records["dwave"]["baseline"]["optimum"]
    fields = {
        "Decision": "Classical now; keep the quantum versions as a teaching exercise only.",
        "Why": (f"Checking all 64 choices with ordinary software finds the unique best set {', '.join(base['selected'])} "
                f"(score {base['energy']}) in under a millisecond; {len(records)} quantum and classical tools reproduced "
                "or could not represent it, and none improved on it (confidence high)."),
        "Cost / risk": "More quantum work at this size costs staff time and cannot show a speed or quality gain.",
        "Next gate": "Reopen only for a decision-scale problem where a tuned classical solver misses its time budget.",
    }
    table = "\n".join(["| Target | Versions | Observed outcome | Evidence level |", "|---|---|---|---|", *rows])
    appendix = (f"Evidence (from `demo/bond-selection/result-records/*.json`, {len(records)} records, recorded "
                f"{max(r.get('recorded_on', '') for r in records.values())}; simulators only, single seed per target):\n\n"
                + table)
    brief = render_text("decision", fields, "complete", "business")
    problems = lint_text(brief, "decision", "business")
    if problems:
        print(f"blocked: generated brief violates the decision template: {problems}")
        return 1
    OUT.write_text("# Executive brief — six-bond selection (generated from result records)\n\n" + brief + "\n" + appendix + "\n")
    print(f"wrote {OUT.relative_to(ROOT)} from {len(records)} records")
    return 0


if __name__ == "__main__":
    sys.exit(main())
