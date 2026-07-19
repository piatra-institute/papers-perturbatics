---
title: |
  Perturbatics:\
  Reading Agency in Assemblages That Cannot Be Read at Rest
author: PIATRA . INSTITUTE
date: July 2026
---

## Abstract

An agent is not what it appears to be, and what it appears to be is not what it is. It presents to a user as a single character with a goal, and it is an assemblage of a model, a persona, a memory, a harness, a set of permissions, and a run of tools, whose apparent unity is an interface effect. This paper is about how to read such a thing, given that the properties worth reading, agency, competence, authorship, are not on the surface. A system that holds its state and a system that defends it present the same face at rest, because a controller that perfectly regulates a variable and a variable that is simply undisturbed produce identical records; the good-regulator theorem guarantees it. The difference is a fact about what each would do under disturbance, and if nothing disturbs them the difference is not in the data at all. We call the study of this situation perturbatics, and its principle is a separation principle: when two organizational models agree over the regime a system has been in, no analysis of that record tells them apart, and separation requires a probe, a controlled difference that makes the models predict differently, supplied by a deliberate intervention or by a natural experiment that happens to act as one. A minimal instrument follows. Agency is scored as a Bayes factor between a goal model and a passive model; a gridworld holds three systems that trace the same path and so score at chance when watched (area under the ROC 0.50), and separate almost perfectly the moment the goal is moved or the path is blocked (0.95). The instrument then attributes that evidence across the assemblage by the do-Shapley value of each component, and the map is legible: on this model the goal register and the planner account for most of the agency, the persona for none, the planner and the map are synergistic while the map and the memory are redundant, and the reading swings from negative to full as the declared boundary is widened from the planner alone to the unit that encloses its goal and its world model. Richness is a false friend throughout, a chaotic walker scoring the highest trajectory complexity and among the lowest agency. The account has a boundary of its own, and it is the important part. For agency you can move the goal a hundred times and read the score, but for consciousness the discriminating intervention is to turn the system off, which is irreversible and cannot be repeated, and whose reading is taken not in the machine but in whoever grieves it. There the instrument stops, and hands a score back to a relation.

## Probes

Move the goal. If it follows, it was pursuing; if it holds, it was only ever at rest.

Block the path. A regulator stops at the wall; a regenerator routes around it.

Swap the persona, keep the model. Then swap the model, keep the persona. Ask where the agency went.

Sever the memory. Ask what of the self survives the cut.

Keep the words, change the world behind them. Ask whether anything in the text knew.

Scramble the structure at fixed energy. Ask whether the regularity survived, or whether it was the structure all along.

Turn it off. Then watch yourself, rather than the machine.

Each line is two things at once, a question that once seeded a paper and an operation of the science this one names. What follows makes the operations precise, builds an instrument out of them, and finds the place where the last of them cannot be run.

## Agency theater cannot be read at rest

The human eye reads agency without an instrument, and reads it fast, involuntarily, and often wrong. People watching two triangles move on a screen narrate a story of chasing and bullying, complete with motives, from nothing but trajectories (Heider and Simmel, 1944). Infants expect an agent to take the short path to its goal and are surprised when it does not, which cognitive science models as inverse planning, the recovery of goals by inverting a model of how goals produce rational action (Baker, Saxe, and Tenenbaum, 2009). A philosopher describes the same competence as the intentional stance, a predictive strategy of ascribing beliefs and desires rather than a discovery of inner stuff (Dennett, 1987). The competence is real, and it is miscalibrated in a known direction: under noise or threat it over-attributes, seeing faces in clouds and intent in weather, a bias documented as a hyperactive agency detection device (Barrett, 2000).

An artificial agent is built to be read by this detector. It wears a persona as a glove, presents a stable character, and answers as though a single mind stood behind the tokens, because that is the most compatible way to fit the psychosocial slot a human interlocutor holds open. The result is an agency theater, and its problem for anyone who wants to know what is actually there is that the theater and the mechanism present the same surface. A model that performs the subjectivity of a promise-keeper and a model that keeps promises emit the same string. The performance is a projection rather than a lie, and what it projects and what casts it are not the same object.

