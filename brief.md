# Brief

Written before research begins. See the workspace docs (run `papers docs`):
research-pipeline.md §1.

## Question

An artificial agent presents as one character and is an assemblage of a model, a persona, a memory, a harness, permissions, and tools. The properties worth reading, agency, competence, authorship, are not on its surface, because a system that holds its state and a system that defends it look the same at rest. How do you read such a thing, and is there a science of the reading?

## Claim

Name the science perturbatics (from Latin *perturbare*; the Greek ancestor is *peira*, trial, the root of *empirical*). Its principle is a separation principle: when two organizational models are observationally equivalent over the regime a system has been in, no analysis of that record separates them, so identification requires a model-separating probe, a controlled difference that makes the models predict differently, supplied by a deliberate intervention or by a natural experiment. This is not "perturb and see"; it is interventional model separation plus causal realization mapping, with a restricted object (latent capacities), a distinctive primitive (the model-separating probe), and a specific product (a boundary-relative realization map). The paper builds an instrument for the human-AI assemblage, a centaur agentoscope: score agency as a Bayes factor between a goal model and a passive model; attribute the evidence across components by the do-Shapley value under an interventional value function; report synergy and redundancy via the interaction index; sweep the boundary rather than assume it; and guard against a strawman null (a family of complexity-matched alternatives) and against mistaking richness for agency. A deterministic gridworld demonstrates the whole: three systems indistinguishable at rest (AUROC 0.50) separate under a probe (AUROC 0.95); the realization map gives the goal register and planner most of the agency and the persona exactly zero; the planner and map are synergistic, the map and memory redundant; the reading swings from negative to full as the boundary widens; a chaotic walker has the highest complexity and lowest agency. The account ends where its own method cannot go: for consciousness the discriminating intervention is to turn the system off, which is irreversible, unrepeatable, and read not in the machine but in whoever grieves it. There the instrument hands a score back to a relation.

## Kind

formal-model (ships a simulation). `has_simulation: true`, `claims_target: results.json`. The gridworld is illustrative and instantiates the definitions; every number it produces is a key in `results.json`. The literature results and the formalism are cited or defined, not simulation output.

## Cornerstone literature

- Interventionism / testing / causation: Pearl (2009, do-calculus, the ladder); Woodward (2003, manipulationist causation); Mayo (2018, severe testing); Hacking (1983, intervention and realism); Lindley (1956, expected information gain).
- Cybernetics / regulation: Rosenblueth, Wiener & Bigelow (1943); Conant & Ashby (1970, the good-regulator theorem, the observational-equivalence core); Ashby (1956).
- Agency detection / intentional stance: Heider & Simmel (1944); Baker, Saxe & Tenenbaum (2009, inverse planning); Dennett (1987); Barrett (2000, HADD); Barandiaran, Di Paolo & Rohde (2009, agency ≠ consciousness).
- Goal-directedness measurement (the dangerous neighbour): MacDermott, Fox, Belardinelli & Everitt (2024, MEG); Klyubin, Polani & Nehaniv (2005, empowerment).
- Attribution: Heskes et al. (2020, causal Shapley); Jung et al. (2022, do-Shapley); Witter et al. (2026, exact do-Shapley).
- Neighbours to differentiate: Geiger et al. (2021, causal abstraction / interchange interventions); Basiri et al. (2016, chaos engineering).
- Boundary / autonomy: Maturana & Varela (1980); Montévil & Mossio (2015, closure of constraints).
- The frontier and equifinality: Levin (2019, agency in tissue); Von Bertalanffy (1968, equifinality); Kass & Raftery (1995, Bayes factors).
