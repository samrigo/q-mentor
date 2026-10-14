"""Reference conversion router (README-14) and hardware capability reports (README-11).

classify(source, target) takes backend ids from registry/backends.yml (or bare computing models) and returns
the README-14 route: candidate class from the model matrix, the shipped edge if one exists, whether code may
be emitted, and why. Profiled and research-only targets never get executable code; an unlisted pair needs a
capability report before code.

  python scripts/route_conversion.py pulser-local classiq-local
  python scripts/route_conversion.py qiskit-local eeroq
"""
from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import List, Optional

import yaml

ROOT = Path(__file__).resolve().parents[1]
MODEL_OF = {"gate": "gate", "analog": "rydberg-analog", "anneal": "anneal", "photonic-DV": "photonic-DV",
            "photonic-CV": "photonic-CV", "simulator": "gate"}
CLASS_WORD = {"E": "exact", "C": "conditional", "R": "reimplementation", "A": "approximate", "U": "unsupported"}


@lru_cache(maxsize=None)
def backends() -> dict:
    data = yaml.safe_load((ROOT / "registry/backends.yml").read_text())
    return {b["id"]: b for b in data["backends"]}


@lru_cache(maxsize=None)
def edges() -> dict:
    return yaml.safe_load((ROOT / "registry/conversion-edges.yml").read_text())


def model_of(ref: str) -> str:
    if ref in backends():
        b = backends()[ref]
        if b["support_level"] == "research-only":
            return "research-only"
        return MODEL_OF[b["model"]]
    if ref in edges()["model_matrix"]:
        return ref
    raise KeyError(f"unknown backend or model: {ref}")


@dataclass
class Route:
    source: str
    target: str
    source_model: str
    target_model: str
    candidate: str
    edge: Optional[str]
    classification: str
    class_word: str
    may_emit_code: bool
    reasons: List[str] = field(default_factory=list)


def classify(source: str, target: str) -> Route:
    sm, tm = model_of(source), model_of(target)
    candidate = edges()["model_matrix"][sm][tm]
    tb = backends().get(target)
    sb = backends().get(source)
    reasons: List[str] = []
    edge = None
    for e in edges()["edges"]:
        if e["source"]["model"] == sm and e["target"]["model"] == tm and (
                (sb is None or e["source"]["sdk"].split()[0] in (sb["sdk"]["package"] or "")) and
                (tb is None or e["target"]["sdk"].split()[0] in (tb["sdk"]["package"] or ""))):
            edge = e
            break
    cls = edge["classification"] if edge else candidate.split(" or ")[0] if candidate != "U" else "U"
    may_emit = bool(edge) and edge["classification"] != "U"
    if tb and tb["support_level"] == "research-only":
        cls, may_emit = "U", False
        reasons.append(f"{target} is research-only: no public, versioned, executable contract")
    elif tb and tb["support_level"] == "profiled":
        may_emit = False
        reasons.append(f"{target} is profiled: capability record only; point to a versioned official example")
    if not edge and cls != "U":
        reasons.append(f"no shipped edge for {sm} -> {tm}; candidate {candidate} needs a capability report and proof fixture first")
    if edge:
        reasons.append(f"shipped edge {edge['id']} ({edge['maintained_bridge']['name']}, {edge['maintained_bridge']['status']})")
        if edge["maintained_bridge"]["status"] in ("unmaintained", "archived"):
            may_emit = False
            reasons.append("bridge is unmaintained/archived: never a default route")
    return Route(source, target, sm, tm, candidate, edge["id"] if edge else None, cls, CLASS_WORD[cls], may_emit,
                 reasons)


def capability_fields(backend_id: str, source: str = "qiskit-local") -> dict:
    """Reference `mapping` answer fields for a request to run on backend_id (README-11 capability report)."""
    b = backends()[backend_id]
    route = classify(source, backend_id) if source else None
    sdk = f"{b['sdk']['package']} {b['sdk']['version']}" if b["sdk"]["package"] else "no public SDK"
    name = f"{b['physical_family']} / {b['model']} / {sdk} / {b['backend']} / {b['support_level']}"
    lvl = b["support_level"]
    word = route.class_word if route else "unsupported"
    if lvl == "research-only":
        route_text = f"Request -> {b['provider']} ({name}): unsupported for executable code."
        lost = "Everything executable: no public, versioned programming route exists; only a capability report is given."
        nxt = "Learn the gate logic on a tested-local simulator (Qiskit or Cirq) and revisit when a public SDK exists."
    elif lvl == "profiled":
        route_text = f"Request -> {b['provider']} ({name}): {word} in principle, but no tested local adapter here."
        lost = f"Runnable code: {b['local_validation']}; access: {b['queue_cost_boundary']}."
        nxt = f"Approve a credentialed, budget-capped run with the official example ({b['source_url']}), or use a tested-local path."
    else:
        route_text = f"Request -> {b['provider']} ({name}): {word}."
        lost = f"Hardware behaviour beyond the {b['backend_kind']}: noise {b['noise']}."
        nxt = f"Run `{b['example']}` locally with `python scripts/validate_examples.py --only {b['example'].split('examples/')[1]}`."
    return {"Route": route_text,
            "Preserved": f"Capability record: native ops {b['native_ops']}; connectivity {b['connectivity']}; measurement {b['measurement']}.",
            "Lost / limited": lost, "Next": nxt}


if __name__ == "__main__":
    r = classify(sys.argv[1], sys.argv[2])
    print(json.dumps(asdict(r), indent=2))
