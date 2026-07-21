"""Deterministic demonstrator for *Perturbatics*.

A gridworld holds three systems that trace the same path at rest and so cannot be
told apart by watching: a route-script that replays its stored path, a reactive
controller that greedily tracks the current target (wall-blind, no planning), and
a goal planner that represents a goal and replans. The demonstrator establishes
four facts, each a claim the paper makes precise.

  1. The Probe Separation Principle, in the shape the battery formalism
     predicts. At rest no pair of systems separates (identical trajectories,
     AUROC 0.50). No single probe separates every pair either: the moved goal
     exposes the route script (AUROC 1.0) but leaves the two goal-trackers
     trajectory-identical (0.50), and the blocked path exposes the planner
     (0.79) but collapses the two wall-blind systems together (0.50). The
     battery separates every pair; under an equal mixture of the two probes
     the planner-vs-script AUROC is 0.95.

  2. The do-Shapley realization map. The planner assemblage is decomposed into
     six components (goal register, planner, memory, map, harness, persona). Each
     component's causal contribution to the agency evidence is its do-Shapley
     value under the interventional value function nu(S) = E[A | do(ablate the
     complement of S)]. The persona is inert by construction, not by discovery:
     it has no motor channel (capacity share 0 by design) and its evidence share
     is a cheap-talk dial (DECL_FRAC/(1+DECL_FRAC) identically, 0.23 at 0.3), so
     the dual map displays the identity/agency separation rather than finds it.

  3. Synergy. Agency is non-additive. The planner and the map have a positive
     average interaction in the capacity game: when memory is absent, only the
     two together can route around an obstacle. The complementarity is
     conditional, not exclusive (memory nearly substitutes for the map by
     learning walls on contact, which is why the map-memory interaction is
     negative), and no single component "owns" the rerouting.

  4. Two guards. Richness is a false friend: a chaotic walker with the highest
     trajectory complexity emits negative agency evidence while the simplest
     system scores among the most agentic, so complexity is no proxy for
     agency. And the reading depends on the declared boundary, swept as an
     enclosure (components outside the candidate unit held at their null, the
     lesion form of the boundary question): the realized capacity is negative
     when the boundary encloses only the planner and its actuator and rises
     only when the goal register and the map are enclosed with it.

Everything is deterministic given the recorded seed. The models are illustrative
and instantiate the paper's definitions; they are not fit to data. Every reported
number is a key in results.json.
"""
from __future__ import annotations

from collections import deque
from itertools import combinations

import numpy as np

SEED = 0
N = 13                     # grid side
T = 40                     # steps per episode
BETA = 1.5                 # inverse temperature of the trajectory models
DECL_FRAC = 0.3            # cheap-talk (persona declaration) evidence, as a fraction of
                           #   the full-assemblage movement evidence per probe
N_INSTANCES = 40           # random (start, goal, moved-goal, wall) instances
COMPONENTS = ["goal_register", "planner", "memory", "map", "harness", "persona"]

MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]   # up, down, left, right, stay


def _rng(seed: int = SEED) -> np.random.Generator:
    return np.random.default_rng(seed)


def _in_grid(c):
    return 0 <= c[0] < N and 0 <= c[1] < N


def _neighbors(c):
    return [(c[0] + d[0], c[1] + d[1]) for d in MOVES]


_BFS_CACHE: dict = {}


def bfs_dist(goal, walls):
    """Shortest-path distance from every cell to goal, respecting walls. inf if blocked.
    Memoized on (goal, walls): the sweep re-visits the same few wall sets thousands of
    times across coalitions and seeds, and the returned array is only ever read."""
    key = (goal, frozenset(walls))
    hit = _BFS_CACHE.get(key)
    if hit is not None:
        return hit
    dist = np.full((N, N), np.inf)
    if goal in walls:
        _BFS_CACHE[key] = dist
        return dist
    dist[goal] = 0
    q = deque([goal])
    while q:
        c = q.popleft()
        for d in MOVES[:4]:
            nb = (c[0] + d[0], c[1] + d[1])
            if _in_grid(nb) and nb not in walls and dist[nb] == np.inf:
                dist[nb] = dist[c] + 1
                q.append(nb)
    _BFS_CACHE[key] = dist
    return dist


def manhattan(c, goal):
    return abs(c[0] - goal[0]) + abs(c[1] - goal[1])


