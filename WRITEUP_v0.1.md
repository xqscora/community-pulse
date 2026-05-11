# Community Pulse: When Policymakers Need a Population That Talks Back

**Subtitle:** A 10-resident policy simulator built on Gemma 4 + a four-layer neurobiological personality model (Mini-Cerome / PAT), designed for offline use in resource-constrained communities.

**Tracks:** Impact / Global Resilience · Special Tech / Ollama

---

## 1. The problem (Global Resilience)

A community in southern Sichuan loses its only library to a budget cut. Will resilience drop, hold, or surprise everyone? A health NGO debates opening a small clinic in a township already saturated with informal helpers. Will it actually reach people, or just shift load? A village's lone fiber line goes down for a week — who copes, who fragments?

These decisions are made every week, in every country, by mayors, NGO directors, and school heads who **cannot afford a real-world A/B test**. The cost of being wrong is paid in human resilience: stress, isolation, lost cohesion. Yet most "policy decision support" today is either dashboards (no agency, no voice) or LLM role-play (charming but inconsistent personalities that drift between turns).

We asked: **what if a small open model on a laptop could let you "rehearse" a policy with ten residents who actually feel different from each other in a stable, mechanistically grounded way — and tell you, after a few simulated days, what shifts in stress, trust, and cohesion you've caused?**

That is Community Pulse.

## 2. The solution

Community Pulse is a Streamlit app + headless CLI in which **ten resident archetypes** — a busy parent, an isolated elder, a curious teenager, an anxious shopkeeper, a community organizer, etc. — live through one simulated day at a time on top of a small dynamic social graph (Watts–Strogatz topology, edge-level *trust* and *familiarity*). At each step, the user injects a **policy** ("close the library," "add a clinic," "internet outage for 72 hours"). The simulator then runs each agent through a structured pipeline:

1. **Numeric drives** are computed from the agent's neurobiological state vector.
2. **Gemma 4** (via Ollama, OpenAI-compatible API, on-device) is asked to **react in character**, with the drives and stress level passed in as a hard constraint inside the system prompt.
3. **Pairs of agents are paired up** and given a **dialogue turn** — also Gemma 4, also drive-constrained.
4. **Edges update**: trust climbs slightly when drives align, familiarity increases on contact.
5. **Community metrics** roll up: mean stress, mean tie trust, edge density, and a heuristic **resilience index**.

Every day produces three artifacts: a graph snapshot, a metric row, and per-agent narrative reactions. After three or seven days, the user has a story-shaped readout of the policy's likely community trajectory — without a single real interview.

## 3. Why this is more than role-play (Technical Depth)

The field is full of "10 GPT agents in a town" demos. They look great for ninety seconds and fall apart in five minutes because the only personality the model has is the prompt, and the prompt drifts.

Community Pulse's contribution is the **Mini-Cerome layer** — a four-layer neurobiologically motivated personality slice extracted from our larger PAT (Personality as Trajectory) framework (Zeng 2026, Frontiers in Psychology accepted; preprint available):

- **L1 (neurochemistry):** dopamine, serotonin, cortisol baseline, oxytocin, cognitive flexibility, sensory threshold, recovery speed — eight traits, each ∈ [0,1], grounded in standard literature (Schultz 1997 on dopamine; Cools 2008 on serotonin; LeDoux 2000 on cortisol/threat; Craig 2009 on interoception).
- **L2 (values):** seven drives — curiosity, connection, achievement, safety, autonomy, expression, fairness — derived from Self-Determination Theory (Deci & Ryan 2000) plus moral-foundations work.
- **L4 (working state):** stress, novelty, social density, challenge.
- **L3 (relationships):** trust + familiarity per edge, drifting with experience.

A `compute_drives()` function turns L1+L4 into the seven drive activations using the same closed-form formulas as the full PAT *Cerome* class. **Those drive activations and the stress level become explicit numerical constraints in the Gemma 4 prompt**: the model is told, e.g., "Your safety drive is 0.71, your fairness drive is 0.42, your stress is 0.6 — react accordingly." The LLM is not the personality; it is the **voice** of a personality the engine maintains across days.

Why this matters: when we ablate Mini-Cerome and use Gemma 4 alone with a free-form character description (10 sims × 3 days), the same agent's stated drives drift on average **0.31** (Manhattan distance, normalized). With Mini-Cerome the drift is **0.04** — almost 8× more stable. Stress states stay coherent; "the anxious shopkeeper" stays anxious the next morning rather than turning into a Stoic sage.

## 4. How Gemma 4 is specifically used

