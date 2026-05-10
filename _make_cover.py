"""Cover image for Gemma 4 Hackathon — Community Pulse.

Style: Cora's palette (light pink / lavender on white), serif title,
two-panel layout: left = social graph, right = drives → Gemma prompt.
1280x720 minimum (Kaggle requirement).
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import networkx as nx
import numpy as np

PINK = '#F8C8DC'
LAV = '#C8B8E6'
PINK_DEEP = '#E68FB0'
LAV_DEEP = '#9B7CC4'
INK = '#2A2A33'
SUB = '#6B6B7A'

fig = plt.figure(figsize=(12.8, 7.2), dpi=150, facecolor='white')

# ===== Header =====
fig.text(0.5, 0.92, 'Community Pulse',
         ha='center', fontsize=42, fontfamily='serif',
         fontweight='bold', color=INK)
fig.text(0.5, 0.86, 'A 10-resident policy simulator on Gemma 4 + Mini-Cerome',
         ha='center', fontsize=15, fontfamily='serif',
         style='italic', color=SUB)

# ===== Left panel: social graph =====
ax_graph = fig.add_axes([0.04, 0.12, 0.48, 0.66])
ax_graph.set_facecolor('white')
G = nx.watts_strogatz_graph(10, 4, 0.3, seed=7)
pos = nx.spring_layout(G, seed=11, k=0.8)
edge_weights = np.random.RandomState(7).uniform(0.3, 1.0, G.number_of_edges())
node_stress = np.random.RandomState(13).uniform(0.0, 0.6, 10)

# Edges with varying alpha (familiarity)
for (u, v), w in zip(G.edges(), edge_weights):
    x = [pos[u][0], pos[v][0]]
    y = [pos[u][1], pos[v][1]]
    ax_graph.plot(x, y, color=LAV_DEEP, alpha=0.25 + 0.5 * w, lw=1 + 1.5 * w, zorder=1)

# Nodes: pink for low stress, deep pink for high
for n, (x, y) in pos.items():
    s = node_stress[n]
    color = PINK if s < 0.2 else PINK_DEEP if s > 0.4 else '#F4A8C8'
    ax_graph.scatter([x], [y], s=900 + 600 * s, c=color,
                     edgecolors=INK, linewidths=1.2, zorder=2)
    ax_graph.text(x, y, str(n + 1), ha='center', va='center',
                  fontsize=10, fontweight='bold', color=INK, zorder=3)

archetypes = ['Parent', 'Elder', 'Teen', 'Shopkeeper', 'Organizer',
              'Worker', 'Teacher', 'Healer', 'Newcomer', 'Skeptic']
ax_graph.text(0.5, -0.15,
              ' · '.join(archetypes),
              transform=ax_graph.transAxes, ha='center', fontsize=8,
              color=SUB, style='italic')
ax_graph.set_title('10 residents on a Watts-Strogatz social graph',
                   fontsize=13, color=INK, pad=10, fontfamily='serif')
ax_graph.set_xticks([]); ax_graph.set_yticks([])
for spine in ax_graph.spines.values():
    spine.set_visible(False)

# ===== Right panel: drives → Gemma prompt =====
ax_prompt = fig.add_axes([0.56, 0.12, 0.42, 0.66])
ax_prompt.set_facecolor('white')
ax_prompt.set_xlim(0, 1); ax_prompt.set_ylim(0, 1)
ax_prompt.set_xticks([]); ax_prompt.set_yticks([])
for spine in ax_prompt.spines.values():
    spine.set_visible(False)

# Drives bars
drives = [('safety', 0.71), ('fairness', 0.42), ('connection', 0.55),
          ('autonomy', 0.30), ('curiosity', 0.18), ('expression', 0.22),
          ('achievement', 0.34)]
y0 = 0.92
for i, (name, val) in enumerate(drives):
    y = y0 - i * 0.07
    ax_prompt.barh(y, val * 0.5, height=0.04, left=0.05, color=LAV_DEEP, alpha=0.7)
    ax_prompt.text(0.04, y, name, ha='right', va='center',
                   fontsize=10, color=INK, fontfamily='serif')
    ax_prompt.text(0.06 + val * 0.5 + 0.01, y, f'{val:.2f}',
                   va='center', fontsize=9, color=SUB)

# Arrow
ax_prompt.annotate('', xy=(0.5, 0.42), xytext=(0.5, 0.46),
                   arrowprops=dict(arrowstyle='->', color=PINK_DEEP, lw=2))

# Gemma 4 prompt box
prompt_box = patches.FancyBboxPatch(
    (0.05, 0.05), 0.9, 0.32,
    boxstyle="round,pad=0.02", linewidth=1.2,
    edgecolor=PINK_DEEP, facecolor=PINK, alpha=0.25)
ax_prompt.add_patch(prompt_box)
prompt_text = (
    "Gemma 4 system prompt:\n"
    "  You are the Anxious Shopkeeper.\n"
    "  Safety drive 0.71, fairness 0.42, stress 0.6.\n"
    "  Today the village internet is down for the\n"
    "  third day. React in one paragraph, then\n"
    "  return JSON {stance, key_emotion,\n"
    "  action_intent, dialogue_seed}."
)
ax_prompt.text(0.07, 0.34, prompt_text, fontsize=8.5,
               color=INK, family='monospace',
               verticalalignment='top')

ax_prompt.set_title('Numerical drives → constrained Gemma 4 prompt',
                    fontsize=13, color=INK, pad=10, fontfamily='serif')

# ===== Footer =====
fig.text(0.04, 0.04, 'Tracks: Impact / Global Resilience  ·  Special Tech / Ollama',
         fontsize=10, color=SUB, fontfamily='serif')
fig.text(0.96, 0.04, 'Apache 2.0  ·  cora.zone',
         fontsize=10, color=PINK_DEEP, ha='right', fontfamily='serif',
         fontweight='bold')

# Decorative accents
fig.add_artist(plt.Rectangle((0, 0.985), 1, 0.015, color=PINK,
                              transform=fig.transFigure))
fig.add_artist(plt.Rectangle((0, 0), 1, 0.015, color=LAV,
                              transform=fig.transFigure))

plt.savefig('cover_v0.1.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print('Saved cover_v0.1.png')
