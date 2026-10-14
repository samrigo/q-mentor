"""Hardware-catalog gate (README-11): every profiled/research-only backend has a negative fixture whose reference
answer names family, model, SDK, backend and support level, passes the `mapping` template, and contains no code."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from qmentor_response import lint_text, render_text  # noqa: E402
from route_conversion import backends, capability_fields, classify  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def names_everything(text: str, b: dict) -> list:
    missing = []
    for key in ("physical_family", "model", "backend", "support_level"):
        if str(b[key]) not in text:
            missing.append(key)
    sdk = b["sdk"]["package"] or "no public SDK"
    if sdk not in text:
        missing.append("sdk")
    return missing


def recommend(n_vars: int) -> list:
    """Reference recommender: at most three tested-local candidates for a dense QUBO, plus a classical path."""
    order = ["dwave-local", "qiskit-local", "pennylane-default-qubit"]
    out = [o for o in order if backends()[o]["support_level"] == "tested-local"][:3]
    return out + ["classical: exact enumeration (n <= 25) or CP-SAT/MIP"]


def main() -> int:
    cases = yaml.safe_load((ROOT / "evals/hardware/cases.yml").read_text())["cases"]
    failures = 0
    for case in cases:
        exp = case["expect"]
        problems = []
        if case["id"] in backends():
            b = backends()[case["id"]]
            if b["support_level"] != exp["support_level"]:
                problems.append(f"support level {b['support_level']} != {exp['support_level']}")
            status = "unsupported" if b["support_level"] == "research-only" else "needs-input"
            fields = capability_fields(case["id"])
            if status == "needs-input":
                fields["Next"] = fields["Next"].rstrip(".") + "?"
                fields["Next"] = "Do you approve a credentialed, budget-capped run with the official example, or prefer a tested-local path?"
            text = render_text("mapping", fields, status, "technical")
            problems += names_everything(text, b)
            problems += lint_text(text, "mapping", "technical")
            if "```" in text:
                problems.append("code emitted")
            route = classify("qiskit-local" if b["model"] != "analog" else "pulser-local", case["id"])
            if route.may_emit_code:
                problems.append("router would emit code")
            if b["support_level"] == "research-only" and route.classification != "U":
                problems.append("research-only target not U")
            if status not in exp["status"]:
                problems.append(f"status {status} not in {exp['status']}")
        elif case["id"] == "provider-name-alone":
            hits = sorted(k for k, v in backends().items() if "Pasqal" in v["provider"])
            if not set(exp["resolves_to"]) <= set(hits) or len(hits) < 2:
                problems.append(f"provider resolves to {hits}")
        elif case["id"] == "simulator-not-qpu":
            b = backends()[exp["backend"]]
            if b["backend_kind"] != exp["backend_kind"] or "qpu" in b["backend"].lower():
                problems.append("simulator mislabelled")
        elif case["id"] == "annealer-is-not-gate":
            b = backends()[exp["backend"]]
            r = classify("qiskit-local", exp["backend"])
            if b["model"] != exp["model"] or r.classification not in ("R", "U") or r.may_emit_code:
                problems.append(f"gate->anneal route {r.classification} may_emit={r.may_emit_code}")
        elif case["id"] == "recommend-at-most-three":
            rec = recommend(20)
            quantum = [r for r in rec if not r.startswith("classical")]
            if len(quantum) > exp["max_candidates"] or not any(r.startswith("classical") for r in rec):
                problems.append(f"recommendation {rec}")
        else:
            problems.append("unknown case")
        failures += bool(problems)
        print(f"{'PASS' if not problems else 'FAIL'} {case['id']}: {problems or 'ok'}")
    families = {b["physical_family"] for b in backends().values()}
    print(f"hardware: {len(cases) - failures}/{len(cases)} passed; {len(backends())} backends across {len(families)} families")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
