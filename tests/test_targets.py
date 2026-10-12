"""Cross-target energy equivalence on all 64 assignments (offline, no credentials)."""
import pytest

from qmentor.canonical import qubo_to_ising
from qmentor.targets import TargetUnavailable, check_equivalence
from qmentor.targets import classiq_target, dwave_target, pennylane_target, qiskit_target

EXACT_TARGETS = [qiskit_target, pennylane_target, classiq_target, dwave_target]


def table_or_skip(fn, q):
    try:
        return fn(q)
    except TargetUnavailable as exc:
        pytest.skip(str(exc))


@pytest.mark.parametrize("mod", EXACT_TARGETS, ids=lambda m: m.TARGET)
def test_exact_target_matches_canonical_energy(mod, qubo):
    assert mod.capability(qubo)["status"] == "exact"
    eq = check_equivalence(qubo, table_or_skip(mod.energy_table, qubo))
    assert eq["states_checked"] == 64
    assert eq["equivalent"], eq["mismatches"]


def test_qiskit_optimization_independent_cross_check(qubo):
    eq = check_equivalence(qubo, table_or_skip(qiskit_target.energy_table_via_qiskit_optimization, qubo))
    assert eq["equivalent"], eq["mismatches"]


def test_qiskit_decode_reverses_little_endian():
    assert qiskit_target.decode("010101") == "101010"


def test_dwave_spin_convention_is_flipped_explicitly(qubo):
    pytest.importorskip("dimod")
    ours = qubo_to_ising(qubo)
    theirs = dwave_target.to_canonical_ising(qubo)
    for i, v in enumerate(qubo.variables):
        assert theirs["h"][v] == pytest.approx(ours.h[i])
    assert theirs["offset"] == pytest.approx(ours.offset)


def test_pennylane_names_its_device(qubo):
    cap = pennylane_target.capability(qubo)
    assert cap["device"] == "default.qubit"
    assert "not a hardware provider" in cap["role"]


def test_classiq_never_authenticates_offline():
    assert classiq_target.plan()["authenticate_called"] is False


def test_tampered_target_fails_equivalence(qubo):
    table = table_or_skip(dwave_target.energy_table, qubo)
    table["101010"] += 0.5  # silently changed problem
    assert not check_equivalence(qubo, table)["equivalent"]


@pytest.mark.slow
@pytest.mark.parametrize("mod", [qiskit_target, pennylane_target], ids=lambda m: m.TARGET)
def test_local_qaoa_is_seed_reproducible_and_decodes(mod, qubo):
    try:
        a = mod.run_qaoa_local(qubo, shots=512)
    except TargetUnavailable as exc:
        pytest.skip(str(exc))
    b = mod.run_qaoa_local(qubo, shots=512)
    assert a["samples"] == b["samples"]
    assert all(len(k) == 6 and set(k) <= {"0", "1"} for k in a["samples"])
    assert sum(a["samples"].values()) == 512
    assert a["seed"] == 7 and a["versions"]