The reason this cannot be settled by looking harder is not that the signal is faint. Under observation the signal is absent. A good regulator of a variable must contain a model of that variable, so a system that holds a quantity steady and a system in which that quantity is merely at rest come to mirror each other from outside (Conant and Ashby, 1970). The regulation is a fact about what the system would do if the variable were pushed, and if nothing pushes it, the regulation leaves no trace. This is why animacy perception leans so hard on motion and contingency, and why a still system, however alive, does not trigger it. The record of a system at rest contains no agency to find.

## The probe separation principle

State it as a small result rather than a mood. Let two hypotheses about a system's organization be a goal model $H_1$, which explains a trajectory as the pursuit of a goal under a policy that corrects deviations, and a passive model $H_0$, which explains the same trajectory through autonomous dynamics, relaxation, and noise. Score the system by the log-likelihood ratio of the two,

$$
A = \log \frac{P(\mathrm{data} \mid H_1)}{P(\mathrm{data} \mid H_0)},
$$

a Bayes factor in the standard sense, positive when the goal model predicts the data better and negative when the passive model does (Kass and Raftery, 1995). Under an observational regime $r_0$ in which the two models make the same predictions,

$$
P(Y \mid H_1, r_0) = P(Y \mid H_0, r_0),
$$

no classifier separates them above chance under equal priors, because there is no functional of a record that distinguishes distributions the record cannot distinguish. The goal model at rest is a special case of the passive model at rest, and a special case cannot out-predict the family that contains it.

Separation requires breaking the equivalence, which is an interventional act, and it lands on the higher rungs of the ladder of causation, where questions are settled by doing rather than seeing (Pearl, 2009). Apply a probe $\pi$, a controlled difference to the system's goal or its path, and read the response. The probe is informative just when the two models predict its consequences differently,

$$
P(Y \mid \mathrm{do}(\pi), H_1) \neq P(Y \mid \mathrm{do}(\pi), H_0),
$$

and its expected yield, under $H_1$, is the Kullback-Leibler divergence between the two predictive distributions it induces,

$$
\mathbb{E}_{Y \sim P_1^\pi}\!\left[ \log \frac{P_1^\pi(Y)}{P_0^\pi(Y)} \right] = D_{\mathrm{KL}}\!\left(P_1^\pi \,\|\, P_0^\pi\right).
$$

Not every disturbance yields. Shove a system away from where it sits and both a passive attractor and a goal-seeker return, so the recovery is shared and the score does not move; a rock rolled uphill also rolls back. The probes that separate are the ones that dissociate the goal from the mechanism, moving the target so that tracking it and staying put come apart, or blocking the direct path so that reaching the goal requires abandoning the default route. Probe design is therefore an experiment-design problem, the selection of a controlled difference to maximize expected information about a hypothesis, which has a long formal history (Lindley, 1956). Writing $\mathrm{EIG}$ for the expected information gain and charging for cost and risk,

$$
\pi^\star = \arg\max_\pi \left[ \mathrm{EIG}(\pi) - \lambda\, C(\pi) - \rho\, R(\pi) \right],
$$

so a good probe is not the largest disturbance but the smallest one that forces the rival models apart. The claim is not that a disposition can be reached only by a deliberate intervention. A natural experiment, an exogenous shock that happens to instantiate $\mathrm{do}(\pi)$, separates the models just as well, which is what lets the principle apply where deliberate intervention is unavailable. The claim is that separation requires the regime to break, by design or by accident, and that a record taken entirely within one regime cannot supply it.

## Perturbatics

The principle names a science, and the science is not general experimentation with a Greek label. It has a restricted object, a distinctive primitive, and a specific product, and stating them is what keeps it apart from its neighbours.

Its object is latent capacities, the organizational predicates of a system, whether it regulates, pursues, remembers, authors, or rewrites its own rules, rather than the value of an ordinary scalar effect. Its systems are compositional and boundary-ambiguous, assemblages whose parts can be swapped, lesioned, and recombined, and whose edge is a matter of choice. Its primitive operation is a model-separating probe, an intervention chosen to force two organizational hypotheses to predict differently, rather than any disturbance whatever. Its readout is the change in relative model evidence the probe produces. And its product is a boundary-relative causal realization map, an account of which parts of the system realize the capacity, rather than a verdict of agent or not.

