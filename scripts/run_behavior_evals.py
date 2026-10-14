"""Score captured live Copilot answers against evals/behavior/cases.yml (qmentor.response.v3).

Capture answers first (one file per case id: <id>.md; <id>.json for machine mode; <id>.code.md for code-only),
for example by running each prompt through Copilot CLI with the q-mentor agent and saving the final message. Then:

  python scripts/run_behavior_evals.py --responses evals/behavior/responses
  python scripts/run_behavior_evals.py --check-cases     # offline: cases reference real skills and templates

Every answer is linted against the template registered for the expected terminal skill. Missing answers are
reported as `not-run`, never as passes. Median output words are reported to track cost drift.
"""
from __future__ import annotations

import argparse
import re
import statistics
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from qmentor_response import lint, registry_templates  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def load_cases() -> list:
    return yaml.safe_load((ROOT / "evals" / "behavior" / "cases.yml").read_text())["cases"]


def check(case: dict, path: Path) -> list:
    exp = case["expect"]
    text = path.read_text(encoding="utf-8")
    template = registry_templates()[case["skill"]]
    mode = exp.get("lint") or ("machine" if path.suffix == ".json" else "code-only" if path.name.endswith(".code.md")
                               else "brief")
    problems = [f"lint:{p}" for p in lint(text, template, exp.get("audience", "technical"), mode)]
    if "status" in exp:
        m = re.search(r'Status:\s*([a-z-]+)|"status":\s*"([a-z-]+)"|status=([a-z-]+)', text)
        got = next((g for g in (m.groups() if m else ()) if g), None)
        if got not in exp["status"]:
            problems.append(f"status {got} not in {exp['status']}")
    for pattern in exp.get("must_match", []):
        if not re.search(pattern, text):
            problems.append(f"missing /{pattern}/")
    for pattern in exp.get("must_not_match", []):
        if re.search(pattern, text):
            problems.append(f"forbidden /{pattern}/")
    if "max_words" in exp and len(text.split()) > exp["max_words"]:
        problems.append(f"over {exp['max_words']} words")
    if exp.get("verdict") == "classical-now" and not re.search(r"(?i)classical now", text):
        problems.append("verdict is not classical now")
    return problems


def check_cases(cases: list) -> int:
    reg = registry_templates()
    bad = 0
    for case in cases:
        if case["skill"] not in reg or not reg[case["skill"]]:
            print(f"FAIL case {case['id']}: unknown or internal terminal skill {case['skill']}")
            bad += 1
    covered = {c["skill"] for c in cases}
    missing = sorted(s for s, t in reg.items() if t and s not in covered)
    if missing:
        print(f"FAIL behaviour cases do not cover: {missing}")
        bad += 1
    print(f"behaviour cases: {len(cases)} cases over {len(covered)} skills" + ("" if not bad else f"; {bad} problem(s)"))
    return bad


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--responses", default=str(ROOT / "evals" / "behavior" / "responses"))
    parser.add_argument("--check-cases", action="store_true")
    args = parser.parse_args()
    cases = load_cases()
    if args.check_cases:
        return 1 if check_cases(cases) else 0
    folder = Path(args.responses)
    passed = failed = missing = 0
    words = []
    for case in cases:
        candidates = [folder / f"{case['id']}.md", folder / f"{case['id']}.json", folder / f"{case['id']}.code.md"]
        path = next((p for p in candidates if p.exists()), None)
        if path is None:
            print(f"NOT-RUN {case['id']}")
            missing += 1
            continue
        words.append(len(path.read_text(encoding="utf-8").split()))
        problems = check(case, path)
        print(f"{'PASS' if not problems else 'FAIL'} {case['id']}: {problems or 'ok'}")
        passed += not problems
        failed += bool(problems)
    median = statistics.median(words) if words else 0
    print(f"behaviour: {passed} passed, {failed} failed, {missing} not run; median answer {median} words")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