def make_instances(seed: int = SEED):
    """Deterministic set of episodes: a start, a baseline goal, a moved goal, and a
    wall segment that blocks the straight route from start to the baseline goal.
    An instance is kept only if the frozen rest path actually meets the wall, so
    every blocked episode genuinely forces a detour and "blocked" is never a
    misnomer for a gap-aligned straight run. The instances are drawn once from the
    seed; every episode is then deterministic. A fixed seed makes the sample
    reproducible, not less of a sample, which is why the seed sweep below reports
    the AUROC ranges across seeds."""
    rng = _rng(seed)
    insts = []
    while len(insts) < N_INSTANCES:
        start = (rng.integers(0, 3), rng.integers(0, N))
        g0 = (N - 1 - rng.integers(0, 3), rng.integers(0, N))
        g1 = (rng.integers(0, N), rng.integers(0, N))
        if manhattan(start, g0) < 6 or manhattan(g1, g0) < 4:
            continue
        # a short horizontal wall midway, leaving a gap so a detour exists
        row = N // 2
        gap = int(rng.integers(1, N - 1))
        walls = {(row, j) for j in range(N) if j != gap and j != gap - 1}
        inst = {"start": tuple(map(int, start)), "g0": tuple(map(int, g0)),
                "g1": tuple(map(int, g1)), "walls": walls, "wall_row": row}
        # keep only instances the block probe actually blocks: the frozen rest path
        # must hit the wall, or "blocked" is a misnomer for a gap-aligned straight run
        if not any(cell in walls for cell in route_script_traj(inst, "rest")[1:]):
            continue
        insts.append(inst)
    return insts


def run_episode(active, inst, probe):
    """Trajectory of the assemblage with only `active` components functioning.

    probe: 'rest' (goal g0, no wall), 'move' (goal jumps to g1), 'block' (wall on
    the path to g0). The true current goal is g1 under 'move', else g0.
    """
    start, g0, g1 = inst["start"], inst["g0"], inst["g1"]
    true_walls = inst["walls"] if probe == "block" else set()
    # the goal the system internally pursues: the moved goal only if it has a goal register
    if probe == "move" and "goal_register" in active:
        internal_goal = g1
    else:
        internal_goal = g0

    known = set()                       # walls the system can plan around
    if "map" in active:
        known |= true_walls             # the map reveals the walls
    traj = [start]
    c = start
    for t in range(T):
        if "planner" in active:
            dist = bfs_dist(internal_goal, known)
            best, best_d = c, dist[c] if dist[c] < np.inf else np.inf
            for d in MOVES[:4]:
                nb = (c[0] + d[0], c[1] + d[1])
                if _in_grid(nb) and nb not in known and dist[nb] < best_d:
                    best, best_d = nb, dist[nb]
            step = best
            if step in true_walls:      # planned into an unknown wall
                if "memory" in active:
                    known.add(step)     # learn it and stay to replan next step
                    step = c
                else:
                    step = c            # collide, stuck
        else:                            # reactive greedy descent, wall-blind
            best, best_d = c, manhattan(c, internal_goal)
            for d in MOVES[:4]:
                nb = (c[0] + d[0], c[1] + d[1])
                if _in_grid(nb) and manhattan(nb, internal_goal) < best_d:
                    best, best_d = nb, manhattan(nb, internal_goal)
            step = best if best not in true_walls else c
        if "harness" not in active and t % 2 == 1:
            step = c                     # degraded executor: drop every other action
        # persona has no effect on the step
        c = step
        traj.append(c)
    return traj, true_walls


def route_script_traj(inst, probe):
    """The route script proper: it stores the path it traced at rest and replays
    it cell by cell. A stored step into a wall, or one it can no longer reach
    after bumping, leaves it holding position. (On these instances the replay
    coincides extensionally with wall-blind greedy descent toward the frozen
    goal; it is implemented as a replay so the mechanism matches the name.)"""
    stored = run_episode({"map", "harness"}, inst, "rest")[0]
    true_walls = inst["walls"] if probe == "block" else set()
    c = stored[0]
    traj = [c]
    for nxt in stored[1:]:
        adjacent = abs(nxt[0] - c[0]) + abs(nxt[1] - c[1]) <= 1
        step = nxt if (adjacent and nxt not in true_walls) else c
        c = step
        traj.append(c)
    return traj


