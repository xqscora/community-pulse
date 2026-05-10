from community_metrics import metrics_from_day


def test_metrics_contains_core_keys():
    rows = [
        {
            "id": "x",
            "name": "Test",
            "L4": {"stress": 0.2, "challenge": 0.1},
            "drives": {
                "social": 0.5,
                "safety": 0.4,
                "fairness": 0.45,
                "curiosity": 0.5,
                "achievement": 0.5,
                "expression": 0.5,
                "autonomy": 0.5,
            },
        }
    ]
    ties = {("a", "b"): {"trust": 0.5, "familiarity": 0.4}}
    m = metrics_from_day(rows, ties)
    for k in (
        "mean_stress",
        "social_cohesion_trust",
        "resilience_index",
        "n_edges",
    ):
        assert k in m
