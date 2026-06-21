"""
make_charts.py — rebuild the three benchmark-risk charts in the Editorial Light
style. Reads data/scorecard.csv; writes <root>/0N_*.png and 0N_*.svg.

Charts:
  01  Risk vs raw coding generalization  (quadrant scatter, size = confidence)
  02  Highest benchmark-gaming risk      (ranked horizontal bars)
  03  Risk vs generalization gap         (dumbbell / connected-dot plot)
"""
from __future__ import annotations
import os, sys
sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

import chartkit as ck

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "scorecard.csv")
ck.apply_rc()

SOURCE = "Source: scorecard.csv · methodology.md · run 2026-06-21 · n = 10 labs"
CAVEAT = "Benchmark-gaming risk is an evidence-based estimate, not proof of intent or misconduct."

df = pd.read_csv(DATA)
df = df.rename(columns={
    "benchmark_gaming_risk_0_100": "risk",
    "raw_coding_generalization_0_100": "gen",
    "confidence_0_100": "conf",
})
df["gap"] = df["gen"] - df["risk"]
RISK_NORM = Normalize(vmin=30, vmax=78)   # shared ramp domain across charts


def save(fig, stem):
    for ext in ("png", "svg"):
        fig.savefig(os.path.join(ROOT, f"{stem}.{ext}"),
                    dpi=200, bbox_inches=None, pad_inches=0)
    plt.close(fig)
    print("wrote", stem + ".png / .svg")


# --------------------------------------------------------------------------- #
# 01 — Risk vs generalization scatter
# --------------------------------------------------------------------------- #
def chart_scatter():
    fig = plt.figure(figsize=(11.6, 7.9))
    ax = fig.add_axes([0.075, 0.17, 0.895, 0.595])

    d = df.copy()
    x, y, conf = d["risk"].values, d["gen"].values, d["conf"].values

    # medians -> quadrant crosshair
    mx, my = np.median(x), np.median(y)
    ax.axvline(mx, color=ck.HAIRLINE, lw=1.2, zorder=1)
    ax.axhline(my, color=ck.HAIRLINE, lw=1.2, zorder=1)

    # confidence -> marker area
    s = 170 + (conf - 58) / (86 - 58) * (560 - 170)
    ax.scatter(x, y, s=s, c=x, cmap=ck.RISK_RAMP, norm=RISK_NORM,
               edgecolor="white", linewidth=1.6, zorder=4, alpha=0.96)

    # direct labels (hand-tuned offsets to avoid collisions)
    off = {
        "DeepSeek": (0, -3.0, "center", "top"),
        "Moonshot / Kimi": (3.4, 0.4, "left", "center"),
        "Z.ai / Zhipu": (3.0, 1.6, "left", "bottom"),
        "MiniMax": (-3.2, 1.6, "right", "bottom"),
        "xAI": (0, -3.0, "center", "top"),
        "Alibaba / Qwen": (-3.2, 0.0, "right", "center"),
        "Meta": (3.2, 0.6, "left", "center"),
        "Google DeepMind": (-3.4, -1.2, "right", "top"),
        "OpenAI": (3.2, -0.4, "left", "center"),
        "Anthropic": (0.2, 2.7, "center", "bottom"),
    }
    short = {"Moonshot / Kimi": "Kimi", "Z.ai / Zhipu": "Z.ai",
             "Alibaba / Qwen": "Qwen", "Google DeepMind": "Google"}
    for _, r in d.iterrows():
        dx, dy, ha, va = off[r["lab"]]
        ax.annotate(short.get(r["lab"], r["lab"]),
                    (r["risk"], r["gen"]), (r["risk"] + dx, r["gen"] + dy),
                    ha=ha, va=va, fontsize=12, color=ck.INK,
                    fontweight="medium", zorder=5)

    # quadrant pole tags (corners, just inside the frame)
    ax.text(27.2, 94.2, "LOWER RISK · STRONGER GENERALIZATION", fontsize=9.5,
            color=ck.GOOD, family=ck.SANS, fontweight="medium", va="top")
    ax.text(79.8, 54.2, "HIGHER RISK · WEAKER GENERALIZATION", fontsize=9.5,
            color=ck.RISK, family=ck.SANS, fontweight="medium",
            ha="right", va="bottom")

    # confidence size legend (top-right empty quadrant)
    lx = 71.5
    for i, cv in enumerate([86, 72, 58]):
        ly = 90.0 - i * 3.4
        sz = 170 + (cv - 58) / (86 - 58) * (560 - 170)
        ax.scatter([lx], [ly], s=sz, facecolor="none",
                   edgecolor=ck.MUTE, linewidth=1.3, zorder=3)
        ax.text(lx + 2.4, ly, f"{cv}", fontsize=10.5, family=ck.MONO,
                color=ck.INK_SOFT, va="center")
    ax.text(lx - 0.4, 93.4, "CONFIDENCE", fontsize=9.5, family=ck.SANS,
            color=ck.MUTE, fontweight="medium", va="top", ha="center")

    ax.set_xlim(26.5, 80.5); ax.set_ylim(53, 95)
    ax.set_xticks(range(30, 81, 10)); ax.set_yticks(range(55, 96, 5))
    ck.despine(ax, keep=("bottom", "left"))
    ax.grid(axis="y", color=ck.HAIRLINE, lw=0.7, zorder=0)
    ax.tick_params(labelsize=11)
    ax.set_xlabel("Benchmark-gaming risk  (0–100)", fontsize=12.5, color=ck.INK_SOFT, labelpad=8)
    ax.set_ylabel("Raw coding generalization  (0–100)", fontsize=12.5, color=ck.INK_SOFT, labelpad=8)
    for lbl in ax.get_xticklabels() + ax.get_yticklabels():
        lbl.set_family(ck.MONO)

    ck.header(fig,
              "Frontier coding labs: benchmark-gaming risk vs real-world generalization",
              "Each bubble is a lab's best current coding model · bubble size = evidence confidence",
              top=0.905)
    ck.footer(fig, SOURCE, note=CAVEAT)
    save(fig, "01_risk_vs_generalization")


