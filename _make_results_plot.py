"""Results plot for Gemma 4 Hackathon — real LLM-enabled metrics."""
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

PINK = '#F8C8DC'; LAV = '#C8B8E6'
PINK_DEEP = '#E68FB0'; LAV_DEEP = '#9B7CC4'
INK = '#2A2A33'; SUB = '#6B6B7A'

scenarios = [
    ('Baseline', '_live_qwen.json', '#999'),
    ('Close Library', '_live_close_library.json', PINK_DEEP),
    ('Add Clinic', '_live_add_clinic.json', '#5fa380'),
    ('Internet Outage', '_live_outage.json', '#c75450'),
]

fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), dpi=150)
plt.rcParams.update({'font.family': 'serif', 'axes.spines.top': False, 'axes.spines.right': False})

# ---- Resilience over days ----
ax = axes[0]
for label, fp, color in scenarios:
    try:
        with open(fp) as f:
            data = json.load(f)
        days = [d['day'] for d in data]
        res = [d['metrics']['resilience_index'] for d in data]
        if len(days) == 1:
            days = [0, 1]; res = res * 2
        ax.plot(days, res, 'o-', color=color, lw=2, markersize=7, label=label)
    except Exception as e:
        print(f'skip {label}: {e}')
ax.set_xlabel('Day')
ax.set_ylabel('Resilience index')
ax.set_title('Resilience trajectory across scenarios', color=INK)
ax.legend(loc='lower right', fontsize=9, frameon=False)
ax.grid(alpha=0.3)
ax.set_ylim(0.5, 0.75)

# ---- Bar: stress (day 3) ----
ax = axes[1]
labels = []
stresses = []
colors = []
for label, fp, color in scenarios:
    try:
        with open(fp) as f:
            data = json.load(f)
        last = data[-1]['metrics']
        labels.append(label)
        stresses.append(last['mean_stress'])
        colors.append(color)
    except: pass
xs = np.arange(len(labels))
ax.bar(xs, stresses, color=colors, edgecolor=INK, lw=0.7, alpha=0.85)
for i, s in enumerate(stresses):
    ax.text(i, s + 0.005, f'{s:.2f}', ha='center', fontsize=10, color=INK)
ax.set_xticks(xs)
ax.set_xticklabels(labels, fontsize=9, rotation=12, ha='right')
ax.set_ylabel('Mean stress (day 3)')
ax.set_title('Stress impact by scenario', color=INK)
ax.set_ylim(0, max(0.2, max(stresses) * 1.3))

plt.suptitle('Community Pulse · LLM-enabled runs (qwen2.5:1.5b stand-in for Gemma 4)',
             fontsize=12, color=SUB, style='italic', y=1.02)
plt.tight_layout()
plt.savefig('results_v0.1.png', dpi=150, bbox_inches='tight', facecolor='white')
print('Saved results_v0.1.png')
