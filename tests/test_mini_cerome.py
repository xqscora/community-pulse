from mini_cerome import Cerome, DriveState, compute_drives


def test_drives_are_bounded_zero_one():
    c = Cerome()
    d = compute_drives(c, DriveState())
    assert len(d) == 7
    assert all(0.0 <= v <= 1.0 for v in d.values())


def test_higher_stress_raises_safety_drive():
    c = Cerome()
    low = compute_drives(c, DriveState())
    c.L4["stress"] = 0.9
    high = compute_drives(c, DriveState())
    assert high["safety"] >= low["safety"]
