"""Negative fixture: deprecated emulator API (pulser 1.9)."""
import numpy as np
from pulser import Register, Sequence
from pulser.devices import AnalogDevice
from pulser_simulation import QutipEmulator

reg = Register.from_coordinates(np.array([[0.0, 0.0], [6.0, 0.0]]), prefix="q")
seq = Sequence(reg, AnalogDevice)
counts = QutipEmulator.from_sequence(seq).run().sample_final_state()
