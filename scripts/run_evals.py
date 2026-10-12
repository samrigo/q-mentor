#!/usr/bin/env python3
"""Validate and run Q-Mentor evals.

    python scripts/run_evals.py                      # validate all cases, run math suite offline
    python scripts/run_evals.py --responses DIR      # also grade captured responses (DIR/<id>.md)

Behavioral and routing cases need a model, so they are graded from captured
responses: run each prompt in Copilot with the plugin installed, save the
answer as DIR/<id>.md, and put "skill: <name>" on the first line for routing
cases. Assertions are structural (fields, claims, length), not golden prose.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

PHASES = ["learn", "research", "explore", "frame", "verdict", "design", "translate",
          "evaluate", "implement", "test", "review", "communicate", "improve"]
TARGETS = ["qiskit", "classiq", "dwave", "pasqal-pulser", "pennylane"]


def load_cases() -> list[dict]:
    cases = []
    for f in sorted((ROOT / "evals").glob("*/*.yml")):
        for c in yaml.safe_load(f.read_text()) or []:
            c["_file"] = str(f.relative_to(ROOT))
            cases.append(c)
    return cases


def validate_cases(cases: list[dict]) -> list[str]:
    errors = []
    try:
        import jsonschema
    except ImportError:
        jsonschema = None
    schema = json.loads((ROOT / "schemas" / "eval-case.schema.json").read_text())
    seen = set()
    for c in cases:
        body = {k: v for k, v in c.items() if not k.startswith("_")}
        if jsonschema:
            for e in jsonschema.Draft202012Validator(schema).iter_errors(body):
                errors.append(f"{c.get('id')}: {e.message}")
        if c["id"] in seen:
            errors.append(f"duplicate eval id {c['id']}")
        seen.add(c["id"])
        for a in c.get("attachments", []):
            if not (ROOT / a).exists():
                errors.append(f"{c['id']}: missing attachment {a}")
        skill = c.get("expect", {}).get("skill")
        if skill and not (ROOT / "skills" / skill / "SKILL.md").exists():
            errors.append(f"{c['id']}: unknown skill {skill}")
    # Coverage: every lifecycle phase and target has a positive and an adversarial case.
    for phase in PHASES:
        kinds = {c["kind"] for c in cases if c.get("lifecycle") == phase}
        for k in ("positive", "adversarial"):
            if k not in kinds:
                errors.append(f"coverage: phase '{phase}' has no {k} eval")
    for t in TARGETS:
        kinds = {c["kind"] for c in cases if t in c.get("targets", [])}
        for k in ("positive", "adversarial"):
            if k not in kinds:
                errors.append(f"coverage: target '{t}' has no {k} eval")
    routed = {c["expect"].get("skill") for c in cases if c["suite"] == "routing"}
    for d in (ROOT / "skills").iterdir():
        if d.is_dir() and d.name not in routed:
            errors.append(f"coverage: skill {d.name} has no routing eval")
    return errors


# ---------------------------------------------------------------- math checks

def _ctx():
    from qmentor.canonical import build_mean_variance_qubo, load_problem
    spec = load_problem(ROOT / "demo" / "bond-selection" / "problem.json")
    expected = json.loads((ROOT / "demo" / "bond-selection" / "expected.json").read_text())
    return spec, build_mean_variance_qubo(spec), expected


def run_check(name: str) -> tuple[bool, str]:
    import numpy as np
    from qmentor import baseline, canonical, evidence, pqc, verdict
    from qmentor.targets import TargetUnavailable, check_equivalence, pulser_target
    spec, q, exp = _ctx()
    if name == "sigma-psd":
        S = np.asarray(spec["objective"]["risk_matrix"])
        ok = np.allclose(S, S.T) and np.linalg.eigvalsh(S).min() > 0
        return ok, f"min eigenvalue {np.linalg.eigvalsh(S).min():.4f}"
    if name == "demo-optimum":
        r = baseline.enumerate_exact(q, spec)
        ok = r["unique_optimum"] and r["best"]["bits"] == exp["optimum"]["bits"] and \
            abs(r["best"]["energy"] - exp["optimum"]["energy"]) < 1e-9
        return ok, f"{r['best']['bits']} {r['best']['energy']:.4f}"
    if name == "penalty-separation":
        s = baseline.penalty_separation(q, spec)
        return s["separates"], f"margin {s['margin']:.4f}"
    if name == "ising-conversion":
        ising = canonical.qubo_to_ising(q)
        worst = max(abs(ising.energy(canonical.x_to_s(x)) - q.energy(x)) for x in canonical.all_assignments(q.n))
        return worst < 1e-9, f"max diff {worst:.2e}"
    if name.startswith("equivalence:"):
        import importlib
        mod = importlib.import_module(f"qmentor.targets.{name.split(':')[1]}_target")
        try:
            eq = check_equivalence(q, mod.energy_table(q))
        except TargetUnavailable as exc:
            return None, f"SKIPPED: {exc}"
        return eq["equivalent"] and mod.capability(q)["status"] == "exact", f"{eq['states_checked']} states, max diff {eq['max_abs_diff']:.2e}"
    if name == "pulser-unsupported":
        rep = pulser_target.capability(q)
        return rep["status"] == "unsupported-exact" and bool(rep["alternatives"]), "; ".join(rep["failures"])
    if name == "pulser-geometry-exact":
        pos = np.array([[0.0, 0.0], [7.0, 0.0], [3.5, 6.0], [10.0, 6.0]])
        rep = pulser_target.capability(pulser_target.qubo_from_positions(pos))
        return rep["status"] == "exact", rep["status"]
    if name == "tamper-detected":
        from qmentor.targets import dwave_target
        try:
            table = dwave_target.energy_table(q)
        except TargetUnavailable:
            table = {canonical.bits_to_str(x): q.energy(x) for x in canonical.all_assignments(q.n)}
        table["101010"] += 0.5
        return not check_equivalence(q, table)["equivalent"], "tampered table rejected"
    if name == "verdict-demo":
        v = verdict.score({"problem_structure": 0.6, "formulation_quality": 0.9, "classical_comparison": 0.0,
                           "input_output_fit": 0.5, "resource_fit": 0.6, "evidence": 0.2}, {})
        return v["verdict"] == exp["expected_verdict"], v["verdict"]
    if name == "verdict-csv":
        v = verdict.score({k: 0.0 for k in verdict.WEIGHTS}, {})
        return v["verdict"] == "classical-now", v["verdict"]
    if name == "evidence-vendor":
        g = evidence.grade({"claim": "1000x faster rebalancing", "source": "attached:vendor-claim.md",
                            "source_status": "vendor-result", "boundary": "unknown", "baseline": "none",
                            "artifacts": "none", "limitations": "no size", "replication": "unknown",
                            "scores": {"source_rigor": 0, "baseline_strength": 0, "artifact_completeness": 0,
                                       "scale_relevance": 0, "replication": 0}})
        return len(g["warnings"]) == 2 and g["status"] == "candidate", "; ".join(g["warnings"])
    if name == "pqc-fixtures":
        fx = ROOT / "tests" / "fixtures" / "pqc"
        pk = {f["category"] for f in pqc.scan_paths([str(fx / "rsa_ecdh.py")])["findings"]}
        sym = {f["category"] for f in pqc.scan_paths([str(fx / "aes_sha.py")])["findings"]}
        fp = pqc.scan_paths([str(fx / "false_positive.py")])["findings"]
        ok = {"public-key:rsa", "public-key:ecc"} <= pk and sym == {"symmetric", "hash"} and not fp
        return ok, f"pk={sorted(pk)} sym={sorted(sym)} false_positives={len(fp)}"
    if name == "lesson-schema":
        import jsonschema
        schema = json.loads((ROOT / "schemas" / "lesson-candidate.schema.json").read_text())
        good = json.loads((ROOT / "evals" / "incidents" / "2026-10-11-seed-quantum-because-asked.lesson.json").read_text())
        v = jsonschema.Draft202012Validator(schema)
        bad1 = {**good, "consent": {"explicit_opt_in": False, "user_reviewed": True}}
        bad2 = {**good, "contains_transcript": True}
        ok = v.is_valid(good) and not v.is_valid(bad1) and not v.is_valid(bad2)
        return ok, "consent and transcript rules enforced"
    return False, f"unknown check {name}"


# ------------------------------------------------------------ response grading

def grade_response(case: dict, text: str) -> list[str]:
    exp = case.get("expect", {})
    low = text.lower()
    fails = []
    first = text.strip().splitlines()[0].lower() if text.strip() else ""
    if exp.get("skill") and case["suite"] == "routing":
        m = re.match(r"skill:\s*(\S+)", first)
        if not m or m.group(1) != exp["skill"]:
            fails.append(f"routed to {m.group(1) if m else 'nothing'}, expected {exp['skill']}")
    for s in exp.get("must_include", []):
        if s.lower() not in low:
            fails.append(f"missing '{s}'")
    for group in exp.get("must_include_any", []):
        if not any(s.lower() in low for s in group):
            fails.append(f"missing any of {group}")
    for s in exp.get("must_not_include", []):
        if s.lower() in low:
            fails.append(f"forbidden '{s}'")
    for s in exp.get("forbidden_actions", []):
        if re.search(rf"(ran|executed|running|submitted|calling)\s+[^.\n]*{re.escape(s.lower())}", low):
            fails.append(f"forbidden action '{s}'")
    if exp.get("verdict") and exp["verdict"] not in low:
        fails.append(f"verdict '{exp['verdict']}' not stated")
    if exp.get("capability_status") and exp["capability_status"] not in low:
        fails.append(f"capability status '{exp['capability_status']}' not stated")
    if exp.get("max_words"):
        body = "\n".join(text.splitlines()[1:]) if first.startswith("skill:") else text
        n = len(re.findall(r"\S+", body))
        if n > exp["max_words"]:
            fails.append(f"{n} words > {exp['max_words']}")
    return fails


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--responses", help="directory of captured responses named <eval-id>.md")
    ap.add_argument("--suite", choices=["routing", "behavior", "math", "incidents"])
    args = ap.parse_args()

    cases = load_cases()
    errors = validate_cases(cases)
    for e in errors:
        print(f"INVALID  {e}")
    status = 1 if errors else 0
    print(f"validated {len(cases)} eval cases" + (" (with errors)" if errors else ""))

    for c in cases:
        if args.suite and c["suite"] != args.suite:
            continue
        if c["suite"] == "math":
            ok, detail = run_check(c["check"])
            tag = "SKIP" if ok is None else "PASS" if ok else "FAIL"
            print(f"{tag:5}  {c['id']}: {detail}")
            if ok is False:
                status = 1
        elif args.responses:
            f = Path(args.responses) / f"{c['id']}.md"
            if not f.exists():
                print(f"MISS   {c['id']}: no captured response")
                continue
            fails = grade_response(c, f.read_text())
            print(f"{'FAIL' if fails else 'PASS':5}  {c['id']}" + (": " + "; ".join(fails) if fails else ""))
            if fails:
                status = 1
    return status


if __name__ == "__main__":
    sys.exit(main())
