"""Routing gate: registry-intent selection, chain fixtures, and a sweep over every declared handoff edge."""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from route import RoutingError, load_registry, plan, select_primary  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def edge_sweep(registry: dict) -> tuple[int, list]:
    """Every (skill -> follow_on) edge must route as [skill, follow_on] when all artifacts exist."""
    everything = {a for s in registry["skills"] for a in s["produces"]} | set(registry["user_supplied_artifacts"]) \
        | {"ConsentRecord"}
    failures, count = [], 0
    for spec in registry["skills"]:
        if not spec["user_invocable"]:
            continue
        for follow in spec["follow_ons"]:
            count += 1
            try:
                chain = plan(registry, spec["name"], everything, [follow])
                if chain != [spec["name"], follow]:
                    failures.append(f"{spec['name']} -> {follow}: chain {chain}")
            except RoutingError as exc:
                failures.append(f"{spec['name']} -> {follow}: {exc.status} {exc}")
    return count, failures


def main() -> int:
    registry = load_registry()
    cases = yaml.safe_load((ROOT / "evals" / "routing" / "cases.yml").read_text())["cases"]
    failures = 0
    exercised = set()
    for case in cases:
        exp = case["expect"]
        if "select" in exp:
            got = select_primary(registry, case["prompt"])
            ok = got == exp["select"]
            print(f"{'PASS' if ok else 'FAIL'} {case['id']}: selected {got}")
            failures += not ok
            continue
        try:
            chain = plan(registry, case["primary"], case.get("present", []), case.get("follow_ons", []))
            status = "complete"
        except RoutingError as err:
            chain, status = None, err.status
        ok = status == exp["status"] and ("chain" not in exp or chain == exp["chain"])
        if chain:
            exercised.update(zip(chain, chain[1:]))
        print(f"{'PASS' if ok else 'FAIL'} {case['id']}: status={status} chain={chain}")
        failures += not ok
    count, sweep_failures = edge_sweep(registry)
    for f in sweep_failures:
        print("FAIL edge", f)
    print(f"{len(cases) - failures}/{len(cases)} routing cases passed; {len(exercised)} edges in fixtures; "
          f"{count - len(sweep_failures)}/{count} declared handoff edges route cleanly")
    return 1 if failures or sweep_failures else 0


if __name__ == "__main__":
    sys.exit(main())
