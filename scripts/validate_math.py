#!/usr/bin/env python3
"""Deterministic math gate: runs the offline math eval suite (no model, no network).

    python scripts/validate_math.py
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.exit(subprocess.call([sys.executable, str(ROOT / "scripts" / "run_evals.py"), "--suite", "math"]))
