import json
from pathlib import Path

import pytest

from qmentor.canonical import build_mean_variance_qubo, load_problem

ROOT = Path(__file__).resolve().parent.parent
DEMO = ROOT / "demo" / "bond-selection"


@pytest.fixture(scope="session")
def spec():
    return load_problem(DEMO / "problem.json")


@pytest.fixture(scope="session")
def qubo(spec):
    return build_mean_variance_qubo(spec)


@pytest.fixture(scope="session")
def expected():
    return json.loads((DEMO / "expected.json").read_text())
