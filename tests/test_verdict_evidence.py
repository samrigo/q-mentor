import pytest

from qmentor.evidence import grade
from qmentor.verdict import score

DEMO_DIMS = {"problem_structure": 0.6, "formulation_quality": 0.9, "classical_comparison": 0.0,
             "input_output_fit": 0.5, "resource_fit": 0.6, "evidence": 0.2}


def test_demo_verdict_is_classical_now(expected):
    v = score(DEMO_DIMS, {})
    assert v["verdict"] == expected["expected_verdict"] == "classical-now"
    assert v["teaching_poc_ok"] and not v["advantage_claimed"]


def test_sorting_csv_is_classical_now():
    v = score({"problem_structure": 0.0, "formulation_quality": 0.2, "classical_comparison": 0.0,
               "input_output_fit": 0.0, "resource_fit": 0.0, "evidence": 0.0}, {})
    assert v["verdict"] == "classical-now" and not v["teaching_poc_ok"]


def test_hard_gate_blocks_fit_now():
    dims = {k: 1.0 for k in DEMO_DIMS}
    assert score(dims, {})["verdict"] == "candidate-experiment"
    assert score(dims, {"no_resource_estimate": True})["verdict"] == "research-or-teaching-poc"
    assert score(dims, {"prohibited_data": True})["verdict"] == "stop-prohibited-data"


def test_unknown_dimension_rejected():
    with pytest.raises(ValueError):
        score({"vibes": 1.0}, {})


CARD = {"claim": "QAOA matched optimum on 12-asset toy", "source": "https://arxiv.org/abs/0000.00000",
        "source_status": "vendor-result", "boundary": "12 assets, simulator", "baseline": "random search",
        "artifacts": "none", "limitations": "toy", "replication": "unknown",
        "scores": {"source_rigor": 1, "baseline_strength": 0, "artifact_completeness": 0,
                   "scale_relevance": 0, "replication": 0}}


def test_vendor_weak_baseline_card_warned():
    g = grade(CARD)
    assert g["status"] == "candidate" and g["reading_priority"] == "low"
    assert len(g["warnings"]) == 2


def test_remembered_citation_rejected():
    with pytest.raises(ValueError, match="never a remembered citation"):
        grade({**CARD, "source": "Smith et al. 2023"})
