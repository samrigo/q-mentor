# PennyLane adapter

Tested: `pennylane==0.45.1` (last_verified 2026-10-13).

**Rule:** PennyLane is a framework. Always name the device or plugin, interface, gradient method, shots, optimizer and seed.

- Hamiltonian: `qml.Hamiltonian(coeffs, [qml.PauliZ(i), qml.PauliZ(i) @ qml.PauliZ(j), ...])` from canonical `h`, `J`; keep the offset outside and add it back.
- Wire order: wire k = variable k; sample rows list wire 0 first (no reversal).
- QAOA: `qml.qaoa.cost_layer`, `qml.qaoa.mixer_layer`, `qml.qaoa.x_mixer(wires)`.
- Local device: `qml.device("default.qubit", wires=n, seed=...)`. Finite shots via `@qml.set_shots(n)` on a QNode.
- Training: `interface="autograd"`, `diff_method="backprop"` on simulators; parameter-shift for hardware-like settings.
- A PennyLane result is incomplete if the device is unnamed. Hardware plugins are separate packages with their own pins and credentials.

Worked example: `examples/bond-selection/pennylane/`.
