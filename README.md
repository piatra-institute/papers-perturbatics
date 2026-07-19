# Perturbatics

Reading Agency in Assemblages That Cannot Be Read at Rest. The paper coins perturbatics (from Latin *perturbare*, with a Greek ancestor in *peira*, trial, the root of *empirical*) for the interventional separation of latent capacities, agency, competence, authorship, in decomposable systems. Its principle is a separation principle: when two organizational models are observationally equivalent over the regime a system has been in, no analysis of that record tells them apart, so separation requires a model-separating probe, from a deliberate intervention or a natural experiment. It builds an instrument, a centaur agentoscope, that scores agency as a Bayes factor between a goal model and a passive model, attributes it across an assemblage by do-Shapley value (with a persona provably inert and a planner-map synergy), and sweeps the boundary rather than assuming it. It ships a deterministic gridworld demonstrator: three systems indistinguishable at rest (AUROC 0.50) separated by a probe (AUROC 0.95), the realization map, the boundary landscape, and a richness-is-not-agency guard. The account ends where its own method cannot go, at consciousness, whose discriminating intervention is to turn the system off, unrepeatable and read not in the machine but in whoever grieves it.

## Simulation

```bash
cd simulation
uv run run_all.py        # -> output/results.json + output/figures/*.png
```

Deterministic given the recorded seed; nothing is sampled. The gridworld is illustrative and instantiates the paper's definitions; it is not fit to data. Every number cited in the paper is a key in `simulation/output/results.json`.

## Build

```bash
uv run build.py          # -> paper/PAPER.pdf  (vendored canonical recipe)
```

Requires `pandoc` and `xelatex` on PATH. From the workspace you can also run
`papers build perturbatics`.

Part of [piatra-papers](https://github.com/piatra-institute). See the workspace
docs for the research and writing pipelines.
