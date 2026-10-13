"""Conversion gates: objective preserved on all 16 states; optimum and bit order preserved."""
import json
from pathlib import Path

import adapter

HERE = Path(__file__).parent
EXPECTED = json.loads((HERE / "expected.json").read_text())


def test_reimplementation_preserves_objective_and_optimum():
    import main
    record = main.main()
    assert record["max_energy_error_all_states"] < EXPECTED["tolerances"]["energy_abs"]
    assert record["exact_optimum"]["bitstring"] == EXPECTED["optimum_bitstring"]
    assert abs(record["exact_optimum"]["energy"] - EXPECTED["optimum_energy"]) < 1e-6


def test_translation_record_labels_analog_part_unsupported():
    record = json.loads((HERE.parent / "translation_record.json").read_text())
    statuses = {m["source_semantic"]: m["status"] for m in record["mappings"]}
    assert statuses["analog adiabatic evolution Omega(t), delta(t)"] == "unsupported-exact"
    assert record["overall_status"] == "reimplementation"
    assert "equivalent" not in record["overall_status"]
