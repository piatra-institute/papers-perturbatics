"""Figures for *Perturbatics*. Each reads the results dict from ``analyses.run()``
and writes one PNG. No data are recomputed here."""
from __future__ import annotations

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

INK = "#1a1a1a"
AGENT = "#1f4e79"      # the goal-directed / agentic reading
PASSIVE = "#b3202c"    # the passive / null reading
NEUTRAL = "#6a6a6a"
GRID = "#d9d9d9"


def _style(ax) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(INK)
    ax.tick_params(colors=INK, labelsize=9)
    ax.grid(True, color=GRID, linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)


def plot_separation(results: dict, path: str) -> None:
    sep = results["_sep"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.2, 3.7), sharey=True)
    # bins span the data so no shipped score falls outside the panel
    scores = (sep["_probe_planner"] + sep["_probe_passive"] + sep["_probe_reactive"]
              + sep["_rest_planner"] + sep["_rest_passive"] + sep["_rest_reactive"])
    lim = max(90.0, float(np.ceil(max(abs(min(scores)), abs(max(scores))) / 10) * 10))
    bins = np.linspace(-lim, lim, 31)

    a1.hist(sep["_rest_passive"], bins=bins, color=PASSIVE, alpha=0.6, label="route script")
    a1.hist(sep["_rest_planner"], bins=bins, color=AGENT, alpha=0.6, label="goal planner")
    # the reactive controller coincides with the others where trajectories are
    # identical, so it is drawn as an outline on top rather than a filled bar
    a1.hist(sep["_rest_reactive"], bins=bins, histtype="step", color=INK,
            lw=1.4, label="reactive (outline)")
    a1.axvline(0, color=NEUTRAL, lw=0.9)
    a1.set_title(f"at rest: every pairwise AUROC = {results['separation']['auroc_at_rest']:.2f}",
                 fontsize=10, color=INK)
    a1.set_xlabel("agency evidence (log Bayes factor)")
    a1.set_ylabel("episodes")
    a1.legend(frameon=False, fontsize=8.5, loc="upper left")

    a2.hist(sep["_probe_passive"], bins=bins, color=PASSIVE, alpha=0.6, label="route script")
    a2.hist(sep["_probe_planner"], bins=bins, color=AGENT, alpha=0.6, label="goal planner")
    a2.hist(sep["_probe_reactive"], bins=bins, histtype="step", color=INK,
            lw=1.4, label="reactive (outline)")
    a2.axvline(0, color=NEUTRAL, lw=0.9)
    a2.set_title(f"under the battery: planner vs script AUROC = {results['separation']['auroc_under_probe']:.2f}",
                 fontsize=10, color=INK)
    a2.set_xlabel("agency evidence (log Bayes factor)")
    for ax in (a1, a2):
        _style(ax)
    fig.suptitle("the same systems: indistinguishable at rest, separated by the battery",
                 fontsize=11, color=INK, y=1.02)
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


CAP = "#2a9d8f"        # realized-capacity share


def plot_realization_map(results: dict, path: str) -> None:
    rm = results["realization_map"]
    phiE, phiC, L = rm["evidence_map"], rm["capacity_map"], rm["legibility"]
    comps = list(phiE.keys())
    x = np.arange(len(comps))
    labels = [c.replace("_", "\n") for c in comps]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.8, 3.9),
                                 gridspec_kw={"width_ratios": [1.55, 1]})

    w = 0.38
    a1.bar(x - w / 2, [phiE[c] for c in comps], w, color=AGENT, label=r"evidence  $\phi^E$")
    a1.bar(x + w / 2, [phiC[c] for c in comps], w, color=CAP, label=r"capacity  $\phi^C$")
    a1.axhline(0, color=INK, lw=0.8)
    a1.set_xticks(x)
    a1.set_xticklabels(labels, fontsize=8)
    a1.set_ylabel("normalized contribution")
    a1.set_title("what shows agency vs what realizes it", fontsize=10, color=INK)
    a1.legend(frameon=False, fontsize=8.5, loc="upper right")

    colors = [PASSIVE if L[c] > 0.15 else NEUTRAL for c in comps]
    a2.bar(x, [L[c] for c in comps], 0.62, color=colors)
    a2.axhline(0, color=INK, lw=0.8)
    a2.set_xticks(x)
    a2.set_xticklabels(labels, fontsize=8)
    a2.set_ylabel(r"legibility  $L = \phi^E - \phi^C$")
    a2.set_title("agency theater", fontsize=10, color=INK)
    a2.annotate("persona:\nevidence, no capacity", xy=(5, L["persona"]), xytext=(1.9, 0.17),
                fontsize=8, color=PASSIVE,
                arrowprops=dict(arrowstyle="->", color=PASSIVE, lw=0.8))
    for ax in (a1, a2):
        _style(ax)
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_guards(results: dict, path: str) -> None:
    bs = results["boundary_sweep"]
    rg = results["richness_guard"]["systems"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.4, 3.8))

    names = [b[0] for b in bs]
    vals = [b[1] for b in bs]
    a1.plot(range(len(names)), vals, "o-", color=AGENT, lw=1.8, ms=6)
    a1.axhline(0, color=NEUTRAL, lw=0.9)
    a1.set_xticks(range(len(names)))
    a1.set_xticklabels(names, fontsize=8)
    a1.set_ylabel("realized capacity of the enclosed unit")
    a1.set_title("the reading depends on the declared boundary", fontsize=10, color=INK)

    for name, (cx, ay) in rg.items():
        col = PASSIVE if name in ("route_script", "chaotic") else AGENT
        a2.scatter([cx], [ay], s=60, color=col, zorder=3)
        a2.annotate(name.replace("_", " "), xy=(cx, ay), xytext=(4, 4),
                    textcoords="offset points", fontsize=8, color=INK)
    a2.axhline(0, color=NEUTRAL, lw=0.9)
    a2.set_xlabel("trajectory complexity (bits)")
    a2.set_ylabel("agency evidence")
    a2.set_title("richness does not track agency",
                 fontsize=10, color=INK)
    for ax in (a1, a2):
        _style(ax)
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
