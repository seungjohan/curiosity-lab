---
stage: research
category: system
tag: system
concepts: [bridging-structural-holes, multi-signal-fusion]
about: A map of the algorithms that could power the connection engine — gathered while asking how to improve Constellate's resource-to-resource linking — sorted by which kind of connection each one can find.
type: deep-dive
status: open
---

> [!IMPORTANT] Key Takeaway
> **Why this matters:** The idea in [[two-kinds-of-connection|Two Kinds of Connection]] is not new territory. Kind 2 (the hidden shared variable) has a 30-year research field behind it, **literature-based discovery** (Swanson's ABC model), and a formal name, **bisociation**. Kind 1 has a direct ancestor too: **analogy mining** with purpose/mechanism vectors. Graph methods give cheap, explainable ways to run both.
> **How to use it:** Read it as a reading list sorted by question. Each section says what the method finds, how it maps onto my engine, and what to read next. "Open questions" at the bottom is where to pick up.
> **Informs:** The Constellate linking engine (`LINKING-ALGORITHM.md` in the Constellate repo), the [[graphrag-connection-engine|proposer]], and whether Algorithm C (the causal card) gets built.

# Linking Algorithms — a Survey for the Connection Engine

## How this started (2026-10-02 → 10-04)

A chain of questions while improving Constellate's **Related** panel, which today scores pairs of saved resources by keyword overlap (`src/lib/linking.ts`):

1. **Could [Laya](https://huggingface.co/convaiinnovations/laya) judge whether two resources are related, from the summaries and keywords Gemini writes?** → **No.**
   - Laya is a 400–800M-parameter *decision/classification* model (typed questions in, calibrated probabilities out), built for email triage and routing.
   - Judging *pairs* is the wrong cost shape. One new resource against ~1,000 saves is ~1,000 forward passes (my estimate: tens of seconds to a minute or more on a Mac CPU). The whole archive is ~500,000 pairs.
   - Embeddings cost one pass per resource; comparing them afterwards takes milliseconds.
2. **So, embeddings?** → **They're only half the answer.** Embeddings are *similarity*, and similarity is Kind 1 only. In my own words: *"Similarity is not surprise — ranking by similarity is a misfiling detector."* No similarity model, however good, will ever put Nike next to Nintendo.
3. **What about [Twitter's algorithm](https://github.com/twitter/the-algorithm)?** → **Borrow its shape, not its models.**
   - Its rankers learn from billions of engagements by millions of users, which a one-person archive will never have.
   - The pipeline shape transfers well: *several candidate sources → one ranker → filters for diversity → feedback.*
   - The feedback can be my own **Link / Not this** answers.
4. **What other algorithms exist, including from graph engineering?** → the rest of this note.

## Map: which method finds which kind

| Question | Kind | Methods |
| :--- | :--- | :--- |
| Same abstract shape? | 1 — analogy | Analogy mining (purpose/mechanism), Gentner's structure-mapping, embeddings of de-nouned abstractions |
| Wired to the same third thing? | 2 — hidden variable | Swanson's ABC / literature-based discovery, bisociation (bridging concepts), causal knowledge graphs, multi-hop random walks |
| Shares the *rare* things? | both (cheap) | Resource Allocation / Adamic-Adar link prediction |
| Is the link a surprise? | the ranking layer | Communities (Leiden), structural holes (Burt), serendipity = unexpectedness × relevance |
| Is the panel varied? | presentation | MMR |
| Which source to trust? | learning | Thompson sampling over Link / Not this |

---

## Kind 2 — the hidden shared variable

### Swanson's ABC model (literature-based discovery)
- **The idea:** if **A–B** appears in one body of literature and **B–C** in another, but A and C never appear together, then **A–C** is a candidate discovery. B is the hidden variable.
- **The proof it works:** Swanson (1986) found that fish oil could treat Raynaud's disease. No paper linked them, but Raynaud's ↔ *blood viscosity* and *blood viscosity* ↔ fish oil were both published. Later clinical trials confirmed it.
- **Mapping:** this is exactly my Nike → *free time* → Nintendo. The causal card (Algorithm C) is ABC with typed edges (consumes / depends on / produces / competes with / threatened by).
- **What the field adds that I don't have yet:**
  - **Open vs. closed discovery.** Open: start from A and ask what it might link to. Closed: given A and C, find the B that explains the link.
  - **Ranking the B's.** Raw ABC produces huge numbers of meaningless paths. The field ranks intermediate terms by rarity and by how strongly each edge is supported.
- **Read:** [Scientometric analysis of LBD, 1986–2020](https://arxiv.org/pdf/2006.08486) · [LBD overview (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4888806)

### Bisociation (Koestler → Berthold's BISON project)
- **The idea:** Koestler's word for creativity as the collision of two unrelated frames of thought. Berthold's EU project BISON turned it into algorithms for finding links that *cross domains* in information networks.
- **Mapping:** BISON separates **bridging concepts** (a shared node, my Kind 2) from **bridging by structural similarity** (my Kind 1). Their taxonomy is close to my two-kinds split, so it's worth reading to see where they took it.
- **Read:** [*Bisociative Knowledge Discovery* (Berthold, ed., Springer 2012, open access)](https://unglue.it/work/195108/)

### Causal knowledge graphs built by LLMs
- **The idea:** prompt an LLM for cause → effect pairs with a direction and a strength, then merge them into one graph. Recent work handles conflicts between sources and keeps the context each claim came from.
- **Mapping:** this is the build recipe for the causal card. It tells me how to prompt for the five fields and how to merge "free time" written five different ways into one node.
- **Read:** [Causal-aware LLMs](https://arxiv.org/pdf/2505.24710) · [WikiCausal — corpus & evaluation for causal KG construction (IBM)](https://research.ibm.com/publications/wikicausal-corpus-and-evaluation-framework-for-causal-knowledge-graph-construction)

---

## Kind 1 — analogy

### Analogy mining: purpose + mechanism (Hope, Chan, Kittur, Shahaf — KDD 2017)
- **The idea:** represent each product as two separate vectors, *what it is for* (purpose) and *how it works* (mechanism). Query "same purpose, different mechanism", or the reverse. In an ideation experiment, analogies found this way made people significantly more likely to come up with creative ideas.
- **Mapping:** my mechanism card already has the mechanism half (tension / move / abstraction). Adding a **purpose** field gives two search modes: *same goal, different route*, and *same route, different goal*.
- **Read:** [Accelerating Innovation Through Analogy Mining](https://arxiv.org/pdf/1706.05585)

---

## Graph engineering

Treat the archive as **one graph**:
- **Nodes:** resources, keywords, Obsidian notes, Notion pages, and later causal nodes (*time, attention, money, trust, energy, risk…*).
- **Edges:** a resource *has* a keyword, a note *cites* a resource, a resource *consumes* a causal node.

Everything below runs on that graph. This builds on [[graph-theory-foundations|Graph Theory Foundations]] (BFS/DFS/DSU), one rung up.

| Method | What it finds | Mapping | Cost |
| :--- | :--- | :--- | :--- |
| **Resource Allocation index** / **Adamic-Adar** | Two nodes that share neighbours, with *rare* neighbours counting more. In benchmarks, RA tends to beat Adamic-Adar. | The fix for "`ai` links everything". It's the IDF idea, expressed on a graph. | Tiny |
| **Personalised PageRank** / random walk with restart | Everything reachable from one start node, ranked by how easily a walk gets there | ABC on a graph. 2–3 hops = A→B→C, and the path is the explanation. | Small |
| **Leiden community detection** (the core of Microsoft GraphRAG) | Clusters of densely connected nodes, found automatically | "Different community" = surprise, for every resource, not only the ones I filed into a subject by hand | Moderate |
| **Burt's constraint**, betweenness | Nodes that bridge clusters which otherwise don't touch (structural holes) | Surfaces the *bridge* resources, the ones worth an "Inspiration" slot | Small |
| **SimClusters** (Twitter/X) | Overlapping communities as sparse, readable vectors | Later, if the archive grows to many thousands | Large |
| **GraphRAG / LightRAG** | LLM-extracted entity–relation graphs. LightRAG updates incrementally. | The Algorithm A/C cards could be the "relations" | API |

**Read:** [Survey of link prediction algorithms](https://arxiv.org/pdf/2306.12970) · [Predicting missing links via local information (Resource Allocation)](https://arxiv.org/pdf/0901.0553) · [Random walk with extended restart](https://arxiv.org/pdf/1710.06609) · [Microsoft GraphRAG overview](https://www.mintlify.com/microsoft/graphrag/concepts/overview) · [LightRAG](https://arxiv.org/html/2410.05779v3) · [NetworkX structural holes](https://networkx.org/documentation/networkx-2.4/reference/algorithms/generated/networkx.algorithms.structuralholes.effective_size.html) · [SimClusters (X help center)](https://help.x.com/en/resources/recommender-systems/communities-recommendations)

---

## Ranking what gets shown

- **Serendipity = unexpectedness × relevance.** The recommender-systems formalisation of my surprise score.
  - My current version is `surprise = rank(mechanism similarity) − rank(topic similarity)`.
  - The literature adds a **relevance** term, which says the link has to actually be *useful*, not just odd. Link / Not this can measure that.
  - [Serendipity in recommender systems — systematic review](https://jcst.ict.ac.cn/EN/10.1007/s11390-020-0135-9)
- **MMR** (maximal marginal relevance, Carbonell & Goldstein 1998). When choosing the next link to show, penalise links too similar to ones already shown. A general form of my `diversify()`. [Paper](https://people.eng.unimelb.edu.au/ammoffat/sigir98/abstracts/carbonell.html)
- **Thompson sampling.** Keep a Beta(successes, failures) count per candidate source and learn which sources earn a Link. That is enough at one-person scale; the [NeurIPS 2018 implicit-feedback bandit paper](https://papers.nips.cc/paper/2018/hash/d8c9d05ec6e86d5bbad7a2f88a1701d0-Abstract.html) is the heavyweight version.

---

## Putting it together — the Twitter shape at one-person scale

```
graph      resources · keywords · notes · Notion pages · causal nodes
   │
candidate sources
   ├─ Resource Allocation   (shared rare keys)           cheap, explainable
   ├─ personalised PageRank (2–3-hop paths = ABC)        finds Kind 2 through existing edges
   ├─ causal-node collision (same node, sign = type)     Kind 2, needs the causal card
   └─ mechanism similarity  (Algorithm A)                Kind 1, needs the mechanism card
   │
score      relevance × unexpectedness   (unexpected = different Leiden community)
   │
filter     MMR diversity · only show if "connects because …" can be finished
   │
learn      Link / Not this → Thompson sampling re-weights the sources
```

**Cheapest first step:** Resource Allocation + community detection. Pure code, no API, fast at ~1,000 resources. It fixes both standing debts in Constellate's engine: generic keys dominating, and the cross-subject boost depending on hand-filed subjects.

## Where this went (2026-10-05)

Development moved into the Constellate repo, branch `algorithm`, with Constellate's own archive
as the test bed. Its `LINKING-ALGORITHM.md` §8 holds the current state. In short:

- **The minus is the core of Kind 2.** Cards became signed arrows — what a thing *pushes* up or
  down, what it *needs* up or down — and a link whose signs multiply to minus is one quietly
  working against the other (Nintendo lowers outdoor activity, which Nike needs). In the
  archive: a home ab workout ⇄ running videos, home pizza ⇄ pizzerias.
- **Hidden variables must be quantities that rise and fall in daily life** (outdoor activity,
  time at home, sleep, prices). Abstract ones (trust, risk, skill) linked the unrelated.
- **"Which hidden variables to watch"** (the first open question above) is now partly answered
  by that rule; the list is still growing.
- **Then thinking flows (N303).** The example was one case, not the rule: every resource got a
  small signed graph — what moves it, what it moves, cause → effect steps up to three out, the
  entities it names — and two flows link where they reach the same variable. *How* they reach it
  is the kind: works against / feeds, rivals for a limited budget, pulls against, opposite stakes.
  Found in the archive with no shared words: China's AI catch-up → more export controls → works
  against a US export-lift story; a Spanish report on Ceuta → "more irregular migration" → a
  Korean report on Germany's far right. Shahaf storylines, Kleinberg bursts, label-propagation
  groups and bridges were built on top. Full measurements: Constellate `LINKING-ALGORITHM.md` §8.
- **Where GraphRAG and LLMs fit:** thinking flows *are* GraphRAG's extraction step. What it adds
  next — write what moves each resource (COMET-style), merge synonym variables (entity
  resolution), let a model check each "because" before it is shown, summarise each group (the
  Trend Read's input), and extract at capture (LightRAG's incremental update).
- **All six built (N307).** Writing the `up` side turned 108 influence meetings into thousands;
  merged names let flows meet on meaning; a model read 1,707 becauses and dropped 301, nearly all
  traced to a few weak labels ("tech hiring" on every career post), fixed at the source. 84 groups
  got summaries, whole-archive questions run map-reduce over them, and the app now writes a flow
  at capture. A Claude QA pass rechecks what Gemini wrote. One lesson worth keeping: **a verdict
  is only stable if the ranking is** (ties broken by name).
- **Named "the linking algorithm" and made portable (N308).** The skill is now
  [[../../../skills/linking-algorithm/SKILL|skills/linking-algorithm]], with the full algorithm and
  an adapting guide. Adapted twice by resource type: **Dendrite** (study notes: `causes` /
  `enables` / `competes_for` fields, leads ranked across subjects, never written) and **Dayweb**
  (private days and moments: no LLM; the owner's own topics and `←` `~` `≠` are the flows; time is
  the distance, so a link inside a week counts half; echo × tension signs propose new ones).

## Open questions — where to dig next

- [ ] **Which hidden variables?** The node vocabulary for the causal card: *time, attention, money, trust, physical presence, status, energy, risk*, and what else? LBD uses a domain ontology (UMLS in medicine). What's the ontology of *everyday life*?
- [ ] **How does LBD rank the B's?** Read the scientometric review for the ranking functions, before inventing my own.
- [ ] **BISON's bridging-graph definitions.** How close are they to Kind 1 / Kind 2? Steal the formal vocabulary.
- [ ] **Purpose field.** Add it to the mechanism card and test "same purpose, different mechanism" on my own notes.
- [ ] **Measure before trusting.** On my archive, how many pairs does Resource Allocation surface that keyword overlap missed, and are they any good?
- [ ] **Evaluation.** What is "a good link" for me, measurably? Link-rate on the panel? Links that later turn into an idea?

## 🔗 Connections

### ⬆ Pipeline
- Back ← [[two-kinds-of-connection|Two Kinds of Connection]] — the split this survey sorts every method by; its open question ("which hidden variables to watch") is this note's first open question
- Back ← [[connecting_the_dot|Connecting the Dots — The Field]] — the named theories (Gentner, Burt, TRIZ); this note adds the computational methods
- Builds on ← [[graph-theory-foundations|Graph Theory Foundations]] — BFS/DFS/DSU is the rung below link prediction and random walks
- Feeds → [[graphrag-connection-engine|GraphRAG & the Connection Engine]] — candidate upgrades for the proposer
- Feeds → [[../../projects/prd/Constellate_prd|Constellate PRD]] — the app whose Related panel started this
- Hub → [[../../index|Master Index]]

<!-- AUTO-CONCEPTS:START -->
### 🔀 Concepts (auto-generated — do not edit)
- **bridging-structural-holes** → [[../../ideation/Connecting the Dots]] (system), [[../../projects/prd/Constellate_prd]] (product), [[AI-Industry-Map-2026]] (system), [[connecting_the_dot]] (system), [[graph-theory-foundations]] (system), [[graphrag-connection-engine]] (system), [[two-kinds-of-connection]] (system)
- **multi-signal-fusion** → [[../../ideation/Advance Planner]] (system), [[../../ideation/Been There]] (system), [[../../ideation/Chronicle - Personal Topic Timeline]] (product), [[../../ideation/Company Fit Finder - Where to Work]] (system), [[../../ideation/Connecting the Dots]] (system), [[../../ideation/Taste Detector]] (system), [[../../ideation/Triathlon Photo Finder]] (system), [[../../ideation/Wine Value Advisor]] (system), [[../../projects/Michelin Filter]] (system), [[../../projects/Trip Guide - Shareable Restaurant Map]] (travel), [[../../projects/prd/Chronicle_prd]] (product), [[../cooking/selected-restaurants]] (cooking), [[connecting_the_dot]] (system), [[graph-theory-foundations]] (system), [[graphrag-connection-engine]] (system)
<!-- AUTO-CONCEPTS:END -->