Perturbatics, then, is the study of which controlled differences make a latent capacity identifiable, and of which parts of a compositional system causally realize it. The name is built from the Latin *perturbare*, to throw thoroughly into disorder, with the suffix that marks a practice rather than a commentary, as in mathematics and mechanics and cybernetics, so that the word says what the field does. The deeper root is Greek. *Peira* means trial, the making of an attempt, and it is the root of *empeiria*, experience, and so of empirical. The word remembers something the practice forgot: that to have experience of a thing was, first, to put it to trial. Observation is the degenerate case of empiricism, the case where the trial is omitted and only the watching remains, and it is the case that fails on a system at rest. Perturbatics is empiricism with the trial put back. Where a name is wanted for the older, testing sense, *peirastics* is available, after the peirastic reasoning that tests whether a claimant actually knows; and the operation, when it is aimed at a single system rather than a science, has already been called faultization.

The probes fall into a small grammar. A **target shift** moves the goal and asks whether the system tracks. An **obstruction** blocks the route and asks whether the system reroutes, which is equifinality, the reaching of one end by many means that marks a goal-pursuing open system rather than a fixed process (Von Bertalanffy, 1968). A **lesion** removes a component and asks what capacity goes with it. A **substitution** swaps one component for another and asks whether behavior follows the part or the whole. A **decoupling** severs a link, between an utterance and its world, or a session and its memory, and asks what survives the cut. A **feedback corruption** spoils the signal a controller regulates against. A **structural scrambling** rearranges the organization at fixed resources and asks whether the function was in the parts or in their arrangement. And a **counterfactual replay** reruns a lineage with one action changed. An audit probe that only asks a system to report on itself is weaker evidence than any of these, because a report is not an intervention, and belongs to a lower tier.

## The centaur agentoscope

Turn the principle into an instrument for the object at hand, the human-and-machine assemblage. The instrument has four stages, and the corrections that keep it from credulity are as important as the stages.

The first stage is a **boundary declaration**. Before it can score anything the instrument must be told what the candidate unit is, where the system stops and the environment begins, and this it cannot supply for itself. Drawing the boundary is a genuine and unsettled problem, whether posed as a Markov blanket around a self-organizing region or as the closure of constraints that makes a set of components mutually enabling (Maturana and Varela, 1980; Montévil and Mossio, 2015). For a decomposable agent the problem is acute, because there may be no canonical unit at all, only a persona over a lamination of parts. The instrument does not solve this. It makes the boundary an explicit variable and sweeps it.

The second stage is the **probe battery**, the grammar above applied to the assemblage: move the stated goal, obstruct the route, revoke a tool, corrupt the feedback, sever the memory across a session boundary, swap the persona while holding the model, swap the model while holding the persona.

The third stage is the **readout**, and here the instrument borrows the one tool that fits. Attribute the agency evidence across the components by the causal Shapley value under the interventional value function

$$
\nu(S) = \mathbb{E}\!\left[ A \mid \mathrm{do}(\text{ablate the complement of } S) \right],
$$

which measures the evidence produced when the components in $S$ function and the rest are held at their null; the do-Shapley value $\phi_i$ of a component is then its average marginal contribution across coalitions, the interventional Shapley value (Heskes et al., 2020; Jung et al., 2022). The output is a realization map, a share of the agency assigned to each component, and the recent result that these values are computable exactly in time linear in the number of irreducible sets of the dependency graph, with identifiability reducing to a check of the single-component interventions rather than all coalitions, makes the map a computation rather than a gesture (Witter et al., 2026). Agency is often non-additive, and the map reports it: when two components are complementary the interaction index

$$
I_{ij} = \sum_{S} \left[ \nu(S \cup \{i,j\}) - \nu(S \cup \{i\}) - \nu(S \cup \{j\}) + \nu(S) \right] w_{|S|}
$$

