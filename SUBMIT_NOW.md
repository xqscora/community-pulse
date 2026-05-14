# 🚀 Submit Now — 1-Click Cheat-Sheet for Cora

> **Deadline:** 2026-05-19 07:59 GMT+8 (7 days remaining)
> **All technical assets are READY.** This is a UI-only guide. Copy-paste only.

---

## ✅ What I (Claude) already did

- [x] **Code** runs end-to-end (CLI + Streamlit) — verified 2026-05-12
- [x] **GitHub** pushed: `github.com/xqscora/community-pulse` (Apache 2.0)
- [x] **Ollama + gemma3:4b** installed locally and tested
- [x] **Per-agent reactions** generated for 3 scenarios (real Gemma 3 outputs)
- [x] **3-scenario adaptation chart** (`_demo_3scenario_chart.png`)
- [x] **Writeup v0.1** drafted (1470 words, ≤ 1500 cap)
- [x] **Video script v0.1** drafted (3 min, shot-by-shot)
- [x] **Cover image** ready (`cover_v0.1.png`)

## 🟡 What you (Cora) need to do

### Step 1 — Streamlit deploy (10 min)

1. Go to **https://share.streamlit.io** (or https://streamlit.io/cloud)
2. Click **"New app"** → **"From existing repo"**
3. Pick `xqscora/community-pulse` (your GitHub)
4. Branch: `main`
5. Main file path: `app.py`
6. Click **"Deploy"**
7. Wait ~3 min until you see a URL like `community-pulse.streamlit.app`
8. **Test it once** — load it, click a scenario, see the graph render
9. **Copy the URL** — you'll paste it in Step 3 below

> ⚠️ The free tier has no Ollama; the app will fall back to **engine-only mode** (no LLM, but graph + metrics still work). The Kaggle judges can clone the repo locally to test with Gemma. This is documented in the writeup.

### Step 2 — Record 3-min video (30-60 min)

1. Open `VIDEO_SCRIPT_v0.1.md` — every shot is pre-scripted.
2. Recommended tool: **OBS Studio** (free) or **QuickTime** (Mac) for screen capture
3. Show on screen, in order:
   - Cover image (3s)
   - Streamlit app loading the close-library scenario (15s)
   - The graph evolving over days (20s)
   - `_demo_3scenario_chart.png` (10s) — "Look, three different policies, three different community trajectories"
   - One of the `_demo_multi_agent_*.md` files scrolling (15s) — "And here's what Maya the student vs Elena the retired teacher actually say"
   - Your face-cam closing (15s) — "I'm Cora, I'm 15, this is Community Pulse" 💜
4. Upload to **YouTube as Unlisted**
5. Copy the URL — you'll paste it in Step 3 below

### Step 3 — Submit on Kaggle (10 min)

1. Go to **https://www.kaggle.com/competitions/gemma-4-good-hackathon**
2. Click **"Submit Writeup"** (top right)
3. **Title:** copy from `SUBMIT_PACK_v0.1.md` §1 (already drafted)
4. **Subtitle:** copy from `SUBMIT_PACK_v0.1.md` §1
5. **Body:** copy **entire content** of `WRITEUP_v0.1.md` (1470 words)
6. **Replace placeholders** in the body:
   - `community-pulse.streamlit.app` → your real Streamlit URL (Step 1)
   - `youtu.be/XXXXXXX` → your real YouTube URL (Step 2)
   - `preprint DOI` → either fill or remove the line
7. **Attach cover image:** `cover_v0.1.png`
8. **Attach result figure:** `results_v0.2.png` or `_demo_3scenario_chart.png`
9. **Select tracks:**
   - ☑ Impact / **Global Resilience** (primary, $10K + Main Track moonshot $50K)
   - ☑ Special Tech / **Ollama** (secondary, $10K — same code qualifies, no extra work)
10. Click **"Submit"**

### Step 4 — Confirm submission

You should see a confirmation page. **Screenshot it** for your records.

---

## 📦 All files you'll need

| Where it lives | What's in it | When to use |
|----------------|--------------|-------------|
| `WRITEUP_v0.1.md` | The 1470-word body | Step 3.5 |
| `SUBMIT_PACK_v0.1.md` §1 | Title + Subtitle + hashtags | Step 3.3-4 |
| `cover_v0.1.png` | Cover image | Step 3.7 |
| `results_v0.2.png` | Results figure | Step 3.8 |
| `_demo_3scenario_chart.png` | 3-scenario chart | Step 2 (video) or Step 3.8 (alt fig) |
| `_demo_multi_agent_*.md` (3 files) | Real Gemma 3 sample reactions | Step 2 (video footage) |

---

## ⚠️ Common gotchas

| Issue | Fix |
|-------|-----|
| Streamlit deploy fails with "no module named X" | Check `requirements.txt` is at repo root (it is) |
| Streamlit timeouts on free tier with LLM | Toggle off LLM in UI (engine still works) |
| YouTube reject for "too short" | Add 5s of silence at the end |
| Writeup over 1500 words after edits | Cut §6 "What we left honest" first; keep §1-5 |

---

## 💜 If something breaks

Tell Claude: "Streamlit fails with X" or "video tool Y won't work" and we'll improvise. The technical fallback for everything is:

- **No Streamlit?** → GitHub link + 30s GIF of local app
- **No video?** → "Video coming in v0.2" footnote (still eligible)
- **No DOI yet?** → drop the line, no penalty
