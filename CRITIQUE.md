# A Ruthless Critique of *Perturbatics*

## Verdict

This is a stylish manifesto attached to a circular toy program. It identifies a real methodological habit—use interventions that force rival models to diverge—but does not establish a new science, a validated instrument, or even a nontrivial simulation result. The separation principle is an identifiability tautology. The “agentoscope” is a collection of familiar methods joined by new vocabulary. The code then hard-codes the systems, disturbances, scorer, component effects, and nulls so that the advertised conclusions follow by construction.

The paper is unusually candid about some of this. It says that the gridworld is illustrative, that the persona result is constructed, that the boundary is declared, that Shapley values depend on the game, and that the method is not yet a science. Those concessions are good scholarship, but they do not repair the evidential problem. A result can be honestly labeled “by construction” and still be doing no scientific work. Here, most of the central demonstration is exactly that.

As a conceptual essay, the paper has a memorable intuition: behavioral equivalence in one regime can be broken by a discriminating intervention, and evidence for a capacity should be distinguished from causal contribution to performance. As a formal-model paper with a simulation, it is not ready. The code does not test the method; it stages it.

## The decisive problems

### 1. The headline result at rest is a scorer identity, not a finding about the systems

The abstract and results section make the 0.50 AUROC at rest sound like an empirical demonstration of observational equivalence. The code guarantees it before any trajectory is examined.

