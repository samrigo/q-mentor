"""Negative fixture: generated target code with a missing import."""
from classiq import QArray, QBit, Output, allocate, qfunc


@qfunc
def main(x: Output[QArray[QBit, 4]]):
    allocate(x)
    hadamard_transform(x)
