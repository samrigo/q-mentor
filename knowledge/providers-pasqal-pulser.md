# Pasqal / Pulser Target

Neutral-atom analog/digital pulse programs. Geometry, interaction signs, device limits, and addressability constrain which QUBOs are physically representable.

## Capability gate (required before any claim of equivalence)

1. Sign of interactions compatible with the device?
2. Register geometry feasible?
3. Addressability sufficient?
4. Pulse and measurement constraints satisfied?

If any check fails → return `unsupported` (or a separately labeled approximation). Never pass an equivalence test by silently changing the problem.
