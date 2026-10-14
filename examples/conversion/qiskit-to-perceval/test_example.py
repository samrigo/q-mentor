"""Gate -> photonic DV proof fixtures (class C)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

import adapter
import canonical

EXPECTED = json.loads((Path(__file__).parent / "expected.json").read_text())
PROBLEM = canonical.load_problem()


def test_conditional_distribution_and_success_rate():
    for gamma, beta in adapter.angles_grid():
        qc = adapter.qaoa_circuit(PROBLEM, gamma, beta)
        photonic, success, res = adapter.photonic_distribution(qc)
        assert adapter.tvd(adapter.gate_distribution(qc), photonic) < 1e-9
        assert success == pytest.approx(EXPECTED["success"]["qaoa_two_cnots_same_pair"], rel=1e-6)
        assert res["cnots"] == 2


def test_success_shrinks_with_each_postselected_gate():
    _, s2, _ = adapter.photonic_distribution(adapter.ghz_circuit(2))
    _, s3, _ = adapter.photonic_distribution(adapter.ghz_circuit(3))
    assert s2 == pytest.approx(1 / 9, rel=1e-6)
    assert s3 == pytest.approx(1 / 81, rel=1e-6)


def test_postselected_fidelity_not_reported_as_deterministic():
    import main
    record = main.main()
    assert adapter.validate_claim(record) == []
    assert adapter.validate_claim({**record, "route_class": "E"})
    bad = dict(record)
    bad.pop("unconditional_success_probability")
    assert adapter.validate_claim(bad)


def test_decode_rejects_non_logical_states():
    import perceval as pcvl
    assert adapter.decode(pcvl.BasicState([0, 1, 1, 0])) == "10"
    with pytest.raises(ValueError):
        adapter.decode(pcvl.BasicState([0, 2, 0, 0]))


def test_upstream_import_defect_documented():
    """perceval-interop 1.3.0: package import fails without the myqlm extra. When this test fails, upstream fixed
    it: drop the workaround in adapter.load_converter and this test."""
    import subprocess
    import sys
    proc = subprocess.run([sys.executable, "-c", "import perceval_interop"], capture_output=True, text=True)
    assert proc.returncode != 0 and "MyQLMCommunicationLayer" in proc.stderr
