"""Generate a silent screencast-style MP4 from existing assets.
Cora can then overlay her voice via OBS, or submit as-is with captions.

Style: pastel/lavender/pink, soft, cinematic.
"""
from pathlib import Path
import imageio.v3 as iio
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import textwrap, re, os

ROOT = Path(__file__).resolve().parent
W, H = 1280, 720
FPS = 24
OUT_VIDEO = ROOT / "_demo_video_v1.mp4"

# Try to find a decent font
def find_font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/calibri.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    if bold:
        candidates = [
            "C:/Windows/Fonts/segoeuib.ttf",
            "C:/Windows/Fonts/calibrib.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
        ] + candidates
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


BG = (250, 245, 252)   # very pale lavender
INK = (45, 45, 70)
ACCENT = (180, 130, 200)  # mauve
SOFT_PINK = (245, 225, 240)


def make_solid(color=BG):
    img = Image.new("RGB", (W, H), color)
    return img


def make_title(headline, subhead=None, color=INK, accent=ACCENT):
    img = make_solid()
    d = ImageDraw.Draw(img)
    f_big = find_font(60, bold=True)
    f_small = find_font(28)
    # Center headline
    bbox = d.textbbox((0, 0), headline, font=f_big)
    tw = bbox[2] - bbox[0]; th = bbox[3] - bbox[1]
    d.text(((W - tw) // 2, (H - th) // 2 - 40), headline, fill=color, font=f_big)
    if subhead:
        bbox = d.textbbox((0, 0), subhead, font=f_small)
        sw = bbox[2] - bbox[0]; sh = bbox[3] - bbox[1]
        d.text(((W - sw) // 2, (H - th) // 2 + 60), subhead, fill=accent, font=f_small)
    return img


def fit_image(path, max_w, max_h):
    im = Image.open(path).convert("RGB")
    iw, ih = im.size
    s = min(max_w / iw, max_h / ih)
    if s < 1.0:
        im = im.resize((int(iw * s), int(ih * s)), Image.LANCZOS)
    return im


def make_image_slide(img_path, caption=None):
    canvas = make_solid()
    d = ImageDraw.Draw(canvas)
    im = fit_image(img_path, W - 120, H - 200 if caption else H - 80)
    x = (W - im.width) // 2; y = (H - im.height - (60 if caption else 0)) // 2
    canvas.paste(im, (x, y))
    if caption:
        f = find_font(24)
        bbox = d.textbbox((0, 0), caption, font=f)
        cw = bbox[2] - bbox[0]
        d.text(((W - cw) // 2, y + im.height + 20), caption, fill=INK, font=f)
    return canvas


def make_text_slide(title, body_lines, accent=ACCENT):
    img = make_solid()
    d = ImageDraw.Draw(img)
    f_title = find_font(40, bold=True)
    f_body = find_font(24)
    # Title at top
    bbox = d.textbbox((0, 0), title, font=f_title)
    tw = bbox[2] - bbox[0]
    d.text(((W - tw) // 2, 50), title, fill=accent, font=f_title)
    # Soft pink box
    pad = 40
    box_top = 130
    d.rectangle([pad, box_top, W - pad, H - 60], fill=SOFT_PINK)
    # Body
    y = box_top + 30
    for line in body_lines:
        wrapped = textwrap.wrap(line, width=80)
        for w_line in wrapped:
            d.text((pad + 30, y), w_line, fill=INK, font=f_body)
            y += 34
        y += 8
    return img


def img_to_arr(im):
    return np.asarray(im, dtype=np.uint8)


def fade_pair(im_a, im_b, n_frames):
    """Crossfade between two PIL images."""
    a = img_to_arr(im_a).astype(np.float32)
    b = img_to_arr(im_b).astype(np.float32)
    for i in range(n_frames):
        t = (i + 1) / (n_frames + 1)
        m = (a * (1 - t) + b * t).astype(np.uint8)
        yield m


def hold(im, n_frames):
    arr = img_to_arr(im)
    for _ in range(n_frames):
        yield arr


# ============ Build the timeline ============

frames = []

def add(gen):
    for f in gen:
        frames.append(f)

def secs(s):
    return int(round(s * FPS))

# Slide 1: Title (3s)
slide_title = make_title("Community Pulse", "A 10-resident policy simulator")
add(hold(slide_title, secs(3)))

# Slide 2: Cover image (3s) — if exists
cover = ROOT / "cover_v0.1.png"
if cover.exists():
    slide_cover = make_image_slide(cover, "Built on Gemma 4 + Mini-Cerome (Apache 2.0)")
    add(fade_pair(slide_title, slide_cover, secs(0.5)))
    add(hold(slide_cover, secs(3)))
    last = slide_cover
else:
    last = slide_title

# Slide 3: The problem (4s)
slide_problem = make_text_slide(
    "The problem",
    [
        "A library closes. Will resilience drop?",
        "A clinic opens. Will it actually reach people?",
        "Internet goes out for 72 hours. Who fragments first?",
        "",
        "Policymakers can't afford a real-world A/B test.",
    ],
)
add(fade_pair(last, slide_problem, secs(0.5)))
add(hold(slide_problem, secs(4)))
last = slide_problem

# Slide 4: The solution (4s)
slide_solution = make_text_slide(
    "What we built",
    [
        "10 resident archetypes (parent, elder, teen, ...)",
        "Each gets a 4-layer numerical personality (Mini-Cerome)",
        "Gemma 4 reacts in character; engine keeps drives stable",
        "Daily metrics: stress, trust, resilience index",
        "",
        "Offline. On-device. Private. Reproducible.",
    ],
)
add(fade_pair(last, slide_solution, secs(0.5)))
add(hold(slide_solution, secs(4)))
last = slide_solution

# Slide 5: 3-scenario chart (5s)
chart = ROOT / "_demo_3scenario_chart.png"
if chart.exists():
    slide_chart = make_image_slide(chart, "Three policies, three community trajectories — 7-day simulation")
    add(fade_pair(last, slide_chart, secs(0.5)))
    add(hold(slide_chart, secs(5)))
    last = slide_chart

# Slide 6-8: Per-agent Gemma 3 reactions (one slide per agent)
def excerpt(md_path, agent_name):
    try:
        text = Path(md_path).read_text(encoding='utf-8')
        # find "## {agent_name}" block
        m = re.search(rf"## {re.escape(agent_name)}.*?\n(.*?)(?=\n---\n|\Z)", text, re.DOTALL)
        if not m:
            return None
        body = m.group(1).strip()
        # strip markdown bold
        body = body.replace("**", "")
        # take first 4 lines or 300 chars
        lines = [l.strip() for l in body.split("\n") if l.strip() and not l.startswith("Top drives:")][:4]
        return lines
    except Exception:
        return None

md = ROOT / "_demo_multi_agent_close_library.md"
for agent, role, drives in [
    ("Maya Chen", "high school student", "curiosity 0.74"),
    ("Elena Ruiz", "retired teacher", "social 0.64 / fairness 0.57"),
    ("Jordan Lee", "librarian", "curiosity 0.57 / fairness 0.54"),
]:
    lines = excerpt(md, agent)
    if not lines:
        lines = ["(sample missing)"]
    # truncate each line to keep slide clean
    short = []
    for l in lines:
        if len(l) > 110:
            l = l[:107] + "..."
        short.append(l)
    slide = make_text_slide(
        f"{agent} — {role}",
        [f"Top drives: {drives}", ""] + short,
    )
    add(fade_pair(last, slide, secs(0.4)))
    add(hold(slide, secs(6)))
    last = slide

# Slide 9: Why it's more than role-play (4s)
slide_tech = make_text_slide(
    "Why it's not 'ten chatbots in a trench coat'",
    [
        "Mini-Cerome: 8 neurochem traits + 7 drives + working state",
        "Drives are NUMERICAL constraints passed into every Gemma prompt",
        "Ablation: GPT alone drifts 0.31 per agent over 3 days",
        "                Community Pulse: drift 0.04 — 8x more stable",
        "",
        "Gemma 4 is the VOICE; the engine is the PERSONALITY.",
    ],
)
add(fade_pair(last, slide_tech, secs(0.5)))
add(hold(slide_tech, secs(5)))
last = slide_tech

# Slide 10: Numbers (4s)
slide_results = make_text_slide(
    "Results — 7-day adaptation signature",
    [
        "Close library:   stress +0.11, resilience -0.05, edges +1",
        "Add clinic:      stress  0.00, resilience flat,  edges +1",
        "Internet outage: stress +0.14 then DROP to 0.12 by day 7",
        "                 edges 19 -> 23 (compensating ties form)",
        "",
        "The shape of compensation emerges — we didn't code it in.",
    ],
)
add(fade_pair(last, slide_results, secs(0.5)))
add(hold(slide_results, secs(5)))
last = slide_results

# Slide 11: Closing
slide_close = make_title(
    "Community Pulse",
    "github.com/xqscora/community-pulse  ·  Apache 2.0",
)
add(fade_pair(last, slide_close, secs(0.5)))
add(hold(slide_close, secs(3)))

print(f"Total frames: {len(frames)}, duration: {len(frames)/FPS:.1f}s")
print(f"Writing {OUT_VIDEO} ...")
iio.imwrite(OUT_VIDEO, np.stack(frames), fps=FPS, codec="libx264", quality=8, macro_block_size=None)
print("Done.")
