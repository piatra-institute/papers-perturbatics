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

- Numbers current as of the v4 (2026-07-20) run; earlier entries in this block reported the v1 simulation and were stale against the shipped paper.
- Separation, battery-shaped: every pairwise AUROC 0.50 at rest. Per probe: move exposes the script (planner and reactive vs script both 1.0) and leaves planner vs reactive at 0.50 (trajectory-identical); block exposes the planner (0.78 vs both) and leaves reactive vs script at 0.50. Planner vs script pooled 0.945. Mean probe evidence: planner +29.8, script -31.4, reactive +26.1.
- Realization map (dual, do-Shapley): evidence phi_E goal register 0.70, planner 0.36, persona 0.23 (= DECL_FRAC/(1+DECL_FRAC), the cheap-talk dial, by construction); capacity phi_C goal register 0.68, planner 0.23, persona 0.00 (no motor channel, by design). Legibility L: persona 0.23 (largest), planner 0.13 (second), goal register 0.01; harness -0.03 evidence / +0.01 capacity (executor sign flip). Maps are marginal contributions: phi_E sums to 1.45, empty coalition -0.45.
- Interaction (capacity game): planner-map +0.18 (synergy), map-memory -0.16 (redundancy), goal-register-planner 0 (additive). The evidence-game interactions (+0.30 / -0.25) ship alongside under `interaction_index_evidence_game`; the v5.3-and-earlier paper reported the evidence values against a capacity claim, corrected in the v6 audit pass. Persona swap 1.0 (identity by design), model swap 0.65. Boundary sweep (capacity, enclosure form) -0.04 to 1.0. Richness-agency correlation -0.09 over four systems (near zero: complexity carries no signal for agency; the earlier -0.68 was an artifact of a chaotic walker that walked through walls, fixed in the v6 pass). All keys in `simulation/output/results.json`.

### Neighbours added in the audit pass (2026-07-20)

- [T2] Martin (1994, *Phil. Quarterly* 44(174):1-8); Lewis (1997, *Phil. Quarterly* 47(187):143-158); Johnston (1992, *Phil. Studies* 68(3):221-263); Bird (1998, *Phil. Quarterly* 48(191):227-234). Finks, masks/antidotes, mimics: the dispositions literature's pathologies. Agency theater is a mimic; a probe that installs a capacity is a fink. Locators web-verified 2026-07-20.
- [T2] Box & Hill (1967, *Technometrics* 9(1):57-71); Atkinson & Fedorov (1975, *Biometrika* 62(1):57-70). Experiment design for discriminating rival models, T-optimality: the probe-selection objective's statistical ancestor. Moore (1956, *Automata Studies* 34:129-153): distinguishing experiments for machines, and machines no experiment tells apart, the ancestor of the battery and of perturbational equivalence. Ljung (1999): persistency of excitation, the one-regime claim in engineering form.
- [T2] Block (1981, *Phil. Review* 90(1):5-43): the lookup-table interlocutor; grounds the retrieval null. Crawford & Sobel (1982, *Econometrica* 50(6):1431-1451): cheap talk; names the persona's declaration channel. Grabisch & Roubens (1999, *Int. J. Game Theory* 28(4):547-565): the Shapley interaction index used in the readout.
- [T1] Casali et al. (2013, *Sci. Transl. Med.* 5(198):198ra105): the perturbational complexity index, a perturbational consciousness index for the human brain, calibrated on subjects who can report. Added in the second (Codex) critique pass to bound the unperformable-probe claim: the index exists within a class known to contain experience; the instrument's problem is the class with no calibration set. Locator web-verified 2026-07-20.
- Simulation robustness (same pass): seed sweep over 20 redrawn instance sets, planner-vs-script AUROC pooled 0.93-0.97, move 1.0 throughout, block 0.71-0.87; invariant checks (rest-path identity, at-rest zero evidence for any trajectory, Shapley efficiency, persona capacity-dummy) asserted in the run; enclosure landscape (capacity range per coalition size over all 2^6 enclosures) shipped in `results.json`.

### Note on the consciousness boundary-case

The claim that consciousness is read in the griever, not the machine, is the paper's own philosophical thesis, not a literature result. It is grounded on the interventional epistemology (the discriminating probe is termination, unrepeatable and forbidden) and on the agency-vs-personhood distinction (Barandiaran et al. 2009), and it inverts the readout the rest of the paper uses. Presented as a position, not as evidence.
