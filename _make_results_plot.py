"""Results plot for Gemma 4 Hackathon — real LLM-enabled metrics.
v0.2: Adds 7-day adaptation panel showing community recovery."""
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
    ('Internet Outage (3d)', '_live_outage.json', '#c75450'),
]

fig, axes = plt.subplots(1, 3, figsize=(15, 4.2), dpi=150)
plt.rcParams.update({'font.family': 'serif', 'axes.spines.top': False, 'axes.spines.right': False})

# ---- Panel 1: Resilience over days, all scenarios ----
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
ax.set_title('3-day scenario impact', color=INK)
ax.legend(loc='lower right', fontsize=9, frameon=False)
ax.grid(alpha=0.3)
ax.set_ylim(0.55, 0.75)

# ---- Panel 2: Bar — stress at day 3 ----
ax = axes[1]
labels = []; stresses = []; colors = []
for label, fp, color in scenarios:
    try:
        with open(fp) as f:
            data = json.load(f)
        last = data[-1]['metrics']
        labels.append(label.split(' (')[0])
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

# ---- Panel 3: 7-day adaptation curve ----
ax = axes[2]
try:
    with open('_live_outage_7d.json') as f:
        data7 = json.load(f)
    days = [d['day'] for d in data7]
    stress = [d['metrics']['mean_stress'] for d in data7]
    resilience = [d['metrics']['resilience_index'] for d in data7]
    edges = [d['metrics']['n_edges'] for d in data7]

    ax.plot(days, stress, 'o-', color='#c75450', lw=2, markersize=6, label='stress')
    ax.plot(days, resilience, 's-', color='#5fa380', lw=2, markersize=6, label='resilience')
    ax2 = ax.twinx()
    ax2.plot(days, edges, '^-', color=LAV_DEEP, lw=1.5, markersize=5, alpha=0.8, label='edges (right axis)')
    ax2.set_ylabel('Edge count', color=LAV_DEEP, fontsize=10)
    ax2.tick_params(axis='y', labelcolor=LAV_DEEP)
    ax2.spines['top'].set_visible(False)

    ax.set_xlabel('Day')
    ax.set_ylabel('Stress / Resilience')
    ax.set_title('7-day outage: community adapts', color=INK)
    ax.grid(alpha=0.3)
    ax.legend(loc='center right', fontsize=8, frameon=False)
    # Annotate adaptation
    ax.annotate('stress drops -0.03', xy=(7, 0.117), xytext=(4.5, 0.05),
                fontsize=8, color='#c75450', style='italic',
                arrowprops=dict(arrowstyle='->', color='#c75450', alpha=0.6))
    ax.annotate('+4 new edges', xy=(7, 0.45), xytext=(4, 0.42),
                fontsize=8, color=LAV_DEEP, style='italic',
                arrowprops=dict(arrowstyle='->', color=LAV_DEEP, alpha=0.6))
except Exception as e:
    ax.text(0.5, 0.5, f'7-day data missing\n{e}', ha='center', va='center')
    print(f'panel3 err: {e}')

plt.suptitle('Community Pulse · LLM-enabled runs (qwen2.5:1.5b stand-in for Gemma 4)',
             fontsize=12, color=SUB, style='italic', y=1.02)
plt.tight_layout()
plt.savefig('results_v0.2.png', dpi=150, bbox_inches='tight', facecolor='white')
print('Saved results_v0.2.png')