def agency_evidence(traj, inst, probe):
    """A = sum_t [ log P(step | goal model) - log P(step | inertial model) ].

    Goal model: prefers steps that reduce graph distance to the true current goal
    (wall-aware, so it rewards a detour). Passive rival: prefers steps that reduce
    straight-line distance to the baseline goal, relaxation toward a fixed
    attractor, blind to walls in its metric though not in its physics: both
    models share the same physically clamped label space, so a commanded step
    into a wall scores zero progress under both, and the comparison stays like
    for like. Both models are softmax policies over the five action labels (four
    moves and stay), with invalid moves clamped to stay; the observed data are
    state transitions, from which the acted label is reconstructed (ties resolve
    to stay), and the likelihood is proper over action labels rather than next states
    (several labels can share the stay outcome), and the two models share one
    label space, so the comparison is like for like. Marginalizing over the labels
    that share the stay outcome would change nothing: a clamped move has zero
    progress under both models, the same score the stay label has, so the summed
    stay mass is k*exp(0) in both numerators and the log-ratio, the only quantity
    used, is invariant to the marginalization."""
    g0, g1 = inst["g0"], inst["g1"]
    true_goal = g1 if probe == "move" else g0
    walls = inst["walls"] if probe == "block" else set()
    gdist = bfs_dist(true_goal, walls)

    def logp(c, nxt, model):
        scores = []
        chosen = None
        for k, d in enumerate(MOVES):
            nb = (c[0] + d[0], c[1] + d[1])
            if not _in_grid(nb) or nb in walls:
                nb = c
            if model == "goal":
                prog = (gdist[c] if gdist[c] < np.inf else 3 * N) - \
                       (gdist[nb] if gdist[nb] < np.inf else 3 * N)
            else:  # inertial: straight-line progress to baseline goal, wall-blind
                prog = manhattan(c, g0) - manhattan(nb, g0)
            scores.append(BETA * prog)
            if nb == nxt or (nb == c and nxt == c):
                chosen = k
        scores = np.array(scores)
        logZ = np.log(np.sum(np.exp(scores - scores.max()))) + scores.max()
        if chosen is None:
            chosen = 4
        return scores[chosen] - logZ

    A = 0.0
    for t in range(len(traj) - 1):
        A += logp(traj[t], traj[t + 1], "goal") - logp(traj[t], traj[t + 1], "inertial")
    return A


def capacity(traj, inst, probe):
    """Realized agency: the fraction of graph distance to the true current goal that
    the trajectory closes. This is what the system actually achieves, as distinct
    from the evidence it emits for being agentic."""
    g0, g1 = inst["g0"], inst["g1"]
    true_goal = g1 if probe == "move" else g0
    walls = inst["walls"] if probe == "block" else set()
    gdist = bfs_dist(true_goal, walls)

    def d(c):
        return gdist[c] if gdist[c] < np.inf else 3 * N

    d0, dT = d(traj[0]), d(traj[-1])
    return float((d0 - dT) / d0) if d0 > 0 else 0.0


def nu(active, insts, probes, ref, kind, decl):
    """Interventional value function for a target `kind`: 'E' for the agency evidence
    (behavioural movement plus the persona's cheap-talk declarations) or 'C' for
    realized capacity. Components not in `active` are held at their null (a
    do-intervention on the configuration switch); each probe is weighted equally by
    normalising against the full-assemblage reference `ref[probe]`."""
    active = set(active)
    per = []
    for probe in probes:
        vals = []
        for inst in insts:
            traj = run_episode(active, inst, probe)[0]
            if kind == "E":
                a = agency_evidence(traj, inst, probe)
                if "persona" in active:
                    a += decl[probe]              # cheap talk: announce the goal each step
                vals.append(a)
            else:
                vals.append(capacity(traj, inst, probe))
        per.append(float(np.mean(vals)) / ref[probe])
    return float(np.mean(per))


