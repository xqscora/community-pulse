"""
Resident agents with PAT profiles (archetypes for Community Pulse).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from mini_cerome import Cerome, DriveState, compute_drives, personality_prompt_block


@dataclass
class Agent:
    id: str
    name: str
    role: str
    backstory: str
    cerome: Cerome
    age_days: float = 12000.0
    social_last_day: float = 11990.0
    resources: float = 45.0
    health: float = 0.88
    last_reaction: str = ""

    def drive_state(self) -> DriveState:
        return DriveState(
            age_days=self.age_days,
            social_last_day=self.social_last_day,
            resources=self.resources,
            health=self.health,
        )

    def drives(self) -> Dict[str, float]:
        return compute_drives(self.cerome, self.drive_state())

    def personality_for_llm(self) -> str:
        return personality_prompt_block(self.cerome, self.drives())


def _cerome(L1: Dict[str, float], L2: Dict[str, float]) -> Cerome:
    c = Cerome(L1=dict(L1))
    for k, v in L2.items():
        if k in c.L2:
            c.L2[k] = v
    return c


def default_archetypes() -> List[Agent]:
    """10 diverse residents; L1/L2 chosen for spread across drives."""
    return [
        Agent(
            id="a1",
            name="Maya Chen",
            role="high school student",
            backstory="Loves robotics club and the public library; applies to internships.",
            cerome=_cerome(
                {
                    "dopamine": 0.82,
                    "serotonin": 0.45,
                    "cortisol_baseline": 0.35,
                    "oxytocin": 0.55,
                    "cognitive_flexibility": 0.8,
                    "sensory_threshold": 0.55,
                    "recovery_speed": 0.65,
                    "sex_drive": 0.4,
                },
                {
                    "curiosity": 0.85,
                    "achievement": 0.7,
                    "connection": 0.45,
                    "safety": 0.35,
                    "autonomy": 0.6,
                    "expression": 0.5,
                    "fairness": 0.4,
                },
            ),
        ),
        Agent(
            id="a2",
            name="Elena Ruiz",
            role="retired teacher",
            backstory="Volunteers at the community center; knows most neighbors by name.",
            cerome=_cerome(
                {
                    "dopamine": 0.4,
                    "serotonin": 0.72,
                    "cortisol_baseline": 0.3,
                    "oxytocin": 0.88,
                    "cognitive_flexibility": 0.55,
                    "sensory_threshold": 0.4,
                    "recovery_speed": 0.5,
                    "sex_drive": 0.2,
                },
                {
                    "connection": 0.9,
                    "fairness": 0.75,
                    "safety": 0.55,
                    "curiosity": 0.45,
                    "achievement": 0.35,
                    "autonomy": 0.4,
                    "expression": 0.35,
                },
            ),
        ),
        Agent(
            id="a3",
            name="Sam Okonkwo",
            role="corner store owner",
            backstory="Long hours, thin margins; daughter needs asthma meds.",
            cerome=_cerome(
                {
                    "dopamine": 0.45,
                    "serotonin": 0.4,
                    "cortisol_baseline": 0.85,
                    "oxytocin": 0.5,
                    "cognitive_flexibility": 0.45,
                    "sensory_threshold": 0.5,
                    "recovery_speed": 0.4,
                    "sex_drive": 0.35,
                },
                {
                    "safety": 0.85,
                    "achievement": 0.65,
                    "connection": 0.5,
                    "fairness": 0.45,
                    "curiosity": 0.25,
                    "autonomy": 0.55,
                    "expression": 0.2,
                },
            ),
            resources=28.0,
        ),
        Agent(
            id="a4",
            name="Jordan Lee",
            role="librarian",
            backstory="Runs teen programs; fights for open access to information.",
            cerome=_cerome(
                {
                    "dopamine": 0.5,
                    "serotonin": 0.68,
                    "cortisol_baseline": 0.38,
                    "oxytocin": 0.62,
                    "cognitive_flexibility": 0.7,
                    "sensory_threshold": 0.48,
                    "recovery_speed": 0.55,
                    "sex_drive": 0.35,
                },
                {
                    "curiosity": 0.75,
                    "fairness": 0.8,
                    "autonomy": 0.5,
                    "connection": 0.65,
                    "achievement": 0.45,
                    "safety": 0.4,
                    "expression": 0.55,
                },
            ),
        ),
        Agent(
            id="a5",
            name="Rico Alvarez",
            role="community organizer",
            backstory="Runs mutual aid chats; skeptical of city hall announcements.",
            cerome=_cerome(
                {
                    "dopamine": 0.65,
                    "serotonin": 0.55,
                    "cortisol_baseline": 0.55,
                    "oxytocin": 0.58,
                    "cognitive_flexibility": 0.72,
                    "sensory_threshold": 0.62,
                    "recovery_speed": 0.58,
                    "sex_drive": 0.45,
                },
                {
                    "fairness": 0.92,
                    "connection": 0.7,
                    "autonomy": 0.75,
                    "achievement": 0.5,
                    "curiosity": 0.6,
                    "safety": 0.45,
                    "expression": 0.7,
                },
            ),
        ),
        Agent(
            id="a6",
            name="Priya Nair",
            role="nurse and parent of two",
            backstory="Night shifts; depends on after-school programs and clinic wait times.",
            cerome=_cerome(
                {
                    "dopamine": 0.48,
                    "serotonin": 0.58,
                    "cortisol_baseline": 0.62,
                    "oxytocin": 0.75,
                    "cognitive_flexibility": 0.6,
                    "sensory_threshold": 0.42,
                    "recovery_speed": 0.48,
                    "sex_drive": 0.35,
                },
                {
                    "safety": 0.8,
                    "connection": 0.78,
                    "achievement": 0.55,
                    "fairness": 0.6,
                    "curiosity": 0.4,
                    "autonomy": 0.45,
                    "expression": 0.3,
                },
            ),
            health=0.78,
        ),
        Agent(
            id="a7",
            name="Walter Hsu",
            role="retired engineer",
            backstory="Values quiet routines; distrusts sudden policy swings.",
            cerome=_cerome(
                {
                    "dopamine": 0.38,
                    "serotonin": 0.65,
                    "cortisol_baseline": 0.42,
                    "oxytocin": 0.45,
                    "cognitive_flexibility": 0.5,
                    "sensory_threshold": 0.35,
                    "recovery_speed": 0.45,
                    "sex_drive": 0.2,
                },
                {
                    "autonomy": 0.82,
                    "safety": 0.7,
                    "curiosity": 0.35,
                    "achievement": 0.3,
                    "connection": 0.4,
                    "fairness": 0.55,
                    "expression": 0.25,
                },
            ),
        ),
        Agent(
            id="a8",
            name="Tasha Williams",
            role="delivery driver",
            backstory="Gig work, rent pressure; coffee shop is her social hub.",
            cerome=_cerome(
                {
                    "dopamine": 0.7,
                    "serotonin": 0.42,
                    "cortisol_baseline": 0.68,
                    "oxytocin": 0.48,
                    "cognitive_flexibility": 0.55,
                    "sensory_threshold": 0.58,
                    "recovery_speed": 0.52,
                    "sex_drive": 0.5,
                },
                {
                    "achievement": 0.78,
                    "autonomy": 0.68,
                    "connection": 0.55,
                    "safety": 0.6,
                    "curiosity": 0.45,
                    "fairness": 0.5,
                    "expression": 0.4,
                },
            ),
            resources=32.0,
        ),
        Agent(
            id="a9",
            name="Omar Haddad",
            role="imam and counselor",
            backstory="Listens to family stress; bridges elders and youth.",
            cerome=_cerome(
                {
                    "dopamine": 0.46,
                    "serotonin": 0.75,
                    "cortisol_baseline": 0.4,
                    "oxytocin": 0.8,
                    "cognitive_flexibility": 0.65,
                    "sensory_threshold": 0.45,
                    "recovery_speed": 0.6,
                    "sex_drive": 0.3,
                },
                {
                    "connection": 0.88,
                    "fairness": 0.72,
                    "safety": 0.65,
                    "curiosity": 0.5,
                    "achievement": 0.4,
                    "autonomy": 0.45,
                    "expression": 0.55,
                },
            ),
        ),
        Agent(
            id="a10",
            name="Chris Park",
            role="teen gamer and streamer",
            backstory="Online friends worldwide; local internet outages hit hard.",
            cerome=_cerome(
                {
                    "dopamine": 0.78,
                    "serotonin": 0.48,
                    "cortisol_baseline": 0.45,
                    "oxytocin": 0.52,
                    "cognitive_flexibility": 0.75,
                    "sensory_threshold": 0.72,
                    "recovery_speed": 0.7,
                    "sex_drive": 0.45,
                },
                {
                    "expression": 0.85,
                    "curiosity": 0.8,
                    "connection": 0.6,
                    "autonomy": 0.7,
                    "achievement": 0.55,
                    "safety": 0.35,
                    "fairness": 0.4,
                },
            ),
        ),
    ]

