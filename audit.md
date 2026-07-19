# Audit

Dated log of editorial passes and verification runs. Newest first.
See the workspace docs (run `papers docs`): writing-pipeline.md §7 and refresh-pipeline.md.

## 2026-07-19 — first draft through publish

Scope: authored the paper end to end from a design brief and its external critique (the seed `chats/chat.md` is a ChatGPT analysis of an earlier `perturbatics-brief.md`), through the full pipeline to a built and web-synced PDF with an accompanying simulation. This is a meta-paper: it names a method that recurs across the institute's corpus and builds an instrument out of it.

Kind: formal-model. `has_simulation: true`, `claims_target: results.json`. The gridworld is illustrative and instantiates the definitions; every number it produces is a key in `simulation/output/results.json`. The literature and the formalism are cited or defined, not simulation output.

Design decisions carried from the critique (a self-applied severe test):
- The v1 thesis, "dispositions are invisible to observation and knowable only under intervention," was too universal (natural experiments reveal dispositions). Reframed to the probe separation principle: observational equivalence over the encountered regime, broken by a deliberate intervention or a natural experiment. This is the defensible core.
- Perturbatics is stated as interventional model separation plus causal realization mapping, with a restricted object, a model-separating primitive, and a realization-map product, to differentiate it from causal inference, experimental design, ablation, cybernetics, chaos engineering, and mechanistic interpretability (an explicit "What Perturbatics is not" section).
- The device readout is the do-Shapley value under an interventional value function, with the interaction index for synergy/redundancy, grounded on Heskes et al. (2020), Jung et al. (2022), and the exactness result of Witter et al. (2026). The boundary is swept, not assumed. The null is a family, not a strawman. The Textual Shadow is used as a projection-induced equivalence, not a null.
- The consciousness idea (the discriminating intervention is termination, unrepeatable and read in the griever, not the machine) is the paper's climax, folded into "what the instrument cannot certify."

Changes:
- `brief.md`, `research.md`, `sources.md` written first. Citations web-verified against the publisher/DOI/arXiv record (verification pass, 2026-07-19): 26/26 verified, 0 corrected. Notable confirmations: MacDermott, Fox, Belardinelli & Everitt (2024, MEG, arXiv:2412.04758), the nearest technical neighbour; Witter et al. (2026, exact do-Shapley, arXiv:2602.07203).
- Simulation authored in `simulation/` (numpy + matplotlib, `uv run run_all.py`, deterministic, seed 0). A gridworld with three observationally-equivalent systems and a six-component planner assemblage, ablated by do-intervention. Establishes: the separation principle (AUROC 0.50 at rest, 0.945 under a probe; mean evidence +29.8 vs -31.4); the do-Shapley realization map (goal register 0.53, planner 0.30, persona exactly 0.00) with interactions (planner-map +0.15 synergy, map-memory -0.22 redundancy, goal-register-planner additive); the persona-swap (1.0/1.0) vs model-swap (0.26) result; the boundary sweep (-0.79 to 1.0); and the richness guard (complexity-agency correlation -0.68). The value function was equal-weighted across the probe battery (per-probe normalisation) so no single probe dominates the attribution; the harness ablation was made anti-goal so its contribution is clean; the boundary sweep encloses the actuator in every candidate unit and varies the cognitive enclosure. Three figures generated and embedded.
- `paper/PAPER.md` drafted in the house voice: a §0 Probes section of bare imperatives that double as corpus seeds and as operations; prose section titles; no roadmap; limits and prior art folded into "What Perturbatics is not" and the closing; formal spine in display and inline math, no raw Unicode; ends on the grievable, not a tagline. A Perturbatic Atlas appendix maps eight corpus papers to their probe and reading by title (the body cites no PIATRA paper author-year, so every reference is external and the reconciler stays clean; the corpus appears only as the titled Atlas).
- Voice pass: cleared the negate-pivot and inline-contrastive review candidates to zero (two genuine negate-pivots rewritten to positive declaratives; several ", not X" contrasts to "rather than"), trimmed the pet-vocabulary (`exactly` 10 -> 3, `carries` 7 -> 2, `honest` 4 -> 2).
- `metadata.yaml`: title, header, `date: July 2026`, plain-prose abstract, `has_simulation: true`, `claims_target: results.json`, `status: published`. `README.md` rewritten with the simulation and build commands. `build.py` vendored from `tooling/build/build.py`.

Verification:
- voice: 0 errors, 0 review-candidates. Advisories: lexical density mild; tricolons 10 (2.1/k), acceptable; rhythm 17% short. The spelled-quantity advisory retained for the rhetorical "a hundred times / a hundred ways" (emphasis, not measurement).
- refs: 25 in-text keys / 25 bib entries, 0 missing, 0 unused. Note: Von Bertalanffy is written with a capitalised particle (APA 7) so the reconciler parses the entry.
- claims: 13 prose decimal claims, 3 flagged no-match (31.4, 0.22, 0.68), all of them negative sim values present in results.json (mean evidence -31.37, map-memory interaction -0.222, complexity-agency correlation -0.675); the reconciler's decimal regex drops the leading minus, so the negatives are not matched against the unsigned prose tokens. No paper error.
- build: 14 pages, 0 missing-character warnings. Math, the three embedded figures, and the running header render.
- check => PASS. PDF synced to `public/papers/perturbatics.pdf`.

Post-publish (from this session): the emitted `web-entry` object was added to the top of `app/papers/page.tsx` `ownPapers[]` with `topics: ['philosophy', 'computer-science', 'psychology']` and `kinds: ['formal', 'simulation']` (the web repo is left uncommitted for the author). The GitHub repo `piatra-institute/papers-perturbatics` was created, described, and the initial commit pushed.
