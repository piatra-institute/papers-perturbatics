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
ABSORB_G = "#1a7f37"   # the battery that includes a matched sham


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

    # highlight by a principled rule, not a plotting threshold: red marks the pure
    # channel, the component whose capacity share is exactly zero (dummy player)
    colors = [PASSIVE if abs(phiC[c]) < 1e-9 else NEUTRAL for c in comps]
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


SHAM = "#8a6d3b"       # the matched sham condition


def plot_sham_control(results: dict, path: str) -> None:
    sc = results["sham_control"]
    auroc = sc["auroc_reactive_vs_marker_tracker_by_probe"]
    resp = sc["mean_response_to_probe"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 3.8),
                                 gridspec_kw={"width_ratios": [1, 1.25]})

    probes = ["rest", "move", "block", "sham"]
    vals = [auroc[p] for p in probes]
    cols = [SHAM if p == "sham" else NEUTRAL for p in probes]
    a1.bar(range(len(probes)), vals, 0.6, color=cols)
    a1.axhline(0.5, color=INK, lw=0.9, ls="--")
    a1.set_xticks(range(len(probes)))
    a1.set_xticklabels(probes, fontsize=9)
    a1.set_ylim(0, 1.05)
    a1.set_ylabel("AUROC, goal tracker vs marker tracker")
    a1.set_title("the declared battery does not reach the mimic", fontsize=10, color=INK)

    systems = ["planner", "reactive", "route_script", "marker_tracker"]
    x = np.arange(len(systems))
    w = 0.38
    a2.bar(x - w / 2, [resp[s]["move"] for s in systems], w, color=AGENT,
           label="response to the moved goal")
    a2.bar(x + w / 2, [resp[s]["sham"] for s in systems], w, color=SHAM,
           label="response to the matched sham")
    # a system silent under both leaves two empty slots, which reads as missing data
    # rather than as the finding it is; say so on the panel
    for k, s in enumerate(systems):
        if resp[s]["move"] < 1e-9 and resp[s]["sham"] < 1e-9:
            a2.annotate("silent under\nboth", xy=(k, 0.02), fontsize=8, color=NEUTRAL,
                        ha="center", va="bottom")
    a2.set_xticks(x)
    a2.set_xticklabels([s.replace("_", "\n") for s in systems], fontsize=8)
    a2.set_ylim(0, 1.12)
    a2.set_ylabel("fraction of cells departing the rest path")
    a2.set_title("three ways to fail: no response, equal response, selective response",
                 fontsize=9.5, color=INK)
    a2.legend(frameon=False, fontsize=8.5, loc="upper right")
    for ax in (a1, a2):
        _style(ax)
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


HUMAN = "#6a3d9a"      # the operator, when it holds goal authority


