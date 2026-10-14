"""Six-bond selection with PennyLane QAOA on the local `default.qubit` device.

Interface: autograd (pennylane.numpy); gradient: backprop on the analytic device;
optimizer: AdamOptimizer, fixed seed. Final sampling uses a finite-shot device.
"""
from __future__ import annotations

import json
import time

import pennylane as qml
from pennylane import numpy as pnp

import adapter
import canonical

SEED = 7
LAYERS = 2
STEPS = 80
SHOTS = 4096
WIRES = 6


def main() -> dict:
    problem = canonical.load_problem()
    cost_h, offset = adapter.build_cost_hamiltonian(problem)
    mixer_h = qml.qaoa.x_mixer(range(WIRES))
    scale = float(max(abs(c) for c in cost_h.coeffs))

    def layer(gamma, alpha):
        qml.qaoa.cost_layer(gamma, cost_h)
        qml.qaoa.mixer_layer(alpha, mixer_h)

    def ansatz(params):
        for w in range(WIRES):
            qml.Hadamard(wires=w)
        qml.layer(layer, LAYERS, params[0], params[1])

    analytic = qml.device(adapter.DEVICE_NAME, wires=WIRES)

    @qml.qnode(analytic, interface="autograd", diff_method="backprop")
    def expected_cost(params):
        ansatz(params)
        return qml.expval(cost_h)

    sampler = qml.device(adapter.DEVICE_NAME, wires=WIRES, seed=SEED)

    @qml.set_shots(SHOTS)
    @qml.qnode(sampler)
    def sample(params):
        ansatz(params)
        return qml.sample(wires=range(WIRES))

    pnp.random.seed(SEED)
    params = pnp.array(pnp.random.uniform(0, 0.5, (2, LAYERS)), requires_grad=True)
    opt = qml.AdamOptimizer(stepsize=0.05)
    start = time.perf_counter()
    for _ in range(STEPS):
        params = opt.step(lambda p: expected_cost(p) / scale, params)
    rows = sample(params)
    elapsed = time.perf_counter() - start

    counts = {}
    for row in rows:
        key = canonical.bitstring([int(b) for b in row])
        counts[key] = counts.get(key, 0) + 1
    decoded = sorted((dict(canonical.decode(canonical.parse_bitstring(b), problem), count=c)
                      for b, c in counts.items()), key=lambda d: d["energy"])
    feasible = [d for d in decoded if d["feasible"]]
    baseline = canonical.exact_baseline(problem)
    record = {
        "schema": "qmentor.result-record.v3",
        "target": "pennylane",
        "versions": {"pennylane": qml.__version__},
        "device": adapter.DEVICE_NAME,
        "interface": "autograd",
        "diff_method": "backprop",
        "optimizer": f"AdamOptimizer(stepsize=0.05), steps={STEPS}",
        "layers": LAYERS,
        "seed": SEED,
        "shots": SHOTS,
        "baseline": baseline,
        "quantum": {
            "final_expected_energy": round(float(expected_cost(params)) + offset, 6),
            "best_sampled": decoded[0],
            "feasibility_rate": round(sum(d["count"] for d in feasible) / SHOTS, 4),
            "optimum_probability": round(counts.get(baseline["optimum"]["bitstring"], 0) / SHOTS, 4),
            "wall_clock_s": round(elapsed, 3),
        },
        "evidence_level": "executable on a local simulator; not a hardware result and not quantum advantage",
    }
    print(json.dumps(record, indent=2))
    return record


if __name__ == "__main__":
    main()
