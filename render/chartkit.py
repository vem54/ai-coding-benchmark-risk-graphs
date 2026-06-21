"""
chartkit.py — shared "Editorial Light" style system for the benchmark-risk charts.

Design language: warm off-white canvas, near-black ink, a single red->stone risk
ramp, one slate accent. Left-aligned title + deck, hairline grid, source footer.
Typeface: IBM Plex Sans (prose / labels) + IBM Plex Mono (numerals / source line).

Intended to read cleanly on a light Substack/editorial page.
"""
from __future__ import annotations
import glob
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.colors import LinearSegmentedColormap, to_rgba

# --------------------------------------------------------------------------- #
# Fonts
# --------------------------------------------------------------------------- #
# Font lookup is portable: env override -> bundled render/fonts -> ~/fonts.
_HERE = os.path.dirname(os.path.abspath(__file__))
_FONT_DIRS = [
    os.environ.get("CHART_FONT_DIR", ""),
    os.path.join(_HERE, "fonts"),
    "/home/claude/fonts",
]
_loaded = 0
for _dir in _FONT_DIRS:
    if _dir and os.path.isdir(_dir):
        for _f in glob.glob(os.path.join(_dir, "*.ttf")):
            fm.fontManager.addfont(_f); _loaded += 1
        if _loaded:
            break
if not _loaded:
    print("[chartkit] warning: IBM Plex fonts not found — run render/fetch_fonts.sh; "
          "falling back to DejaVu Sans.")

SANS = "IBM Plex Sans"
MONO = "IBM Plex Mono"

# --------------------------------------------------------------------------- #
# Palette  (Editorial Light)
# --------------------------------------------------------------------------- #
INK        = "#1A1A18"   # primary text
INK_SOFT   = "#57564E"   # secondary text / axis titles
MUTE       = "#8A887E"   # tertiary text / quadrant tags
HAIRLINE   = "#E4E0D6"   # gridlines / rules
PAGE       = "#FAFAF7"   # warm off-white canvas
PANEL      = "#FAFAF7"   # plot area (seamless with page)

RISK       = "#B23A20"   # benchmark-gaming risk (brick red)
RISK_DK    = "#8E2E18"
GEN        = "#33536B"   # raw coding generalization (slate blue)
GOOD       = "#3E6B52"   # positive-gap accent (muted green)

# Sequential ramp for risk magnitude: light stone -> deep brick red.
RISK_RAMP = LinearSegmentedColormap.from_list(
    "risk_ramp",
    ["#E7E1D4", "#E2B79C", "#D08454", "#BF5630", "#A4331C", "#7E2614"],
)

# --------------------------------------------------------------------------- #
# Global rcParams
# --------------------------------------------------------------------------- #
def apply_rc():
    plt.rcParams.update({
        "figure.facecolor":  PAGE,
        "axes.facecolor":    PANEL,
        "savefig.facecolor": PAGE,
        "font.family":       SANS,
        "font.size":         13,
        "text.color":        INK,
        "axes.edgecolor":    HAIRLINE,
        "axes.labelcolor":   INK_SOFT,
        "xtick.color":       INK_SOFT,
        "ytick.color":       INK_SOFT,
        "xtick.labelcolor":  INK_SOFT,
        "ytick.labelcolor":  INK_SOFT,
        "axes.linewidth":    1.0,
        "xtick.major.size":  0,
        "ytick.major.size":  0,
        "svg.fonttype":      "path",      # outline text -> SVGs render anywhere
        "figure.dpi":        200,
    })

# --------------------------------------------------------------------------- #
# Header / footer helpers (figure-coordinate text blocks)
# --------------------------------------------------------------------------- #
def header(fig, title, deck, x=0.045, top=0.945):
    """Left-aligned editorial title block with a short red accent rule."""
    # accent rule
    fig.lines.append(plt.Line2D(
        [x, x + 0.038], [top + 0.052, top + 0.052],
        transform=fig.transFigure, color=RISK, lw=3.2, solid_capstyle="butt",
    ))
    fig.text(x, top, title, ha="left", va="top",
             fontsize=21, fontweight="bold", color=INK, family=SANS)
    fig.text(x, top - 0.062, deck, ha="left", va="top",
             fontsize=12.5, color=INK_SOFT, family=SANS)


def footer(fig, source=None, note=None, x=0.045, y=0.040):
    """Source line (mono, small) bottom-left, optional italic note above it."""
    if not (source or note):
        return
    # hairline rule separating footer from plot
    fig.lines.append(plt.Line2D(
        [x, 0.955], [y + 0.066, y + 0.066], transform=fig.transFigure,
        color=HAIRLINE, lw=0.8,
    ))
    if note:
        fig.text(x, y + 0.030, note, ha="left", va="bottom",
                 fontsize=10.5, color=INK_SOFT, family=SANS, style="italic")
    if source:
        fig.text(x, y, source, ha="left", va="bottom",
                 fontsize=9.5, color=MUTE, family=MONO)


def despine(ax, keep=("bottom",)):
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(side in keep)
    for side in keep:
        ax.spines[side].set_color(HAIRLINE)


def tint(hex_color, amount):
    """Mix a colour toward white by `amount` (0..1)."""
    r, g, b, _ = to_rgba(hex_color)
    return (r + (1 - r) * amount, g + (1 - g) * amount, b + (1 - b) * amount)
