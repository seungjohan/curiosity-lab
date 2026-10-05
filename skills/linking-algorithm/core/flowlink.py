"""flowlink — the linking algorithm's core, portable (N311).

The latest version of the algorithm, as built and measured in Constellate
(`algorithm/pipeline/thinking.py`, `graph.py`, `trends.py`, `flows.py`), in one
standard-library file that any project copies into its own `scripts/`. A
project brings its resources' thinking flows; this finds where they meet.

    A flow     up        what moves it            {"interest-rates": -1}
               down      what it moves            {"prices": +1}
               chain     cause → effect steps     [["prices", "emigration", +1]]
               entities  who and what it is about ["Nintendo"]

Two flows meet wherever they reach the same variable, and *how* they reach it
is the kind of link and the reason shown: one feeds or works against the
other, they rival for a limited budget, pull a thing opposite ways, or hold
opposite stakes. Merged names, edges every flow may walk, rarity, hubs and
verdicts make it trustworthy. Part A is Constellate's rules unchanged —
`test_flowlink.py` holds them to that pipeline's own output.

Part B is new here: **time**. Constellate reads dates only for trends inside a
market flow. A study log and a day journal are indexed by date first, so a
flow may carry `when` and the core then knows two things Constellate never
needed: **a cause comes before its effect** (an influence running backwards in
time is demoted to hindsight) and **how far apart two things are**, which each
project weighs its own way through `time_factor`.

Part C is the whole-collection layer — groups, bridges, storylines that move
forward in time, bursts.

Copied, not imported: each project keeps its copy beside its own adapter.
Source of truth: curiosity-lab `skills/linking-algorithm/core/flowlink.py`.
"""

from __future__ import annotations

import math
import re
from collections import Counter, defaultdict, deque
from dataclasses import dataclass, replace
from datetime import date

VERSION = "2026-10-05 · Constellate algorithm @ N310 + time layer"

# ── Part A: thinking flows (Constellate thinking.py, unchanged) ─────────────

CONSENSUS = 2      # an edge this many flows wrote is shared knowledge
MAX_HOPS = 3
DECAY = 0.7        # each extra step of reasoning is a little less sure
HUB_SHARE = 0.1    # a variable on more than this share of flows (floor below) is background
HUB_FLOOR = 20

# kind: (weight, can justify a link on its own)
KINDS = {
    "influence": (1.0, True),
    "rivals": (0.9, True),
    "opposite-pull": (0.8, True),
    "opposite-stakes": (0.8, True),
    "co-drivers": (0.5, False),
    "shared-exposure": (0.4, False),
    "distant-stakes": (0.4, False),   # opposite stakes found down a chain: measured as noise
    "hindsight": (0.3, False),        # Part B: an influence that would run backwards in time
}


@dataclass
class Meeting:
    kind: str
    variable: str
    sign: int          # −1 one works against the other, +1 helps / allies
    score: float
    sentence: str      # with {A} and {B} for the two resources
    cause: str | None = None   # "A" or "B" for an influence: which side is the cause


def label(m: Meeting) -> str:
    if m.kind == "influence":
        return "works against" if m.sign < 0 else "feeds"
    return {"opposite-pull": "pulls against", "opposite-stakes": "opposite stakes",
            "co-drivers": "allies", "shared-exposure": "shared exposure"}.get(m.kind, m.kind)


def can_justify(m: Meeting) -> bool:
    return KINDS[m.kind][1]


def canonical(flow: dict, canon: dict) -> dict:
    """Merged names: two flows can only meet on the very same name."""
    same, names = canon.get("same", {}), canon.get("entities", {})
    if not same and not names:
        return flow
    out = dict(flow)
    for side in ("up", "down"):
        if side in flow:
            out[side] = {same.get(v, v): s for v, s in flow[side].items()}
    if "chain" in flow:
        out["chain"] = [[same.get(a, a), same.get(b, b), s] for a, b, s in flow["chain"]]
    if "entities" in flow:
        out["entities"] = list(dict.fromkeys(names.get(e, e) for e in flow["entities"]))
    return out


