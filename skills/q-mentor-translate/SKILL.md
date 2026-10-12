---
name: q-mentor-translate
description: >
  Map one canonical problem to two execution targets and explain non-equivalent
  details. Use when the user asks how the same QUBO looks in different SDKs.
  Output one comparison table.
---

# q-mentor-translate

## Workflow

1. Load the accepted CanonicalQUBO / ProblemSpec.
2. For each requested target produce a CapabilityReport: exact | approximate | unsupported | unknown.
3. Exact adapters must preserve energy for all assignments after documented constant/sign conversion.
4. Pasqal/Pulser must first issue a representability report (geometry, coupling, addressability, device limits). Never mislabel an approximation as equivalent.
5. PennyLane must name the concrete device (e.g. `default.qubit`) and gradient/optimizer settings.
6. Output a side-by-side comparison table of encoding, resource estimate, lost semantics, and version pins.

## Supported targets (MVP)

- Qiskit
- Classiq
- D-Wave Ocean
- Pasqal / Pulser
- PennyLane

## Knowledge links

- `knowledge/providers-qiskit.md`
- `knowledge/providers-classiq.md`
- `knowledge/providers-dwave.md`
- `knowledge/providers-pasqal-pulser.md`
- `knowledge/framework-pennylane.md`
