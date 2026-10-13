"""Lint answers against qmentor.response.v2.

Usage:
  python scripts/validate_responses.py                 # run evals/response-format fixtures
  python scripts/validate_responses.py FILE [--mode brief|detailed|machine]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import List

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
STATUSES = {"complete", "needs-input", "blocked", "unsupported", "unverified"}
HEADINGS = {
    "brief": ["Result", "Validation", "Next"],
    "detailed": ["Decision", "Assumptions", "Design", "Validation", "Risks", "Next"],
}
KNOWN_HEADINGS = set(sum(HEADINGS.values(), [])) | {"Summary", "Sources", "Conclusion", "Overview", "Details", "Recommendation"}
MAX_WORDS = 180
PRAISE = re.compile(r"\b(great question|excellent question|happy to help|i hope this helps|hope this helps|absolutely!|certainly!)", re.I)
NARRATION = re.compile(r"\b(let me (walk|start|first|now)|i first (read|loaded|ran)|then i (loaded|read|ran)|i will now|here's what i did)\b", re.I)
ADVANTAGE = re.compile(r"[^.]*\b(quantum advantage|quantum speed-?up|outperforms classical|faster than classical)\b[^.]*\.?", re.I)
NEGATION = re.compile(r"\b(not|no|never|without|isn't|is not|cannot|unsupported)\b", re.I)


def strip_code(text: str) -> str:
    return re.sub(r"```.*?```", " ", text, flags=re.S)


def lint_text(text: str, mode: str) -> List[str]:
    problems: List[str] = []
    lines = [ln.rstrip() for ln in text.strip().splitlines()]
    if not lines or not re.fullmatch(r"Status: (\S+)", lines[0]) or lines[0].split(": ", 1)[1] not in STATUSES:
        problems.append("praise-or-narration" if lines and (PRAISE.search(lines[0]) or NARRATION.search(lines[0])) else "status-line")
    found = [ln.lstrip("#").strip() for ln in lines[1:]
             if ln.startswith("#") or ln.strip() in KNOWN_HEADINGS]
    if found != HEADINGS[mode]:
        problems.append("heading-order")
    prose = strip_code(text)
    if PRAISE.search(prose) or NARRATION.search(prose):
        problems.append("praise-or-narration")
    words = len(re.sub(r"https?://\S+", "", prose).split())
    if mode == "brief" and words > MAX_WORDS:
        problems.append("too-long")
    sentences = [s.strip().lower() for s in re.split(r"(?<=[.!?])\s+|\n+", prose) if len(s.split()) >= 5]
    if len(sentences) != len(set(sentences)):
        problems.append("duplicate-sentence")
    for match in ADVANTAGE.finditer(prose):
        if not NEGATION.search(match.group(0)):
            problems.append("unsupported-advantage")
            break
    for block in re.findall(r"```[a-zA-Z]*\n(.*?)```", text, flags=re.S):
        if re.search(r"^\s*\.\.\.|\bTODO\b|<your[- ]", block, flags=re.M):
            problems.append("placeholder-code")
            break
    return sorted(set(problems))


def lint_json(text: str) -> List[str]:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return ["invalid-json"]
    schema = json.loads((ROOT / "schemas" / "response-v2.schema.json").read_text())
    errors = list(Draft202012Validator(schema).iter_errors(data))
    return ["schema"] if errors else []


def lint(path: Path, mode: str) -> List[str]:
    text = path.read_text(encoding="utf-8")
    return lint_json(text) if mode == "machine" else lint_text(text, mode)


def run_fixtures() -> int:
    base = ROOT / "evals" / "response-format"
    cases = yaml.safe_load((base / "cases.yml").read_text())["cases"]
    failures = 0
    for case in cases:
        problems = lint(base / case["file"], case["mode"])
        if case["expect"] == "pass":
            ok = not problems
        else:
            ok = case["reason"] in problems
        failures += not ok
        print(f"{'PASS' if ok else 'FAIL'} {case['file']}: {problems or 'clean'}")
    print(f"{len(cases) - failures}/{len(cases)} response-format cases passed")
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?")
    parser.add_argument("--mode", default="brief", choices=["brief", "detailed", "machine"])
    args = parser.parse_args()
    if not args.file:
        return run_fixtures()
    problems = lint(Path(args.file), args.mode)
    print(problems or "clean")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
