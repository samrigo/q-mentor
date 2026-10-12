# Target: PennyLane (differentiable framework)

`last_verified: 2026-10-12` · tested: `pennylane 0.45.1` · sources: `pennylane-2018`, `pennylane-docs`, `pennylane-qaoa`, `pennylane-interfaces`

## Operational rule

PennyLane is a **framework**, not a hardware provider. Every result names the concrete device or plugin (offline default `default.qubit`), interface, differentiation method, optimizer, shots, and seed.

## Mapping

- `qml.Hamiltonian(coeffs, ops)` with `qml.PauliZ(i)` for h_i and `PauliZ(i) @ PauliZ(j)` for J_ij; add the offset separately.
- Wire i holds variable i. In `qml.matrix(H, wire_order=...)`, wire 0 is the **most significant** bit, matching the canonical leftmost bit order. `qml.sample(wires=...)` columns follow wire order.

## QAOA offline

`qml.qaoa.cost_layer` and `qml.qaoa.mixer_layer` with `qml.qaoa.x_mixer`; optimize `qml.expval(H)` on `default.qubit` (interface `autograd`, `diff_method="backprop"`), e.g. `AdamOptimizer`. Scale coefficients for stable steps and report the scale. Sample with a seeded device and a fixed shot count.

## Devices and plugins

`lightning.qubit` (fast local simulator), noise-capable mixed-state simulators, and provider plugins that forward to hardware. Changing device can change supported diff methods and shot behavior: re-run equivalence and record the plugin version. Hardware plugins need credentials and explicit approval.

## Limits

Backprop is simulator-only; hardware needs parameter-shift or finite differences (more circuit evaluations). Gradients on hardware are shot-noisy; report the shot budget.
