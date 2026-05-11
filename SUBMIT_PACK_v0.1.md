# Submit Pack — Community Pulse · Gemma 4 Good Hackathon

> Copy-paste pack for every form field you'll need on submit day (May 17–18).
> Everything in here is finalized prose — don't redraft, just paste.

---

## 1. Kaggle Writeup form (the main submission page)

### Title (≤120 chars)
```
Community Pulse: A 10-resident policy simulator for offline, on-device Gemma 4 deployment
```

### Subtitle / tagline (one line)
```
A pre-flight check for community policy decisions, powered by Gemma 4 + a four-layer neurobiological personality engine.
```

### Tracks to select
- ✅ **Impact / Global Resilience** (primary)
- ✅ **Special Tech / Ollama** (secondary, no extra work — same Ollama wiring already in `gemma_bridge.py`)

### Hashtags / topics
```
#gemma #ollama #agent-simulation #social-impact #policy-tools #personality-modeling #streamlit #python
```

### Body
Paste the full content of `WRITEUP_v0.1.md` (§1 through §6 plus Project Links + Ollama justification block). Word count: ~1,470 / 1,500 cap.

### Attachments / images
| File | Caption on Kaggle |
|---|---|
| `cover_v0.1.png` | Cover image — pastel community graph (top of writeup) |
| `results_v0.2.png` | Figure 1: 7-day adaptation signature on internet outage scenario |

### External links field
```
GitHub:    https://github.com/xqscora/community-pulse
Live demo: https://community-pulse.streamlit.app
Video:     https://youtu.be/XXXXXXX
Paper:     https://arxiv.org/abs/XXXX.XXXXX  (PAT preprint — fill once arXiv ID is final)
```

---

## 2. Streamlit Cloud deployment (≤30 min)

### Pre-flight checklist
- [ ] `requirements.txt` lives at repo root (it does — verified)
- [ ] `app.py` is the Streamlit entry point (it is — verified)
- [ ] No private filenames in source (verified — `grep` clean)
- [ ] Free tier OK (Cerome engine fits in 1 GB RAM; LLM is optional fallback)

### Deploy steps
1. Go to https://share.streamlit.io/ → "New app"
2. Connect GitHub account `xqscora` (one-click OAuth)
3. Pick repo `community-pulse`, branch `main`, main file `app.py`
4. Advanced settings:
   - Python version: **3.11**
   - No secrets needed (engine runs LLM-free if Ollama unreachable, which it will be on Streamlit Cloud)
5. Custom subdomain: `community-pulse` → live at `https://community-pulse.streamlit.app`
6. First boot takes ~3 min while it pip-installs

### After deployment
- [ ] Open the live URL in incognito to confirm it loads cold
- [ ] Run one scenario (`close_library`, seed=42, days=3) to confirm engine works without Ollama
- [ ] Screenshot the loaded page for video B-roll
- [ ] Paste URL into Kaggle Writeup "External links" field

### If Streamlit Cloud breaks
**Fallback:** record the demo locally with Ollama running, upload the screen recording, and use a static screenshot in place of the live link. Submission is still valid — live demo is recommended, not strictly required.

---

## 3. YouTube video metadata (paste on upload day)

### Title (≤100 chars)
```
Community Pulse — a policy simulator that talks back (Gemma 4 Good Hackathon)
```

### Description
```
Community Pulse is a 10-resident policy simulator built for Gemma 4 + Ollama. Drop a policy
("close the library", "add a clinic", "internet outage for a week") and watch ten agent
archetypes — each backed by a four-layer neurobiological personality engine (Mini-Cerome) —
react in character, talk to each other, and shift a small social graph. The output is a
3- or 7-day trajectory of mean stress, tie trust, and resilience — a pre-flight check before
real consultation, runnable entirely on a laptop with no data leaving the device.

Submitted to the Gemma 4 Good Hackathon 2026.
Tracks: Impact / Global Resilience · Special Tech / Ollama.

— Code (Apache 2.0): https://github.com/xqscora/community-pulse
— Live demo:         https://community-pulse.streamlit.app
— Writeup:           [Kaggle Writeup URL]
— Companion paper:   PAT (Personality as Trajectory), Frontiers in Psychology (accepted, 2026)

Chapters
0:00 The problem
0:30 What Community Pulse does
1:00 Why it's more than role-play (the Mini-Cerome layer)
1:45 Live demo: 7-day internet outage scenario
2:30 What the numbers mean for a policymaker
2:50 Open source + what's next

#Gemma #Ollama #AIforGood #PolicySimulation #AgentBasedModeling #Streamlit
```

### Tags
```
gemma, gemma 4, ollama, agent-based modeling, policy simulation, AI for good,
community resilience, social simulation, streamlit, python, on-device AI,
personality modeling, hackathon, Cerome, PAT
```

### Thumbnail
Use `cover_v0.1.png` cropped to 16:9 (top 1950×1097 region works). Add overlay text in Canva:
- Top-left, 96pt bold: "Community Pulse"
- Bottom-left, 48pt regular: "A policy sim that talks back · Gemma 4"

### Visibility
- Upload as **Unlisted** while iterating
- Flip to **Public** the morning of May 17 (before submitting Kaggle Writeup)

---

## 4. GitHub repo settings (after `gh repo create`)

### Repo description (≤350 chars)
```
A 10-resident community policy simulator powered by Gemma 4 + a four-layer neurobiological personality engine (Mini-Cerome). Built for the Gemma 4 Good Hackathon 2026. Runs offline on a laptop via Ollama; Streamlit UI + headless CLI; Apache 2.0.
```

### Topics (GitHub tags)
```
gemma, gemma-4, ollama, agent-based-modeling, policy-simulation, social-simulation,
streamlit, python, personality-modeling, ai-for-good, hackathon
```

### Pinned README sections (already in `README.md`)
- Quickstart (uvx / pip)
- Demo GIF link (drops in once video is recorded)
- Architecture diagram pointer
- Citation block (PAT preprint)

### Branch protection
Optional — for a 7-day hackathon repo with a solo contributor, leave `main` unprotected and push directly. Add protection later if v0.2 brings collaborators.

---

## 5. Submission day final checklist (May 17 morning)

Print this and tick as you go.

- [ ] `git status` clean, latest commit pushed to `main`
- [ ] Streamlit Cloud loads at `community-pulse.streamlit.app` in incognito
- [ ] YouTube video is **Public** (not Unlisted), URL copies cleanly
- [ ] Kaggle Writeup body pasted (1,470 words, both figures attached)
- [ ] External links block filled (GitHub / Streamlit / YouTube / arXiv)
- [ ] Both tracks ticked (Impact + Special Tech / Ollama)
- [ ] Hit "Submit" → confirm submission badge appears
- [ ] Screenshot the confirmation page (defensive copy)

After submit:
- [ ] Post on `r/LocalLLaMA` and `r/MachineLearning` (one paragraph, GitHub + demo link)
- [ ] Cross-post to your own profile on Kaggle for visibility
- [ ] Sleep 💜

---

**Status as of 2026-05-11 10:40 — 7 days to deadline. All five form fields above are paste-ready.**