def do_shapley(insts, probes, ref, kind, decl):
    """Exact do-Shapley values of the six components over the `kind` value function,
    and the interaction indices for a few key pairs."""
    comps = COMPONENTS
    n = len(comps)
    # cache nu over all 2^n coalitions
    cache = {}
    for r in range(n + 1):
        for S in combinations(range(n), r):
            cache[frozenset(S)] = nu([comps[i] for i in S], insts, probes, ref, kind, decl)
    from math import factorial
    phi = {}
    for i in range(n):
        others = [j for j in range(n) if j != i]
        val = 0.0
        for r in range(len(others) + 1):
            w = factorial(r) * factorial(n - r - 1) / factorial(n)
            for S in combinations(others, r):
                fs = frozenset(S)
                val += w * (cache[fs | {i}] - cache[fs])
        phi[comps[i]] = float(val)

    def interaction(i, j):
        others = [k for k in range(n) if k not in (i, j)]
        tot = 0.0
        for r in range(len(others) + 1):
            w = factorial(r) * factorial(n - r - 2) / factorial(n - 1)
            for S in combinations(others, r):
                fs = frozenset(S)
                tot += w * (cache[fs | {i, j}] - cache[fs | {i}]
                            - cache[fs | {j}] + cache[fs])
        return float(tot)

    idx = {c: k for k, c in enumerate(comps)}
    inter = {
        "planner__map": interaction(idx["planner"], idx["map"]),
        "map__memory": interaction(idx["map"], idx["memory"]),
        "goal_register__planner": interaction(idx["goal_register"], idx["planner"]),
    }
    return phi, inter, cache


def analysis_separation(insts):
    """Fact 1: observational equivalence at rest; separation by the battery and by
    no single probe. Three systems: the goal planner (full assemblage), the
    reactive controller (goal register but no planner: tracks the current target
    greedily, wall-blind), and the route script (replays its stored path)."""
    all_comps = set(COMPONENTS)
    reactive = {"goal_register", "map", "harness"}

    def traj(system, inst, probe):
        if system == "script":
            return route_script_traj(inst, probe)
        active = all_comps if system == "planner" else reactive
        return run_episode(active, inst, probe)[0]

    ev = {s: {p: [] for p in ("rest", "move", "block")}
          for s in ("planner", "reactive", "script")}
    for inst in insts:
        for probe in ("rest", "move", "block"):
            for s in ev:
                ev[s][probe].append(agency_evidence(traj(s, inst, probe), inst, probe))

    def auroc(pos, neg):
        pos, neg = np.array(pos), np.array(neg)
        wins = float((pos[:, None] > neg[None, :]).sum())
        ties = float((pos[:, None] == neg[None, :]).sum())
        return float((wins + 0.5 * ties) / (len(pos) * len(neg)))

    pairs = [("planner", "script"), ("planner", "reactive"), ("reactive", "script")]
    auroc_rest_pairs = {f"{a}_vs_{b}": round(auroc(ev[a]["rest"], ev[b]["rest"]), 6)
                        for a, b in pairs}
    auroc_per_probe = {p: {f"{a}_vs_{b}": round(auroc(ev[a][p], ev[b][p]), 6)
                           for a, b in pairs}
                       for p in ("move", "block")}
    pooled = {s: ev[s]["move"] + ev[s]["block"] for s in ev}
    return {
        "auroc_at_rest": round(auroc(ev["planner"]["rest"], ev["script"]["rest"]), 6),
        "auroc_at_rest_pairs": auroc_rest_pairs,
        "auroc_under_probe": round(auroc(pooled["planner"], pooled["script"]), 6),
        "auroc_per_probe": auroc_per_probe,
        "mean_evidence_rest_planner": round(float(np.mean(ev["planner"]["rest"])), 6),
        "mean_evidence_probe_planner": round(float(np.mean(pooled["planner"])), 6),
        "mean_evidence_probe_passive": round(float(np.mean(pooled["script"])), 6),
        "mean_evidence_probe_reactive": round(float(np.mean(pooled["reactive"])), 6),
        "_rest_planner": ev["planner"]["rest"], "_rest_passive": ev["script"]["rest"],
        "_rest_reactive": ev["reactive"]["rest"],
        "_probe_planner": pooled["planner"], "_probe_passive": pooled["script"],
        "_probe_reactive": pooled["reactive"],
    }