In [`agency_evidence`](simulation/analyses.py#L182), the “goal” score uses shortest-path distance to `true_goal`, while the “inertial” score uses Manhattan distance to the baseline goal `g0`. Under the `rest` condition:

- `true_goal == g0`;
- there are no walls; and
- shortest-path distance on an empty four-neighbor grid equals Manhattan distance.

The two likelihood functions are therefore identical action by action. Their log-likelihood ratio is zero for **every possible trajectory**, not merely for the planner, reactive controller, and route script. A stationary trajectory scores zero. A chaotic trajectory scores zero. A deliberately anti-goal trajectory scores zero. I verified all three implications directly; the shipped code returns `0.0` even for its chaotic walker at rest.

That destroys the intended interpretation of the left side of Figure 1. The result does not show that “the record held no agency to find.” It shows that the author supplied the same scoring rule twice under that condition. The three systems do happen to be engineered to trace the same baseline path, but the reported evidence and AUROC cannot demonstrate this because the metric would return the same result even if they did not.

This is the most serious defect in the paper because the abstract presents 0.50 as the calibration point for everything that follows.

### 2. The “passive” null is another goal-directed policy

The formal paper contrasts a goal model with a passive model based on “autonomous dynamics, relaxation, and noise.” The implementation does nothing of the kind. Its null rewards actions that reduce distance to the original goal:

```python
prog = manhattan(c, g0) - manhattan(nb, g0)
```

That is a goal-directed policy with a frozen target and a wall-blind utility, not a passive process. The code therefore measures relative support for:

1. pursuing the currently declared goal with access to the wall layout; versus
2. pursuing the original goal without using the wall layout in the utility.

This can be a useful comparison, but it is not “agency versus passivity.” It is adaptive goal pursuit versus a particular fixed-goal controller. The paper itself insists that scores are only margins against named alternatives, yet repeatedly relabels this particular margin as “agency evidence.”

The mismatch is especially damaging because the paper’s guard stage demands a family of calibrated, complexity-matched nulls: behavior cloning, fixed policy, reactive descent, and retrieval. The simulation compares only two hand-authored scorers and implements no null fitting, model complexity penalty, posterior predictive check, or strongest-surviving-null selection. The promised guard is absent from the demonstration.

### 3. The probe’s answer is encoded in an oracle scorer

Under the moved-goal probe, the goal scorer is handed `g1` while the null remains attached to `g0`. Under the blocked-path probe, the goal scorer is handed the complete wall set and the null’s utility remains wall-blind. These are precisely the distinctions the two probes are supposed to discover.

The reported separation is therefore unsurprising:

- a controller written to read `g1` is rewarded by a scorer written to reward `g1`;
- a planner written to use the wall set is rewarded by a scorer written to use the wall set; and
- a script written to replay the old route is punished by the complementary scorer.

The experiment does not infer a latent organizational property from behavior. It evaluates hand-authored programs with a privileged description of the environment and the “true” goal. The score knows the answer in the same vocabulary used to construct the systems.

A serious demonstration would keep the evaluator blind to implementation class, infer or fit its competing models from training data, and test predictions on held-out interventions. This repository does none of those things.

### 4. Almost none of the paper’s formal apparatus is implemented

The paper introduces mutual information, Jensen–Shannon divergence, a robust objective against the strongest null, cost and risk penalties, perturbational signatures, epsilon-separating batteries, moral admissibility, and a minimal-battery optimization problem. The simulation implements none of them.

It manually chooses two probes, manually chooses two fixed likelihood functions, and reports AUROC. There is no:

- prior over hypotheses;
- estimate of mutual information;
- search or optimization over probes;
- cost or risk model;
- null family or minimax comparison;
- specified divergence `D` or epsilon;
- learned perturbational signature;
- minimality analysis; or
- battery classifier evaluated out of sample.

The equations are consequently ornamental relative to the evidence. They describe a possible future system. They do not describe the shipped one.

The same problem applies to the paper’s invocation of recent do-Shapley efficiency results. The code simply evaluates all `2^6 = 64` coalitions by brute force. It defines no structural causal model, proves no identifiability condition, constructs no irreducible sets, and uses none of the cited algorithm. The paper verbally acknowledges that those conditions would have to be shown; the code never shows them.

### 5. The “do-Shapley” map is an arbitrary ablation game with a hidden component

Calling a configuration switch `do(...)` does not by itself make the result a causal realization map. The code creates a bespoke set-membership game over six labels and assigns behavior to every subset. Many of those coalitions have no natural interpretation, and their behavior depends on arbitrary fallback rules.

The worst example is the planner switch. When `planner` is absent, [`run_episode`](simulation/analyses.py#L115) does not produce a planner-less system. It activates a reactive greedy controller in the `else` branch. That reactive controller is not one of `COMPONENTS`; it is a hidden seventh mechanism. Removing one component silently substitutes another. The resulting Shapley value attributes differences across systems whose architecture changes in an undeclared way.

Other baselines are equally authored:

- removing the harness does not revoke action; it drops every second action;
- removing the goal register freezes the original goal;
- removing the map deletes prior wall knowledge;
- memory matters only in the specially written collision branch; and
- removing the persona affects no behavior at all.

Shapley values are exquisitely sensitive to the feature partition, baseline, and behavior of off-manifold coalitions. The paper notes baseline dependence but then narrates the resulting numbers as locations of agency. They are locations of value in this particular invented game. Change the fallback controller or ablation semantics and the map changes, without any change in the full system.

### 6. “Agency theater made a number” is literally a dial made a number

The persona does not speak, generate text, strategically communicate, or affect an observer. The code simply adds a constant when the string `"persona"` is present:

```python
if "persona" in active:
    a += decl[probe]
```

That constant is set to 30% of the full system’s movement evidence. After normalization its Shapley contribution is mechanically `0.3 / 1.3 = 0.230769...`. Its capacity contribution is mechanically zero because the persona has no branch in the movement code. The paper discloses both facts, but still treats the difference as validation of a “legibility term.” Nothing was detected. The desired answer was inserted as a constant and recovered by an attribution method with the dummy-player property.

The appeal to “cheap talk in the strict sense” is also misplaced. Crawford–Sobel cheap talk is a strategic communication game involving an informed sender, a receiver, beliefs, incentives, and an action. This program has none of those. It has an additive bonus with no message distribution or joint likelihood. The underlying literature describes costless, non-binding, unverifiable communication; it does not license adding an arbitrary fraction to a Bayes factor ([Crawford–Sobel overview](https://ideas.repec.org/a/ecm/emetrp/v50y1982i6p1431-51.html)).

Worse, once this arbitrary bonus is added, the evidence score is no longer the log Bayes factor defined in the paper. A declaration could contribute to a joint log Bayes factor only through specified likelihoods under both hypotheses. No such likelihoods exist here.

### 7. The legibility term subtracts quantities that have no principled common scale

The paper defines `L_i = phi_E_i - phi_C_i` while conceding that the two Shapley games normalize different targets. That concession is fatal to the interpretation, not a minor unit warning.

`phi_E` is computed from a hand-authored likelihood ratio plus the persona constant. `phi_C` is computed from normalized final-distance progress. The games have different baselines, different empty-coalition values, different sums, and different semantics. Subtracting their normalized marginal contributions creates a number, but no theory shows that zero means faithful legibility, that positive values measure theater, or that values are comparable across systems, probes, decompositions, or normalization choices.

The planner’s positive `L` already exposes the ambiguity: a genuinely effective component is labeled partly theatrical because the arbitrary evidence game gives it a larger normalized marginal contribution than the arbitrary capacity game. The paper calls this a “reminder”; it is actually evidence that `L` has no validated construct meaning.

### 8. The likelihood implementation is wrong for the data it receives

The scorer claims to define a proper likelihood over action labels. Its input, however, is only a trajectory of positions. At boundaries and walls, several action labels can produce the same next position because invalid moves are clamped to “stay.” The code loops over those labels and keeps whichever matching label occurs last, usually the explicit stay action:

```python
if nb == nxt or (nb == c and nxt == c):
    chosen = k
```

If the observation is the next position, the likelihood must marginalize over every action label that could yield that position. If the observation is an action label, the generator must record the attempted action. It does neither. A wall-blind controller that attempts to move into a wall is scored as though it deliberately chose to stay. This is a substantive likelihood error exactly where the blocked-path probe obtains its signal.

### 9. “Realized agency” is final-distance progress, not agency, attainment, or rerouting

The capacity function is:

```python
(initial_graph_distance - final_graph_distance) / initial_graph_distance
```

It ignores path quality, correction dynamics, robustness, repeated attainment, internal goal representation, and whether the final progress was accidental. A script, rolling object, or lucky random walk can score positive. A controller that reaches the target and then leaves can score poorly. A controller that makes a sophisticated detour but has not completed it by the arbitrary horizon can score poorly. Calling this “goal attainment and rerouting” overstates what is measured; it is final geodesic progress toward an externally supplied target.

The construct validity problem propagates into the capacity Shapley map, persona swap, interaction terms, and boundary sweep. Those analyses attribute this distance statistic, not agency.

### 10. The boundary sweep is a nested ablation curve mislabeled as a boundary analysis

The code examines one hand-picked sequence:

1. planner plus harness;
2. add goal register;
3. add map and memory together; and
4. add the inert persona.

Everything outside each subset is disabled. That is not a sweep over plausible system–environment boundaries. It is a cumulative feature ablation in an order chosen to produce an ascending curve. It does not compare alternate boundaries, preserve external components as an environment, vary coupling across a boundary, or establish individuation. Adding components that were explicitly written to be necessary and normalizing the full coalition to 1.0 guarantees the story’s direction.

The paper carefully calls this the “lesion form” of the question, but it still claims that the result shows the reading depends on the declared boundary. What it shows is that the chosen performance statistic depends on removing pieces of its implementation. Nobody doubted that.

### 11. The richness guard is a four-point illustration designed to win

“Trajectory complexity” is the Shannon entropy of the marginal distribution of move directions. It ignores temporal order, compressibility, state dependence, policy complexity, internal state, and computational sophistication. A periodic sequence and a shuffled sequence can receive the same value. The “chaotic” walker is deliberately goal-insensitive and designed to spread moves across directions. Of course it receives high direction entropy and low score under a goal-alignment metric.

The reported correlation of -0.68 over four selected systems has no inferential meaning, as the paper admits. More importantly, it does not establish the claimed guard. It only shows that two deliberately different metrics can rank four deliberately selected programs differently. A guard would need adversarial complexity-matched nulls and evidence that the agency score remains calibrated when non-agentic systems are optimized against it.

### 12. The deterministic design is still a single pseudorandom sample

The README says “nothing is sampled,” but [`make_instances`](simulation/analyses.py#L95) uses a pseudorandom generator and rejection sampling to select 40 instances. Fixing the seed makes a sample reproducible; it does not make it cease to be a sample.

The repository reports no variation over seeds, grid geometry, wall layouts, horizons, model temperature, or noise. A small diagnostic sweep over seeds 0–19 changed:

- pooled planner-versus-script AUROC from 0.928 to 0.968; and
- blocked-path planner-versus-script AUROC from 0.712 to 0.873.

Those ranges do not reverse the engineered ranking, but they show that the prominently quoted 0.95 and 0.78 are arbitrary realizations of one generated instance set, not stable properties of the method.

The evidence magnitudes are even less meaningful. Changing only `BETA` from 0.01 to 10 moved mean planner evidence from about 0.16 to 191.96 and mean script evidence from about -0.18 to -210.36, while leaving the broad ranking similar. Quoting `+29.8` and `-31.4` as substantive readings without a calibration or sensitivity analysis invites an interpretation their scale cannot support.

Pooling the move and block scores into one AUROC is also questionable. These are different regimes with very different score distributions and reference scales. The formal battery criterion only needs each pair to be separated by some identified probe. A pooled scalar AUROC is neither that criterion nor an evaluated classifier that conditions on probe identity.

## Problems in the paper’s argument

### The “separation principle” is true because it restates its premise

If two hypotheses assign exactly the same distribution to the observed data, no statistic of those data can distinguish them. This is elementary identifiability, not a new result. The displayed derivation adds no theorem, bound, algorithm, or condition for recognizing equivalence in practice. “Perturbational signature” renames a vector of interventional predictive distributions. “Minimal separating battery” restates classical discriminating experiment design and distinguishing sequences.

The prior-art section effectively concedes the point: cybernetics, interventionism, severe testing, discriminating experimental design, automata theory, system identification, causal abstraction, ablation, and chaos engineering already contain the core operations. Restricting the object to “organizational predicates,” calling interventions “model-separating probes,” and appending a Shapley map may be a useful synthesis. It does not yet justify declaring a new science.

The novelty claim would need to identify a problem existing methods cannot formulate or solve, then demonstrate that the proposed apparatus solves it. The paper instead gives old machinery a shared aesthetic and asserts that the organization is “enough for a method.” That is a proposal, not a result.

### The title overstates what cannot be learned observationally

The impossibility claim holds only relative to a chosen observation channel and a pair of hypotheses that are assumed to be observationally equivalent on that channel. It does not hold for “the system” in general. An artificial agent’s source code, weights, state, configuration, traces, and dependency graph may reveal a planner, a goal register, or a script without perturbing behavior. Indeed, this repository’s three systems are trivially distinguishable at rest by reading the code.

The paper quietly narrows “observation” to an output trajectory and then expands its conclusion to agency in assemblages. That is an equivocation. Black-box behavioral non-identifiability is real; universal unreadability “at rest” is not.

### Agency is never defined independently of the metric

The paper moves among regulation, adaptive goal pursuit, competence, causal contribution, authorship, and agency. Its formal score means “relative predictive fit of one goal policy versus one alternative.” Its capacity score means “final progress toward an externally declared target.” Neither provides necessary or sufficient conditions for agency.

This creates circularity at the conceptual level as well as in the code: a system counts as agentic when it behaves as the chosen goal model expects under the chosen probes. A passive process can mimic that behavior; an agent with a different goal, irrational policy, partial knowledge, exploration strategy, or self-generated objective can fail it. The paper knows the verdict is model-relative but continues to use ontological language—“locate the agency,” “what realizes it,” “a thermostat has a little agency”—that the formalism cannot earn.

### The etymology is false

The paper says the “deeper root” of *perturbatics* is Greek *peira*, trial, and the README is even more explicit that *perturbare* has “a Greek ancestor in *peira*.” It does not. Latin *perturbare* is formed from *per-* plus *turbare*, from *turba* (disorder or crowd). Greek *peira* belongs to the separate history of *empeiria* and *empirical*. Standard etymologies trace the two through different roots ([*perturb*](https://www.etymonline.com/word/perturb), [*empirical*](https://www.etymonline.com/word/empirical); see also [Merriam-Webster on *perturb*](https://www.merriam-webster.com/dictionary/perturb)).

The connection is a thematic pun, not ancestry. Presenting it as philology is avoidable self-mythologizing, and it is particularly awkward in a paper whose rhetoric depends heavily on naming a field.

### The consciousness ending is a non sequitur dressed as a limit theorem

The paper never specifies rival theories of consciousness, their predicted observables, or a reason shutdown is the unique candidate probe. It simply asserts that turning a system off is “the” discriminating intervention, immediately concedes that it has zero mutual information, and then builds an ethical climax around calling the same non-probe a killing.

By the paper’s own definition, an intervention under which rival hypotheses predict no different observable outcome is not a model-separating probe. It therefore cannot establish a special boundary of perturbatics. It is merely an uninformative intervention. Adding `M(pi) = infinity` contributes no analysis because no admissibility function, units, decision procedure, or connection to the agency instrument is provided.

Grief is then introduced, correctly rejected as evidence of consciousness, and retained as the emotional endpoint anyway. That may work as literary prose. It does not follow from the formalism. The argument slides among shutdown, irreversible destruction, loss of numerical identity, subjective experience, and human attachment without a theory connecting them. The paper cites no consciousness-science literature for its claim that termination is the privileged test.

The defensible conclusion is modest: some interventions may be unethical, and model-relative uncertainty can warrant precaution. The published conclusion is grander and unsupported: that consciousness uniquely drives the instrument into silence and leaves grief in place of measurement.

## Engineering and reproducibility weaknesses

The codebase is small and readable, but it lacks the basic safeguards expected of a repository making quantitative claims.

- There are no tests and essentially no runtime assertions.
- There is no check that paper numbers match regenerated results.
- There is no test of Shapley efficiency, dummy-player behavior, interaction weights, or baseline invariance.
- There is no test exposing the at-rest scorer identity.
- There is no sensitivity or robustness script.
- Global constants control every experiment.
- `run_all.py` catches every exception from figure generation, prints “skipped,” and can exit successfully with missing or stale figures.
- The figure histogram range omits at least one shipped score below -90.
- The code conflates policy generation, observation, scoring, intervention semantics, attribution, and reporting in one module.
- The tracked JSON contains rounded summaries but no per-instance records, model specifications, uncertainty, environment hashes, or version provenance.

The repository is reproducible in the narrow sense that the same dependency lock and seed regenerate the same artifacts. It is not robust, statistically characterized, or protected against regression.

## Claim-to-evidence ledger

| Paper claim | What the code actually supplies | Assessment |
|---|---|---|
| Agency cannot be read at rest | Two scoring functions that are algebraically identical at rest | Non-test; any trajectory scores zero |
| A probe battery separates organizational hypotheses | Two manually chosen environments scored by an oracle given the moved goal and full wall set | Construction, not discovery |
| Agency is scored against a passive model | A current-goal/wall-aware policy versus an original-goal/wall-blind policy | Mislabelled model comparison |
| Strong nulls guard the instrument | No learned or complexity-matched null family | Not implemented |
| do-Shapley locates causal realization | Brute-force Shapley over arbitrary component switches and a hidden fallback controller | Baseline-relative ablation attribution |
| The persona demonstrates agency theater | An additive constant plus a component with no motor code | Exact identity inserted by hand |
| `L` measures legibility | Difference of Shapley values from incomparable games | Unvalidated construct |
| Capacity measures attainment and rerouting | Normalized final geodesic progress | Narrow task-performance proxy |
| Boundary sweeping reveals the agent’s boundary | One cumulative lesion sequence | Not a boundary sweep |
| Richness is not agency | Four selected programs under a crude direction-entropy metric | Anecdote |
| The formal probe objective guides the demonstration | No mutual information, optimization, cost, risk, or minimal-battery computation | Decorative formalism |
| Consciousness exposes an unperformable separating probe | Shutdown is asserted to have zero separating information | By definition, not a separating probe |

## What would make this publishable

The shortest honest route is to stop presenting the current repository as validation. Recast the paper as a position piece proposing a synthesis, and label the gridworld as an executable diagram. If the goal is a formal-model paper, the minimum repair is much larger:

1. **Define the construct.** State operational criteria for agency that are not identical to the chosen score. Separate goal-directedness, competence, regulation, and causal contribution.
2. **Specify real hypothesis families.** Include strong adaptive, scripted, retrieval, behavior-cloning, and stochastic nulls with priors or complexity control. Make “passive” actually passive if that contrast is retained.
3. **Fit, then test blind.** Learn or calibrate models on baseline data and evaluate predeclared predictions on held-out interventions. Keep the evaluator blind to implementation labels.
4. **Implement the advertised method.** Estimate mutual information, optimize over candidate probes, report costs and risks, define epsilon and divergence, and solve or approximate the battery problem.
5. **Use interventions that occur during behavior.** Move a goal or introduce an obstruction after a trajectory has begun, so correction and replanning are observed rather than implied by restarting a condition with oracle knowledge.
6. **Fix the likelihood.** Record action labels or marginalize over latent actions that produce the same observed next state. Specify every likelihood term, including declarations.
7. **Build an explicit SCM.** Remove hidden fallback controllers, define plausible component interventions, justify counterfactual coalitions, and analyze sensitivity to baselines, partitions, and invalid coalitions.
8. **Validate attribution against known ground truth.** Compare Shapley maps with direct causal effects and alternative attribution methods across multiple architectures. Do not use a constant dummy player as the flagship validation.
9. **Retire or validate `L`.** A difference between normalized Shapley profiles needs a construct-validity argument and invariance or calibration results before it can be called agency theater.
10. **Run a real assemblage.** The paper is motivated by model/persona/memory/harness/tool systems and calls the device a “centaur” agentoscope. Test at least one actual tool-using language-model system and one human–machine workflow.
11. **Add robustness and uncertainty.** Sweep seeds, geometries, horizons, temperatures, noise, goals, probe orders, and null misspecification. Report intervals and held-out performance rather than one rounded seed.
12. **Add tests and fail loudly.** Unit-test the scorer, interventions, action likelihood, Shapley identities, and claim ledger. Figure failures should fail the build.
13. **Cut the false etymology.** Call *peira* an analogy if desired, not an ancestor.
14. **Move the consciousness section to a clearly marked philosophical coda.** Either engage actual consciousness theories and derive testable consequences, or present the precautionary stance without pretending it follows from the agentoscope.

## Bottom line

The paper’s best insight is a sentence: when rival organizational models agree on the observations available so far, choose an intervention under which they disagree. That sentence is correct, useful, and old.

Everything beyond it must earn its keep. In the current version, the new field is largely branding, the instrument is largely a diagram, the formalism is largely unapplied, and the simulation is largely self-confirmation. The prose repeatedly announces epistemic severity while the code gives every test its answer in advance. Until the method survives blind evaluation against strong nulls on a real assemblage, *Perturbatics* should be read as an evocative research program—not as a science, an agentoscope, or evidence that agency has been measured and mapped.
