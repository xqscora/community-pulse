"""
Headless runs for Community Pulse (CI, batch experiments, Kaggle reproducibility).

Examples:
  python cli.py run --days 3 --no-llm --seed 42
  python cli.py run --days 1 --scenario close_library --out run.json
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCENARIOS = ROOT / "scenarios"


def _cmd_run(ns: argparse.Namespace) -> int:
    from simulation import CommunitySim, load_scenario

    sim = CommunitySim.fresh(random_seed=ns.seed)
    if ns.scenario:
        path = SCENARIOS / f"{ns.scenario}.json"
        if not path.is_file():
            print(f"Scenario not found: {path}", file=sys.stderr)
            return 2
        sim.apply_policy(load_scenario(path))

    bridge = None
    if not ns.no_llm:
        try:
            from gemma_bridge import bridge_from_env

            bridge = bridge_from_env()
        except Exception as exc:  # noqa: BLE001
            print(f"Warning: LLM disabled ({exc}). Use --no-llm to silence.", file=sys.stderr)
            bridge = None

    rng = random.Random(ns.day_seed)
    for _ in range(ns.days):
        sim.step_day(
            bridge,
            rng=rng,
            max_reason_llm=ns.max_llm,
            dialogue_pairs=ns.pairs,
            llm_workers=ns.workers,
        )

    if ns.out:
        ns.out.write_text(json.dumps(sim.history, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Wrote {ns.out} ({len(sim.history)} days)")
    else:
        if sim.history:
            m = sim.history[-1].get("metrics", {})
            print(json.dumps(m, indent=2))
        print(f"Completed {ns.days} simulated day(s); calendar day index = {sim.day}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Community Pulse CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="Simulate N days")
    run.add_argument("--days", type=int, default=1)
    run.add_argument(
        "--scenario",
        type=str,
        default=None,
        help="JSON stem in scenarios/ (e.g. close_library)",
    )
    run.add_argument("--no-llm", action="store_true", help="Heuristics only (no Ollama)")
    run.add_argument("--max-llm", type=int, default=10, help="Max agents to query per day")
    run.add_argument("--pairs", type=int, default=2, help="Dialogue pairs per day")
    run.add_argument("--workers", type=int, default=4, help="Thread pool size for LLM")
    run.add_argument(
        "--seed",
        type=int,
        default=None,
        help="RNG seed for initial social graph only",
    )
    run.add_argument(
        "--day-seed",
        type=int,
        default=0,
        dest="day_seed",
        help="RNG seed for within-day sampling (dialogue pairs)",
    )
    run.add_argument("--out", type=Path, default=None, help="Write full history JSON")
    run.set_defaults(_handler=_cmd_run)

    ns = parser.parse_args(argv)
    handler = getattr(ns, "_handler", None)
    if handler is None:
        parser.print_help()
        return 1
    return handler(ns)


if __name__ == "__main__":
    raise SystemExit(main())
