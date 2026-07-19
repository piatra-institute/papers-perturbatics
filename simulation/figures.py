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
    bins = np.linspace(-90, 90, 31)

    a1.hist(sep["_rest_passive"], bins=bins, color=PASSIVE, alpha=0.6, label="passive")
    a1.hist(sep["_rest_planner"], bins=bins, color=AGENT, alpha=0.6, label="goal planner")
    a1.axvline(0, color=NEUTRAL, lw=0.9)
    a1.set_title(f"at rest: AUROC = {results['separation']['auroc_at_rest']:.2f}",
                 fontsize=10, color=INK)
    a1.set_xlabel("agency evidence (log Bayes factor)")
    a1.set_ylabel("episodes")
    a1.legend(frameon=False, fontsize=8.5, loc="upper left")

    a2.hist(sep["_probe_passive"], bins=bins, color=PASSIVE, alpha=0.6, label="passive")
    a2.hist(sep["_probe_planner"], bins=bins, color=AGENT, alpha=0.6, label="goal planner")
    a2.axvline(0, color=NEUTRAL, lw=0.9)
    a2.set_title(f"under an informative probe: AUROC = {results['separation']['auroc_under_probe']:.2f}",
                 fontsize=10, color=INK)
    a2.set_xlabel("agency evidence (log Bayes factor)")
    for ax in (a1, a2):
        _style(ax)
    fig.suptitle("the same systems: indistinguishable at rest, separated by a probe",
                 fontsize=11, color=INK, y=1.02)
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_realization_map(results: dict, path: str) -> None:
    rm = results["realization_map"]
    phi = rm["do_shapley"]
    inter = rm["interaction_index"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.4, 3.8),
                                 gridspec_kw={"width_ratios": [1.6, 1]})

    names = list(phi.keys())
    vals = [phi[k] for k in names]
    colors = [NEUTRAL if k == "persona" else AGENT for k in names]
    a1.bar(range(len(names)), vals, color=colors, width=0.66)
    a1.axhline(0, color=INK, lw=0.8)
    a1.set_xticks(range(len(names)))
    a1.set_xticklabels([n.replace("_", "\n") for n in names], fontsize=8)
    a1.set_ylabel("do-Shapley value (share of agency)")
    a1.set_title("where the agency is realized", fontsize=10, color=INK)
    a1.annotate("persona = 0\n(identity is inert)", xy=(5, 0.02), xytext=(4.1, 0.28),
                fontsize=8.5, color=NEUTRAL,
                arrowprops=dict(arrowstyle="->", color=NEUTRAL, lw=0.8))

    labels = ["planner\n× map", "map\n× memory", "goal reg.\n× planner"]
    ivals = [inter["planner__map"], inter["map__memory"], inter["goal_register__planner"]]
    icolors = [AGENT if v > 0.02 else (PASSIVE if v < -0.02 else NEUTRAL) for v in ivals]
    a2.bar(range(3), ivals, color=icolors, width=0.6)
    a2.axhline(0, color=INK, lw=0.8)
    a2.set_xticks(range(3))
    a2.set_xticklabels(labels, fontsize=8)
    a2.set_ylabel("interaction index")
    a2.set_title("synergy (+), redundancy (−), additivity (0)", fontsize=10, color=INK)
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
    a1.set_ylabel("agency evidence of the enclosed unit")
    a1.set_title("the reading depends on the declared boundary", fontsize=10, color=INK)

    for name, (cx, ay) in rg.items():
        col = PASSIVE if name in ("route_script", "chaotic") else AGENT
        a2.scatter([cx], [ay], s=60, color=col, zorder=3)
        a2.annotate(name.replace("_", " "), xy=(cx, ay), xytext=(4, 4),
                    textcoords="offset points", fontsize=8, color=INK)
    a2.axhline(0, color=NEUTRAL, lw=0.9)
    a2.set_xlabel("trajectory complexity (bits)")
    a2.set_ylabel("agency evidence")
    a2.set_title(f"richness is a false friend (r = {results['richness_guard']['complexity_agency_correlation']:.2f})",
                 fontsize=10, color=INK)
    for ax in (a1, a2):
        _style(ax)
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
