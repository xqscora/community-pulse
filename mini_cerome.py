"""
Mini-Cerome: simplified PAT personality layer (L1/L2/L3/L4 + drives).
Extracted from CogArch Cerome + compute_drives (Zeng 2026 PAT; drives align with
Self-Determination Theory, Deci & Ryan 2000).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple

_clip = lambda x, lo=0.0, hi=1.0: max(lo, min(hi, x))


class Cerome:
    """Four-layer slice of PAT (no L5 momentary layer in this hackathon build)."""

    def __init__(self, L1: Optional[Dict[str, float]] = None):
        self.L1 = L1 or {
            "dopamine": 0.5,
            "serotonin": 0.5,
            "cortisol_baseline": 0.5,
            "oxytocin": 0.5,
            "cognitive_flexibility": 0.5,
            "sensory_threshold": 0.5,
            "recovery_speed": 0.5,
            "sex_drive": 0.5,
        }
        self.L2 = {
            "curiosity": 0.0,
            "connection": 0.0,
            "achievement": 0.0,
            "safety": 0.0,
            "autonomy": 0.0,
            "expression": 0.0,
            "fairness": 0.0,
        }
        self.L3: Dict[str, Any] = {}
        self.L4 = {
            "stress": 0.0,
            "novelty": 0.5,
            "social_density": 0.0,
            "challenge": 0.0,
        }

    def snapshot(self) -> Dict[str, Any]:
        return {
            "L1": dict(self.L1),
            "L2": dict(self.L2),
            "L4": dict(self.L4),
            "n_rels": len(self.L3),
        }

    def top_values(self, n: int = 3) -> list[Tuple[str, float]]:
        ranked = sorted(self.L2.items(), key=lambda x: x[1], reverse=True)
        return [(k, round(v, 3)) for k, v in ranked[:n] if v > 0.01]


@dataclass
class DriveState:
    """Minimal world state for drive computation (replaces full CogArch agent)."""

    age_days: float = 365.0
    social_last_day: float = 0.0
    resources: float = 50.0
    health: float = 0.85
    resource_low_threshold: float = 20.0


def compute_drives(cerome: Cerome, state: Optional[DriveState] = None) -> Dict[str, float]:
    """Seven drives from L1, L2, L4 (same structure as CogArch.compute_drives)."""
    st = state or DriveState()
    L1 = cerome.L1
    L2 = cerome.L2
    L4 = cerome.L4
    stress = L4.get("stress", 0.0)
    age_y = max(0.01, st.age_days / 365.0)

    drives: Dict[str, float] = {}
    drives["curiosity"] = _clip(
        L1["dopamine"] * 0.35
        + L1["cognitive_flexibility"] * 0.25
        + L2.get("curiosity", 0) * 0.3
        - stress * 0.15
    )
    social_gap = max(0.0, st.age_days - st.social_last_day)
    social_deprivation = min(1.0, social_gap / max(1.0, age_y * 2))
    drives["social"] = _clip(
        L1["oxytocin"] * 0.4
        + L2.get("connection", 0) * 0.3
        + social_deprivation * 0.12
        - stress * 0.1
    )
    drives["achievement"] = _clip(
        L1["dopamine"] * 0.25
        + L1["serotonin"] * 0.15
        + L2.get("achievement", 0) * 0.35
        - stress * 0.1
    )
    drives["expression"] = _clip(
        L1["sensory_threshold"] * 0.3
        + L1["cognitive_flexibility"] * 0.2
        + L2.get("expression", 0) * 0.3
        - stress * 0.05
    )
    resource_pressure = max(
        0.0, 1.0 - st.resources / max(1.0, st.resource_low_threshold)
    )
    health_pressure = max(0.0, 0.6 - st.health) * 0.5
    drives["safety"] = _clip(
        L1["cortisol_baseline"] * 0.15
        + stress * 0.35
        + L2.get("safety", 0) * 0.15
        + health_pressure
        + resource_pressure * 0.25
    )
    drives["autonomy"] = _clip(
        L1["dopamine"] * 0.2
        + L2.get("autonomy", 0) * 0.35
        - L1["cortisol_baseline"] * 0.1
    )
    drives["fairness"] = _clip(
        L1["serotonin"] * 0.25
        + L1["oxytocin"] * 0.15
        + L2.get("fairness", 0) * 0.35
        - stress * 0.05
    )
    return drives


def personality_prompt_block(cerome: Cerome, drives: Dict[str, float]) -> str:
    """Structured text for LLM system context (numeric PAT constraints)."""
    tops = cerome.top_values(4)
    l4 = cerome.L4
    lines = [
        "PERSONALITY_ENGINE (PAT / Cerome — numeric baselines; stay consistent):",
        f"  L1 neurochemical baselines: {', '.join(f'{k}={v:.2f}' for k, v in cerome.L1.items())}",
        f"  Top values L2: {tops}",
        f"  State L4: stress={l4.get('stress', 0):.2f}, novelty={l4.get('novelty', 0):.2f}, "
        f"social_density={l4.get('social_density', 0):.2f}, challenge={l4.get('challenge', 0):.2f}",
        f"  Computed drives (0–1): {', '.join(f'{k}={v:.2f}' for k, v in sorted(drives.items()))}",
    ]
    return "\n".join(lines)