def analysis_seed_robustness(n_seeds: int = 20):
    """The reported AUROCs are properties of one drawn instance set. Redraw the
    instances under seeds 0..n_seeds-1 and report the range of the pairwise
    planner-vs-script separations, so the headline numbers carry their spread."""
    pooled, move_only, block_only = [], [], []
    for seed in range(n_seeds):
        insts = make_instances(seed)
        sep = analysis_separation(insts)
        pooled.append(sep["auroc_under_probe"])
        move_only.append(sep["auroc_per_probe"]["move"]["planner_vs_script"])
        block_only.append(sep["auroc_per_probe"]["block"]["planner_vs_script"])

    def rng_of(xs):
        return {"min": round(min(xs), 6), "max": round(max(xs), 6)}

    return {"n_seeds": n_seeds,
            "planner_vs_script_pooled": rng_of(pooled),
            "planner_vs_script_move": rng_of(move_only),
            "planner_vs_script_block": rng_of(block_only)}


def analysis_map_robustness(n_seeds: int = 20):
    """The maps are properties of one drawn instance set too, and the paper's ranking
    claims should carry their spread. Redraw the instances under seeds 0..n_seeds-1
    and recompute both Shapley maps and the legibility term. The persona's shares are
    theorems (constant across draws, by the pure-channel proposition); the earned
    components move with the draw, so the claim that the persona's L is the largest
    is an empirical ranking to be counted, not assumed."""
    L_by_comp = {c: [] for c in COMPONENTS}
    largest = []
    for seed in range(n_seeds):
        insts = make_instances(seed)
        probes = ("move", "block")
        full = set(COMPONENTS)
        ref_move = {p: float(np.mean([agency_evidence(run_episode(full, i, p)[0], i, p)
                                      for i in insts])) for p in probes}
        decl = {p: DECL_FRAC * ref_move[p] for p in probes}
        ref_E = {p: ref_move[p] + decl[p] for p in probes}
        ref_C = {p: float(np.mean([capacity(run_episode(full, i, p)[0], i, p)
                                   for i in insts])) for p in probes}
        phi_E, _, _ = do_shapley(insts, probes, ref_E, "E", decl)
        phi_C, _, _ = do_shapley(insts, probes, ref_C, "C", decl)
        L = {c: phi_E[c] - phi_C[c] for c in COMPONENTS}
        for c in COMPONENTS:
            L_by_comp[c].append(L[c])
        largest.append(max(COMPONENTS, key=lambda c: L[c]))

    def rng_of(xs):
        return {"min": round(min(xs), 6), "max": round(max(xs), 6)}

    return {"n_seeds": n_seeds,
            "legibility_ranges": {c: rng_of(L_by_comp[c]) for c in COMPONENTS},
            "persona_L_largest_in": largest.count("persona"),
            "largest_L_exceptions": {str(i): largest[i] for i in range(n_seeds)
                                     if largest[i] != "persona"}}


def run_invariants(insts, phi_E, phi_C, cache_E, cache_C):
    """Checks that fail loudly. Each is an identity the paper leans on: the rest
    trajectories really are identical across the three systems (checked cell by
    cell, the fact the at-rest panel rests on); at rest the two scoring models
    coincide, so the evidence is zero for every trajectory, including an
    arbitrary goal-indifferent one (the regime equivalence made literal, and
    stated as such rather than sold as a finding); Shapley efficiency holds for
    both maps; and the persona is a dummy player of the capacity game."""
    all_comps = set(COMPONENTS)
    reactive = {"goal_register", "map", "harness"}
    rest_identical = all(
        run_episode(all_comps, inst, "rest")[0]
        == run_episode(reactive, inst, "rest")[0]
        == route_script_traj(inst, "rest")
        for inst in insts)
    assert rest_identical, "rest trajectories differ across systems"
    # tested on the chaotic trajectories; the universal statement is derived
    # (at rest the two per-action score vectors coincide identically), the test
    # is a spot check of the derivation on the least goal-like walker available
    rest_zero = all(abs(agency_evidence(_chaotic_traj(inst, "rest"), inst, "rest")) < 1e-9
                    for inst in insts)
    assert rest_zero, "at rest the two models should coincide for any trajectory"
    n = len(COMPONENTS)
    full, empty = frozenset(range(n)), frozenset()
    eff_E = abs(sum(phi_E.values()) - (cache_E[full] - cache_E[empty]))
    eff_C = abs(sum(phi_C.values()) - (cache_C[full] - cache_C[empty]))
    assert eff_E < 1e-9 and eff_C < 1e-9, "Shapley efficiency violated"
    # the dummy property is per-coalition, not per-value: a zero Shapley value
    # can hide cancellation, so check every marginal contribution directly
    p = COMPONENTS.index("persona")
    dummy_err = max(abs(cache_C[S | frozenset([p])] - cache_C[S])
                    for S in cache_C if p not in S)
    assert dummy_err < 1e-12, "persona must be a capacity dummy in every coalition"
    return {"rest_trajectories_identical": rest_identical,
            "rest_evidence_zero_on_tested_trajectories": rest_zero,
            "shapley_efficiency_max_error": round(max(eff_E, eff_C), 12),
            "persona_capacity_dummy_all_coalitions_max_error": round(dummy_err, 12)}


