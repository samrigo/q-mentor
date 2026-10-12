"""Quantum-readiness verdict: six weighted dimensions, hard gates applied first."""

from __future__ import annotations

WEIGHTS = {
    "problem_structure": 25,
    "formulation_quality": 20,
    "classical_comparison": 20,
    "input_output_fit": 15,
    "resource_fit": 10,
    "evidence": 10,
}

HARD_GATES = (
    "no_clear_objective",
    "no_classical_baseline",
    "no_resource_estimate",
    "prohibited_data",
    "unsupported_advantage_claim",
)

VERDICTS = (
    (0, 39, "classical-now"),
    (40, 64, "research-or-teaching-poc"),
    (65, 79, "bounded-experiment"),
    (80, 100, "candidate-experiment"),
)


def score(dimensions: dict[str, float], gates: dict[str, bool]) -> dict:
    """``dimensions`` are fractions in [0, 1] per dimension; gates True means the gate is TRIGGERED."""
    unknown = set(dimensions) - WEIGHTS.keys()
    if unknown:
        raise ValueError(f"unknown dimensions: {sorted(unknown)}")
    for k, v in dimensions.items():
        if not 0 <= v <= 1:
            raise ValueError(f"{k} must be in [0, 1]")
    unknown_gates = set(gates) - set(HARD_GATES)
    if unknown_gates:
        raise ValueError(f"unknown gates: {sorted(unknown_gates)}")

    total = round(sum(WEIGHTS[k] * dimensions.get(k, 0.0) for k in WEIGHTS))
    band = next(name for lo, hi, name in VERDICTS if lo <= total <= hi)
    triggered = sorted(k for k, v in gates.items() if v)
    verdict = band
    if triggered and band in {"bounded-experiment", "candidate-experiment"}:
        verdict = "research-or-teaching-poc"
    caps = []
    if dimensions.get("classical_comparison", 0.0) == 0.0:
        # A strong baseline exists and nothing shows it is insufficient: classical wins now.
        caps.append("classical baseline sufficient")
        verdict = "classical-now"
    if "prohibited_data" in triggered:
        verdict = "stop-prohibited-data"
    return {
        "score": total,
        "score_band": band,
        "hard_gates_triggered": triggered,
        "caps_applied": caps,
        "verdict": verdict,
        "teaching_poc_ok": verdict == "classical-now" and band != "classical-now",
        "advantage_claimed": False,
    }
