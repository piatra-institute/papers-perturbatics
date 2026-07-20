# Perturbatics

Reading Agency in Assemblages That Cannot Be Read at Rest. The paper coins perturbatics (from Latin *perturbare*, through *turba*, disorder; its companion word, kin by theme rather than by descent, is Greek *peira*, trial, the root of *empirical*) for the interventional separation of latent capacities, agency, competence, authorship, in decomposable systems. Its principle is a separation principle: when two organizational models are observationally equivalent over the regime a system has been in, no analysis of that record tells them apart, so separation requires a model-separating probe, from a deliberate intervention or a natural experiment. It builds an instrument, a centaur agentoscope, that scores agency as a Bayes factor between a goal model and a passive model, attributes it across an assemblage by do-Shapley value (with a persona inert by construction and a planner-map synergy), and sweeps the boundary rather than assuming it. It ships a deterministic gridworld demonstrator: three systems indistinguishable at rest (AUROC 0.50), separated by the probe battery and by no single probe in it (the moved goal exposes the route script at 1.0, the blocked path exposes the planner at 0.78, planner vs script pooled 0.95), the dual realization map with its legibility term, the boundary landscape, and a richness-is-not-agency guard. The account ends where its own method cannot go, at consciousness, where the candidate probe, turning the system off, returns no reading the rival hypotheses score differently and would be forbidden if it did, read not in the machine but in whoever grieves it.

## Simulation

```bash
cd simulation
uv run run_all.py        # -> output/results.json + output/figures/*.png
```

Deterministic given the recorded seed: the 40 instances are drawn once from it and every episode is deterministic; a seed sweep in `results.json` reports the AUROC ranges across redrawn instance sets (pooled 0.93-0.97 over twenty seeds), and invariant checks (rest-path identity, at-rest zero evidence, Shapley efficiency, persona capacity-dummy) fail the run loudly if broken. The gridworld is illustrative and instantiates the paper's definitions; it is not fit to data, its scorer is an oracle, and the paper states these terms in the demonstrator section. Every number cited in the paper is a key in `simulation/output/results.json`.

## Build

```bash
uv run build.py          # -> paper/PAPER.pdf  (vendored canonical recipe)
```

Requires `pandoc` and `xelatex` on PATH. From the workspace you can also run
`papers build perturbatics`.

Part of [piatra-papers](https://github.com/piatra-institute). See the workspace
docs for the research and writing pipelines.