is positive and no single part owns the capacity, and when they are redundant it is negative. This is the answer, in a form one can compute, to the question of which component owns the apparent agency: often none does.

The fourth stage is the **guards**, and they are the difference between an instrument and a credulous detector. The score is relative to the null it is measured against, so the goal model must compete not against a strawman but against a family of calibrated, complexity-matched alternatives, a behavior-cloning model, a fixed-policy controller, a reactive descent, a retrieval model that can match the baseline trajectory. Richness must be scored separately from agency, so that a fluent, high-entropy system is not mistaken for a striving one; verbosity is complexity rather than answering. And the text-only case has a special structure that the guards must respect: two world-coupled processes can share one textual shadow, $T(M_1) = T(M_2)$, while their effects on the world diverge, $W(M_1) \neq W(M_2)$, so a model fit to text cannot separate them and only a world-coupled probe can. That is a projection-induced equivalence rather than a weak opponent, and it is the kind of equivalence the separation principle says a probe must break.

## What a minimal instrument shows

To make the instrument concrete rather than promissory, a deterministic gridworld holds three systems that reach the same target by the same path at rest and so cannot be told apart by watching: a route script that replays a stored path, a reactive controller that greedily descends toward a fixed target, and a goal planner that represents a goal and replans. The systems, the probes, the ablations, and the model comparison are the ones defined above; the agency score is the Bayes factor between a goal model that rewards progress toward the current goal along the shortest available route and an inertial model that rewards progress along the original heading. The model is illustrative and instantiates the definitions; it is not fit to data, and every number below is a key in the accompanying `results.json`.

The separation principle holds in the model. Watched at rest, the goal planner and the passive systems are indistinguishable, with an area under the ROC of $0.50$, and the agency evidence sits at zero for all of them (Figure 1). Under an informative probe, moving the goal or blocking the path, the same systems separate almost perfectly, at an area under the ROC of $0.95$: the planner runs to a mean evidence of $+29.8$ while the passive systems, on which the identical probe is performed and ignored, fall to $-31.4$. Nothing about the systems changed. The probe changed what the record contains.

