# Community Pulse — 3-Minute Video Script

**Target length:** 2:55–3:00 (Kaggle limit 3:00)
**Tone:** Quiet, confident, slightly cinematic. No hype.
**Music:** Soft instrumental, lower for VO clarity.
**Model name on screen:** `Gemma 4 / E4B` (per Kaggle naming guidelines).

---

## SHOT-BY-SHOT

### 0:00 – 0:15 · Hook (real stake)
**VISUAL:** Drone shot of a small Sichuan town at dawn. A library marquee reads "暂停服务 / Service Suspended."
**TEXT OVERLAY:** "Last month, this library closed. Nobody knows what it cost the community."
**VO:**
> "When a town loses its library, or its clinic, or its only fiber line for a week — what *actually* happens to the people who live there?"

### 0:15 – 0:45 · Problem (3 quiet beats)
**VISUAL:** Three quick cuts —
1. A mayor staring at a spreadsheet.
2. An NGO director on a phone call.
3. A school principal at midnight, head in hands.
**TEXT OVERLAY (each beat):** "No A/B test." · "No control town." · "No reset button."
**VO:**
> "Most policy decisions are made without rehearsal. There is no A/B test for closing a library, no control town for an outage. The cost of being wrong is paid in stress, isolation, and lost trust — and it is paid mostly by the people the policy was meant to help."

### 0:45 – 1:30 · The product (live demo)
**VISUAL:** Screen recording of Streamlit app at 1.5× speed.
- Click "Load Scenario → Internet Outage."
- Run "Day 1." Ten agent cards animate in a NetworkX graph; Plotly time-series begins.
- A speech bubble pops from "Anxious Shopkeeper": *"I can't take WeChat Pay today. Old Mr. Hu left without paying — I let him."*
**VO:**
> "Community Pulse runs on your laptop, offline. You inject a policy. Ten resident archetypes — the busy parent, the isolated elder, the curious teenager — react in character, talk to each other in pairs, and update a small social graph. After three simulated days, you get a readout: how stress moved, how trust moved, how cohesion moved."

### 1:30 – 2:15 · The technical novelty (Gemma 4 + Mini-Cerome)
**VISUAL:** Split screen.
- Left: a numeric panel showing one agent's L1 (dopamine 0.4, cortisol 0.7) → drives (safety 0.71, fairness 0.42).
- Right: the actual Gemma 4 prompt being constructed with those numbers injected.
- Then: the Gemma 4 output streaming in.
**TEXT OVERLAY:** "Gemma 4 (E4B) via Ollama, 100% local."
**VO:**
> "What makes this more than a chatbot trench coat: every agent has a four-layer personality vector — neurochemistry, drives, working state, relationships — that we maintain in code. Those numbers go into the Gemma 4 prompt as hard constraints. Without this layer, the same agent's stated drives drift 8× more between days. With it, the anxious shopkeeper stays anxious."

### 2:15 – 2:45 · Numbers + range
**VISUAL:** A clean comparison chart. Three policies, three resilience indexes (real LLM-enabled runs):
- Close library: **0.65 ↓**
- Add clinic: **0.70 ≈** (cohesion neutral; upside in long run)
- Internet outage (3d): **0.63 ↓↓**
**TEXT OVERLAY:** "Same engine, four reproducible runs (`seed=42`, 3 days each)."
**VO:**
> "Same seed, four scenarios, fully reproducible. Closing the library knocks resilience from 0.70 down to 0.65; a 72-hour internet outage costs another 0.07; adding a clinic is short-term neutral for cohesion. These are pre-flight checks — not predictions about your specific town, but signals telling you which decisions deserve a real ethnographic visit *before* you sign them."

### 2:45 – 3:00 · Close
**VISUAL:** Cora's face on camera, soft natural light, calm.
**TEXT OVERLAY (lower third):** "Community Pulse · Apache 2.0 · github.com/corazeng/community-pulse"
**VO:**
> "Community Pulse runs on a single laptop, no cloud, no data leaving the room. The whole engine is open source. We built it because the people most affected by policy are the ones least represented in the rooms where policy is decided. Gemma 4 helps us put a small population back in that room."
**FINAL FRAME:** Logo + URL + "Made for the Gemma 4 Good Hackathon · 2026."

---

## PRODUCTION NOTES

| Item | Plan |
|------|------|
| Drone shot | Stock footage (Pexels/Pixabay free) — Chinese small-town dawn |
| Streamlit demo | Pre-record with `--seed 42 --no-llm` *first* (fast), then re-record with Gemma 4 enabled and overlay Gemma's actual streaming output |
| Voice | Cora's own voice, English with light Mandarin accent — adds authenticity to "Sichuan town" framing |
| Music | YouTube Audio Library royalty-free; suggest "Solitude" or "Quiet Reflection" |
| Captions | English burned-in (judges multilingual), CC track for Mandarin |
| Cover image | Single still: Streamlit graph view with one agent's prompt + Gemma 4 output side-by-side, pink/lavender accents matching cora.zone palette |
| Length budget | Rehearse VO at ~150 wpm = 450 words for 3:00; current draft is ~430 words |

## ALTERNATIVE 90-SECOND CUT (for social)
Drop the live demo (0:45–1:30) and the technical split-screen (1:30–2:15). Keep only Hook → Problem → 1 metric → Close.
