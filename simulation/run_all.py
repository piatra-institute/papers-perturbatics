"""Orchestrator: reproduces every number and all three figures in the paper.

    cd simulation
    uv run run_all.py

Writes output/results.json and output/figures/{separation,realization_map,
guards}.png. Deterministic given the recorded seed: the instances are drawn once
from it and every episode is deterministic; a seed sweep reports the AUROC
ranges across redrawn instance sets. A failed figure fails the run.
"""
from __future__ import annotations

import json
from pathlib import Path

from analyses import run

OUT = Path(__file__).parent / "output"


def _strip_private(obj):
    if isinstance(obj, dict):
        return {k: _strip_private(v) for k, v in obj.items() if not k.startswith("_")}
    return obj


def main() -> None:
    (OUT / "figures").mkdir(parents=True, exist_ok=True)
    results = run()
    (OUT / "results.json").write_text(json.dumps(_strip_private(results), indent=2))
    from figures import (plot_separation, plot_realization_map, plot_guards,
                         plot_sham_control, plot_centaur,
                         plot_blind_recovery, plot_second_order)
    plot_separation(results, str(OUT / "figures" / "separation.png"))
    plot_realization_map(results, str(OUT / "figures" / "realization_map.png"))
    plot_guards(results, str(OUT / "figures" / "guards.png"))
    plot_sham_control(results, str(OUT / "figures" / "sham_control.png"))
    plot_centaur(results, str(OUT / "figures" / "centaur.png"))
    plot_blind_recovery(results, str(OUT / "figures" / "blind_recovery.png"))
    plot_second_order(results, str(OUT / "figures" / "second_order.png"))

    sep = results["separation"]
    rm = results["realization_map"]
    rg = results["richness_guard"]
    ps = results["persona_swap"]
    print(f"separation: AUROC at rest {sep['auroc_at_rest']}, planner-vs-script pooled "
          f"{sep['auroc_under_probe']}; per-probe {sep['auroc_per_probe']}; "
          f"mean evidence rest {sep['mean_evidence_rest_planner']}, "
          f"probe planner {sep['mean_evidence_probe_planner']}, probe script "
          f"{sep['mean_evidence_probe_passive']}, probe reactive "
          f"{sep['mean_evidence_probe_reactive']}")
    print("evidence map phi_E:", {k: round(v, 2) for k, v in rm["evidence_map"].items()})
    print("capacity map phi_C:", {k: round(v, 2) for k, v in rm["capacity_map"].items()})
    print("legibility L=phi_E-phi_C:", {k: round(v, 2) for k, v in rm["legibility"].items()})
    print("interaction:", {k: round(v, 2) for k, v in rm["interaction_index"].items()})
    print("boundary sweep (capacity):", results["boundary_sweep"])
    print(f"persona: capacity full {ps['capacity_full']}, persona-identity "
          f"{ps['capacity_persona_identity']}, swap-model "
          f"{ps['capacity_swap_model_keep_persona']}")
    print("richness:", rg["systems"], "corr", rg["complexity_agency_correlation"])
    sc = results["sham_control"]
    print("sham control AUROC by probe:", sc["auroc_reactive_vs_marker_tracker_by_probe"])
    print("sham selectivity:", sc["selectivity_move_minus_sham"])
    for s, v in sc["verdict"].items():
        print(f"  {s:15s} {v}")
    ct = results["centaur"]
    for a in ("human", "machine"):
        m = ct["maps"][a]
        print(f"centaur {a:8s} holder={m['authority_holder']:14s} "
              f"channel={m['pure_channel']:14s} L(channel)={m['legibility'][m['pure_channel']]}")
    print("centaur crossover by latency:", ct["crossover_decoy_rate_by_latency"])
    br = results["blind_recovery"]
    print(f"blind recovery: chance {br['chance_level']}; "
          f"expected {br['without_sham']['overall_expected']} -> {br['with_sham']['overall_expected']}, "
          f"unique {br['without_sham']['overall_unique']} -> {br['with_sham']['overall_unique']}, "
          f"mean class {br['without_sham']['overall_mean_class_size']} -> "
          f"{br['with_sham']['overall_mean_class_size']}")
    print("  unique per mechanism (with sham):", br["with_sham"]["unique_recovery"])
    so = results["second_order"]
    print("second order AUROC planner vs probe-aware mimic:",
          so["auroc_planner_vs_probe_aware_by_probe"])
    print("robustness:", results["separation_robustness"])
    print("map robustness:", results["map_robustness"])
    print("checks:", results["checks"])
    print("wrote", OUT / "results.json")


if __name__ == "__main__":
    main()
