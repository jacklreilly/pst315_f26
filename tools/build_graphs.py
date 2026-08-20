"""Generate example bar graphs that follow the PST 315 graphing guidelines:
bar graph; <=5 bars vertical / >=6 horizontal; everything solid black; all text
Times New Roman 12pt; bold title and axis titles; y-axis starts at 0; outside-end
data labels; 'n=' under the title; major outside tick marks; no chart border."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams
import swco_data as d

rcParams["font.family"] = "Times New Roman"
rcParams["font.size"] = 12
rcParams["axes.linewidth"] = 1.2

OUT = os.path.join(os.path.dirname(__file__), "..", "guidelines", "images")

def bar(spec, fname, ylabel="Percentage", figsize=(6.5, 4.4)):
    cats, vals, n = spec["cats"], spec["vals"], spec["n"]
    horizontal = len(cats) >= 6
    fig, ax = plt.subplots(figsize=figsize, dpi=200)
    if horizontal:
        ax.barh(cats[::-1], vals[::-1], color="black")
        ax.set_xlabel(ylabel, fontweight="bold", fontsize=12)
        ax.set_ylabel(spec["xlabel"], fontweight="bold", fontsize=12)
        ax.set_xlim(0, max(vals) * 1.18)
        for i, v in enumerate(vals[::-1]):
            ax.text(v + max(vals) * 0.02, i, f"{v}%", va="center", fontsize=12)
        ax.xaxis.set_major_formatter(lambda x, p: f"{int(x)}%")
    else:
        ax.bar(cats, vals, color="black", width=0.6)
        ax.set_ylabel(ylabel, fontweight="bold", fontsize=12)
        ax.set_xlabel(spec["xlabel"], fontweight="bold", fontsize=12)
        ax.set_ylim(0, max(100, max(vals) * 1.25))
        for i, v in enumerate(vals):
            ax.text(i, v + max(vals) * 0.03, f"{v}%", ha="center", fontsize=12)
        ax.yaxis.set_major_formatter(lambda x, p: f"{int(x)}%")

    ax.set_title(f"{spec['title']}\n(n={n})", fontweight="bold", fontsize=12, pad=12)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)          # no chart border
    for s in ("left", "bottom"):
        ax.spines[s].set_color("black")
    ax.tick_params(direction="out", length=5, width=1.2, colors="black", labelsize=12)
    fig.tight_layout()
    p = os.path.join(OUT, fname)
    fig.savefig(p, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  wrote {fname}")

if __name__ == "__main__":
    bar(d.F1, "ex-finding1-coaches.png")
    bar(d.F2, "ex-finding2-engagement-by-site.png")
    bar(d.F3, "ex-finding3-improvements.png", figsize=(7.2, 4.6))