# --------------------------------------------------------------------------- #
# 02 — Highest risk ranking
# --------------------------------------------------------------------------- #
def chart_ranking():
    fig = plt.figure(figsize=(11.6, 8.0))
    ax = fig.add_axes([0.165, 0.155, 0.74, 0.61])

    d = df.sort_values("risk").reset_index(drop=True)   # ascending -> highest on top
    short = {"Moonshot / Kimi": "Kimi", "Z.ai / Zhipu": "Z.ai",
             "Alibaba / Qwen": "Qwen", "Google DeepMind": "Google"}
    names = [short.get(n, n) for n in d["lab"]]
    yp = np.arange(len(d))

    # faint reference gridlines
    for gx in (20, 40, 60, 80):
        ax.axvline(gx, color=ck.HAIRLINE, lw=0.7, zorder=0)

    for yi, r in zip(yp, d.itertuples()):
        col = ck.RISK_RAMP(RISK_NORM(r.risk))
        ax.barh(yi, r.risk, height=0.66, color=col, zorder=3,
                edgecolor=ck.PAGE, linewidth=0.5)
        ax.text(r.risk + 1.4, yi, f"{r.risk}", va="center", ha="left",
                family=ck.MONO, fontsize=13.5, fontweight="bold", color=ck.INK)
        ax.text(r.risk + 6.0, yi, f"conf {r.conf}", va="center", ha="left",
                family=ck.MONO, fontsize=10, color=ck.MUTE)

    ax.set_yticks(yp); ax.set_yticklabels(names, fontsize=13, color=ck.INK)
    ax.set_xlim(0, 100); ax.set_ylim(-0.7, len(d) - 0.3)
    ax.set_xticks(range(0, 101, 20))
    for lbl in ax.get_xticklabels():
        lbl.set_family(ck.MONO); lbl.set_fontsize(11)
    ck.despine(ax, keep=("bottom",))
    ax.tick_params(axis="y", pad=8)
    ax.set_xlabel("Benchmark-gaming risk score  (0–100)", fontsize=12.5, color=ck.INK_SOFT, labelpad=8)

    ck.header(fig,
              "Where benchmark-gaming risk is highest",
              "Risk drivers: public/private score gaps · saturated public benchmarks · sparse private evidence · scaffold dependence",
              top=0.905)
    ck.footer(fig, SOURCE, note=CAVEAT)
    save(fig, "02_highest_risk_ranking")


