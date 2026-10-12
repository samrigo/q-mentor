"""Q-Mentor deterministic helpers.

Markdown skills are the source of behavior. This package exists only where
deterministic code adds value: canonical math, exact baselines, target
equivalence checks, capability gates, verdict/evidence scoring, and PQC
inventory. The base install depends on numpy and PyYAML only; every
provider SDK is an optional extra.
"""

__version__ = "0.1.0"

# Canonical bit order for every record in this repository:
# variable index 0 is the LEFTMOST character of a bitstring.
BIT_ORDER = "index0-leftmost"
