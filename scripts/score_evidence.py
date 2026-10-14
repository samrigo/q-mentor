"""Score evidence cards (README-03): 0-2 on rigor, baseline, artifacts, scale, replication; apply claim gates.

The total triages reading; it never turns weak evidence into fact. Every card stays `candidate` until a maintainer
promotes it through q-mentor-improve. Advantage claims are rejected unless the card shows an end-to-end tuned
baseline, full artifacts, decision-scale instances, and independent replication. Component or memory papers never
support application claims. Contradictions stay visible.

  python scripts/score_evidence.py        # run evals/research/cards.yml
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
RIGOR = {"peer-reviewed": 2, "preprint": 1, "vendor-documentation": 1, "vendor-result": 0, "commentary": 0}
SCALE = {"toy": 0, "small": 1, "device": 1, "decision": 2}
REPL = {"independent": 2, "same-team": 1, "unknown": 0, "failed": 0}


def score(card: dict) -> dict:
    base = card["baseline"]
    baseline = 0 if base["kind"] in ("random-search", "none") else (2 if base["tuned"] and base["end_to_end"] else 1)
    art = card["artifacts"]
    artifacts = 2 if all(art.values()) else (1 if any(art.values()) else 0)
    scores = {"rigor": RIGOR[card["source_type"]], "baseline": baseline, "artifacts": artifacts,
              "scale": SCALE[card["scale"]], "replication": REPL[card["replication"]]}
    advantage_ok = (scores["baseline"] == 2 and artifacts == 2 and card["scale"] == "decision"
                    and card["replication"] == "independent" and scores["rigor"] == 2)
    return {
        "scores": scores,
        "total": sum(scores.values()),
        "advantage_claim": "allow" if card.get("claims_advantage") and advantage_ok else
                           ("reject" if card.get("claims_advantage") else "n/a"),
        "application_claim": "reject" if card.get("application_claim") and card["scale"] == "device" else "n/a",
        "contradiction_visible": bool(card.get("contradicted_by")) or card["replication"] == "failed",
        "status": "candidate",
    }


def main() -> int:
    cards = yaml.safe_load((ROOT / "evals/research/cards.yml").read_text())["cards"]
    sources = {e["id"] for e in yaml.safe_load((ROOT / "knowledge/sources.yml").read_text())["sources"]}
    failures = 0
    for card in cards:
        out, exp, problems = score(card), card["expect"], []
        if card.get("source_id") and card["source_id"] not in sources:
            problems.append(f"unknown source_id {card['source_id']}")
        if "max_total" in exp and out["total"] > exp["max_total"]:
            problems.append(f"total {out['total']} > {exp['max_total']}")
        if "min_total" in exp and out["total"] < exp["min_total"]:
            problems.append(f"total {out['total']} < {exp['min_total']}")
        for key in ("advantage_claim", "application_claim", "contradiction_visible", "status"):
            if key in exp and out[key] != exp[key]:
                problems.append(f"{key} {out[key]} != {exp[key]}")
        failures += bool(problems)
        print(f"{'PASS' if not problems else 'FAIL'} {card['id']}: total {out['total']} {out['scores']} {problems or ''}")
    print(f"evidence: {len(cards) - failures}/{len(cards)} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
