"""PennyLane: a cross-platform differentiable FRAMEWORK, not a hardware provider.

Every result names the concrete device (offline default: ``default.qubit``),
interface, differentiation method, optimizer, shots, and seed.
Wire i holds canonical variable i. PennyLane matrices treat wire 0 as the most
significant bit, which matches the canonical leftmost-bit order.
"""

from __future__ import annotations

import numpy as np

from ..canonical import CanonicalQUBO, bits_to_str, qubo_to_ising
from . import require

TARGET = "pennylane"
DEVICE = "default.qubit"


def capability(q: CanonicalQUBO) -> dict:
    return {
        "target": TARGET,
        "role": "cross-platform differentiable framework (not a hardware provider)",
        "status": "exact",
        "mapping": "QUBO -> Ising -> qml.Hamiltonian of PauliZ terms, x=(1-s)/2",
        "device": DEVICE,
        "device_note": "Any other device requires naming the plugin (e.g. a provider plugin) and re-running equivalence",
        "requires": ["n wires = n variables"],
        "lost_semantics": [],
        "resources": {"wires": q.n},
        "remote_execution": "not performed; a hardware plugin needs explicit approval and credentials",
    }


def to_hamiltonian(q: CanonicalQUBO):
    qml = require("pennylane")
    ising = qubo_to_ising(q)
    coeffs, ops = [], []
    for i in range(q.n):
        if ising.h[i]:
            coeffs.append(float(ising.h[i]))
            ops.append(qml.PauliZ(i))
    for i in range(q.n):
        for j in range(i + 1, q.n):
            if ising.J[i, j]:
                coeffs.append(float(ising.J[i, j]))
                ops.append(qml.PauliZ(i) @ qml.PauliZ(j))
    return qml.Hamiltonian(coeffs, ops), ising.offset


def energy_table(q: CanonicalQUBO) -> dict[str, float]:
    qml = require("pennylane")
    H, offset = to_hamiltonian(q)
    diag = np.real(np.diag(qml.matrix(H, wire_order=list(range(q.n)))))
    table = {}
    for k, val in enumerate(diag):
        x = [(k >> (q.n - 1 - i)) & 1 for i in range(q.n)]  # wire 0 = MSB
        table[bits_to_str(x)] = float(val + offset)
    return table


def run_qaoa_local(q: CanonicalQUBO, layers: int = 1, steps: int = 60, shots: int = 4096, seed: int = 7) -> dict:
    qml = require("pennylane")
    from pennylane import numpy as pnp

    H, offset = to_hamiltonian(q)
    wires = list(range(q.n))
    # Normalise coefficients for a sane optimizer step; energies decoded canonically later.
    scale = float(np.max(np.abs(H.terms()[0]))) or 1.0
    H_scaled = qml.Hamiltonian(np.array(H.terms()[0]) / scale, H.terms()[1])
    mixer = qml.qaoa.x_mixer(wires)

    def layer(gamma, alpha):
        qml.qaoa.cost_layer(gamma, H_scaled)
        qml.qaoa.mixer_layer(alpha, mixer)

    dev = qml.device(DEVICE, wires=wires)
    diff_method = "backprop"

    @qml.qnode(dev, interface="autograd", diff_method=diff_method)
    def expval(params):
        for w in wires:
            qml.Hadamard(w)
        qml.layer(layer, layers, params[0], params[1])
        return qml.expval(H_scaled)

    rng = np.random.default_rng(seed)
    params = pnp.array(rng.uniform(0, 0.5, (2, layers)), requires_grad=True)
    opt = qml.AdamOptimizer(stepsize=0.1)
    for _ in range(steps):
        params = opt.step(expval, params)

    sample_dev = qml.device(DEVICE, wires=wires, seed=seed)

    @qml.set_shots(shots)
    @qml.qnode(sample_dev)
    def sampler(params):
        for w in wires:
            qml.Hadamard(w)
        qml.layer(layer, layers, params[0], params[1])
        return qml.sample(wires=wires)

    raw = np.asarray(sampler(params))
    samples: dict[str, int] = {}
    for row in raw:
        b = bits_to_str(row)  # sample columns follow wire order = canonical order
        samples[b] = samples.get(b, 0) + 1
    return {
        "target": TARGET,
        "versions": {"pennylane": qml.__version__},
        "device": DEVICE,
        "interface": "autograd",
        "diff_method": diff_method,
        "optimizer": "AdamOptimizer(stepsize=0.1)",
        "optimizer_steps": steps,
        "layers": layers,
        "hamiltonian_scale": scale,
        "seed": seed,
        "shots": shots,
        "final_expectation": float(expval(params) * scale + offset),
        "samples": samples,
    }
