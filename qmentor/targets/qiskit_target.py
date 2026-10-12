"""Qiskit gate-model target (local simulator only by default).

Bit-order note: Qiskit is little-endian. Qubit i holds canonical variable i,
and Qiskit prints qubit 0 as the RIGHTMOST character of a measured bitstring,
so decoding reverses the string. Tested in tests/test_targets.py.
"""

from __future__ import annotations

import numpy as np

from ..canonical import CanonicalQUBO, bits_to_str, qubo_to_ising
from . import require

TARGET = "qiskit"


def capability(q: CanonicalQUBO) -> dict:
    return {
        "target": TARGET,
        "role": "gate-model SDK",
        "status": "exact",
        "mapping": "QUBO -> Ising -> SparsePauliOp (Z and ZZ terms), x=(1-s)/2",
        "requires": ["n qubits = n variables", "ZZ couplings for every nonzero J_ij"],
        "lost_semantics": [],
        "resources": {"logical_qubits": q.n, "zz_terms": int(np.count_nonzero(qubo_to_ising(q).J))},
        "offline_path": "qiskit.primitives.StatevectorSampler (seeded)",
        "remote_execution": "not performed; requires explicit approval, credentials, and cost estimate",
    }


def to_operator(q: CanonicalQUBO):
    """Return (SparsePauliOp, offset). Pauli labels are little-endian in Qiskit."""
    qi = require("qiskit.quantum_info")
    ising = qubo_to_ising(q)
    terms = []
    for i in range(q.n):
        if ising.h[i]:
            terms.append(("Z", [i], ising.h[i]))
    for i in range(q.n):
        for j in range(i + 1, q.n):
            if ising.J[i, j]:
                terms.append(("ZZ", [i, j], ising.J[i, j]))
    op = qi.SparsePauliOp.from_sparse_list(terms, num_qubits=q.n)
    return op, ising.offset


def decode(qiskit_bitstring: str) -> str:
    """Qiskit measurement string -> canonical bitstring (variable 0 leftmost)."""
    return qiskit_bitstring[::-1]


def energy_table(q: CanonicalQUBO) -> dict[str, float]:
    op, offset = to_operator(q)
    diag = np.real(op.to_matrix(sparse=True).diagonal())
    table = {}
    for k, val in enumerate(diag):
        x = [(k >> i) & 1 for i in range(q.n)]  # qubit i = variable i
        table[bits_to_str(x)] = float(val + offset)
    return table


def energy_table_via_qiskit_optimization(q: CanonicalQUBO) -> dict[str, float]:
    """Independent cross-check: QuadraticProgram.to_ising() (qiskit-optimization)."""
    qo = require("qiskit_optimization")
    qp = qo.QuadraticProgram("canonical")
    for v in q.variables:
        qp.binary_var(v)
    linear = {v: float(q.Q[i, i]) for i, v in enumerate(q.variables)}
    quadratic = {}
    for i in range(q.n):
        for j in range(i + 1, q.n):
            if q.Q[i, j]:
                quadratic[(q.variables[i], q.variables[j])] = float(2 * q.Q[i, j])
    qp.minimize(constant=q.constant, linear=linear, quadratic=quadratic)
    op, offset = qp.to_ising()
    diag = np.real(op.to_matrix(sparse=True).diagonal())
    return {
        bits_to_str([(k >> i) & 1 for i in range(q.n)]): float(val + offset) for k, val in enumerate(diag)
    }


def run_qaoa_local(q: CanonicalQUBO, reps: int = 1, shots: int = 4096, seed: int = 7) -> dict:
    """Seeded QAOA on the local statevector sampler. Teaching experiment, not a benchmark."""
    qiskit = require("qiskit")
    from qiskit.circuit.library import QAOAAnsatz
    from qiskit.primitives import StatevectorEstimator, StatevectorSampler
    from scipy.optimize import minimize

    op, offset = to_operator(q)
    ansatz = QAOAAnsatz(op, reps=reps)
    estimator = StatevectorEstimator(seed=seed)
    rng = np.random.default_rng(seed)
    x0 = rng.uniform(0, np.pi, ansatz.num_parameters)

    def cost(theta):
        return float(estimator.run([(ansatz, op, theta)]).result()[0].data.evs)

    opt = minimize(cost, x0, method="COBYLA", options={"maxiter": 200})
    circ = ansatz.assign_parameters(opt.x)
    circ.measure_all()
    sampler = StatevectorSampler(seed=seed)
    counts = sampler.run([circ], shots=shots).result()[0].data.meas.get_counts()
    samples: dict[str, int] = {}
    for raw, c in counts.items():
        samples[decode(raw)] = samples.get(decode(raw), 0) + c
    return {
        "target": TARGET,
        "versions": {"qiskit": qiskit.__version__},
        "backend": "StatevectorSampler (local, noiseless)",
        "algorithm": f"QAOA p={reps}, COBYLA maxiter=200",
        "seed": seed,
        "shots": shots,
        "optimizer_evals": int(opt.nfev),
        "final_expectation": float(opt.fun + offset),
        "samples": samples,
    }
