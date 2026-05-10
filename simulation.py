"""
Day loop, policy injection, social graph, telemetry for Community Pulse.
"""

from __future__ import annotations

import json
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from agents import Agent, default_archetypes
from community_metrics import metrics_from_day
from gemma_bridge import GemmaBridge


@dataclass
class PolicyContext:
    title: str
    description: str
    stress_delta: float = 0.0
    novelty_delta: float = 0.0
    challenge_delta: float = 0.0


@dataclass
class CommunitySim:
    agents: List[Agent]
    day: int = 1
    policy: PolicyContext = field(
        default_factory=lambda: PolicyContext(
            title="Baseline",
            description="No major policy change.",
        )
    )
    # undirected edges (min_id, max_id) -> metrics
    ties: Dict[Tuple[str, str], Dict[str, float]] = field(default_factory=dict)
    history: List[Dict[str, Any]] = field(default_factory=list)
    dialogue_log: List[str] = field(default_factory=list)
    last_summary: str = ""

    @classmethod
    def fresh(cls, random_seed: Optional[int] = None) -> "CommunitySim":
        agents = default_archetypes()
        sim = cls(agents=agents)
        if random_seed is not None:
            sim._seed_ties(random.Random(random_seed))
        else:
            sim._seed_ties()
        return sim

    def _seed_ties(
        self,
        rng: Optional[random.Random] = None,
        trust: float = 0.45,
        familiarity: float = 0.35,
        p_edge: float = 0.35,
    ) -> None:
        rnd = rng if rng is not None else random
        ids = [a.id for a in self.agents]
        for i, u in enumerate(ids):
            for v in ids[i + 1 :]:
                if rnd.random() < p_edge:
                    self._set_edge(u, v, trust=trust, familiarity=familiarity)

    def _edge_key(self, u: str, v: str) -> Tuple[str, str]:
        return (u, v) if u < v else (v, u)

    def _set_edge(self, u: str, v: str, trust: float, familiarity: float) -> None:
        k = self._edge_key(u, v)
        self.ties[k] = {"trust": trust, "familiarity": familiarity}

    def apply_policy(self, policy: PolicyContext) -> None:
        self.policy = policy
        for a in self.agents:
            a.cerome.L4["stress"] = _clip(
                a.cerome.L4.get("stress", 0) + policy.stress_delta
            )
            a.cerome.L4["novelty"] = _clip(
                a.cerome.L4.get("novelty", 0.5) + policy.novelty_delta
            )
            a.cerome.L4["challenge"] = _clip(
                a.cerome.L4.get("challenge", 0) + policy.challenge_delta
            )

    def _reason_with_bridge(self, agent: Agent, bridge: GemmaBridge) -> str:
        return bridge.reason_about_policy(
            agent.name,
            agent.role,
            agent.backstory,
            agent.personality_for_llm(),
            self.policy.title,
            self.policy.description,
            self.day,
        )

    def step_day(
        self,
        bridge: Optional[GemmaBridge],
        rng: Optional[random.Random] = None,
        max_reason_llm: int = 6,
        dialogue_pairs: int = 2,
        llm_workers: int = 4,
    ) -> None:
        rng = rng or random.Random()
        day_record: Dict[str, Any] = {
            "day": self.day,
            "policy": self.policy.title,
            "agents": [],
        }

        reactions_for_summary: List[str] = [""] * len(self.agents)
        llm_results: Dict[int, str] = {}

        llm_indices = [i for i in range(len(self.agents)) if bridge is not None and i < max_reason_llm]
        if llm_indices:
            workers = max(1, min(llm_workers, len(llm_indices)))

            assert bridge is not None

            def _job(idx: int) -> tuple[int, str]:
                agent = self.agents[idx]
                try:
                    text = self._reason_with_bridge(agent, bridge)
                    return idx, text
                except Exception as exc:  # noqa: BLE001
                    fallback = (
                        f"[LLM offline or error: {exc}] Local stress-driven reaction: "
                        f"I feel the change in my body-budget — stress is now "
                        f"{agent.cerome.L4.get('stress', 0):.2f}."
                    )
                    return idx, fallback

            with ThreadPoolExecutor(max_workers=workers) as pool:
                futures = {pool.submit(_job, idx): idx for idx in llm_indices}
                for fut in as_completed(futures):
                    idx, text = fut.result()
                    llm_results[idx] = text

        for i, agent in enumerate(self.agents):
            if i in llm_results:
                agent.last_reaction = llm_results[i]
                reactions_for_summary[i] = f"{agent.name}: {agent.last_reaction[:280]}"
            else:
                d = agent.drives()
                top = max(d.items(), key=lambda x: x[1])[0]
                agent.last_reaction = (
                    f"(Heuristic day {self.day}) Strongest drive today: {top}. "
                    f"Policy «{self.policy.title}» bumps my attention toward what matters for {top}."
                )
                reactions_for_summary[i] = f"{agent.name}: {agent.last_reaction}"

            day_record["agents"].append(
                {
                    "id": agent.id,
                    "name": agent.name,
                    "drives": agent.drives(),
                    "L4": dict(agent.cerome.L4),
                }
            )

        day_record["metrics"] = metrics_from_day(day_record["agents"], self.ties)

        if bridge and reactions_for_summary:
            try:
                self.last_summary = bridge.day_summary(
                    self.policy.title, list(reactions_for_summary)
                )
            except Exception:  # noqa: BLE001
                self.last_summary = ""
        else:
            self.last_summary = ""

        self._run_dialogues(bridge, rng, dialogue_pairs, llm_workers)
        self._decay_stress()
        self.history.append(day_record)
        self.day += 1

    def _weighted_dialogue_pair(self, rng: random.Random) -> tuple[str, str]:
        """Bias pairs toward agents with higher social drive and stronger ties (PAT / L3)."""
        by_id = {a.id: a for a in self.agents}
        ids = list(by_id.keys())
        social_w = [max(0.06, by_id[i].drives()["social"]) for i in ids]
        u = rng.choices(ids, weights=social_w, k=1)[0]
        others = [j for j in ids if j != u]
        tie_w = []
        for j in others:
            key = self._edge_key(u, j)
            t = self.ties.get(key, {"trust": 0.2, "familiarity": 0.2})
            tie_w.append(0.12 + t["trust"] + 0.45 * t["familiarity"])
        v = rng.choices(others, weights=tie_w, k=1)[0]
        return u, v

    def _pair_dialogue_block(
        self,
        bridge: Optional[GemmaBridge],
        u: str,
        v: str,
        agents_by_id: Dict[str, Agent],
    ) -> tuple[str, str, str]:
        a, b = agents_by_id[u], agents_by_id[v]
        key = self._edge_key(u, v)
        tie = self.ties.get(key, {"trust": 0.35, "familiarity": 0.25})
        rel = f"trust={tie['trust']:.2f}, familiarity={tie['familiarity']:.2f}"
        topic = f"the policy: {self.policy.title}"
        if bridge:
            try:
                dlg = bridge.pairwise_dialogue(
                    a.name,
                    a.role,
                    a.personality_for_llm(),
                    b.name,
                    b.role,
                    b.personality_for_llm(),
                    rel,
                    topic,
                )
                text = f"--- Day {self.day} | {a.name} & {b.name} ---\n{dlg}"
            except Exception as exc:  # noqa: BLE001
                text = f"--- Day {self.day} | {a.name} & {b.name} ---\n[dialogue error: {exc}]"
        else:
            text = (
                f"--- Day {self.day} | {a.name} & {b.name} ---\n"
                f"(No LLM) They would discuss {topic} given {rel}."
            )
        return u, v, text

    def _run_dialogues(
        self,
        bridge: Optional[GemmaBridge],
        rng: random.Random,
        pairs: int,
        llm_workers: int = 4,
    ) -> None:
        ids = [a.id for a in self.agents]
        if len(ids) < 2 or pairs <= 0:
            return
        agents_by_id = {a.id: a for a in self.agents}
        sampled: List[tuple[str, str]] = []
        for _ in range(pairs):
            sampled.append(self._weighted_dialogue_pair(rng))

        results: List[tuple[str, str, str]] = []
        if bridge and pairs > 1:
            workers = max(1, min(llm_workers, pairs))

            def _dlg(uv: tuple[str, str]) -> tuple[str, str, str]:
                return self._pair_dialogue_block(bridge, uv[0], uv[1], agents_by_id)

            with ThreadPoolExecutor(max_workers=workers) as pool:
                for r in pool.map(_dlg, sampled):
                    results.append(r)
        else:
            for u, v in sampled:
                results.append(self._pair_dialogue_block(bridge, u, v, agents_by_id))

        for u, v, block in results:
            self.dialogue_log.append(block)
            a, b = agents_by_id[u], agents_by_id[v]
            key = self._edge_key(u, v)
            tie = self.ties.get(key, {"trust": 0.35, "familiarity": 0.25})
            nt = _clip(tie["trust"] + 0.02)
            nf = _clip(tie["familiarity"] + 0.03)
            self._set_edge(u, v, trust=nt, familiarity=nf)
            for ag in (a, b):
                ag.social_last_day = float(self.day)

    def _decay_stress(self, rate: float = 0.04) -> None:
        for a in self.agents:
            s = a.cerome.L4.get("stress", 0) * (1.0 - rate)
            a.cerome.L4["stress"] = max(0.0, s)


def _clip(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def load_scenario(path: Path) -> PolicyContext:
    data = json.loads(path.read_text(encoding="utf-8"))
    return PolicyContext(
        title=data["title"],
        description=data.get("description", ""),
        stress_delta=float(data.get("stress_delta", 0)),
        novelty_delta=float(data.get("novelty_delta", 0)),
        challenge_delta=float(data.get("challenge_delta", 0)),
    )


def list_scenarios(dir_path: Path) -> List[Path]:
    if not dir_path.is_dir():
        return []
    return sorted(dir_path.glob("*.json"))