# --------------------------------------------------------------------------- #
# 03 — Risk vs generalization gap (dumbbell)
# --------------------------------------------------------------------------- #
def chart_gap():
    fig = plt.figure(figsize=(11.6, 8.0))
    ax = fig.add_axes([0.165, 0.155, 0.74, 0.61])

    d = df.sort_values("gap").reset_index(drop=True)     # most negative bottom-up
    short = {"Moonshot / Kimi": "Kimi", "Z.ai / Zhipu": "Z.ai",
             "Alibaba / Qwen": "Qwen", "Google DeepMind": "Google"}
    names = [short.get(n, n) for n in d["lab"]]
    yp = np.arange(len(d))

    for gx in (40, 50, 60, 70, 80, 90):
        ax.axvline(gx, color=ck.HAIRLINE, lw=0.7, zorder=0)

    for yi, r in zip(yp, d.itertuples()):
        lo, hi = min(r.risk, r.gen), max(r.risk, r.gen)
        ax.plot([lo, hi], [yi, yi], color="#CFC9BC", lw=2.6, zorder=2,
                solid_capstyle="round")
        ax.scatter(r.risk, yi, s=135, color=ck.RISK, edgecolor="white",
                   linewidth=1.5, zorder=4)
        ax.scatter(r.gen, yi, s=135, color=ck.GEN, edgecolor="white",
                   linewidth=1.5, zorder=4)
        gcol = ck.GOOD if r.gap >= 0 else ck.RISK
        ax.text(hi + 2.2, yi, f"{'+' if r.gap >= 0 else '−'}{abs(r.gap)}",
                va="center", ha="left", family=ck.MONO, fontsize=12,
                fontweight="bold", color=gcol)

    # direct-label the two series on the top row
    top = d.iloc[-1]
    ax.annotate("benchmark-gaming risk", (top.risk, yp[-1]),
                (top.risk, yp[-1] + 0.48), ha="center", va="bottom",
                fontsize=10.5, color=ck.RISK, fontweight="medium")
    ax.annotate("raw coding generalization", (top.gen, yp[-1]),
                (top.gen, yp[-1] + 0.48), ha="center", va="bottom",
                fontsize=10.5, color=ck.GEN, fontweight="medium")

    ax.set_yticks(yp); ax.set_yticklabels(names, fontsize=13, color=ck.INK)
    ax.set_xlim(30, 97); ax.set_ylim(-0.7, len(d) + 0.1)
    ax.set_xticks(range(30, 91, 10))
    for lbl in ax.get_xticklabels():
        lbl.set_family(ck.MONO); lbl.set_fontsize(11)
    ck.despine(ax, keep=("bottom",))
    ax.tick_params(axis="y", pad=8)
    ax.set_xlabel("Score  (0–100)", fontsize=12.5, color=ck.INK_SOFT, labelpad=8)

    ck.header(fig,
              "The gap between real coding skill and benchmark-gaming risk",
              "Labs sorted by gap (generalization − risk). Positive = capability outruns risk; negative = risk outruns demonstrated skill.",
              top=0.905)
    ck.footer(fig, SOURCE, note=CAVEAT)
    save(fig, "03_risk_generalization_gap")


if __name__ == "__main__":
    chart_scatter()
    chart_ranking()
    chart_gap()
    print("done")
