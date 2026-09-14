---
stage: research
category: system
tag: system
concepts: [bridging-structural-holes, multi-signal-fusion]
about: The classical O(V+E) graph algorithms (BFS, DFS, DSU) applied to the vault's own link graph — what each answers, why all three agree — and how symbolic graph theory combines with the LLM/embedding layer (neuro-symbolic).
type: deep-dive
---

> [!IMPORTANT] Key Takeaway
> **Why this matters:** [[graphrag-connection-engine|GraphRAG]] and community detection are the *fancy* end. But the vault is literally a graph (notes = vertices, links = edges), and the **foundational** traversals — BFS, DFS, DSU — already answer the questions that matter most day one: *is my knowledge connected, or islands? which notes are orphans? how are two ideas related, minimally?*
> **How to use it:** These run today on my real vault via `scripts/graph_analysis.py`. First run already found 10 orphan notes and proved the concept axis collapsed my graph's diameter to ~1 hop.
> **Informs:** [[connecting_the_dot|Connecting the Dots]] (the parent), [[graphrag-connection-engine|GraphRAG & the Connection Engine]] (the neural half this pairs with).

# Graph Theory Foundations

[[connecting_the_dot|Connecting the Dots]] named the *methods*; [[graphrag-connection-engine|GraphRAG]] covered the LLM-heavy end. This page goes the other direction — **down to the fundamentals** — because the cheapest, most immediately useful analysis needs no embeddings and no LLM at all. It's classical graph theory, and it runs in linear time on the graph I already have.

## The vault *is* a graph

- **Vertices (V):** every managed note (`wiki/**.md`).
- **Edges (E):** every `[[wikilink]]` and relative `[markdown](link.md)` between two notes, treated as **undirected** (Obsidian navigation goes both ways).

Once you see it that way, a pile of textbook algorithms becomes a pile of answers about *your own thinking*.

## The core job: connected components

> **Question:** Is my knowledge one connected body, or a set of disconnected islands? And which notes are floating free, reachable from nothing?

A **connected component** is a maximal set of notes all reachable from each other. One giant component = a well-woven vault. Many small components = fragmented islands. Degree-0 notes = orphans you'll never stumble back into.

There are **three** classic ways to find components, and the beautiful part is they're **interchangeable** — each visits every vertex and edge exactly once, so each is **O(V + E)**, and all three return the *identical* partition. `graph_analysis.py --verify` runs all three and asserts they agree.

### DFS — Depth-First Search
Go as deep as possible, then backtrack. A `visited` array + a stack (or recursion). For each unvisited vertex, launch a traversal; everything it reaches is one component; each fresh launch is a new component.

```
visited = set()
for v in vertices:
    if v not in visited:
        stack = [v]                      # one component starts here
        while stack:
            u = stack.pop()              # LIFO → depth-first
            for w in neighbors[u]:
                if w not in visited:
                    visited.add(w); stack.append(w)
```

### BFS — Breadth-First Search
Same skeleton, but a **queue** instead of a stack, so it explores in rings outward from the start. Identical for *counting* components — but BFS earns its keep on a different job (shortest paths, below), because it reaches every node by the **fewest hops**.

```
q = deque([v]); visited.add(v)           # LIFO→FIFO is the only change
while q:
    u = q.popleft()                      # FIFO → breadth-first
    for w in neighbors[u]:
        if w not in visited:
            visited.add(w); q.append(w)
```

### DSU — Disjoint Set Union (Union-Find)
Don't traverse at all — **merge**. Every node starts as its own set; walk the edges and `union` the two endpoints of each; at the end, nodes sharing a root are one component. With **path compression** + **union by rank** it's effectively O(V + E·α), α ≈ constant.

```
find(x):  follow parent pointers to the root, re-point along the way  (compression)
union(a,b): attach the shorter tree under the taller               (by rank)
for (u,v) in edges: union(u,v)
components = group nodes by find(node)
```

**When to reach for which:**

| | Best when | Killer feature |
| :--- | :--- | :--- |
| **DFS** | You also want cycles / topological structure | Natural recursion; path/backtrack info |
| **BFS** | You want **shortest** paths / fewest hops | Layer-by-layer distance |
| **DSU** | Edges **arrive over time**; "are these two connected *yet*?" | Near-O(1) incremental merge + query, no re-traversal |

For the vault, DSU is the natural fit: I add links incrementally, and "did that new link just merge two islands?" is a one-call question.

