"""Evidence cards: grade research claims; scores triage reading, they never create facts."""

from __future__ import annotations

SOURCE_STATUS = ("peer-reviewed", "preprint", "official-documentation", "vendor-result", "secondary")
REPLICATION = ("independent", "same-team-only", "attempted-and-failed", "unknown")
CRITERIA = ("source_rigor", "baseline_strength", "artifact_completeness", "scale_relevance", "replication")
EVIDENCE_LEVELS = {
    1: "formulated",
    2: "executable",
    3: "competitive-on-a-toy",
    4: "scales-experimentally",
    5: "advantage-evidence",
}


def grade(card: dict) -> dict:
    missing = [k for k in ("claim", "source", "source_status", "boundary", "baseline", "artifacts",
                           "limitations", "replication", "scores") if k not in card]
    if missing:
        raise ValueError(f"evidence card missing: {missing}")
    if card["source_status"] not in SOURCE_STATUS:
        raise ValueError(f"source_status must be one of {SOURCE_STATUS}")
    if card["replication"] not in REPLICATION:
        raise ValueError(f"replication must be one of {REPLICATION}")
    if not str(card["source"]).startswith(("http://", "https://", "doi:", "file:", "attached:")):
        raise ValueError("source must be a link, DOI, or attached file - never a remembered citation")
    for c in CRITERIA:
        v = card["scores"].get(c)
        if v not in (0, 1, 2):
            raise ValueError(f"score {c} must be 0, 1 or 2")
    total = sum(card["scores"][c] for c in CRITERIA)
    warnings = []
    if card["source_status"] == "vendor-result" and card["replication"] != "independent":
        warnings.append("vendor-only evidence: do not treat as established")
    if card["scores"]["baseline_strength"] == 0:
        warnings.append("weak or missing classical baseline: no performance conclusion")
    if card.get("evidence_level", 0) >= 5 and card["scores"]["baseline_strength"] < 2:
        warnings.append("advantage level claimed without a strong baseline: downgrade")
    return {
        "triage_score": total,
        "max_score": 10,
        "status": card.get("status", "candidate"),
        "warnings": warnings,
        "reading_priority": "high" if total >= 7 else "medium" if total >= 4 else "low",
    }
