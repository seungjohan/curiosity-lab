#!/usr/bin/env python3
"""
graph_analysis.py — classical graph theory over the vault's link graph.

Where propose_connections.py is the NEURAL half (embeddings argue for links you
never made), this is the SYMBOLIC half: exact, cheap O(V+E) algorithms over the
links that already EXIST. It answers structural questions no embedding can:

    - Is my knowledge actually one connected body, or islands? .... components
    - Which notes are orphans, reachable from nothing? ............ isolated
    - How are two ideas related, in the fewest hops? ............. BFS path
    - Which notes hold the graph together? ..................... degree hubs

THE GRAPH
    nodes = every managed note (wiki/**.md, minus exclude_paths)
    edges = every [[wikilink]] and every relative [markdown](link.md) between
            two managed notes, treated as UNDIRECTED (navigability goes both
            ways in Obsidian's local graph).

THREE WAYS TO THE SAME ANSWER
    Connected components can be found by BFS, DFS, or a Disjoint Set Union
    (union-find). All three are O(V+E) and MUST agree — `--verify` runs all
    three and asserts they return the identical partition. They are kept as
    separate, readable implementations precisely so this file doubles as a
    reference for the three algorithms, not just a report generator.

Usage:
    python scripts/graph_analysis.py                       # full report (DSU)
    python scripts/graph_analysis.py --method bfs          # components via BFS
    python scripts/graph_analysis.py --method dfs          # components via DFS
    python scripts/graph_analysis.py --verify              # all three must agree
    python scripts/graph_analysis.py --path "Wine Value Advisor" "The Connection"
    python scripts/graph_analysis.py --hubs 15             # top notes by degree

Stdlib only. Config + note enumeration come from wiki_lib / linking.config.json.
See wiki/research/system/graph-theory-foundations.md for the theory.
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from wiki_lib import load_config  # noqa: E402

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
MDLINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+\.md)(?:#[^)]*)?\)")


# --------------------------------------------------------------------------
# graph construction
# --------------------------------------------------------------------------

def build_graph(cfg) -> tuple[list[Path], dict[Path, set[Path]]]:
    """Return (nodes, adjacency). Adjacency is undirected: an edge appears in
    both endpoints' sets. Only edges between two managed notes are kept."""
    notes = cfg.notes()
    node_set = set(notes)

    # Resolver keys: a target string -> a note Path.
    by_relpath: dict[str, Path] = {}          # "research/system/foo" -> Path
    by_stem: dict[str, list[Path]] = {}       # "foo" -> [Path, ...]
    for p in notes:
        by_relpath[cfg.relpath(p).removesuffix(".md")] = p
        by_stem.setdefault(p.stem, []).append(p)

    def resolve(target: str, src: Path) -> Path | None:
        t = target.split("|", 1)[0].split("#", 1)[0].strip()
        # Inside a markdown table a raw `|` would end the cell, so the alias
        # separator is written `\|`. Splitting on `|` leaves that backslash behind.
        t = t.rstrip("\\").strip()
        if not t:
            return None
        if "/" in t:
            # relative to the source note's directory, then to the wiki root,
            # then to the vault root (the repo, where .obsidian lives)
            for base in (src.parent, cfg.wiki, cfg.wiki.parent):
                cand = (base / t).resolve()
                cand = cand if cand.suffix == ".md" else cand.with_suffix(".md")
                if cand in node_set:
                    return cand
            # last resort: match on wiki-relative path string
            key = t.removesuffix(".md").lstrip("./")
            return by_relpath.get(key)
        # bare name, Obsidian-style — written with or without the .md suffix
        hits = by_stem.get(t) or by_stem.get(t.removesuffix(".md"))
        if not hits:
            return None
        if len(hits) > 1:
            # Four notes are named vocabulary.md. Obsidian breaks the tie by
            # preferring the one in the linking note's own folder; match that.
            same_folder = [h for h in hits if h.parent == src.parent]
            if same_folder:
                return same_folder[0]
        return hits[0]

    adj: dict[Path, set[Path]] = {p: set() for p in notes}
    for p in notes:
        text = p.read_text(encoding="utf-8")
        targets = WIKILINK_RE.findall(text) + MDLINK_RE.findall(text)
        for tgt in targets:
            dst = resolve(tgt, p)
            if dst is not None and dst != p:
                adj[p].add(dst)
                adj[dst].add(p)           # undirected
    return notes, adj


# --------------------------------------------------------------------------
# connected components — three independent implementations
# --------------------------------------------------------------------------

def components_bfs(nodes, adj) -> list[list[Path]]:
    visited: set[Path] = set()
    out: list[list[Path]] = []
    for start in nodes:
        if start in visited:
            continue
        comp, q = [], deque([start])
        visited.add(start)
        while q:
            v = q.popleft()
            comp.append(v)
            for w in adj[v]:
                if w not in visited:
                    visited.add(w)
                    q.append(w)
        out.append(comp)
    return out


def components_dfs(nodes, adj) -> list[list[Path]]:
    visited: set[Path] = set()
    out: list[list[Path]] = []
    for start in nodes:
        if start in visited:
            continue
        comp, stack = [], [start]           # iterative DFS — no recursion limit
        visited.add(start)
        while stack:
            v = stack.pop()
            comp.append(v)
            for w in adj[v]:
                if w not in visited:
                    visited.add(w)
                    stack.append(w)
        out.append(comp)
    return out


