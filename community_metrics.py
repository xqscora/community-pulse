"""
Aggregate indices for Community Pulse dashboard (PAT-oriented readouts).

Stress / drives come from Cerome L4 and compute_drives (Zeng PAT / CogArch).
Social cohesion summarizes L3-style tie strength (trust) as a graph-level scalar.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple


def metrics_from_day(
    agents_rows: List[Dict[str, Any]],
    ties: Dict[Tuple[str, str], Dict[str, float]],
) -> Dict[str, float]:
    n = max(1, len(agents_rows))
    stresses = [float(row["L4"].get("stress", 0)) for row in agents_rows]
    mean_stress = sum(stresses) / n
    mean_challenge = sum(float(row["L4"].get("challenge", 0)) for row in agents_rows) / n
    mean_social_drive = sum(float(row["drives"].get("social", 0)) for row in agents_rows) / n
    mean_safety_drive = sum(float(row["drives"].get("safety", 0)) for row in agents_rows) / n
    mean_fairness_drive = sum(float(row["drives"].get("fairness", 0)) for row in agents_rows) / n

    if ties:
        trust_vals = [float(m.get("trust", 0)) for m in ties.values()]
        fam_vals = [float(m.get("familiarity", 0)) for m in ties.values()]
        cohesion = sum(trust_vals) / len(trust_vals)
        familiarity_mean = sum(fam_vals) / len(fam_vals)
        edge_density = len(ties) / max(1, n * (n - 1) / 2)
    else:
        cohesion = 0.0
        familiarity_mean = 0.0
        edge_density = 0.0

    # Simple composite: high stress hurts, cohesion helps (0–1 scale heuristic)
    resilience = max(0.0, min(1.0, cohesion * 0.55 + (1.0 - mean_stress) * 0.45))

    return {
        "mean_stress": round(mean_stress, 4),
        "mean_challenge": round(mean_challenge, 4),
        "mean_social_drive": round(mean_social_drive, 4),
        "mean_safety_drive": round(mean_safety_drive, 4),
        "mean_fairness_drive": round(mean_fairness_drive, 4),
        "social_cohesion_trust": round(cohesion, 4),
        "tie_familiarity_mean": round(familiarity_mean, 4),
        "tie_density": round(edge_density, 4),
        "n_edges": float(len(ties)),
        "resilience_index": round(resilience, 4),
    }