def shared_edges(flows: dict[str, dict], canon: dict) -> list[tuple[str, str, int]]:
    """Every is-a step, the short world list, and every edge CONSENSUS flows wrote."""
    seen: dict[tuple[str, str, int], int] = defaultdict(int)
    for f in flows.values():
        for a, b, s in {tuple(e) for e in f.get("chain", [])}:
            seen[a, b, s] += 1
    edges = {(a, b, +1) for a, b in canon.get("is_a", [])}
    edges |= {(a, b, s) for a, b, s in canon.get("world", [])}
    edges |= {e for e, n in seen.items() if n >= CONSENSUS}
    return sorted(edges)


def _walk(start: dict[str, int], edges: dict[str, list[tuple[str, int]]]) -> dict:
    seen = {v: (s, 1, [v], [s]) for v, s in start.items()}
    frontier = dict(seen)
    for _ in range(MAX_HOPS - 1):
        nxt = {}
        for v, (s, h, path, steps) in frontier.items():
            for w, ws in edges.get(v, ()):
                if w not in seen:
                    seen[w] = nxt[w] = (s * ws, h + 1, path + [w], steps + [ws])
        frontier = nxt
    return seen


def reach(flow: dict, shared=()) -> tuple[dict, dict]:
    """(downstream, upstream): every variable within MAX_HOPS, with its sign,
    hops, path and step signs, both reading in the direction of cause."""
    fwd, back = defaultdict(list), defaultdict(list)
    for a, b, s in dict.fromkeys(tuple(e) for e in [*flow.get("chain", []), *shared]):
        fwd[a].append((b, s))
        back[b].append((a, s))
    down = _walk(flow.get("down", {}), fwd)
    up = {}
    for v, (s, h, path, steps) in _walk(flow.get("up", {}), back).items():
        up[v] = (s, h, list(reversed(path)), list(reversed(steps[1:])) + [steps[0]])
    return down, up


def variable_idf(reaches: dict[str, tuple[dict, dict]]) -> dict[str, float]:
    df: dict[str, int] = defaultdict(int)
    for down, up in reaches.values():
        for v in set(down) | set(up):
            df[v] += 1
    n = len(reaches) or 1
    return {v: math.log((n + 1) / (c + 1)) + 1 for v, c in df.items()}


def _words(v: str) -> str:
    return v.replace("-", " ")


def _told(first: str, down: tuple, up: tuple, second: str) -> str:
    _, _, dpath, dsteps = down
    _, _, upath, usteps = up
    running, parts = 1, []
    for v, st in zip(dpath, dsteps):
        running *= st
        parts.append(f"{'more' if running > 0 else 'less'} {_words(v)}")
    for v, st in zip(upath[1:], usteps[:-1]):
        running *= st
        parts.append(f"{'more' if running > 0 else 'less'} {_words(v)}")
    running *= usteps[-1]
    return f"{first} → " + " → ".join(parts) + f" → {'feeds' if running > 0 else 'works against'} {second}"


def meetings(ra: tuple, rb: tuple, idf: dict, limited: set[str], skip=frozenset()) -> list[Meeting]:
    """Every way two flows meet, best first; ties by name so either side sees the same order."""
    (da, ua), (db, ub) = ra, rb
    out: list[Meeting] = []

    def add(kind, v, sign, hops, sentence, cause=None):
        w, _ = KINDS[kind]
        out.append(Meeting(kind, v, sign, w * idf.get(v, 1.0) * DECAY ** (hops - 1), sentence, cause))

    for dx, ux, first, second, cause in ((da, ub, "{A}", "{B}", "A"), (db, ua, "{B}", "{A}", "B")):
        for v in (set(dx) & set(ux)) - skip:
            add("influence", v, dx[v][0] * ux[v][0], dx[v][1] + ux[v][1] - 1, _told(first, dx[v], ux[v], second), cause)
    for v in (set(da) & set(db)) - skip:
        sa, ha, sb, hb = da[v][0], da[v][1], db[v][0], db[v][1]
        if sa < 0 and sb < 0 and v in limited:
            add("rivals", v, -1, ha + hb - 1, f"{{A}} and {{B}} both take {_words(v)} — they compete for it")
        elif sa * sb < 0:
            up, down = ("{A}", "{B}") if sa > 0 else ("{B}", "{A}")
            add("opposite-pull", v, -1, ha + hb - 1, f"{up} pushes {_words(v)} up, {down} pulls it down")
        else:
            add("co-drivers", v, +1, ha + hb - 1, f"both push {_words(v)} {'up' if sa > 0 else 'down'}")
    for v in (set(ua) & set(ub)) - skip:
        sa, ha, sb, hb = ua[v][0], ua[v][1], ub[v][0], ub[v][1]
        if sa * sb < 0:
            win, lose = ("{A}", "{B}") if sa > 0 else ("{B}", "{A}")
            add("opposite-stakes" if ha == hb == 1 else "distant-stakes", v, -1, ha + hb - 1,
                f"more {_words(v)} helps {win} and hurts {lose}")
        else:
            add("shared-exposure", v, +1, ha + hb - 1, f"both rise and fall with {_words(v)}")
    return sorted(out, key=lambda m: (-m.score, m.variable, m.kind))


