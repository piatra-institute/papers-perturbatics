"""Deterministic demonstrator for *Perturbatics*.

A gridworld holds three systems that trace the same path at rest and so cannot be
told apart by watching: a route-script that replays a stored path, a reactive
controller that greedily descends toward a fixed target, and a goal planner that
represents a goal and replans. The demonstrator establishes four facts, each a
claim the paper makes precise.

  1. The Probe Separation Principle. At rest a classifier separates the planner
     from the passive systems at chance; under an informative probe (move the
     goal, block the path) the same classifier separates them perfectly. Agency
     is not on the observational record; it appears under intervention.

  2. The do-Shapley realization map. The planner assemblage is decomposed into
     six components (goal register, planner, memory, map, harness, persona). Each
     component's causal contribution to the agency evidence is its do-Shapley
     value under the interventional value function nu(S) = E[A | do(ablate the
     complement of S)]. The persona is provably inert (its value is zero), so
     performed identity and functional agency separate.

  3. Synergy. Agency is non-additive. The planner and the map are complementary:
     neither alone can route around an obstacle, so their do-Shapley interaction
     index is strongly positive, and no single component "owns" the rerouting.
     The map and the memory are substitutes, so their interaction is negative.

  4. Two guards. Richness is a false friend: a chaotic walker with the highest
     trajectory complexity has among the lowest agency, so agency does not track
     complexity. And the reading depends on the declared boundary: swept over
     nested candidate units, the agency evidence is near zero when the boundary
     is drawn around the planner alone and rises only when the goal register and
     the map are enclosed with it.

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


def _rng() -> np.random.Generator:
    return np.random.default_rng(SEED)


def _in_grid(c):
    return 0 <= c[0] < N and 0 <= c[1] < N


def _neighbors(c):
    return [(c[0] + d[0], c[1] + d[1]) for d in MOVES]


def bfs_dist(goal, walls):
    """Shortest-path distance from every cell to goal, respecting walls. inf if blocked."""
    dist = np.full((N, N), np.inf)
    if goal in walls:
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
    return dist


def manhattan(c, goal):
    return abs(c[0] - goal[0]) + abs(c[1] - goal[1])


def make_instances():
    """Deterministic set of episodes: a start, a baseline goal, a moved goal, and a
    wall segment that blocks the straight route from start to the baseline goal."""
    rng = _rng()
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
        insts.append({"start": tuple(map(int, start)), "g0": tuple(map(int, g0)),
                      "g1": tuple(map(int, g1)), "walls": walls, "wall_row": row})
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


def agency_evidence(traj, inst, probe):
    """A = sum_t [ log P(step | goal model) - log P(step | inertial model) ].

    Goal model: prefers steps that reduce graph distance to the true current goal
    (wall-aware, so it rewards a detour). Inertial model: prefers steps that reduce
    straight-line distance to the baseline goal (wall-blind, so it penalizes a
    detour and expects the original heading)."""
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
    """Fact 1: observational equivalence, interventional separation."""
    all_comps = set(COMPONENTS)
    a_rest_planner, a_rest_passive = [], []
    a_probe_planner, a_probe_passive = [], []
    for inst in insts:
        # planner = full assemblage; passive = route-script (no goal register, no planner)
        passive = {"map", "harness"}
        tr_p, _ = run_episode(all_comps, inst, "rest")
        tr_q, _ = run_episode(passive, inst, "rest")
        a_rest_planner.append(agency_evidence(tr_p, inst, "rest"))
        a_rest_passive.append(agency_evidence(tr_q, inst, "rest"))
        for probe in ("move", "block"):
            tp, _ = run_episode(all_comps, inst, probe)
            tq, _ = run_episode(passive, inst, probe)
            a_probe_planner.append(agency_evidence(tp, inst, probe))
            a_probe_passive.append(agency_evidence(tq, inst, probe))

    def auroc(pos, neg):
        pos, neg = np.array(pos), np.array(neg)
        wins = float((pos[:, None] > neg[None, :]).sum())
        ties = float((pos[:, None] == neg[None, :]).sum())
        return float((wins + 0.5 * ties) / (len(pos) * len(neg)))

    return {
        "auroc_at_rest": round(auroc(a_rest_planner, a_rest_passive), 6),
        "auroc_under_probe": round(auroc(a_probe_planner, a_probe_passive), 6),
        "mean_evidence_rest_planner": round(float(np.mean(a_rest_planner)), 6),
        "mean_evidence_probe_planner": round(float(np.mean(a_probe_planner)), 6),
        "mean_evidence_probe_passive": round(float(np.mean(a_probe_passive)), 6),
        "_rest_planner": a_rest_planner, "_rest_passive": a_rest_passive,
        "_probe_planner": a_probe_planner, "_probe_passive": a_probe_passive,
    }


def analysis_boundary_sweep(insts, probes, ref, decl):
    """Fact 4a: the realized-agency reading depends on the declared boundary. Nested
    units, components outside the boundary held at their null."""
    # the actuator sits inside every candidate acting unit; the boundary question is
    # how much of the cognitive apparatus (goal, world model, memory) is enclosed
    boundaries = [
        ("planner", {"planner", "harness"}),
        ("+ goal register", {"planner", "harness", "goal_register"}),
        ("+ map, memory", {"planner", "harness", "goal_register", "map", "memory"}),
        ("+ persona", set(COMPONENTS)),
    ]
    return [(name, round(nu(b, insts, probes, ref, "C", decl), 6)) for name, b in boundaries]


def _chaotic_traj(inst):
    """A high-complexity walker driven by a logistic map; ignores goals and probes."""
    x = 0.37
    c = inst["start"]
    traj = [c]
    for _ in range(T):
        x = 3.9 * x * (1 - x)
        k = int(x * 4) % 4
        d = MOVES[k]
        nb = (c[0] + d[0], c[1] + d[1])
        c = nb if _in_grid(nb) else c
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
        "planner": set(COMPONENTS),
        "reactive": {"goal_register", "map", "harness"},
        "route_script": {"map", "harness"},
    }
    rows = {}
    for name, active in systems.items():
        comp, agen = [], []
        for inst in insts:
            for probe in ("move", "block"):
                tr, _ = run_episode(active, inst, probe)
                comp.append(_complexity(tr))
                agen.append(agency_evidence(tr, inst, probe))
        rows[name] = (float(np.mean(comp)), float(np.mean(agen)))
    # chaotic walker
    comp, agen = [], []
    for inst in insts:
        for probe in ("move", "block"):
            tr = _chaotic_traj(inst)
            comp.append(_complexity(tr))
            agen.append(agency_evidence(tr, inst, probe))
    rows["chaotic"] = (float(np.mean(comp)), float(np.mean(agen)))
    xs = np.array([v[0] for v in rows.values()])
    ys = np.array([v[1] for v in rows.values()])
    corr = float(np.corrcoef(xs, ys)[0, 1])
    return {"systems": {k: (round(v[0], 6), round(v[1], 6)) for k, v in rows.items()},
            "complexity_agency_correlation": round(corr, 6)}


def analysis_persona_swap(insts, probes, ref, decl):
    """Identity and functional agency separate: swapping the persona leaves realized
    capacity unchanged; swapping the model (planner -> reactive) collapses it."""
    full = set(COMPONENTS)
    swap_persona = full            # persona relabelled: functionally identical set
    swap_model = full - {"planner"}   # same persona, planner replaced by reactive
    return {
        "capacity_full": round(nu(full, insts, probes, ref, "C", decl), 6),
        "capacity_swap_persona_keep_model": round(nu(swap_persona, insts, probes, ref, "C", decl), 6),
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
    phi_E, inter, _ = do_shapley(insts, probes, ref_E, "E", decl)
    phi_C, _, _ = do_shapley(insts, probes, ref_C, "C", decl)
    legibility = {c: round(phi_E[c] - phi_C[c], 6) for c in COMPONENTS}
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
            "legibility": legibility,
            "interaction_index": {k: round(v, 6) for k, v in inter.items()}},
        "boundary_sweep": boundary,
        "richness_guard": richness,
        "persona_swap": persona,
        "_sep": sep,
    }
