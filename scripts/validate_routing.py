"""Run routing fixtures against the registry with the reference router."""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from route import RoutingError, load_registry, plan  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    registry = load_registry()
    cases = yaml.safe_load((ROOT / "evals" / "routing" / "cases.yml").read_text())["cases"]
    failures = 0
    exercised = set()
    for case in cases:
        try:
            chain = plan(registry, case["primary"], case.get("present", []), case.get("follow_ons", []))
            status = "complete"
        except RoutingError as err:
            chain, status = None, err.status
        ok = status == case["expect"]["status"] and (
            "chain" not in case["expect"] or chain == case["expect"]["chain"])
        if chain:
            exercised.update(zip(chain, chain[1:]))
        print(f"{'PASS' if ok else 'FAIL'} {case['id']}: status={status} chain={chain}")
        failures += not ok
    print(f"{len(cases) - failures}/{len(cases)} routing cases passed; {len(exercised)} handoff edges exercised")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