def verdict_key(a: str, b: str, variable: str, kind: str) -> str:
    x, y = sorted((a, b))
    return f"{x}|{y}|{variable}|{kind}"


class Web:
    """Everything that depends on the whole collection, built once."""

    def __init__(self, flows: dict[str, dict], canon: dict | None = None, limited=(), broad=(), drops=(),
                 when: dict[str, "When"] | None = None, hub_share: float = HUB_SHARE, hub_floor: int = HUB_FLOOR):
        """`hub_share`/`hub_floor` are Constellate's defaults. A project whose
        flows reach far by construction (a day reaches the week before it)
        counts its hubs itself and passes them as `broad`, with hub_share=1."""
        canon = canon or {}
        self.flows = {i: canonical(f, canon) for i, f in flows.items()}
        self.shared = shared_edges(self.flows, canon)
        self.reaches = {i: reach(f, self.shared) for i, f in self.flows.items()}
        self.idf = variable_idf(self.reaches)
        self.limited = set(limited)
        self.drops = set(drops)
        self.when = when or {}
        self.index: dict[str, set[str]] = defaultdict(set)
        for i, (down, up) in self.reaches.items():
            for v in set(down) | set(up):
                self.index[v].add(i)
        cap = max(hub_share * len(self.reaches), hub_floor)
        self.hubs = frozenset(v for v, ids in self.index.items() if len(ids) > cap) | frozenset(broad)

    def meet(self, a: str, b: str) -> list[Meeting]:
        """Every meeting between two resources, dropped verdicts removed, put in time."""
        ms = [m for m in meetings(self.reaches[a], self.reaches[b], self.idf, self.limited, self.hubs)
              if verdict_key(a, b, m.variable, m.kind) not in self.drops]
        if self.when:
            ms = sorted((in_time(m, self.when.get(a), self.when.get(b)) for m in ms),
                        key=lambda m: (-m.score, m.variable, m.kind))
        return ms

    def best(self, a: str) -> dict[str, Meeting]:
        """The best meeting with every resource this one's flow touches, preferring a reason."""
        if a not in self.reaches:
            return {}
        down, up = self.reaches[a]
        others = set().union(*(self.index[v] for v in (set(down) | set(up)) - self.hubs)) - {a}
        found = {}
        for b in sorted(others):
            ms = self.meet(a, b)
            if ms:
                found[b] = next((m for m in ms if can_justify(m)), ms[0])
        return found


# ── Part B: time ────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class When:
    """A span of time in years (fractional): a day, a year, a century."""
    start: float
    end: float

    @property
    def mid(self) -> float:
        return (self.start + self.end) / 2


def _ordinal(n: str) -> int:
    return int(re.match(r"\d+", n).group(0))


