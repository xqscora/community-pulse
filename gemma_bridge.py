"""
Gemma 4 via Ollama OpenAI-compatible API.
"""

from __future__ import annotations

import os
from typing import List, Optional

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover
    OpenAI = None  # type: ignore


DEFAULT_BASE_URL = "http://localhost:11434/v1"
DEFAULT_MODEL = os.environ.get("OLLAMA_GEMMA_MODEL", "gemma3:4b")

# MFA (Multi-Focus Attention) framing for prompts — aligns with PAT simulation in CogArch
# (attention as competition between salience sources; drives/values bias the field).
MFA_ATTENTION_FRAME = (
    "Attention simulation (MFA-style): not every policy detail is equally salient. "
    "Higher numeric *drives* mark what competes for the mental spotlight; L4 *stress* widens "
    "threat- and loss-related salience; dominant L2 *values* pull you toward matching worries and hopes. "
    "Do not say 'MFA', 'algorithm', or 'neurotransmitters' out loud—show it through what you notice first "
    "and what you barely register."
)


class GemmaBridge:
    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        model: str = DEFAULT_MODEL,
        api_key: str = "ollama",
    ):
        if OpenAI is None:
            raise RuntimeError("Install openai package: pip install openai")
        timeout = float(os.environ.get("OLLAMA_TIMEOUT_SEC", "120"))
        self.client = OpenAI(base_url=base_url, api_key=api_key, timeout=timeout)
        self.model = model

    def complete(
        self,
        system: str,
        user: str,
        temperature: float = 0.7,
        max_tokens: int = 512,
    ) -> str:
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        choice = resp.choices[0]
        return (choice.message.content or "").strip()

    def reason_about_policy(
        self,
        agent_name: str,
        role: str,
        backstory: str,
        personality_block: str,
        policy_title: str,
        policy_description: str,
        day: int,
    ) -> str:
        system = (
            "You are simulating one resident in a small community. "
            "Respond in first person, 2–4 short paragraphs max.\n"
            f"{MFA_ATTENTION_FRAME}\n"
            "Honor the numeric personality block; it constrains salience and values."
        )
        user = (
            f"You are {agent_name}, {role}.\n"
            f"Background: {backstory}\n\n"
            f"{personality_block}\n\n"
            f"Day {day}. The community just announced this policy:\n"
            f"Title: {policy_title}\n"
            f"Details: {policy_description}\n\n"
            "Start with the 1–2 policy facets that grab your attention first (others can stay peripheral). "
            "Then: immediate emotional reaction, one worry and one hope, and one concrete action you might take."
        )
        return self.complete(system, user, temperature=0.75)

    def pairwise_dialogue(
        self,
        a_name: str,
        a_role: str,
        a_personality: str,
        b_name: str,
        b_role: str,
        b_personality: str,
        relationship_note: str,
        topic: str,
    ) -> str:
        system = (
            "Write a natural dialogue between two community members (6–12 short lines total, "
            "alternating speakers, format: Name: line). Stay in character per personality blocks.\n"
            f"{MFA_ATTENTION_FRAME} "
            "Let each speaker foreground what their drives/values make salient; disagreement is fine."
        )
        user = (
            f"{a_name} ({a_role}):\n{a_personality}\n\n"
            f"{b_name} ({b_role}):\n{b_personality}\n\n"
            f"Relationship: {relationship_note}\n"
            f"They are discussing: {topic}\n"
        )
        return self.complete(system, user, temperature=0.8, max_tokens=600)

    def day_summary(self, policy_title: str, snippets: List[str]) -> str:
        system = (
            "You are a neutral community analyst. 1 short paragraph, no bullet points. "
            "Note how different residents foreground different facets of the same policy (attention divergence)."
        )
        joined = "\n---\n".join(snippets[:20])
        user = (
            f"Policy in effect: {policy_title}\n\n"
            f"Sample resident reactions:\n{joined}\n\n"
            "Summarize emotional tone, main tensions, and what competing concerns split the community."
        )
        return self.complete(system, user, temperature=0.5, max_tokens=256)


def bridge_from_env() -> GemmaBridge:
    base = os.environ.get("OLLAMA_BASE_URL", DEFAULT_BASE_URL)
    model = os.environ.get("OLLAMA_GEMMA_MODEL", DEFAULT_MODEL)
    return GemmaBridge(base_url=base, model=model)
