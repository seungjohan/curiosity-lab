---
stage: research
category: system
tag: system
concepts: [bridging-structural-holes, needle-in-haystack-retrieval, multi-signal-fusion]
about: Deep dive into GraphRAG (graph + LLM retrieval) — its architecture and variants — and how the same machinery powers both a smarter version of this vault and the ideation "The Connection".
type: deep-dive
---

> [!IMPORTANT] Key Takeaway
> **Why this matters:** Plain vector search finds notes *similar* to a query. GraphRAG finds how my notes *connect*, and can answer whole-corpus questions ("what themes recur across all my ideas?") that similarity search structurally cannot. That's the difference between a search box and a thinking partner.
> **How to use it:** Two payoffs — (1) a concrete architecture for making this vault *propose* connections, and (2) a real technical backbone for [[../../ideation/The Connection|The Connection]], which is the same graph math applied to people.
> **Informs:** [[connecting_the_dot|Connecting the Dots]] (the theory), [[../../ideation/The Connection|The Connection]] (the product).

# GraphRAG & the Connection Engine

The parent page [[connecting_the_dot|Connecting the Dots]] ends on one lever: *embeddings and graphs are complementary; fuse them.* **GraphRAG is that fusion, built and benchmarked.** This page goes deep on it, then applies it twice — to the vault, and to the idea [[../../ideation/The Connection|The Connection]].

## Why plain RAG isn't enough

Standard Retrieval-Augmented Generation embeds every chunk as a vector and, at query time, returns the chunks nearest the question. It's a **similarity** engine. It has two blind spots that matter for a connection-seeking vault:

1. **No structure.** It can find a note *like* your query, but not the *path* between two notes, and not multi-hop reasoning ("A relates to B, which relates to C").
2. **No global view.** Ask "what are the recurring themes across everything I've written?" and similarity search fails — there's no single chunk that answers a question about the *whole corpus*.

On enterprise benchmarks the gap is large: Microsoft reports **~86% accuracy for GraphRAG vs ~32% for baseline RAG** on global sensemaking questions. The value scales with *query complexity* — for a simple lookup, plain RAG is fine and GraphRAG is wasted compute.

## Microsoft GraphRAG — the architecture