def when(value) -> When | None:
    """Read a date the way notes write it: 2026-10-05, 1665, -44, 44 BC, 1600s,
    1960s, 17th century, 5th century BC, 1600-1650. None when it is a name
    (`Ancient Rome`) rather than a date."""
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return When(float(value), float(value) + 1)
    if isinstance(value, date):
        y = value.year + (value.timetuple().tm_yday - 1) / 365.25
        return When(y, y + 1 / 365.25)
    s = str(value).strip().strip("[]\"' ").lower()
    m = re.fullmatch(r"(-?\d{4})-(\d{2})-(\d{2})", s)
    if m:
        try:
            return when(date(int(m.group(1)), int(m.group(2)), int(m.group(3))))
        except ValueError:
            return None
    bc = -1 if re.search(r"\b(bc|bce)\b", s) else 1
    s = re.sub(r"\s*\b(bc|bce|ad|ce)\b", "", s).strip()
    m = re.fullmatch(r"(\d+)(st|nd|rd|th)\s+century", s)
    if m:
        c = _ordinal(m.group(1))
        lo, hi = (c - 1) * 100, c * 100
        return When(lo, hi) if bc > 0 else When(-hi, -lo)
    m = re.fullmatch(r"(\d+)s", s)
    if m:
        y = int(m.group(1))
        span = 100 if y % 100 == 0 else 10
        return When(y, y + span) if bc > 0 else When(-(y + span), -y)
    m = re.fullmatch(r"(-?\d+)\s*[-–]\s*(-?\d+)", s)
    if m:
        a, b = int(m.group(1)) * bc, int(m.group(2)) * bc
        return When(min(a, b), max(a, b) + 1)
    m = re.fullmatch(r"-?\d+", s)
    if m:
        y = int(s) * bc
        return When(y, y + 1)
    return None


def in_time(m: Meeting, wa: When | None, wb: When | None) -> Meeting:
    """A cause comes before its effect. An influence whose cause began only
    after its effect had ended is demoted to hindsight: still a weight, never
    a reason. Unknown dates change nothing."""
    if m.kind != "influence" or wa is None or wb is None or m.cause is None:
        return m
    cause, effect = (wa, wb) if m.cause == "A" else (wb, wa)
    if cause.start < effect.end:
        return m
    w0, w1 = KINDS["influence"][0], KINDS["hindsight"][0]
    return replace(m, kind="hindsight", score=m.score * w1 / w0, sentence="in hindsight: " + m.sentence)


def years_apart(wa: When | None, wb: When | None) -> float | None:
    """Gap between two spans (0 when they overlap), in years."""
    if wa is None or wb is None:
        return None
    return max(0.0, max(wa.start, wb.start) - min(wa.end, wb.end))


# ── Part C: the whole collection ───────────────────────────────────────────

def communities(g: dict[str, set[str]], nodes: set[str] | None = None, rounds: int = 20) -> dict[str, str]:
    """Label propagation, deterministic; an edge counts 1 + the neighbours its
    two ends share, so one label cannot flood across a single bridge."""
    nodes = set(g) if nodes is None else nodes
    lab = {v: v for v in nodes}
    for _ in range(rounds):
        changed = False
        for v in sorted(nodes):
            near: Counter = Counter()
            for u in g.get(v, ()):
                if u in nodes:
                    near[lab[u]] += 1 + len(g[u] & g[v] & nodes)
            if not near:
                continue
            top = max(near.values())
            best = min(l for l, c in near.items() if c == top)
            if best != lab[v]:
                lab[v] = best
                changed = True
        if not changed:
            break
    return lab


def betweenness(g: dict[str, set[str]]) -> dict[str, float]:
    """Brandes, unweighted and undirected."""
    bc = dict.fromkeys(g, 0.0)
    for s in g:
        stack, pred = [], defaultdict(list)
        sigma, dist = defaultdict(int), {s: 0}
        sigma[s] = 1
        q = deque([s])
        while q:
            v = q.popleft()
            stack.append(v)
            for w in g[v]:
                if w not in dist:
                    dist[w] = dist[v] + 1
                    q.append(w)
                if dist[w] == dist[v] + 1:
                    sigma[w] += sigma[v]
                    pred[w].append(v)
        delta = defaultdict(float)
        while stack:
            w = stack.pop()
            for v in pred[w]:
                delta[v] += sigma[v] / sigma[w] * (1 + delta[w])
            if w != s:
                bc[w] += delta[w]
    return {v: x / 2 for v, x in bc.items()}