def components_dsu(nodes, adj) -> list[list[Path]]:
    parent = {p: p for p in nodes}
    rank = {p: 0 for p in nodes}

    def find(x):                            # path compression
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    def union(a, b):                        # union by rank
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        if rank[ra] < rank[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        if rank[ra] == rank[rb]:
            rank[ra] += 1

    for v in nodes:
        for w in adj[v]:
            union(v, w)

    groups: dict[Path, list[Path]] = {}
    for p in nodes:
        groups.setdefault(find(p), []).append(p)
    return list(groups.values())


METHODS = {"bfs": components_bfs, "dfs": components_dfs, "dsu": components_dsu}


def normalize(comps) -> set[frozenset]:
    return {frozenset(c) for c in comps}


# --------------------------------------------------------------------------
# BFS shortest path — "how are these two notes related, minimally?"
# --------------------------------------------------------------------------

def shortest_path(adj, src: Path, dst: Path) -> list[Path] | None:
    if src == dst:
        return [src]
    prev: dict[Path, Path] = {src: src}
    q = deque([src])
    while q:
        v = q.popleft()
        for w in adj[v]:
            if w not in prev:
                prev[w] = v
                if w == dst:
                    path = [w]
                    while path[-1] != src:
                        path.append(prev[path[-1]])
                    return list(reversed(path))
                q.append(w)
    return None


# --------------------------------------------------------------------------
# reporting
# --------------------------------------------------------------------------

def name(cfg, p: Path) -> str:
    return cfg.relpath(p) or p.name


def find_note(cfg, nodes, query: str) -> Path | None:
    q = query.removesuffix(".md")
    for p in nodes:
        if p.stem == q or cfg.relpath(p).removesuffix(".md") == q:
            return p
    matches = [p for p in nodes if q.lower() in p.stem.lower()]
    return matches[0] if len(matches) == 1 else (matches[0] if matches else None)


def report(cfg, nodes, adj, method: str) -> None:
    edges = sum(len(v) for v in adj.values()) // 2
    comps = sorted(METHODS[method](nodes, adj), key=len, reverse=True)
    isolated = [p for p in nodes if not adj[p]]

    print(f"Vault link graph — {len(nodes)} notes (V), {edges} links (E)")
    print(f"Method: {method.upper()}  ·  O(V+E)\n")

    print(f"Connected components: {len(comps)}")
    giant = comps[0] if comps else []
    if giant:
        pct = 100 * len(giant) / len(nodes)
        print(f"  • Giant component: {len(giant)} notes ({pct:.0f}% of the vault)")
    for c in comps[1:]:
        if len(c) > 1:
            print(f"  • Island ({len(c)}): " + ", ".join(name(cfg, p) for p in c))

    print(f"\nIsolated notes (degree 0 — linked from nothing, linking nothing): "
          f"{len(isolated)}")
    for p in sorted(isolated, key=lambda x: name(cfg, x)):
        print(f"  ! {name(cfg, p)}")

    deg = sorted(nodes, key=lambda p: len(adj[p]), reverse=True)[:10]
    print("\nTop hubs (degree — the notes holding the graph together):")
    for p in deg:
        print(f"  {len(adj[p]):>3}  {name(cfg, p)}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--method", choices=list(METHODS), default="dsu",
                    help="component algorithm to use (default: dsu)")
    ap.add_argument("--verify", action="store_true",
                    help="run BFS, DFS and DSU; assert all three agree")
    ap.add_argument("--path", nargs=2, metavar=("FROM", "TO"),
                    help="print the shortest link-path between two notes (BFS)")
    ap.add_argument("--hubs", type=int, metavar="N",
                    help="print the top-N notes by degree, then exit")
    args = ap.parse_args()

    cfg = load_config()
    nodes, adj = build_graph(cfg)

    if args.verify:
        results = {m: normalize(fn(nodes, adj)) for m, fn in METHODS.items()}
        ok = results["bfs"] == results["dfs"] == results["dsu"]
        n = len(results["dsu"])
        print(f"BFS / DFS / DSU agree: {ok}  ({n} components each)")
        return 0 if ok else 1

    if args.hubs:
        for p in sorted(nodes, key=lambda x: len(adj[x]), reverse=True)[:args.hubs]:
            print(f"  {len(adj[p]):>3}  {name(cfg, p)}")
        return 0

    if args.path:
        src, dst = (find_note(cfg, nodes, q) for q in args.path)
        if not src or not dst:
            print("error: could not resolve one of the notes", file=sys.stderr)
            return 1
        path = shortest_path(adj, src, dst)
        if path is None:
            print(f"No link-path between {name(cfg, src)} and {name(cfg, dst)} "
                  "— they are in different components.")
            return 0
        print(f"Shortest path ({len(path) - 1} hops):")
        print("  " + "\n  → ".join(name(cfg, p) for p in path))
        return 0

    report(cfg, nodes, adj, args.method)
    return 0


if __name__ == "__main__":
    sys.exit(main())
