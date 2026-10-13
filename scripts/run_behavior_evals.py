"""Score captured live Copilot answers against evals/behavior/cases.yml.

Capture answers first (one file per case id: <id>.md, or <id>.json for machine mode),
for example by running each prompt through Copilot CLI with the q-mentor agent and
saving the final message. Then:

  python scripts/run_behavior_evals.py --responses evals/behavior/responses

Missing answers are reported as `not-run`, never as passes.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_responses import lint  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def check(case: dict, path: Path) -> list:
    exp = case["expect"]
    text = path.read_text(encoding="utf-8")
    problems = []
    mode = exp.get("lint", "machine" if path.suffix == ".json" else "brief")
    if exp.get("lint") or "status" in exp:
        problems += [f"lint:{p}" for p in lint(path, mode)]
    if "status" in exp and mode != "machine":
        m = re.match(r"Status: (\S+)", text.strip())
        if not m or m.group(1) not in exp["status"]:
            problems.append(f"status not in {exp['status']}")
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--responses", default=str(ROOT / "evals" / "behavior" / "responses"))
    args = parser.parse_args()
    folder = Path(args.responses)
    cases = yaml.safe_load((ROOT / "evals" / "behavior" / "cases.yml").read_text())["cases"]
    passed = failed = missing = 0
    for case in cases:
        candidates = [folder / f"{case['id']}.md", folder / f"{case['id']}.json"]
        path = next((p for p in candidates if p.exists()), None)
        if path is None:
            print(f"NOT-RUN {case['id']}")
            missing += 1
            continue
        problems = check(case, path)
        print(f"{'PASS' if not problems else 'FAIL'} {case['id']}: {problems or 'ok'}")
        passed += not problems
        failed += bool(problems)
    print(f"behaviour: {passed} passed, {failed} failed, {missing} not run")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
