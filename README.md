# Perturbatics

An Agentoscope for Reading Agency.

Observing a natural, artificial or hybrid system at rest does not reveal whether it pursues a goal, whether it is competent, or which component authored its output, because perfect regulation and undisturbed rest leave the same flat record. We call the study of this situation perturbatics. Its separation principle states that when two organizational models agree over the regime a system has occupied, no analysis of that record distinguishes them; separation requires a probe under which the rivals predict differently. Agency is scored as a Bayes factor against a passive rival. In a gridworld, three systems trace one path at rest (every pairwise AUROC $0.50$), and a two-probe battery separates every pair although neither probe does alone. A system tracking the last-announced target is invisible to that battery until a matched sham, a decoy where the goal did not move, separates it at $1.0$. No finite battery certifies a capacity against an unrestricted class of rivals: a mimic that has memorized the declared battery is separated only by an unseen draw. Do-Shapley attribution of both the evidence for agency and the realized performance yields a legibility term, their difference, which takes the same value, $0.23$, for a narrating persona and for a human or machine component that announces a goal held elsewhere. In a blind test with five planted mechanisms, the evaluator never excludes the truth and isolates it uniquely in $0.73$ of readings against a chance of $0.2$, of which the sham contributes $0.22$. For consciousness the deciding probe is uninformative, inadmissible and underdetermined in description, and no number results.

## Simulation

```bash
cd simulation
uv run run_all.py        # -> output/results.json + output/figures/*.png
```

Deterministic given the recorded seed: the 40 instances are drawn once from it and every episode is deterministic; a seed sweep in `results.json` reports the AUROC ranges across redrawn instance sets (pooled 0.93-0.97 over twenty seeds), and 15 invariant checks (rest-path identity, at-rest zero evidence, Shapley efficiency, persona capacity-dummy, sham inertness across all 64 coalitions, the marker tracker's battery-wide identity with the reactive controller, the substrate-independence of the centaur channel's legibility, the measured equivalence the sham breaks, the shrink of the unresolved class, and the probe-aware mimic's identity with the planner on the declared battery, among others) fail the run loudly if broken. The gridworld is illustrative and instantiates the paper's definitions; it is not fit to data, its scorer is an oracle, and the paper states these terms in the demonstrator section. Every number cited in the paper is a key in `simulation/output/results.json`.

## Build

```bash
uv run build.py          # -> paper/PAPER.pdf  (vendored canonical recipe)
```

Requires `pandoc` and `xelatex` on PATH. From the workspace you can also run `papers build perturbatics`.

## Interactive

The same constructions run in the browser at [piatra.institute/playgrounds/agentoscope](https://piatra.institute/playgrounds/agentoscope), where the reader picks the probe: rest, moved goal, blocked path, or matched sham. The instances are redrawn there from a seed the reader sets, so the sample statistics move a little while the identities do not.

Part of [piatra-papers](https://github.com/piatra-institute). See the workspace docs for the research and writing pipelines.
