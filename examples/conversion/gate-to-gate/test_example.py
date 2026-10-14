"""Gate -> gate proof fixtures: E on the bound, OpenQASM-2 subset; explicit refusals elsewhere."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter

import adapter
import canonical

EXPECTED = json.loads((Path(__file__).parent / "expected.json").read_text())
PROBLEM = canonical.load_problem()


def test_qiskit_to_pytket_unitary():
    for gamma, beta in [(0.42, 0.31), (1.1, 0.05), (2.3, 1.4)]:
        qc = adapter.qiskit_qaoa_layer(PROBLEM, gamma, beta)
        assert adapter.equal_up_to_phase(adapter.to_pytket(qc).get_unitary(), adapter.qiskit_operator_big_endian(qc))


def test_qiskit_to_cirq_unitary():
    qc = adapter.qiskit_qaoa_layer(PROBLEM, 0.42, 0.31)
    assert adapter.equal_up_to_phase(adapter.cirq_unitary(adapter.to_cirq(qc)), adapter.qiskit_operator_big_endian(qc))


def test_bit_order_is_converted_not_ignored():
    qc = QuantumCircuit(3)
    qc.x(0)
    big = adapter.qiskit_operator_big_endian(qc)
    tk = adapter.to_pytket(qc).get_unitary()
    assert np.allclose(tk, big)
    assert not np.allclose(tk, adapter.Operator(qc).data)  # little-endian operator differs


def test_cost_diagonal_matches_slice_energy():
    gamma = 0.2
    qc = adapter.qiskit_qaoa_layer(PROBLEM, gamma, 0.0)
    qc.data = [inst for inst in qc.data if inst.operation.name in ("rzz", "rz")]
    diag = np.diag(adapter.qiskit_operator_big_endian(qc))
    h, J, _ = adapter.slice_ising(PROBLEM)
    s = max(abs(v) for v in list(h.values()) + list(J.values()))
    energies = np.array(adapter.slice_energies(PROBLEM))
    phases = np.angle(diag / np.exp(-1j * gamma * energies / s))
    assert np.allclose(phases, phases[0], atol=1e-9)


def test_symbolic_parameters_must_be_bound():
    t = Parameter("t")
    qc = QuantumCircuit(1)
    qc.rx(t, 0)
    with pytest.raises(adapter.UnsupportedRoute, match="bind symbolic parameters"):
        adapter.to_pytket(qc)
    assert adapter.equal_up_to_phase(adapter.to_pytket(qc.assign_parameters({t: 0.7})).get_unitary(),
                                     adapter.qiskit_operator_big_endian(qc.assign_parameters({t: 0.7})))


def test_dynamic_circuit_rejected():
    qc = QuantumCircuit(2, 1)
    qc.h(0)
    qc.measure(0, 0)
    with qc.if_test((qc.clbits[0], 1)):
        qc.x(1)
    with pytest.raises(adapter.UnsupportedRoute, match="OpenQASM 2"):
        adapter.to_cirq(qc)


def test_implicit_swaps_need_the_qubit_maps():
    qc = QuantumCircuit(3)
    qc.cx(0, 2)
    qc.cx(1, 0)
    qc.rz(0.4, 2)
    qc.cx(2, 1)
    tk = adapter.to_pytket(qc)
    mapped, init, final = adapter.map_to_line(tk)
    u = mapped.get_unitary()
    assert not np.allclose(u, tk.get_unitary())  # naive comparison is wrong
    assert np.allclose(adapter.permutation(final, 3).T @ u @ adapter.permutation(init, 3), tk.get_unitary())


def test_unmaintained_bridge_refused():
    for pair in [("pytket", "cirq"), ("pytket", "pennylane"), ("pytket", "pyquil")]:
        with pytest.raises(adapter.UnsupportedRoute, match="unmaintained"):
            adapter.choose_bridge(*pair)
    with pytest.raises(adapter.UnsupportedRoute, match="capability report"):
        adapter.choose_bridge("qiskit", "eeroq")


def test_smoke_run():
    import main
    record = main.main()
    assert record["route_class"] == EXPECTED["route_class"]
    assert all("True" in m["evidence"] or "e-1" in m["evidence"] for m in record["mappings"])
