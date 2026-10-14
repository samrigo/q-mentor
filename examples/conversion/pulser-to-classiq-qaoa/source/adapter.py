"""Pulser source program for the Pasqal/Pulser -> Classiq optimization regression.

Five atoms on pulser.devices.AnalogDevice in a zig-zag. Every pair interacts (C6/r^6 > 0), so the program's final
classical Hamiltonian is a five-variable QUBO with exactly ten pair terms and a uniform linear term -delta_f:

    E(x) = -delta_f * sum_i x_i + sum_{i<j} C6 / r_ij^6 x_i x_j      (x_i = 1 <=> atom i in the Rydberg state)

The source algorithm is a quantum adiabatic sweep (QAA): Omega(t) 0 -> Omega_max -> 0, delta(t) -delta_f -> +delta_f.
Bit order: register q0..q4 = bitstring characters left to right.
"""
from __future__ import annotations

import itertools
from typing import Dict, List, Sequence as Seq, Tuple

import numpy as np
from pulser import InterpolatedWaveform, Pulse, Register, Sequence
from pulser.devices import AnalogDevice

DEVICE = AnalogDevice
COORDS_UM = [(0.0, 0.0), (7.0, 0.0), (14.0, 0.0), (3.3, 6.6), (10.9, 6.4)]
DELTA_FINAL = 6.0                  # rad/us
OMEGA_MAX = 2.0 * np.pi * 0.8      # rad/us (below the AnalogDevice limit)
DURATION_NS = 4000


def register() -> Register:
    coords = np.array(COORDS_UM)
    return Register.from_coordinates(coords - coords.mean(axis=0), prefix="q")


def build_sequence(reg: Register) -> Sequence:
    seq = Sequence(reg, DEVICE)
    seq.declare_channel("ising", "rydberg_global")
    amplitude = InterpolatedWaveform(DURATION_NS, [1e-9, OMEGA_MAX, 1e-9])
    detuning = InterpolatedWaveform(DURATION_NS, [-DELTA_FINAL, 0.0, DELTA_FINAL])
    seq.add(Pulse(amplitude, detuning, 0), "ising")
    seq.measure("ground-rydberg")
    return seq


def qubo(reg: Register) -> Tuple[Dict[int, float], Dict[Tuple[int, int], float], float]:
    pos = [reg.qubits[q].as_array() for q in reg.qubit_ids]
    linear = {i: -DELTA_FINAL for i in range(len(pos))}
    quad = {(i, j): float(DEVICE.interaction_coeff / np.linalg.norm(pos[i] - pos[j]) ** 6)
            for i, j in itertools.combinations(range(len(pos)), 2)}
    return linear, quad, 0.0


def energy(x: Seq[int], q) -> float:
    linear, quad, const = q
    return const + sum(a * x[i] for i, a in linear.items()) + sum(b * x[i] * x[j] for (i, j), b in quad.items())


def ranking(q) -> List[Tuple[float, str]]:
    n = len(q[0])
    return sorted((energy(x, q), "".join(map(str, x))) for x in itertools.product((0, 1), repeat=n))
