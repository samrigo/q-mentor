"""Reference router: the deterministic form of q-mentor-orchestrate's chaining rules.

The custom agent does the real routing in natural language. This module encodes
the same rules so routing fixtures can test the registry itself:
prerequisites only for missing artifacts, topological order, no cycles, no
duplicates, at most `max_skills_per_turn` skills, approval-free.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set

import yaml

ROOT = Path(__file__).resolve().parents[1]


class RoutingError(Exception):
    def __init__(self, status: str, message: str):
        super().__init__(message)
        self.status = status


def load_registry(path: Optional[Path] = None) -> dict:
    path = path or ROOT / "registry" / "skills.yml"
    if not path.exists():
        raise RoutingError("blocked", f"registry missing: {path}")
    with open(path, encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def index(registry: dict) -> Dict[str, dict]:
    return {s["name"]: s for s in registry["skills"]}


def plan(registry: dict, primary: str, present: Iterable[str] = (),
         follow_ons: Iterable[str] = ()) -> List[str]:
    """Return the ordered chain for a primary skill plus requested follow-ons."""
    skills = index(registry)
    have: Set[str] = set(present) | set(registry.get("user_supplied_artifacts", []))
    for name in [primary, *follow_ons]:
        if name not in skills:
            raise RoutingError("blocked", f"unknown or unavailable skill: {name}")

    chain: List[str] = []
    visiting: Set[str] = set()

    def satisfy(name: str) -> None:
        if name in chain:
            return
        if name in visiting:
            raise RoutingError("blocked", f"cycle through {name}")
        visiting.add(name)
        spec = skills[name]
        missing = [a for a in spec.get("requires", []) if a not in have]
        if missing:
            for prereq in spec.get("prerequisites", []):
                satisfy(prereq)
            still = [a for a in spec.get("requires", []) if a not in have]
            if still:
                raise RoutingError("needs-input", f"{name} requires {still}")
        any_of = spec.get("requires_any")
        if any_of and not (set(any_of) & have):
            raise RoutingError("blocked", f"{name} requires one of {any_of}")
        visiting.discard(name)
        chain.append(name)
        have.update(spec.get("produces", []))

    satisfy(primary)
    for extra in follow_ons:
        if extra in chain:
            raise RoutingError("blocked", f"duplicate execution of {extra} in one turn")
        if extra not in skills[chain[-1]].get("follow_ons", []) and not any(
                extra in skills[c].get("follow_ons", []) for c in chain):
            raise RoutingError("blocked", f"{extra} is not a declared follow-on of {chain}")
        satisfy(extra)
    if len(chain) > registry["max_skills_per_turn"]:
        raise RoutingError("checkpoint", f"chain of {len(chain)} exceeds {registry['max_skills_per_turn']}: {chain}")
    return chain


if __name__ == "__main__":
    reg = load_registry()
    print(plan(reg, sys.argv[1], sys.argv[2].split(",") if len(sys.argv) > 2 and sys.argv[2] else [],
               sys.argv[3].split(",") if len(sys.argv) > 3 else []))
