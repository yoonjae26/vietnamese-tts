"""Render the README charts (light + dark SVG) from the result files.

    python docs/assets/make_charts.py

Palette: one blue hue in two steps (this repo's own systems vs. others), validated as an ordinal
ramp against both surfaces. Text uses neutral ink, never the series colour.
"""

import json
import os
import random
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "training" / "translit"))
sys.path.insert(0, str(ROOT / "src"))

THEMES = {
    "light": {
        "hi": "#256abf", "lo": "#86b6ef", "ink": "#0b0b0b", "ink2": "#52514e",
        "grid": "#e4e3df", "surface": "#fcfcfb",
    },
    "dark": {
        "hi": "#5598e7", "lo": "#184f95", "ink": "#ffffff", "ink2": "#c3c2b7",
        "grid": "#2e2e2c", "surface": "#1a1a19",
    },
}  # fmt: skip

plt.rcParams.update(
    {
        "svg.fonttype": "none",
        "font.family": ["Inter", "Segoe UI", "Helvetica Neue", "Arial", "DejaVu Sans", "sans-serif"],
        "font.size": 11,
    }
)


def style_axes(ax, t, grid_axis):
    ax.set_facecolor("none")
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(t["grid"])
    ax.tick_params(which="both", colors=t["ink2"], length=0)
    ax.grid(axis=grid_axis, color=t["grid"], linewidth=0.8)
    ax.set_axisbelow(True)


def rounded_barh(ax, y, width, height, color, t):
    """Horizontal bar anchored at 0 with softly rounded corners and a surface gap."""
    ax.add_patch(
        FancyBboxPatch(
            (0, y - height / 2),
            width,
            height,
            boxstyle="round,pad=0,rounding_size=0.12",
            mutation_aspect=1 / 60,
            facecolor=color,
            edgecolor=t["surface"],
            linewidth=1.5,
        )
    )


def save(fig, name, mode):
    fig.savefig(OUT / f"{name}-{mode}.svg", transparent=True, bbox_inches="tight", pad_inches=0.15)
    preview = os.environ.get("CHART_PREVIEW_DIR")  # PNG on the page background, preview only
    if preview:
        bg = "#ffffff" if mode == "light" else "#0d1117"
        fig.savefig(Path(preview) / f"{name}-{mode}.png", facecolor=bg, dpi=110, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)


def chart_tts():
    data = json.loads((ROOT / "results" / "tts.json").read_text(encoding="utf-8"))["engines"]
    short = {
        "indextts2": "IndexTTS-2", "f5": "F5-TTS", "vieneu": "VieNeu-TTS v3 Turbo", "piper": "Piper (CPU)",
        "mms": "MMS (Meta)", "vixtts": "viXTTS", "viettts": "VietTTS",
    }  # fmt: skip
    offsets = {
        "indextts2": (-8, 8, "right"), "f5": (9, -9, "left"), "vieneu": (-10, 11, "right"), "piper": (8, -4, "left"),
        "mms": (8, -4, "left"), "vixtts": (8, -2, "left"), "viettts": (-8, 6, "right"),
    }  # fmt: skip
    for mode, t in THEMES.items():
        fig, ax = plt.subplots(figsize=(8, 4))
        style_axes(ax, t, "both")
        for r in data:
            e = r["engine"]
            x, y = r["rtf"], 100 * r["overall"]["wer"]
            # One colour for every point: none of these TTS models is ours, so none is highlighted.
            ax.scatter(x, y, s=90, color=t["hi"], edgecolor=t["surface"], linewidth=2, zorder=3)
            dx, dy, ha = offsets[e]
            ax.annotate(short[e], (x, y), xytext=(dx, dy), textcoords="offset points", ha=ha, va="center",
                        color=t["ink"], fontsize=10.5)  # fmt: skip
        ax.set_xscale("log")
        ax.set_xlim(0.008, 2.2)
        ax.set_ylim(0, 13.5)
        ax.set_xticks([0.01, 0.03, 0.1, 0.3, 1])
        ax.set_xticklabels(["0.01", "0.03", "0.1", "0.3", "1"])
        ax.axvline(1, color=t["ink2"], linewidth=0.8, linestyle=(0, (3, 3)))
        ax.text(1.05, 12.9, "real time", color=t["ink2"], fontsize=9.5, va="top")
        ax.set_xlabel("Real-time factor on one H200, log scale  (← faster)", color=t["ink2"])
        ax.set_ylabel("Word error rate, %  (↓ clearer)", color=t["ink2"])
        ax.set_title("Intelligibility vs. speed, 50 Vietnamese sentences", loc="left", color=t["ink"],
                     fontsize=13, fontweight="bold", pad=12)  # fmt: skip
        save(fig, "tts", mode)