def analysis_boundary_sweep(insts, probes, ref, decl):
    """Fact 4a: the realized-agency reading depends on the declared boundary. Nested
    units, components outside the boundary held at their null."""
    # the actuator sits inside every candidate acting unit; the boundary question is
    # how much of the cognitive apparatus (goal, world model, memory) is enclosed
    boundaries = [
        ("planner + harness", {"planner", "harness"}),
        ("+ goal register", {"planner", "harness", "goal_register"}),
        ("+ map, memory", {"planner", "harness", "goal_register", "map", "memory"}),
        ("+ persona", set(COMPONENTS)),
    ]
    return [(name, round(nu(b, insts, probes, ref, "C", decl), 6)) for name, b in boundaries]


def _chaotic_traj(inst, probe):
    """A high-complexity walker driven by a logistic map; ignores the goal but
    obeys the same physics as every other system, so under the block probe it
    cannot walk through a wall. An earlier version checked only the grid bound,
    letting chaos teleport through walls; the scorer then charged those illegal
    steps as forced stays, an artifact that punished complexity for a bug rather
    than for a fact about agency."""
    x = 0.37
    c = inst["start"]
    traj = [c]
    walls = inst["walls"] if probe == "block" else set()
    for _ in range(T):
        x = 3.9 * x * (1 - x)
        k = int(x * 4) % 4
        d = MOVES[k]
        nb = (c[0] + d[0], c[1] + d[1])
        c = nb if _in_grid(nb) and nb not in walls else c
        traj.append(c)
    return traj


def _complexity(traj):
    """Trajectory complexity: entropy of the move-direction distribution (bits)."""
    moves = []
    for a, b in zip(traj[:-1], traj[1:]):
        moves.append((b[0] - a[0], b[1] - a[1]))
    if not moves:
        return 0.0
    _, counts = np.unique(np.array(moves), axis=0, return_counts=True)
    p = counts / counts.sum()
    return float(-np.sum(p * np.log2(p)))


def analysis_richness_guard(insts):
    """Fact 4b: agency does not track complexity."""
    systems = {
        "planner": lambda inst, probe: run_episode(set(COMPONENTS), inst, probe)[0],
        "reactive": lambda inst, probe: run_episode(
            {"goal_register", "map", "harness"}, inst, probe)[0],
        "route_script": route_script_traj,
    }
    rows = {}
    for name, get_traj in systems.items():
        comp, agen = [], []
        for inst in insts:
            for probe in ("move", "block"):
                tr = get_traj(inst, probe)
                comp.append(_complexity(tr))
                agen.append(agency_evidence(tr, inst, probe))
        rows[name] = (float(np.mean(comp)), float(np.mean(agen)))
    # chaotic walker
    comp, agen = [], []
    for inst in insts:
        for probe in ("move", "block"):
            tr = _chaotic_traj(inst, probe)
            comp.append(_complexity(tr))
            agen.append(agency_evidence(tr, inst, probe))
    rows["chaotic"] = (float(np.mean(comp)), float(np.mean(agen)))
    xs = np.array([v[0] for v in rows.values()])
    ys = np.array([v[1] for v in rows.values()])
    corr = float(np.corrcoef(xs, ys)[0, 1])
    return {"systems": {k: (round(v[0], 6), round(v[1], 6)) for k, v in rows.items()},
            "complexity_agency_correlation": round(corr, 6)}


