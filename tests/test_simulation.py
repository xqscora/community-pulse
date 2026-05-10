import random
from pathlib import Path

import pytest

from simulation import CommunitySim, load_scenario


def test_fresh_same_seed_same_ties():
    a = CommunitySim.fresh(42).ties
    b = CommunitySim.fresh(42).ties
    assert a == b


def test_step_day_no_llm_records_metrics():
    s = CommunitySim.fresh(7)
    s.step_day(None, rng=random.Random(0), max_reason_llm=0, dialogue_pairs=1)
    assert len(s.history) == 1
    assert "metrics" in s.history[0]
    assert len(s.dialogue_log) == 1


def test_load_scenario_close_library():
    root = Path(__file__).resolve().parents[1]
    p = root / "scenarios" / "close_library.json"
    if not p.is_file():
        pytest.skip("scenario file missing")
    pol = load_scenario(p)
    assert "library" in pol.title.lower() or "library" in pol.description.lower()