## What it found on *my* vault (first run)

```
Vault link graph — 119 notes (V), 433 links (E)
BFS / DFS / DSU agree: True  (11 components each)

Connected components: 11
  • Giant component: 109 notes (92% of the vault)
Isolated notes (degree 0): 10
  ! research/cooking/baking/{baguette, focaccia, levain}.md
  ! research/cooking/{bouillabaisse, coq-au-vin, paella, soupe-a-loignon}.md
  ! research/{inspiration, music/vocabulary, travel/vocabulary}.md
```

Two real, actionable findings on day one, from zero AI:
1. **92% of the vault is one connected body** — the linking discipline is working.
2. **10 orphan notes** — my French/baking recipe pages and two vocab lists are floating free: nothing links to them, they link to nothing. They're invisible to the loop. *Fix:* link each recipe to `selected-restaurants` or a technique note. (This is a concrete [[../../maintenance|maintenance]] task the graph handed me.)

## BFS's other job: "how are these two ideas related?"

> **Question:** Given two notes, what's the *shortest chain of links* between them?

That's **BFS from A until it reaches B** — the reconstructed path is the minimal explanation of how two ideas connect. Running it revealed something I didn't expect:

```
selected-restaurants (cooking)  →  Company Fit Finder (career)      1 hop
music-social-media   (music)    →  Wine Value Advisor (idea)        1 hop
```

**One hop, across domains that share no topic.** Why? Because the horizontal concept axis put a direct edge between them — they instance the same atom (`multi-signal-fusion`, `high-signal-filter`). **The concept system has collapsed the graph's diameter**: cooking and career are *adjacent* because they share a mechanism. That's [[../../concepts/bridging-structural-holes|bridging-structural-holes]] made literal — and now measurable as graph distance, not just asserted.

## LLM × graph theory — the neuro-symbolic pairing

The deepest point. There are two utterly different ways to reason over a knowledge graph, and the frontier is **combining** them — exactly [[../../concepts/multi-signal-fusion|multi-signal-fusion]] at the architecture level:

| | **Symbolic** (this page) | **Neural / LLM** ([[graphrag-connection-engine|GraphRAG]] page) |
| :--- | :--- | :--- |
| Works on | The explicit link structure | The meaning of the text |
| Strength | Exact, cheap, explainable, O(V+E) | Understands, infers, summarizes |
| Blind spot | Can't read meaning — a missing link is invisible to it | Can't do exact structure — no guaranteed shortest path, hallucinates edges |
| In this vault | `graph_analysis.py` (BFS/DFS/DSU) | `propose_connections.py` (embedding surprise) + me |

Neither alone is enough, and the leading systems fuse them precisely along these seams:

- **GraphRAG / HippoRAG:** the **LLM builds** the graph (extracts entities + relations from text — the neural step), then **classical algorithms traverse** it — Leiden community detection, and **Personalized PageRank** (HippoRAG), which is just a weighted random walk, a graph algorithm. LLM for meaning, graph theory for structure.
- **This vault, already:** `propose_connections.py` uses embeddings to *find* candidate edges (neural); `graph_analysis.py` uses BFS/DFS/DSU to *analyze the structure* those edges form (symbolic). The **structural-hole finder** is the fusion — an unlinked pair is a candidate only if it's semantically close (neural) **and** far apart in the link graph (symbolic: many hops, or different components). Neither signal alone is right; the product is the idea.

The pattern generalizes: **use the LLM to turn fuzzy text into graph structure, then use classical O(V+E) graph theory to reason over that structure exactly and cheaply.** The LLM is the eyes; graph theory is the skeleton.

## The next rung: loops → graphs → agents

Step back and this page is really one *level* of a ladder — the levels of how you tell a computer what to do, each one subsuming the last:

| Rung | You specify… | The tool | In this vault |
| :--- | :--- | :--- | :--- |
| **Sequence** | steps, in order | a script | the one-off scrapers in `scripts/` |
| **Loop** | iterate a pile | `for` / `while` | `build_connections.py` walking every note |
| **Graph** | relationships, then traverse | BFS/DFS/DSU, PageRank | `graph_analysis.py` (this page) |
| **Agent** | a *goal* + tools; it finds the path | an LLM that reasons | `propose_connections.py` + me |

The **loop → graph** jump was: stop processing a pile, model the relationships (this whole page). The **graph → agent** jump is the next development, and it's a genuine change in kind:

- **Graph engineering** — edges are *pre-declared*, the algorithm is *fixed* (BFS is always BFS), the answer is *exact and verifiable*. Its ceiling: it can only traverse edges I already wired.
- **Agent engineering** — I hand an LLM a **goal + tools + context**, and it decides where to go — and, crucially, it can **invent edges that were never in the graph.** Traversal becomes dynamic and goal-directed; *reasoning* replaces a fixed algorithm.

That last part is the point of everything else in this cluster. `graph_analysis.py` can only report links I made. But an agent *reading* the notes can **propose an edge no graph contained** — a shared mechanism ([[connecting_the_dot|Kind 1]]) or a shared hidden variable ([[two-kinds-of-connection|Kind 2]], Nike·Nintendo). The [[../../concepts/bridging-structural-holes|structural hole]] the graph is blind to, the agent can see and *draw*.

But — the load-bearing caveat — **agent engineering doesn't replace graph engineering; it stands on it.** An agent with no graph underneath hallucinates edges, confidently wrong. The graph is the terrain that keeps the agent honest: it reasons *over* verifiable structure instead of *inventing* it from nothing. That's the [[../../concepts/multi-signal-fusion|neuro-symbolic]] pairing again, read as a ladder — the agent is the navigator, the graph is the ground it walks on. Each rung needs the one below.

So the whole arc of this vault, in one line: **loops** processed my notes → **graphs** modelled how they connect → an **agent** proposes the connections I never made. The engineering wasn't replaced at each step; it was *layered*.

## The tool
`scripts/graph_analysis.py` — stdlib, config-driven via `wiki_lib`, keeps BFS/DFS/DSU as three separate readable implementations so it doubles as a reference.

```
python scripts/graph_analysis.py                 # full report (components, orphans, hubs)
python scripts/graph_analysis.py --verify        # prove BFS = DFS = DSU
python scripts/graph_analysis.py --path A B       # shortest link-chain between two notes
python scripts/graph_analysis.py --hubs 15        # notes holding the graph together
```

## References
- 🎥 [Graph Engineering explained in 8min..](https://www.youtube.com/watch?v=mBePcvqLX88) — Caleb Writes Code (YouTube, English). A fast practical tour of graph engineering — the applied, systems-facing companion to the textbook algorithms on this page.
- BFS / DFS / DSU, connected components in O(V+E) — standard (CLRS, *Introduction to Algorithms*, ch. 21–22).
- DSU with path compression + union by rank → near-constant amortized (inverse Ackermann α).
- Personalized PageRank as graph-native retrieval — see HippoRAG in [[graphrag-connection-engine|GraphRAG & the Connection Engine]].

## 🔗 Connections

### ⬆ Pipeline
- Back ← [[connecting_the_dot|Connecting the Dots]] — the parent; this is its "from the ground up" computation layer
- Pairs with → [[graphrag-connection-engine|GraphRAG & the Connection Engine]] — the neural half of the neuro-symbolic pairing
- Feeds → [[../../maintenance|Maintenance]] — the orphan list is a concrete backlog
- Feeds → [[../../ideation/The Connection|The Connection]] — team-synergy graphs use these exact primitives (components, shortest path, PageRank)
- Hub → [[../../index|Master Index]]

<!-- AUTO-CONCEPTS:START -->
### 🔀 Concepts (auto-generated — do not edit)
- **bridging-structural-holes** → [[../../ideation/The Connection]] (system), [[../../projects/prd/Constellate_prd]] (product), [[AI-Industry-Map-2026]] (system), [[connecting_the_dot]] (system), [[graphrag-connection-engine]] (system), [[two-kinds-of-connection]] (system)
- **multi-signal-fusion** → [[../../ideation/Advance Planner]] (system), [[../../ideation/Been There]] (system), [[../../ideation/Chronicle - Personal Topic Timeline]] (product), [[../../ideation/Company Fit Finder - Where to Work]] (system), [[../../ideation/Taste Detector]] (system), [[../../ideation/The Connection]] (system), [[../../ideation/Triathlon Photo Finder]] (system), [[../../ideation/Wine Value Advisor]] (system), [[../../projects/Michelin Filter]] (system), [[../../projects/Trip Guide - Shareable Restaurant Map]] (travel), [[../../projects/prd/Chronicle_prd]] (product), [[../cooking/selected-restaurants]] (cooking), [[connecting_the_dot]] (system), [[graphrag-connection-engine]] (system)
<!-- AUTO-CONCEPTS:END -->
