# Research

Findings, tiered by source proximity. See the workspace docs (`papers docs`): research-pipeline.md §2.
T1 primary · T2 authoritative secondary · T3 reference · T4 general web (leads only).
A claim that reaches the paper rests on a T1 or T2 source. All locators web-verified against the publisher/DOI/arXiv record on 2026-07-19 (provenance in `sources.md`).

## Findings

### The observational-equivalence core

- [T1] Conant & Ashby (1970), *Int. J. Syst. Sci.* 1(2):89-97. A good regulator of a variable must contain a model of it, so a regulated variable at rest and a variable simply undisturbed present the same face from outside. Supports the central claim that agency at rest is not in the record.
- [T2] Pearl (2009), *Causality* (2nd ed.). The ladder of causation: observational, interventional, counterfactual. Supports that separation lives on the do-rung, not the see-rung.
- [T2] Woodward (2003), *Making Things Happen*. A causal claim is defined through what would happen under intervention. Supports the interventionist reframe (and the corrected, non-universal thesis: observational equivalence, not universal invisibility).
- [T2] Mayo (2018), severe testing. A good test has a high probability of exposing a false claim; a model-separating probe is a special case. Hacking (1983): intervention grounds realism. Lindley (1956): expected information gain is the probe-design criterion.

### The instrument (agency as a model comparison)

- [T2] Kass & Raftery (1995), *JASA* 90(430):773-795. The Bayes factor / log-likelihood ratio between two models. Supports the agency score A.
- [T1] MacDermott, Fox, Belardinelli & Everitt (2024), NeurIPS 37 (arXiv:2412.04758). Maximum Entropy Goal-Directedness: goal-directedness as how well behavior is predicted as utility maximization. The nearest technical neighbour; the paper positions against it. Klyubin et al. (2005): empowerment, an alternative.
- [T1] Heider & Simmel (1944); Baker, Saxe & Tenenbaum (2009, inverse planning); Dennett (1987, intentional stance); Barrett (2000, HADD). The human detector: real, involuntary, over-attributing. The prototype the instrument extracts and corrects.
- [T2] Barandiaran, Di Paolo & Rohde (2009). Agency is distinct from intelligence, consciousness, personhood. Supports the instrument's deliberate silence, which sets up the consciousness boundary-case.

### Attribution (the realization map)

- [T1] Heskes et al. (2020, NeurIPS 33); Jung et al. (2022, ICML). Causal / do-Shapley values under the interventional value function ν(S) = E[Y | do(S)]. Supports the realization map and the interaction index (synergy/redundancy).
- [T1] Witter et al. (2026), arXiv:2602.07203. Exact do-Shapley in time linear in the irreducible sets, identifiability from single-component interventions. Makes the map a bounded computation rather than a 2^d intractability.

### Boundary, neighbours, frontier

- [T2] Maturana & Varela (1980, autopoietic closure); Montévil & Mossio (2015, closure of constraints, *J. Theor. Biol.* 372:179-191). Principled boundary criteria; the instrument sweeps the boundary rather than solving it.
- [T1] Geiger et al. (2021, NeurIPS 34): interchange interventions test whether a network realizes a variable. Basiri et al. (2016, *IEEE Software* 33(3):35-41): chaos engineering injects faults to expose organization. The two closest method-neighbours; the paper differentiates its object (latent capacity, not uptime or internal computation).
- [T1] Levin (2019, *Front. Psychol.* 10:2688): goal-directedness in tissue, the instrument's honest frontier. Von Bertalanffy (1968): equifinality (one end by many means) as the top-of-ladder criterion.

### Simulation (this paper's own computation; not literature)

- Separation: AUROC 0.50 at rest, 0.945 under an informative probe; mean evidence +29.8 (planner) vs -31.4 (passive). Realization map (do-Shapley): goal register 0.53, planner 0.30, map/memory/harness small, persona 0.00. Interaction: planner-map +0.15 (synergy), map-memory -0.22 (redundancy), goal-register-planner 0 (additive). Persona swap 1.0/1.0, model swap 0.26. Boundary sweep -0.79 to 1.0. Richness-agency correlation -0.68. All keys in `simulation/output/results.json`.

### Note on the consciousness boundary-case

The claim that consciousness is read in the griever, not the machine, is the paper's own philosophical thesis, not a literature result. It is grounded on the interventional epistemology (the discriminating probe is termination, unrepeatable and forbidden) and on the agency-vs-personhood distinction (Barandiaran et al. 2009), and it inverts the readout the rest of the paper uses. Presented as a position, not as evidence.