The reference design ([*From Local to Global*, 2024](https://arxiv.org/pdf/2404.16130)) has four moves:

1. **Extract a graph with an LLM.** Read the corpus, pull out **entities** (nodes) and **relationships** (edges) into a knowledge graph — instead of leaving everything as flat text chunks.
2. **Detect communities (Leiden), hierarchically.** Partition the graph into clusters of densely-related nodes, then recurse: sub-communities inside communities, down to leaves. Leiden adds a refinement pass guaranteeing each community is internally well-connected (no stragglers). This is [community detection](https://en.wikipedia.org/wiki/Community_structure) doing automatically what my concept atoms do by hand.
3. **Summarize each community at index time.** Every cluster gets an LLM-written summary, bottom-up. These summaries *are* the "themes" of the corpus — pre-computed, so they cost nothing at query time.
4. **Query in two modes:**
   - **Local search** — start from specific entities as entry points, walk their neighborhood. Good for "tell me about X." (This is [[../../concepts/needle-in-haystack-retrieval|needle-in-haystack retrieval]].)
   - **Global search** — answer from the community summaries, map-reduce style across the hierarchy. Good for "what are the big themes?" (This is the part plain RAG can't do.)

**The insight:** structure the information into a hierarchy *before* any query arrives, so the expensive sensemaking is already done.

## The variant landscape (2024–2025)

No single architecture wins everywhere — pick by query distribution and budget:

| System | Core trick | Best at | Cost |
| :--- | :--- | :--- | :--- |
| **Microsoft GraphRAG** | Leiden communities + hierarchical summaries + local/global | Global "what are the themes" sensemaking | Heavy indexing (many LLM calls) |
| **LightRAG** | Dual-level retrieval (low-level entities + high-level concepts) fused with vectors | Balanced coverage + speed; incremental updates | ~30% lower latency |
| **HippoRAG** | Personalized PageRank over an LLM-extracted triple graph, seeded from the query | Cheap **multi-hop** reasoning | 10–30× cheaper multi-hop |
| **PathRAG / OG-RAG** | Retrieve *paths* / ontology-grounded subgraphs | Explainable chains of reasoning | Varies |

Note the direction of travel: everyone is fusing the **graph half** (relations, multi-hop, global view) with the **vector half** (semantic recall). Exactly the [[../../concepts/multi-signal-fusion|multi-signal-fusion]] the vault needs.

## Application A — GraphRAG *over this vault*

My vault is already a hand-built version of the GraphRAG index:

| GraphRAG piece | My vault's hand-built equivalent |
| :--- | :--- |
| LLM entity/relationship extraction | Wikilinks + `concepts:` frontmatter (I extract by hand) |
| Leiden communities | My category folders + concept clusters |
| Community summaries | My MOC hubs + concept-node descriptions |
| Local search | Backlinks / Smart Connections "similar notes" |
| **Global search** | **— missing —** |

The gap is **global search**: nothing in the vault answers "what themes recur across all my ideas?" or "which of my research threads are converging?" That's the highest-value thing GraphRAG would add. Practical path, cheapest first:
1. **Structural-hole finder** (from [[connecting_the_dot|Connecting the Dots]]) — read the Smart Connections vectors, flag high-cosine / no-shared-concept / cross-category pairs as candidate links. Local, no LLM cost. *Start here.*
2. **Community detection** via the [Graph Analysis plugin](https://github.com/SkepticMystic/graph-analysis) — see my real clusters and their boundaries, no code.
3. **Global questions** — periodically run an LLM (me) map-reduce over concept nodes + MOCs to write a "state of the vault: converging themes" note. A poor-man's GraphRAG global search, and it feeds the Reflect stage of the loop.

I do **not** need to stand up Microsoft GraphRAG's full pipeline at this scale — the value is in borrowing its *moves*, not its infrastructure.

## Application B — GraphRAG *is* the backbone for [[../../ideation/The Connection|The Connection]]

[[../../ideation/The Connection|The Connection]] wants to predict **1:N team synergy** from personality + social data. Its roadmap currently points only at Stanford CS224W in the abstract. GraphRAG's machinery gives it a concrete spine — because *a team is a graph of people*, and everything above transfers:

- **The graph:** people = nodes; shared traits, interactions, social ties = edges. (The Connection already plans to fuse survey + social data — that's edge construction.)
- **Community detection (Leiden):** finds natural sub-teams and cliques — who actually clusters together.
- **Betweenness / brokerage (Burt):** identifies the **connectors** who bridge sub-groups — the highest-leverage people for synergy, and the ones a naive 1:1 matcher misses entirely. This is [[../../concepts/bridging-structural-holes|bridging-structural-holes]] applied to humans — which is literally the domain Burt's theory came from.
- **Personalized PageRank (HippoRAG's trick):** "given this person as a seed, who complements them across the network?" — a ready-made synergy-propagation algorithm.
- **Link prediction:** "which two people, not yet paired, would work well together given the rest of the team graph?" — the product's core prediction, as a named, benchmarked task.

So the same page-linking research that improves the vault *is* the technical foundation for The Connection. The vault connects notes; The Connection connects people; the math is one math. That collision is the concept atom [[../../concepts/bridging-structural-holes|bridging-structural-holes]] doing its job.

## References
- Microsoft Research — [From Local to Global: A Graph RAG Approach to Query-Focused Summarization (2024)](https://arxiv.org/pdf/2404.16130)
- [GraphRAG community detection (docs)](https://www.mintlify.com/microsoft/graphrag/concepts/community-detection)
- [GraphRAG vs HippoRAG vs PathRAG vs OG-RAG — architecture comparison](https://medium.com/graph-praxis/graphrag-vs-hipporag-vs-pathrag-vs-og-rag-choosing-the-right-architecture-for-your-knowledge-graph-a4745e8b125f)
- [GraphRAG guide (Meilisearch, 2025)](https://www.meilisearch.com/blog/graph-rag)
- [RAG vs GraphRAG: a systematic evaluation (2025)](https://arxiv.org/html/2502.11371v2)
- Vault raw note: `raw/obsidian/software development/ai/RAG (Retrieval-Augmented Generation).md`

## 🔗 Connections

### ⬆ Pipeline
- Back ← [[connecting_the_dot|Connecting the Dots]] — the theory this engine implements
- Feeds → [[../../ideation/The Connection|The Connection]] — supplies its technical roadmap (community detection, PageRank, link prediction)
- Related → [[../../index|Master Index]]

<!-- AUTO-CONCEPTS:START -->
### 🔀 Concepts (auto-generated — do not edit)
- **bridging-structural-holes** → [[../../ideation/The Connection]] (system), [[connecting_the_dot]] (system)
- **needle-in-haystack-retrieval** → [[../../ideation/Advance Planner]] (system), [[../../ideation/Triathlon Photo Finder]] (system), [[../../ideation/Unified-Media-Insight-Capture-Tool]] (product)
- **multi-signal-fusion** → [[../../ideation/Advance Planner]] (system), [[../../ideation/Been There]] (system), [[../../ideation/Chronicle - Personal Topic Timeline]] (product), [[../../ideation/Company Fit Finder - Where to Work]] (system), [[../../ideation/Taste Detector]] (system), [[../../ideation/The Connection]] (system), [[../../ideation/Triathlon Photo Finder]] (system), [[../../ideation/Wine Value Advisor]] (system), [[../../projects/Michelin Filter]] (system), [[../../projects/prd/Chronicle_prd]] (product), [[../cooking/selected-restaurants]] (cooking), [[connecting_the_dot]] (system)
<!-- AUTO-CONCEPTS:END -->
