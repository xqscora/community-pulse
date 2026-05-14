"""Generate per-agent LLM reactions for video / writeup screenshots."""
import os, sys
sys.path.insert(0, '.')
os.environ.setdefault('OLLAMA_GEMMA_MODEL', 'qwen2.5:1.5b')  # fallback
from gemma_bridge import bridge_from_env
from agents import default_archetypes

import sys as _sys
SCENARIO = _sys.argv[1] if len(_sys.argv) > 1 else "close_library"
SCENARIOS = {
    "close_library": (
        "Close public library",
        "Due to municipal budget cuts, the town's only public library will close permanently on May 20. Operating hours will be reduced over the next two weeks during a phased shutdown.",
    ),
    "internet_outage": (
        "Three-day internet outage",
        "A fiber backbone failure will cut the town's residential and business internet for at least 72 hours starting tomorrow morning. Cellular networks remain functional but will be congested. No firm restoration estimate.",
    ),
    "add_clinic": (
        "Open neighborhood clinic",
        "A new community clinic offering primary care, mental health intake, and free vaccinations will open next month in the converted post office building, staffed by two doctors and three nurses.",
    ),
}
POLICY_TITLE, POLICY_DESC = SCENARIOS[SCENARIO]

b = bridge_from_env()
agents = default_archetypes()
print(f"Model: {b.model}", flush=True)
print(f"Agents: {len(agents)}", flush=True)

out_lines = [
    "# Community Pulse — Sample Multi-Agent Reactions",
    f"\n**Model:** `{b.model}` (production target: `gemma3:4b` / `gemma4:e4b`)",
    f"\n**Policy:** {POLICY_TITLE}",
    f"\n*{POLICY_DESC}*",
    "\n---\n",
]

# Pick 3 most-different agents
sample = [agents[0], agents[1], agents[3]]  # Maya (student), Elena (elder), shopkeeper
for a in sample:
    drives = a.drives()
    top_drives = sorted(drives.items(), key=lambda kv: -kv[1])[:3]
    top_str = ", ".join(f"{k}={v:.2f}" for k, v in top_drives)
    print(f"\n=== {a.name} ({a.role}) ===", flush=True)
    print(f"Top drives: {top_str}", flush=True)
    try:
        r = b.reason_about_policy(
            agent_name=a.name, role=a.role, backstory=a.backstory,
            personality_block=a.personality_for_llm(),
            policy_title=POLICY_TITLE,
            policy_description=POLICY_DESC,
            day=1,
        )
        print(r[:200] + "...", flush=True)
        out_lines.append(f"## {a.name} — {a.role}")
        out_lines.append(f"\n**Top drives:** {top_str}\n")
        out_lines.append(r)
        out_lines.append("\n---\n")
    except Exception as e:
        print(f"failed: {e}", flush=True)

fname = f'_demo_multi_agent_{SCENARIO}.md'
with open(fname, 'w', encoding='utf-8') as f:
    f.write("\n".join(out_lines))
print(f"\nSaved {fname}")
