"""Generate a chart from the 3-scenario demo runs for video / Streamlit screenshot."""
import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

scenarios = {
    "close_library": ("Close library", "#e57373"),
    "add_clinic": ("Add clinic", "#81c784"),
    "internet_outage": ("Internet outage", "#ffb74d"),
}

fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), sharey=False)

for ax, (scen, (label, color)) in zip(axes, scenarios.items()):
    path = Path(f"_demo_{scen}_7d.json")
    if not path.exists():
        continue
    with open(path) as f:
        days = json.load(f)
    day_nums = [d.get("day", i + 1) for i, d in enumerate(days)]
    # Average stress per day across agents
    mean_stress = []
    mean_novelty = []
    for d in days:
        agents = d.get("agents", [])
        stress_vals = [a.get("L4", {}).get("stress", 0) for a in agents if isinstance(a, dict)]
        nov_vals = [a.get("L4", {}).get("novelty", 0) for a in agents if isinstance(a, dict)]
        mean_stress.append(np.mean(stress_vals) if stress_vals else 0)
        mean_novelty.append(np.mean(nov_vals) if nov_vals else 0)
    ax.plot(day_nums, mean_stress, marker="o", color=color, linewidth=2.2, label="mean stress")
    ax.plot(day_nums, mean_novelty, marker="s", color="#90a4ae", linewidth=1.6, alpha=0.7, linestyle="--", label="mean novelty")
    ax.set_title(label, fontsize=13)
    ax.set_xlabel("Day")
    ax.set_ylim(0, 1)
    ax.grid(alpha=0.3)
    ax.legend(loc="best", fontsize=9)

axes[0].set_ylabel("Community signal (0-1)")
fig.suptitle("Community Pulse: 7-day adaptation across 3 policy scenarios", fontsize=14)
fig.tight_layout()
out = "_demo_3scenario_chart.png"
fig.savefig(out, dpi=140, bbox_inches="tight")
print(f"Wrote {out}")
