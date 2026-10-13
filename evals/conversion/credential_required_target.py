"""Negative fixture: credentialed synthesis without an approval gate."""
from classiq import synthesize

from adapter import main

qprog = synthesize(main)