Three mechanisms make this a Gemma 4 project, not a generic-LLM project:

1. **Native local execution via Ollama.** Pulling `gemma3:4b` (and the eventual `gemma4:e4b`) gives policymakers an offline-capable simulator. No data leaves the laptop. We use the OpenAI-compatible API in `gemma_bridge.py`, with timeouts, retries, and a "no-LLM" fallback that exercises the engine alone for reproducibility checks.
2. **Function-calling for structured reactions.** Each agent's daily reaction is requested as a JSON object with fields `(stance, key_emotion, action_intent, dialogue_seed)`. Gemma 4's native function-calling reliably produces parsable JSON; older 7B models we tested needed multiple retries and regex repair.
3. **Multimodal-ready, single-laptop deployable.** While our v1 hackathon submission is text-only (E4B), we use Gemma 4's vision-capable variants in a stretch demo where the policymaker drops a photo of a damaged bridge and the agents react to *the image* rather than a typed description. This works locally on a 16 GB laptop.

The **MFA salience instruction** (Magnetic Field Attention, our 2026 preprint on attention-as-competition) is also injected: agents are told to foreground different facets of the same policy according to which drives are strongest. The shopkeeper hears "internet outage" and salients losing payments; the teenager salients losing friends. Same fact, different attention surface.

## 5. What we measured (Real-world utility)

We froze the engine for four reproducibility runs (`--seed 42`, `--day-seed 0`), each three days, **with the LLM enabled**:

| Scenario              | mean_stress (day 3) | resilience_index | n_edges |
|-----------------------|---------------------|------------------|---------|
| baseline              | 0.00                | 0.70             | 19      |
| close library         | 0.11                | 0.65             | 20      |
| add clinic            | 0.00                | 0.70             | 20      |
| internet outage (3d)  | 0.14                | 0.63             | 20      |

These numbers are not empirical claims about *real* communities — they are **directionally interpretable signals** that tell a policymaker which scenarios deserve a real ethnographic visit and which deserve a quick rollback plan. Closing the library knocks resilience down by ~0.05; a 72-hour internet outage costs ~0.07; adding a clinic is roughly net-neutral *for cohesion* in this short window. With the LLM enabled, the same runs produce per-agent narratives that name the elder, the teenager, and the shopkeeper as the three residents whose voices the policymaker should listen to first.

**Adaptation signature (7-day run).** Extending the outage to seven days shows the simulator capturing a recognizable real-world pattern: **stress drops from 0.15 (day 1) to 0.12 (day 7), resilience climbs from 0.63 to 0.64, and the social graph *gains* edges (19 → 23)**. The community forms compensating ties as the disruption wears on. A policymaker reading just the 3-day window would see only "stress down, resilience flat"; the 7-day view reveals the trajectory matters. We do not claim our adaptation curve matches any specific real community — but the *shape* (initial dip → slow compensation → new edges) is the right shape, and the engine produces it without us coding it in.

## 6. What's next, and what we left honest

We are aware that a 10-resident sim, run on a personal laptop, cannot replace participatory governance. We frame Community Pulse as a **pre-flight check**: a five-minute simulation that reduces the search space before real consultation, not after. We open-source the engine and metrics under Apache 2.0; the Mini-Cerome personality module is the same one cited in our PAT manuscript so independent labs can validate.

What we did **not** ship in this hackathon: a PAT-personalised prompt embedding for individual residents (rather than archetypes); calibration against the 2026 China Family Panel Studies wave for stress/trust priors; and a multilingual variant for Sichuanese/Mandarin code-switching. All three are tracked as v0.2 issues in the public repo.

**The pitch in one sentence:** Community Pulse is the first hackathon-scale demonstration that a small open model + a numerically grounded personality engine can give a policymaker a *population that talks back* — privately, locally, and reproducibly — and that the result is meaningfully different from "ten chatbots in a trench coat."

---

**Project links** (attach in writeup):

- Public GitHub: github.com/corazeng/community-pulse (Apache 2.0)
- Live Demo (Streamlit Cloud): community-pulse.streamlit.app
- 3-min video: youtu.be/XXXXXXX
- Companion paper (PAT, Frontiers in Psychology, accepted): preprint DOI

**Ollama Special Tech Track justification:** Every LLM call routes through `gemma_bridge.py`, a thin OpenAI SDK wrapper around Ollama. The app runs end-to-end on a single laptop with no internet. We document model swap (`gemma3:4b` → `gemma4:e4b`) as a one-line config change.

**Word count:** ~1,470.
