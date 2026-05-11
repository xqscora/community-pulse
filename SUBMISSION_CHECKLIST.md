# Gemma 4 Good Hackathon — Submission Checklist

**Deadline:** May 19, 2026 07:59 GMT+8 (≈ 11 days)
**Tracks targeted:** Impact / **Global Resilience** ($10K) + Special Tech / **Ollama** ($10K) + Main Track moonshot ($50K-1st)

---

## 📋 Required artifacts

| # | Artifact | Status | Owner | Path |
|---|----------|--------|-------|------|
| 1 | Kaggle Writeup (≤1500 words) | ✅ v0.1 drafted | Cora | `WRITEUP_v0.1.md` |
| 2 | YouTube video (≤3 min) | 🟡 script v0.1 | Cora | `VIDEO_SCRIPT_v0.1.md` |
| 3 | Public Code Repository | 🟡 needs publish | Cora | `github.com/xqscora/community-pulse` (TODO) |
| 4 | Live Demo URL | 🟡 needs deploy | Cora | Streamlit Cloud or HuggingFace Space |
| 5 | Cover image | ⬜ not started | Cora | TBD |
| 6 | Track selection | ⬜ pick at submit | Cora | Global Resilience |

---

## 🚀 Day-by-day execution plan (11 days)

### Day 1 (today, May 8) — pre-flight
- [x] Verify CLI runs end-to-end (done: `cli.py run --days 3 --no-llm` ✅)
- [x] Draft writeup v0.1 (done)
- [x] Draft video script v0.1 (done)
- [ ] **Sleep before continuing** — it's 03:30 AM

### Day 2 (May 9)
- [ ] Read writeup with fresh eyes; tighten to ≤1500 words
- [ ] Run 3 scenario seeds with **Gemma 4 enabled** end-to-end (Ollama running)
- [ ] Capture metric tables and per-agent narratives for the video

### Day 3 (May 10)
- [ ] Create public GitHub repo `xqscora/community-pulse`
  - Apache 2.0 LICENSE
  - README badge: `Made for Gemma 4 Good Hackathon 2026`
  - Strip any accidental private notes from `paper-PAT/` parent
- [ ] Push current code (already MIT-clean per quick scan)

### Day 4 (May 11)
- [ ] Deploy Streamlit Cloud demo
  - Use `--no-llm` mode by default (cloud has no Ollama); button to "connect local Ollama"
  - Or: HuggingFace Space with `gemma-3-4b-it` weights bundled
- [ ] Test demo URL renders without login

### Day 5–6 (May 12–13)
- [ ] **Record video** (the 30-point lever)
  - Drone stock footage: Pexels search "small Chinese town dawn"
  - Pre-record Streamlit demo at `--seed 42`
  - Re-record with Ollama on (Gemma 4 streaming)
  - Edit in DaVinci Resolve (free) or CapCut
  - YouTube upload as **Unlisted** until submission day → flip Public

### Day 7 (May 14)
- [ ] Cover image (single still)
  - Concept: Streamlit graph + Gemma prompt + Gemma output, side-by-side, pink/lavender on white
  - Tool: Figma or Canva, 1280×720 minimum

### Day 8 (May 15)
- [ ] Create Kaggle Writeup draft (paste from `WRITEUP_v0.1.md`)
- [ ] Attach video link, repo link, demo URL, cover image
- [ ] Select Track: **Impact / Global Resilience**
- [ ] Save (do not submit yet)

### Day 9 (May 16) — buffer / fix bugs
- [ ] End-to-end dry run: judge persona reads writeup → clicks video → clicks repo → clicks demo
- [ ] Fix anything that broke

### Day 10 (May 17)
- [ ] **Submit on Kaggle** (early, not at deadline)
- [ ] Verify all attachments live + accessible without login

### Day 11 (May 18) — final check
- [ ] One last verification all links work
- [ ] Tweet / cora.zone link (after submit)

---

## 🎯 Track selection logic

We can only pick **one** Track when submitting the Writeup. Recommendation: **Impact / Global Resilience**.

Why:
- Community Pulse explicitly outputs a `resilience_index` metric
- Global Resilience is one of 5 Impact subtracks → $10K; less crowded than Health
- Main Track + Special Tech (Ollama) eligibility is **automatic**, not by selection

So we get up to 3 prize chances from one writeup:
1. Main Track placement (1st-4th: $10K-$50K)
2. Impact / Global Resilience: $10K
3. Special Tech / Ollama: $10K

**Stretch goal:** $70K. **Floor goal:** $10K (one Impact track).

---

## 🔍 Last-minute guardrails

- [ ] No private filenames/paths leaked in the public repo (`grep -r "D:/me/其他/性格"` → none should remain)
- [ ] No personal contact info in the code (use `hello@cora.zone` only)
- [ ] No reference to private Aura/Cerome paper drafts that aren't on arXiv yet
- [ ] All scenario JSON files use synthetic names (no real towns)
- [ ] License: Apache 2.0 (matches PAT manuscript)

---

## 🧊 Honest risk assessment

| Risk | Mitigation |
|------|-----------|
| Judges treat sim as toy | Lead with 8× drift-stability ablation in writeup |
| Streamlit demo fails on judge's browser | Pre-rendered 30s GIF as fallback in cover |
| Gemma 4 model name not yet on Ollama | Use `gemma3:4b` + document one-line swap |
| Video looks AI-generated / low effort | Cora face-cam in close (last 15s) — humanizes |
| Word count over 1500 | Currently ~1470, leave room for 1-2 polish edits |

💜 The real bet here is that Cora's PAT manuscript work + her actual coding (already done) + her writing voice = a hackathon submission that reads like real research, not vibe-coded slop. That's the moat.