def chart_normalization():
    res = json.loads((ROOT / "results" / "normalization_heldout_v2.json").read_text(encoding="utf-8"))["summary"]
    names = {
        "vitts + translit (ours)": "vitts 0.2 + transliteration (this repo)",
        "vietnormalizer": "vietnormalizer",
        "vitts (ours)": "vitts 0.2, rules only (this repo)",
        "soe-vinorm": "soe-vinorm",
        "vinorm": "vinorm",
    }
    rows = sorted(((names[k], v["ALL"]["accuracy"], k) for k, v in res.items() if k in names), key=lambda r: r[1])
    for mode, t in THEMES.items():
        fig, ax = plt.subplots(figsize=(8, 2.9))
        style_axes(ax, t, "x")
        for i, (_label, acc, key) in enumerate(rows):
            best = key == "vitts + translit (ours)"
            rounded_barh(ax, i, 100 * acc, 0.62, t["hi"] if best else t["lo"], t)
            ax.text(100 * acc + 1.2, i, f"{acc:.0%}", va="center", color=t["ink"], fontsize=10.5,
                    fontweight="bold" if best else "normal")  # fmt: skip
        ax.set_yticks(range(len(rows)))
        ax.set_yticklabels([r[0] for r in rows], color=t["ink"])
        ax.set_xlim(0, 100)
        ax.set_ylim(-0.6, len(rows) - 0.4)
        ax.set_xlabel("Sentences normalized exactly right, %", color=t["ink2"])
        ax.set_title("Text normalization, held-out v2 (60 sentences)", loc="left", color=t["ink"], fontsize=13,
                     fontweight="bold", pad=12)  # fmt: skip
        save(fig, "normalization", mode)


def chart_translit():
    from eval_reviewed_models import accepted_sets
    from prepare_data import clean_target

    acc = accepted_sets()
    words = sorted(acc)
    preds = json.loads((ROOT / "data/translit/review/predictions.json").read_text(encoding="utf-8"))
    systems = [
        ("gpt-4o-mini_few-shot", "gpt-4o-mini, few-shot (API)"),
        ("gold", "Training dictionary itself"),
        ("vitts", "vitts translit, 5.6M params (this repo)"),
        ("qwen2.5-7b_few-shot", "Qwen2.5-7B-Instruct, few-shot"),
        ("vietnormalizer_rules", "vietnormalizer rules"),
    ]
    rng = random.Random(0)
    rows = []
    for key, label in systems:
        c = [clean_target(preds[w][key]) in acc[w] for w in words]
        boots = sorted(sum(rng.choice(c) for _ in c) / len(c) for _ in range(5000))
        rows.append((label, sum(c) / len(c), boots[125], boots[4875], key))
    rows.reverse()
    for mode, t in THEMES.items():
        fig, ax = plt.subplots(figsize=(8, 2.9))
        style_axes(ax, t, "x")
        for i, (_label, p, lo, hi, key) in enumerate(rows):
            best = key == "vitts"
            rounded_barh(ax, i, 100 * p, 0.62, t["hi"] if best else t["lo"], t)
            ax.plot([100 * lo, 100 * hi], [i, i], color=t["ink2"], linewidth=1.6, solid_capstyle="round", zorder=4)
            ax.text(100 * hi + 1.2, i, f"{p:.0%}", va="center", color=t["ink"], fontsize=10.5,
                    fontweight="bold" if best else "normal")  # fmt: skip
        ax.set_yticks(range(len(rows)))
        ax.set_yticklabels([r[0] for r in rows], color=t["ink"])
        ax.set_xlim(0, 50)
        ax.set_ylim(-0.6, len(rows) - 0.4)
        ax.set_xlabel(f"Readings accepted by a blind native reviewer, % of {len(words)} words (line = 95% CI)",
                      color=t["ink2"])  # fmt: skip
        ax.set_title("Loanword transliteration, human-judged", loc="left", color=t["ink"], fontsize=13,
                     fontweight="bold", pad=12)  # fmt: skip
        save(fig, "translit", mode)


if __name__ == "__main__":
    chart_tts()
    chart_normalization()
    chart_translit()
    print("\n".join(sorted(p.name for p in OUT.glob("*.svg"))))