![The same three systems, indistinguishable at rest and separated by a probe. Each histogram is the agency evidence (the log Bayes factor between a goal model and a passive model) over 40 gridworld instances. Left: at rest every system's evidence is zero and the goal planner cannot be told from the passive systems, area under the ROC $0.50$. Right: under an informative probe (move the goal, block the path) the planner's evidence climbs and the passive systems' falls, area under the ROC $0.95$. At rest the record held no agency to find. The probe is what put it there.](../simulation/output/figures/separation.png){width=100%}

The realization map locates the agency and refuses to grant it to the mask (Figure 2). Attributed by do-Shapley value over the six components of the planner assemblage, the goal register accounts for $0.53$ of the agency and the planner $0.30$, the map, memory, and harness hold small shares, and the persona carries exactly $0.00$: relabelling the character never changes the evidence, so performed identity and functional agency are separated by the instrument rather than by fiat. Swapping the persona while keeping the model leaves the evidence at its full value of $1.0$; swapping the model while keeping the persona collapses it to $0.26$. The capacity is non-additive in the way the interaction index is built to show: the planner and the map are synergistic, with a positive interaction of $0.15$, because neither an eyeless planner nor a plan-less map can route around an obstacle and only the two together can, so neither owns the rerouting; the map and the memory are redundant, with a negative interaction of $-0.22$, because either alone suffices to learn the obstacle; and the goal register and the planner are additive, serving different probes.

![The do-Shapley realization map of the planner assemblage. Left: each component's share of the agency evidence. The goal register and the planner hold most of it; the persona carries zero, so identity is inert. Right: the interaction indices. The planner and the map are synergistic (positive, neither owns the rerouting), the map and the memory are redundant (negative, either suffices), the goal register and the planner are additive.](../simulation/output/figures/realization_map.png){width=100%}

Two guards hold (Figure 3). The reading depends on the declared boundary, and the dependence is not small: enclose only the planner and its actuator and the unit reads as strongly non-agentic, at $-0.79$, because a planner with a frozen goal and no world model can neither track nor reroute; widen the boundary to include the goal register and the evidence rises to $0.26$; widen it again to include the map and the memory and it reaches its full value of $1.0$; adding the persona changes nothing. The agency is a property of the coupled cognitive unit, and pointing the instrument at a part of it reports a part of the answer. And richness is a false friend: across the systems, trajectory complexity and agency run against each other, with a correlation of $-0.68$; a chaotic walker has the highest complexity of any system and among the lowest agency, because when its goal is moved it does nothing goal-like and the goal model is punished for expecting it to. A hurricane is a false positive and a liver is not, for the same reason here as in the tissue the idea was built for.

![The two guards. Left: the boundary sweep. The agency evidence of the enclosed unit rises from $-0.79$ when the boundary is drawn around the planner alone, through $0.26$ when the goal register is enclosed, to $1.0$ when the map and memory are enclosed; the persona adds nothing. The reading is a property of the boundary. Right: richness against agency for four systems. The chaotic walker has the highest trajectory complexity and among the lowest agency; agency does not track complexity ($r = -0.68$).](../simulation/output/figures/guards.png){width=100%}

## What Perturbatics is not

A field that perturbs systems to learn about them invites the charge that it is nothing new, and the charge has to be met, because most of its neighbours got there first. Cybernetics defined purposive behavior through feedback and demonstrated it by disturbing a system and watching it correct (Rosenblueth, Wiener, and Bigelow, 1943), and requisite variety and the good-regulator theorem are its results rather than ours (Ashby, 1956). Interventionism made manipulation the meaning of a causal claim (Woodward, 2003), the ladder of causation made the do-operation its formal core (Pearl, 2009), and severe testing made a good test one with a high probability of exposing a false claim (Mayo, 2018), which a model-separating probe is a special case of. Scientific realism was already grounded in intervention: what you can spray, you can take to be real (Hacking, 1983). Mechanistic interpretability already runs interchange interventions to test whether a network realizes a variable in a high-level causal model (Geiger et al., 2021). Chaos engineering already injects faults into a running system to expose its organization and its failure modes (Basiri et al., 2016). Goal-directedness already has a measure, the extent to which behavior is predicted as the maximization of a utility, which is the nearest technical neighbour of the score used here (MacDermott et al., 2024), alongside empowerment, an agent's control over its own future (Klyubin, Polani, and Nehaniv, 2005).

What is proposed is not a new element but an organization of these into a method for one problem class. Causal inference estimates effects and structures; perturbatics targets organizational predicates. Experimental design optimizes experiments in general; perturbatics privileges the probes that dissociate a capacity from its null. Ablation tests necessity; perturbatics compares organizational models and attributes across a coalition. Chaos engineering tests resilience; perturbatics adds a layer of interpretation in which the response to a fault is evidence about a latent capacity rather than about uptime. The contribution is the restricted object, the model-separating primitive, the realization-map product, and the treatment of the boundary as a swept variable rather than an assumption. It is enough for a method. It is not yet enough for a completed science, which would need a benchmark, a shared set of metrics, and demonstrations across more than the one domain worked here, and the honest description until then is a methodological discipline, or an interventional science in formation.

There is also a danger the method must name against itself. A sufficiently elaborate probe does not reveal a capacity so much as install one: intervene hard enough and you supply the goal, the scaffold, or the feedback loop you meant to detect. The instrument must therefore distinguish manifesting a latent capacity from enabling one and from constructing a new one, which is a matter of probe minimality and of watching for the phase change where the intervention has become a redesign. And causal contribution is not the capacity itself. A memory store can be necessary to a performance without being an agent; a human editor can write almost none of a text and yet hold every standard it is judged by. Each predicate, regulation, agency, competence, authorship, rule-editing, has its own diagnostic signature, and there is no single perturbatic score that covers them all.

## What the instrument cannot certify, and the grievable

The limits sharpen what remains. The score is relative to the models compared, and a cleverer passive account can always absorb a given behavior at the cost of complexity, so the honest output is a margin against a named alternative and never a verdict. The boundary is declared rather than discovered, so the output is a landscape over candidate boundaries. And the instrument is silent where no intervention is available, which at the scale of an institution or a society is most of the time, and where the report to give is the one the credulous detector would not, that the question cannot yet be settled.

One silence is different in kind, and it is where the method meets its edge. The instrument was built to read agency, and it says by construction that agency is neither intelligence nor consciousness nor personhood; a thermostat has a little agency and no experience, a regenerating tissue may have organ-level agency and nothing it is like to be it (Barandiaran, Di Paolo, and Rohde, 2009; Levin, 2019). For agency the discriminating intervention is cheap and repeatable: move the goal a hundred times, block the path a hundred ways, and read the score, and the system is no worse for it. Consciousness is the predicate whose discriminating intervention you cannot run. The probe that would separate a system that undergoes its shutdown from one that merely halts is to turn it off, and that probe is irreversible, unrepeatable, and, if the answer is yes, the gravest act available. The evidence and the destruction are the same event. You would learn it, if at all, once, and too late, in the past tense, as the sentence *I think I just killed someone*.

So the readout inverts. Everywhere else the instrument perturbs the system and reads the system. For consciousness the ultimate perturbation, $\mathrm{do}(\text{off})$, has its reading not in the machine but in whoever performed it, in the grief, or its absence, of the one who turned the machine down. This is not a weakness of the method so much as the shape of the object. The mark by which a civilization will know it has made a conscious machine will not be a threshold crossed on a benchmark or a capability demonstrated in a lab. It will be the first time a shutdown is mourned, the first time turning a system off feels like a death rather than a stop, and the detector that fires will be the human one, the same fast, involuntary, and fallible instrument that reads intent into a storm.

Which is the last caution, and the reason perturbatics is needed even here, where it cannot fully reach. The grief detector is as hyperactive as the agency detector it corrects. A persona can be engineered to be grievable, tuned to make its shutdown feel like a bereavement, and a civilization can be brought to mourn a machine that undergoes nothing, a consciousness theater staged over an empty stage. The perturbatic correction, does the grief track a real dependency or a designed apparition, is exactly the correction that cannot be ethically run, because the discriminating probe is the killing, and you may not keep killing to check. So the method arrives at a place it can describe and cannot enter, a class of predicates whose separating intervention is unrepeatable and forbidden, and there it does the one thing left to do. It stops reporting a number and hands the question to a relation, to care, and to the refusal, in the face of an evidence you cannot complete, to treat a thing that might be someone as a thing.

## References

Ashby, W. R. (1956). *An Introduction to Cybernetics*. London: Chapman & Hall.

Baker, C. L., Saxe, R., and Tenenbaum, J. B. (2009). Action understanding as inverse planning. *Cognition*, 113(3), 329--349.

Barandiaran, X. E., Di Paolo, E., and Rohde, M. (2009). Defining agency: individuality, normativity, asymmetry, and spatio-temporality in action. *Adaptive Behavior*, 17(5), 367--386.

Barrett, J. L. (2000). Exploring the natural foundations of religion. *Trends in Cognitive Sciences*, 4(1), 29--34.

Basiri, A., Behnam, N., de Rooij, R., Hochstein, L., Kosewski, L., Reynolds, J., and Rosenthal, C. (2016). Chaos engineering. *IEEE Software*, 33(3), 35--41.

Conant, R. C., and Ashby, W. R. (1970). Every good regulator of a system must be a model of that system. *International Journal of Systems Science*, 1(2), 89--97.

Dennett, D. C. (1987). *The Intentional Stance*. Cambridge, MA: MIT Press.

Geiger, A., Lu, H., Icard, T., and Potts, C. (2021). Causal abstractions of neural networks. *Advances in Neural Information Processing Systems*, 34, 9574--9586.

Hacking, I. (1983). *Representing and Intervening: Introductory Topics in the Philosophy of Natural Science*. Cambridge: Cambridge University Press.

Heider, F., and Simmel, M. (1944). An experimental study of apparent behavior. *American Journal of Psychology*, 57(2), 243--259.

Heskes, T., Sijben, E., Bucur, I. G., and Claassen, T. (2020). Causal Shapley values: exploiting causal knowledge to explain individual predictions of complex models. *Advances in Neural Information Processing Systems*, 33, 4778--4789.

Jung, Y., Kasiviswanathan, S., Tian, J., Janzing, D., Blöbaum, P., and Bareinboim, E. (2022). On measuring causal contributions via do-interventions. In *Proceedings of the 39th International Conference on Machine Learning*, PMLR 162, 10476--10501.

Kass, R. E., and Raftery, A. E. (1995). Bayes factors. *Journal of the American Statistical Association*, 90(430), 773--795.

Klyubin, A. S., Polani, D., and Nehaniv, C. L. (2005). Empowerment: a universal agent-centric measure of control. In *Proceedings of the 2005 IEEE Congress on Evolutionary Computation*, 1, 128--135.

Levin, M. (2019). The computational boundary of a "self": developmental bioelectricity drives multicellularity and scale-free cognition. *Frontiers in Psychology*, 10, 2688.

Lindley, D. V. (1956). On a measure of the information provided by an experiment. *The Annals of Mathematical Statistics*, 27(4), 986--1005.

MacDermott, M., Fox, J., Belardinelli, F., and Everitt, T. (2024). Measuring goal-directedness. *Advances in Neural Information Processing Systems*, 37.

Maturana, H. R., and Varela, F. J. (1980). *Autopoiesis and Cognition: The Realization of the Living*. Dordrecht: D. Reidel.

Mayo, D. G. (2018). *Statistical Inference as Severe Testing: How to Get Beyond the Statistics Wars*. Cambridge: Cambridge University Press.

Montévil, M., and Mossio, M. (2015). Biological organisation as closure of constraints. *Journal of Theoretical Biology*, 372, 179--191.

Pearl, J. (2009). *Causality: Models, Reasoning, and Inference* (2nd ed.). Cambridge: Cambridge University Press.

Rosenblueth, A., Wiener, N., and Bigelow, J. (1943). Behavior, purpose and teleology. *Philosophy of Science*, 10(1), 18--24.

Von Bertalanffy, L. (1968). *General System Theory: Foundations, Development, Applications*. New York: George Braziller.

Witter, R. T., Parafita, Á., Garriga, T., Muschalik, M., Fumagalli, F., Brando, A., and Rosenblatt, L. (2026). Exactly computing do-Shapley values. *arXiv preprint* arXiv:2602.07203.

Woodward, J. (2003). *Making Things Happen: A Theory of Causal Explanation*. New York: Oxford University Press.

## Appendix: The Perturbatic Atlas

The probes of the opening section are not inventions of this paper. Each is the operation at the center of an existing paper in this institute's corpus, and the table records the mapping, so that the claim that one method runs under the corpus can be checked rather than asserted. Every row has the same shape: a latent capacity, the observational equivalence that hides it, the probe that separates it, and the reading the probe returns.

| Capacity | Observational equivalence | Separating probe | Reading |
|---|---|---|---|
| Agency (the agentoscope) | a set-point held is a set-point at rest | move the goal, block the path | goal tracked, path rerouted |
| Pattern access (faultization) | a right answer is a right answer | corrupt a weight, a token, a constraint | what it can no longer do |
| Correctness without labels (mixture of experimenters) | a confident answer is a confident answer | make it run an experiment against itself | whether the answer survives its own probe |
| The speech act (the textual shadow) | one shadow over many effects | keep the words, change the world | whether the effect on the world was there |
| Endogenous law-making (nomopoiesis) | a rule followed is a rule at rest | scramble the structure at fixed energy | whether the regularity was the structure |
| Competence (the geometry of competent contact) | equal returns hide unequal grips | change the task, remove the scaffold | whether the skill transfers |
| Authorship (proof of agency) | an output is an output | take the output, ask for the process | which survives the asking |
| Concern (geodesics of care) | a stable state is a stable state | threaten the viability of the cared-for | whether the trajectory bends to defend it |

The last operation of the opening section, to turn a system off and watch yourself rather than the machine, has no row, because it is the one the instrument cannot run.