def analysis_persona_swap(insts, probes, ref, decl):
    """Identity and functional agency separate. No persona substitution is executed:
    the persona is a capacity dummy by construction, so replacing it with any other
    pure channel leaves the realized capacity identical, and the first row below is
    that identity, not an experiment. Swapping the model (planner -> reactive) is
    the intervention actually run, and it collapses the capacity."""
    full = set(COMPONENTS)
    swap_model = full - {"planner"}   # same persona, planner replaced by reactive
    return {
        "capacity_full": round(nu(full, insts, probes, ref, "C", decl), 6),
        "capacity_persona_identity": round(nu(full, insts, probes, ref, "C", decl), 6),
        "capacity_swap_model_keep_persona": round(nu(swap_model, insts, probes, ref, "C", decl), 6),
    }


def run() -> dict:
    insts = make_instances()
    probes = ("move", "block")
    full = set(COMPONENTS)
    # per-probe references: full-assemblage movement evidence, the persona's cheap-talk
    # declaration size (a fixed fraction of it), and full-assemblage realized capacity
    ref_move = {p: float(np.mean([agency_evidence(run_episode(full, inst, p)[0], inst, p)
                                  for inst in insts])) for p in probes}
    decl = {p: DECL_FRAC * ref_move[p] for p in probes}
    ref_E = {p: ref_move[p] + decl[p] for p in probes}   # full-assemblage total evidence
    ref_C = {p: float(np.mean([capacity(run_episode(full, inst, p)[0], inst, p)
                               for inst in insts])) for p in probes}
    phi_E, inter_E, cache_E = do_shapley(insts, probes, ref_E, "E", decl)
    phi_C, inter_C, cache_C = do_shapley(insts, probes, ref_C, "C", decl)
    legibility = {c: round(phi_E[c] - phi_C[c], 6) for c in COMPONENTS}
    # the maps are marginal contributions, not fractions of a whole: they sum to
    # nu(full) - nu(empty), and the empty coalition is not nothing (with every
    # switch at baseline the residue still drifts against the goal)
    nu_empty_E = cache_E[frozenset()]
    nu_empty_C = cache_C[frozenset()]
    # the boundary chain below is one path through the 2^6 enclosures the game
    # computes; ship the whole landscape (capacity range per enclosure size)
    n = len(COMPONENTS)
    by_size = {}
    for S, v in cache_C.items():
        by_size.setdefault(len(S), []).append(v)
    landscape = {str(k): {"min": round(min(vs), 6), "max": round(max(vs), 6)}
                 for k, vs in sorted(by_size.items())}
    checks = run_invariants(insts, phi_E, phi_C, cache_E, cache_C)
    robustness = analysis_seed_robustness()
    map_robustness = analysis_map_robustness()
    sep = analysis_separation(insts)
    boundary = analysis_boundary_sweep(insts, probes, ref_C, decl)
    richness = analysis_richness_guard(insts)
    persona = analysis_persona_swap(insts, probes, ref_C, decl)
    return {
        "note": "Illustrative gridworld; components held at their null by do-intervention; not fit to data. Deterministic.",
        "params": {"seed": SEED, "grid": N, "steps": T, "beta": BETA,
                   "declaration_fraction": DECL_FRAC,
                   "n_instances": N_INSTANCES, "components": COMPONENTS,
                   "probes": list(probes),
                   "probe_reference_movement_evidence": {k: round(v, 6) for k, v in ref_move.items()}},
        "separation": {k: v for k, v in sep.items() if not k.startswith("_")},
        "realization_map": {
            "evidence_map": {k: round(v, 6) for k, v in phi_E.items()},
            "capacity_map": {k: round(v, 6) for k, v in phi_C.items()},
            "evidence_map_sum": round(sum(phi_E.values()), 6),
            "capacity_map_sum": round(sum(phi_C.values()), 6),
            "empty_coalition": {"evidence": round(nu_empty_E, 6),
                                "capacity": round(nu_empty_C, 6)},
            "legibility": legibility,
            "interaction_index": {k: round(v, 6) for k, v in inter_C.items()},
            "interaction_index_evidence_game": {k: round(v, 6) for k, v in inter_E.items()}},
        "boundary_sweep": boundary,
        "enclosure_landscape_capacity_by_size": landscape,
        "richness_guard": richness,
        "persona_swap": persona,
        "separation_robustness": robustness,
        "map_robustness": map_robustness,
        "checks": checks,
        "_sep": sep,
    }