def bridges(g: dict[str, set[str]], k: int = 10, foothold: int = 2, min_group: int = 4) -> list[tuple[str, float, list[str]]]:
    """(node, betweenness, group labels it joins): a bridge needs `foothold`
    links into each of two groups, or vague nodes with one stray link win."""
    lab = communities(g)
    size = Counter(lab.values())
    out = []
    for v, x in sorted(betweenness(g).items(), key=lambda kv: (-kv[1], kv[0])):
        per = Counter(lab[u] for u in g[v] if size[lab[u]] >= min_group)
        held = sorted(l for l, c in per.items() if c >= foothold)
        if len(held) >= 2:
            out.append((v, x, held))
        if len(out) == k:
            break
    return out


def storyline(order: list[str], weight: dict[tuple[str, str], float], steps: int = 5) -> tuple[list[str], float]:
    """Shahaf & Guestrin's coherent chain: of the chains through `order` (the
    resources in time order) whose every step is a known link, the one whose
    weakest link is strongest. Each step moves forward in time."""
    n = len(order)
    w = {(i, j): weight[order[i], order[j]] for i in range(n) for j in range(i + 1, n) if (order[i], order[j]) in weight}
    for k in range(min(steps, n), 1, -1):
        best = [dict() for _ in range(n)]
        for j in range(n):
            best[j][1] = (float("inf"), None)
            for i in range(j):
                if (i, j) not in w:
                    continue
                for m, (weak, _) in best[i].items():
                    if m < k:
                        cand = min(weak, w[i, j])
                        if cand > best[j].get(m + 1, (-1.0, None))[0]:
                            best[j][m + 1] = (cand, i)
        ends = [(best[j][k][0], j) for j in range(n) if k in best[j]]
        if ends:
            weak, j = max(ends)
            chain, m = [j], k
            while m > 1:
                j = best[j][m][1]
                chain.append(j)
                m -= 1
            return [order[c] for c in reversed(chain)], weak
    return [], 0.0


def bursts(term_months: dict[str, list[str]], months: list[str], totals: Counter,
           s: float = 3.0, gamma: float = 1.0, min_count: int = 3) -> list[tuple[str, int, int, float]]:
    """Kleinberg's two-state bursts: (term, first month index, last, weight)."""
    n, D = len(months), sum(totals[m] for m in months)
    out = []
    for term, seen in term_months.items():
        r = Counter(seen)
        R = sum(r.values())
        if R < min_count or D == 0:
            continue
        p0 = R / D
        p1 = min(s * p0, 0.9999)
        if p1 <= p0:
            continue
        up = gamma * math.log(n) if n > 1 else 0.0
        cost_of = lambda r_, d_, p: -(r_ * math.log(p) + (d_ - r_) * math.log(1 - p)) if d_ else 0.0
        c = [[cost_of(r[m], totals[m], p) for m in months] for p in (p0, p1)]
        cost, back = [c[0][0], c[1][0] + up], []
        for t in range(1, n):
            back.append((0 if cost[0] <= cost[1] else 1, 1 if cost[1] <= cost[0] + up else 0))
            cost = [min(cost) + c[0][t], min(cost[1], cost[0] + up) + c[1][t]]
        state = [0 if cost[0] <= cost[1] else 1]
        for b in reversed(back):
            state.append(b[state[-1]])
        state.reverse()
        t = 0
        while t < n:
            if state[t]:
                u = t
                while u + 1 < n and state[u + 1]:
                    u += 1
                weight = sum(c[0][x] - c[1][x] for x in range(t, u + 1))
                if weight > 0:
                    out.append((term, t, u, weight))
                t = u + 1
            else:
                t += 1
    return sorted(out, key=lambda b: (-b[3], b[0]))


def month_range(first: str, last: str) -> list[str]:
    out, y, m = [], int(first[:4]), int(first[5:7])
    while f"{y:04d}-{m:02d}" <= last[:7]:
        out.append(f"{y:04d}-{m:02d}")
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out
