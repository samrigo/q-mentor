# Target: Pasqal / Pulser (neutral atoms)

`last_verified: 2026-10-12` · tested: `pulser-core 1.9.1` · sources: `pulser-2022`, `pulser-docs`, `pulser-qubo-tutorial`, `pulser-noise`

## Operational rule

Pulser programs neutral-atom **pulse sequences** on a **register** of atoms. It is not a generic QUBO compiler. Emit a `CapabilityReport` before any code; if the QUBO is not physically representable, return `unsupported-exact` with alternatives.

## Physics that constrains the mapping

H = sum_i (Omega_i/2) X_i - sum_i delta_i n_i + sum_{i<j} U_ij n_i n_j, with n_i = |r><r|_i and **U_ij = C6 / r_ij^6**.

- U_ij is **strictly positive** and non-zero at finite distance: negative or zero couplings are not exact.
- Couplings are set by **geometry**: required distances r_ij ∝ Q_ij^(-1/6) must exist as points in the device's dimension (2D for current QPUs). Test with classical multidimensional scaling: B = -1/2 J D^2 J must be PSD with rank <= dimension. A dense n-atom QUBO has n(n-1)/2 couplings but only ~2n - 3 geometric degrees of freedom in 2D, so generic dense QUBOs fail.
- Linear terms map to detunings. **Non-uniform** linear terms need local detuning addressability (a DMM channel); some devices (e.g. `AnalogDevice` in pulser-core 1.9.1) lack it.
- Distances must respect the device's minimum atom spacing and maximum radial distance (dynamic range of r_ij).

## Workflow

1. Capability check (signs, geometry rank, addressability, dynamic range) against a named device.
2. Exact -> build register and sequence; emulate locally (e.g. `pulser-simulation`) with a stated noise model.
3. Not exact -> alternatives: reformulate to geometric (unit-disk) structure; a higher-level Pasqal workflow with its own embedding (report its error); a digital route (Qiskit/PennyLane); D-Wave or classical exact.
4. Approximation (e.g. optimized atom positions, as in the Pulser QUBO tutorial) is a separately labeled option with its coupling error in every result.

## Limits

Analog adiabatic protocols (QAA) depend on pulse shape and duration; noise models matter. Cloud execution via Pasqal's services needs credentials and explicit approval.