def plot_blind_recovery(results: dict, path: str) -> None:
    br = results["blind_recovery"]
    mechs = list(br["with_sham"]["unique_recovery"])
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.4, 4.0),
                                 gridspec_kw={"width_ratios": [1.15, 1]})

    x = np.arange(len(mechs))
    w = 0.38
    a1.bar(x - w / 2, [br["without_sham"]["unique_recovery"][m] for m in mechs], w,
           color=NEUTRAL, label="battery without a sham")
    a1.bar(x + w / 2, [br["with_sham"]["unique_recovery"][m] for m in mechs], w,
           color=ABSORB_G, label="battery with a matched sham")
    a1.axhline(br["chance_level"], color=PASSIVE, ls="--", lw=1.0)
    a1.annotate("chance", (len(mechs) - 0.5, br["chance_level"] + 0.02), fontsize=8,
                color=PASSIVE, ha="right")
    a1.set_xticks(x)
    a1.set_xticklabels([m.replace("_", "\n") for m in mechs], fontsize=8)
    a1.set_ylim(0, 1.12)
    a1.set_ylabel("planted mechanism isolated uniquely")
    a1.set_title("what the battery isolates, and what it leaves entangled",
                 fontsize=9.5, color=INK)
    a1.legend(frameon=False, fontsize=8.5, loc="upper center")

    M = np.array([[br["with_sham"]["class_membership"][m][h] for h in mechs]
                  for m in mechs])
    im = a2.imshow(M, cmap="Greens", vmin=0, vmax=1)
    a2.set_xticks(range(len(mechs)))
    a2.set_xticklabels([m.replace("_", "\n") for m in mechs], fontsize=7.5)
    a2.set_yticks(range(len(mechs)))
    a2.set_yticklabels([m.replace("_", " ") for m in mechs], fontsize=7.5)
    for i in range(len(mechs)):
        for j in range(len(mechs)):
            if M[i, j] > 0.01:
                a2.text(j, i, f"{M[i, j]:.2f}", ha="center", va="center", fontsize=7.5,
                        color="white" if M[i, j] > 0.55 else INK)
    a2.set_xlabel("in the reading's equivalence class")
    a2.set_ylabel("planted")
    a2.set_title("the class the battery cannot break, sham included",
                 fontsize=9.5, color=INK)
    a2.grid(False)
    fig.colorbar(im, ax=a2, fraction=0.046, pad=0.04)
    _style(a1)
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_second_order(results: dict, path: str) -> None:
    so = results["second_order"]
    probes = list(so["auroc_planner_vs_probe_aware_by_probe"])
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 3.8),
                                 gridspec_kw={"width_ratios": [1.1, 1]})

    vals = [so["auroc_planner_vs_probe_aware_by_probe"][p] for p in probes]
    cols = [ABSORB_G if p == "sham2" else NEUTRAL for p in probes]
    a1.bar(range(len(probes)), vals, 0.6, color=cols)
    a1.axhline(0.5, color=INK, lw=0.9, ls="--")
    a1.set_xticks(range(len(probes)))
    a1.set_xticklabels(["rest", "move", "block", "sham", "held-out\nsham"], fontsize=8.5)
    a1.set_ylim(0, 1.05)
    a1.set_ylabel("AUROC, planner vs probe-aware mimic")
    a1.set_title("the declared battery, sham included, reads nothing",
                 fontsize=9.5, color=INK)

    systems = ["planner", "probe_aware_mimic"]
    resp = so["mean_response_to_probe"]
    x = np.arange(len(systems))
    w = 0.38
    a2.bar(x - w / 2, [resp[s]["sham"] for s in systems], w, color=NEUTRAL,
           label="declared sham")
    a2.bar(x + w / 2, [resp[s]["sham2"] for s in systems], w, color=ABSORB_G,
           label="held-out sham")
    for k, s in enumerate(systems):
        if resp[s]["sham"] < 1e-9 and resp[s]["sham2"] < 1e-9:
            a2.annotate("withholds\nunder both", xy=(k, 0.02), fontsize=8,
                        color=NEUTRAL, ha="center", va="bottom")
    a2.set_xticks(x)
    a2.set_xticklabels(["planner", "probe-aware\nmimic"], fontsize=8.5)
    a2.set_ylim(0, 1.12)
    a2.set_ylabel("fraction of cells departing the rest path")
    a2.set_title("only a probe it has never seen moves it", fontsize=9.5, color=INK)
    a2.legend(frameon=False, fontsize=8.5, loc="upper left")
    for ax in (a1, a2):
        _style(ax)
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_centaur(results: dict, path: str) -> None:
    ct = results["centaur"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.0, 3.9),
                                 gridspec_kw={"width_ratios": [1.25, 1]})

    cells = [("operator", "human"), ("goal_register", "human"),
             ("operator", "machine"), ("goal_register", "machine")]
    phiC = [ct["maps"][a]["capacity_map"][c] for c, a in cells]
    L = [ct["maps"][a]["legibility"][c] for c, a in cells]
    x = np.arange(len(cells))
    w = 0.38
    a1.bar(x - w / 2, phiC, w, color=CAP, label=r"realized capacity  $\phi^C$")
    a1.bar(x + w / 2, L, w, color=PASSIVE, label=r"legibility  $L$")
    a1.axhline(0, color=INK, lw=0.8)
    a1.axvline(1.5, color=NEUTRAL, lw=0.8, ls=":")
    a1.set_xticks(x)
    a1.set_xticklabels(["operator", "register", "operator", "register"], fontsize=8.5)
    a1.annotate("human holds the goal", (0.5, 0.03), xycoords=("data", "axes fraction"),
                ha="center", fontsize=8.5, color=HUMAN)
    a1.annotate("machine holds the goal", (2.5, 0.03), xycoords=("data", "axes fraction"),
                ha="center", fontsize=8.5, color=AGENT)
    a1.set_ylabel("normalized contribution")
    a1.set_title("the legibility follows the authority, not the substrate",
                 fontsize=9.5, color=INK)
    a1.legend(frameon=False, fontsize=8.5, loc="upper right")
    a1.set_ylim(-0.25, 1.12)

    # the whole crossing rests on the stipulation that the register is credulous, so
    # the stipulation is drawn as a family rather than assumed at its extreme
    shades = {"0.0": "#cfcfcf", "0.25": "#b3a2cc", "0.5": "#9377b8", "0.75": "#7a55a5",
              "1.0": HUMAN}
    for c in ct["machine_credulity_values"]:
        pts = [(k, d) for k, d in ct["crossover_surface_by_credulity"][str(c)]
               if d is not None]
        if not pts:
            continue
        a2.plot([p[0] for p in pts], [p[1] for p in pts], "o-",
                color=shades[str(c)], lw=1.7, ms=3.4, label=f"credulity {c}")
    first = ct["first_latency_with_a_crossover"]
    if first is not None:
        a2.axvspan(0, first, color=NEUTRAL, alpha=0.13)
        a2.annotate("delay is free", (first / 2, 0.52), ha="center", fontsize=8,
                    color=NEUTRAL)
    a2.set_xlabel("operator delay (steps before the goal is re-issued)")
    a2.set_ylabel("decoy rate at which human authority wins")
    a2.set_title("the crossing is carried entirely by how credulous the channel is",
                 fontsize=9.0, color=INK)
    a2.set_ylim(0, 1.05)
    a2.legend(frameon=False, fontsize=7.5, loc="lower right")
    for ax in (a1, a2):
        _style(ax)
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_guards(results: dict, path: str) -> None:
    bs = results["boundary_sweep"]
    rg = results["richness_guard"]["systems"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.4, 3.8))

    # the full landscape over all 2^6 enclosures, not one flattering path through it:
    # the band is the min/max realized capacity at each enclosure size, and the line
    # is the nested chain the prose walks
    land = results["enclosure_landscape_capacity_by_size"]
    sizes = sorted(int(k) for k in land)
    lo = [land[str(s)]["min"] for s in sizes]
    hi = [land[str(s)]["max"] for s in sizes]
    a1.fill_between(sizes, lo, hi, color=AGENT, alpha=0.18,
                    label="all enclosures of that size (min to max)")
    chain_sizes = [2, 3, 5, 6]     # planner+harness, +goal register, +map+memory, +persona
    a1.plot(chain_sizes, [b[1] for b in bs], "o-", color=AGENT, lw=1.8, ms=6,
            label="the nested chain of the text")
    offsets = [(6, 6), (6, -12), (0, -15), (6, -4)]
    aligns = ["left", "left", "center", "left"]
    for (s, b), off, ha in zip(zip(chain_sizes, bs), offsets, aligns):
        a1.annotate(b[0], (s, b[1]), xytext=off, textcoords="offset points",
                    fontsize=7.2, color=INK, ha=ha)
    a1.axhline(0, color=NEUTRAL, lw=0.9)
    a1.set_xlabel("components enclosed")
    a1.set_ylabel("realized capacity of the enclosed unit")
    a1.set_title("the landscape over every declarable boundary", fontsize=10, color=INK)
    a1.legend(frameon=False, fontsize=7.5, loc="upper left")

    for name, (cx, ay) in rg.items():
        col = PASSIVE if name in ("route_script", "chaotic") else AGENT
        a2.scatter([cx], [ay], s=60, color=col, zorder=3)
        a2.annotate(name.replace("_", " "), xy=(cx, ay), xytext=(4, 4),
                    textcoords="offset points", fontsize=8, color=INK)
    a2.axhline(0, color=NEUTRAL, lw=0.9)
    a2.set_xlabel("trajectory complexity (bits)")
    a2.set_ylabel("agency evidence")
    a2.set_title("complexity is no proxy for agency",
                 fontsize=10, color=INK)
    for ax in (a1, a2):
        _style(ax)
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
