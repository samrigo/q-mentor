"""Response-contract gate for qmentor.response.v3 (README-13).

1. Template matrix (evals/response-format/answers.yml): every user-facing skill has answers in the statuses that
   apply to it, in business and technical audiences; each is rendered brief/detailed/machine (and code-only for
   code/conversion templates) and linted against the template the registry assigns to that skill.
2. Fixtures (evals/response-format/cases.yml): negative and edge texts must return exactly the expected problems.

Usage:
  python scripts/validate_responses.py
  python scripts/validate_responses.py FILE --skill q-mentor-verdict [--audience business] [--mode brief]
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from qmentor_response import (STATUSES, lint, lint_code_only, lint_machine, lint_text, registry_templates,  # noqa: E402
                              render_code_only, render_machine, render_text)

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_STATUS = {"complete"}  # every skill; plus at least one non-complete status
MIN_NON_COMPLETE = 1


def matrix() -> int:
    cases = yaml.safe_load((ROOT / "evals/response-format/answers.yml").read_text())["cases"]
    reg = registry_templates()
    failures = 0
    coverage = defaultdict(lambda: {"status": set(), "audience": set()})
    for case in cases:
        skill = case["skill"]
        tid = reg.get(skill)
        if not tid:
            print(f"FAIL {case['id']}: {skill} has no template in the registry")
            failures += 1
            continue
        if case["skills_used"][-1] != skill:
            print(f"FAIL {case['id']}: terminal skill must be {skill}")
            failures += 1
        coverage[skill]["status"].add(case["status"])
        coverage[skill]["audience"].add(case["audience"])
        renders = {
            f"brief/{case['audience']}": (render_text(tid, case["fields"], case["status"], case["audience"]),
                                         lambda t: lint_text(t, tid, case["audience"], "brief")),
            "detailed/technical": (render_text(tid, case["fields"], case["status"], "technical", "detailed"),
                                   lambda t: lint_text(t, tid, "technical", "detailed")),
        }
        machine = render_machine(tid, case["fields"], case["status"], audience=case["audience"],
                                 skills_used=case["skills_used"], validation_state=case["validation_state"],
                                 next_action=case.get("next_action"))
        renders["machine"] = (json.dumps(machine), lambda t: lint_machine(t, tid))
        if tid in ("code", "conversion") and case["audience"] == "technical":
            files = machine["artifacts"] or ["none"]
            checks = case["fields"].get("Checks") or case["fields"].get("Validation")
            code = {"example.py": ("python", "import json\n\nprint(json.dumps({'status': 'ok'}))")} \
                if case["status"] == "complete" else {}
            renders["code-only"] = (render_code_only(tid, case["status"], files, checks, machine["next_action"], code),
                                    lambda t: lint_code_only(t, tid))
        for mode, (text, check) in renders.items():
            problems = check(text)
            if problems:
                failures += 1
                print(f"FAIL {case['id']} [{mode}]: {problems}")
    for name, tid in reg.items():
        if not tid:
            continue
        cov = coverage.get(name)
        if not cov:
            print(f"FAIL coverage: {name} has no template answers")
            failures += 1
            continue
        missing = []
        if "complete" not in cov["status"]:
            missing.append("complete")
        if len(cov["status"] - {"complete"}) < MIN_NON_COMPLETE:
            missing.append("a needs-input/blocked/unsupported/unverified answer")
        if name not in ("q-mentor-exec", "q-mentor-improve") and cov["audience"] != {"business", "technical"}:
            missing.append("both audiences")
        if missing:
            failures += 1
            print(f"FAIL coverage: {name} lacks {', '.join(missing)}")
    statuses = set().union(*(c["status"] for c in coverage.values()))
    if statuses != set(STATUSES):
        failures += 1
        print(f"FAIL coverage: statuses exercised {sorted(statuses)}")
    print(f"matrix: {len(cases)} answers x modes over {len(coverage)} skills; "
          f"{'all passed' if not failures else f'{failures} failure(s)'}")
    return failures


def fixtures() -> int:
    cases = yaml.safe_load((ROOT / "evals/response-format/cases.yml").read_text())["cases"]
    failures = 0
    for case in cases:
        got = lint(case["text"], case["template"], case.get("audience", "technical"), case.get("mode", "brief"))
        ok = sorted(got) == sorted(case["expect"])
        failures += not ok
        print(f"{'PASS' if ok else 'FAIL'} {case['id']}: {got}" + ("" if ok else f" (expected {case['expect']})"))
    print(f"fixtures: {len(cases) - failures}/{len(cases)} passed")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?")
    parser.add_argument("--skill")
    parser.add_argument("--audience", default="technical")
    parser.add_argument("--mode", default="brief")
    args = parser.parse_args()
    if args.file:
        tid = registry_templates()[args.skill]
        problems = lint(Path(args.file).read_text(encoding="utf-8"), tid, args.audience, args.mode)
        print("OK" if not problems else " ".join(problems))
        return 1 if problems else 0
    failures = matrix() + fixtures()
    print("responses: OK" if not failures else f"responses: {failures} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
