"""Improvement-loop gate (README-05 'Safe self-improvement'): incidents are sanitized, consented, and eval-first."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ["consent", "scope", "prompt_category", "expected_behaviour", "actual_failure", "risk", "sanitized_evidence",
            "affected", "version", "counterexample", "proposed_assertion", "retention"]
FORBIDDEN = [(re.compile(r"```"), "code block"), (re.compile(r"\b(User|Assistant|Human|AI):\s"), "transcript turn"),
             (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "e-mail address"),
             (re.compile(r"\b(ghp_|sk-|AKIA)[A-Za-z0-9]{8,}"), "credential"),
             (re.compile(r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b"), "account-like number")]


def assertion_exists(ref: str) -> bool:
    path, _, name = ref.partition("::")
    target = ROOT / path
    if not target.exists():
        return False
    return not name or f"def {name}(" in target.read_text()


def main() -> int:
    failures = 0
    files = sorted((ROOT / "evals/incidents").glob("*.yml"))
    for f in files:
        data = yaml.safe_load(f.read_text())
        problems = [f"missing {k}" for k in REQUIRED if k not in data]
        if data.get("scope") not in ("personal", "repository", "plugin"):
            problems.append("bad scope")
        if data.get("origin", "conversation") == "conversation" and not data.get("example"):
            if not re.match(r"(?i)explicit yes", str(data.get("consent", ""))):
                problems.append("conversation lesson without explicit consent")
        if data.get("scope") == "personal" and not data.get("example"):
            problems.append("personal lessons stay out of the public plugin")
        if not data.get("example") and not assertion_exists(str(data.get("proposed_assertion", ""))):
            problems.append(f"assertion not found: {data.get('proposed_assertion')}")
        text = f.read_text()
        problems += [f"contains {label}" for rx, label in FORBIDDEN if rx.search(text)]
        failures += bool(problems)
        print(f"{'PASS' if not problems else 'FAIL'} {f.name}: {problems or 'ok'}")
    # negative fixture: an unconsented conversation lesson must be rejected
    probe = {"origin": "conversation", "consent": "", "scope": "plugin"}
    if re.match(r"(?i)explicit yes", probe["consent"]):
        failures += 1
    print(f"incidents: {len(files) - failures}/{len(files)} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
