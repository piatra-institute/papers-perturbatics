"""Orchestrator: reproduces every number and all three figures in the paper.

    cd simulation
    uv run run_all.py

Writes output/results.json and output/figures/{separation,realization_map,
guards}.png. Deterministic given the recorded seed; nothing is sampled.
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
    try:
        from figures import plot_separation, plot_realization_map, plot_guards
        plot_separation(results, str(OUT / "figures" / "separation.png"))
        plot_realization_map(results, str(OUT / "figures" / "realization_map.png"))
        plot_guards(results, str(OUT / "figures" / "guards.png"))
    except Exception as e:  # figures are secondary to the numbers
        print("figure step skipped:", e)

    sep = results["separation"]
    rm = results["realization_map"]
    rg = results["richness_guard"]
    ps = results["persona_swap"]
    print(f"separation: AUROC at rest {sep['auroc_at_rest']}, under probe "
          f"{sep['auroc_under_probe']}; mean evidence rest {sep['mean_evidence_rest_planner']}, "
          f"probe planner {sep['mean_evidence_probe_planner']}, probe passive "
          f"{sep['mean_evidence_probe_passive']}")
    print("evidence map phi_E:", {k: round(v, 2) for k, v in rm["evidence_map"].items()})
    print("capacity map phi_C:", {k: round(v, 2) for k, v in rm["capacity_map"].items()})
    print("legibility L=phi_E-phi_C:", {k: round(v, 2) for k, v in rm["legibility"].items()})
    print("interaction:", {k: round(v, 2) for k, v in rm["interaction_index"].items()})
    print("boundary sweep (capacity):", results["boundary_sweep"])
    print(f"persona: capacity full {ps['capacity_full']}, swap-persona "
          f"{ps['capacity_swap_persona_keep_model']}, swap-model "
          f"{ps['capacity_swap_model_keep_persona']}")
    print("richness:", rg["systems"], "corr", rg["complexity_agency_correlation"])
    print("wrote", OUT / "results.json")


if __name__ == "__main__":
    main()
