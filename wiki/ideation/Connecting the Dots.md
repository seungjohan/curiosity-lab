---
stage: ideation
category: system
concepts: [multi-signal-fusion, interpretation-over-artifact, ai-as-enabler-not-replacer, bridging-structural-holes]
lifecycle: researching
aliases: [The Connection]
---

> [!IMPORTANT] Key Takeaway
> **Why this matters:** One engine, two graphs. The linking algorithm surfaces non-obvious connections between *notes*; The Connection surfaces non-obvious synergy between *people*. Same math (bridging structural holes, community detection, link prediction), different nodes.
> **How to use it:** This is the project's main writing page. Write here first; the map below points to every rule, script, research note, and reference the project draws on.
> **Informs:** The vault's own [[../../LINKING.md|linking standard]], the Constellate **graph** project, and a future people-graph product.

# Connecting the Dots

Research from unrelated domains, colliding on a shared underlying pattern, is where new ideas come from (의외의 연결성). This project turns that from a personal knack into a system: first for my notes, then for people.

## 💭 Reflection: One Engine, Two Graphs

<!-- Your writing space. Raw, first-person thinking — start anywhere. -->

## 🧭 Project map

**Rules**
- [[../../LINKING.md|LINKING.md]]: the canonical two-axis standard (vertical pipeline + horizontal concept atoms)
- `linking.config.json`: the config every script reads

**Concept atoms** (the horizontal axis): [[../concepts/index|Concept index]]
- [[../concepts/bridging-structural-holes|bridging-structural-holes]]: the atom that ties the notes graph to the people graph

**Engine** (`scripts/`)
- `build_connections.py`: renders the auto-generated concept blocks
- `propose_connections.py`: proposes links I haven't made → [[../_proposals|Proposals]] · [[../_proposal-decisions|Decisions]]
- `graph_analysis.py`: BFS/DFS/DSU over the link graph (orphans, distances)
- `lint_wiki.py` + `wiki_lib.py`: structure checks and shared helpers
- `skills/linking-algorithm/`: the portable skill that installs all of the above into another project

**Research**
- [[../research/system/connecting_the_dot|Connecting the Dots — The Field]]: the named theories behind the instinct
- [[../research/system/graphrag-connection-engine|GraphRAG & the Connection Engine]]: how to make the vault *propose* connections
- [[../research/system/graph-theory-foundations|Graph Theory Foundations]]: the classical layer, runnable today
- [[../research/system/two-kinds-of-connection|Two Kinds of Connection]]: analogy vs. hidden shared variable — the open question

**Sibling ideas**
- [[Chronicle - Personal Topic Timeline]]: connecting the dots is its main value
- [[../projects/prd/Constellate_prd|Constellate PRD]]: the archive where this project's references live

## 🌌 Constellate: graph

References for this project are collected in Constellate's **graph** project.

**→ [Open Constellate](file:///Applications/Constellate.app)**, then choose **graph** under Projects. (Constellate has no deep links yet, so this opens the app, not the project directly.)

What's in it (snapshot 2026-09-26; Constellate is the source of truth):

*Vault files*
- [[../../LINKING.md|LINKING.md]]
- [[../research/system/connecting_the_dot|Connecting the Dots — The Field]]
- [[../research/system/graphrag-connection-engine|GraphRAG & the Connection Engine]]

*Media*
- [Stanford CS224W: Machine Learning with Graphs — Lecture 1.1, Why Graphs](https://www.youtube.com/watch?v=JAB_plj2rbA&list=PLoROMvodv4rPLKxIpqhjhPgdQy7imNkDn)
- [Why Agentic Systems Need Ontologies — Frank Coyle, UC Berkeley](https://www.youtube.com/watch?v=Sir59K8ZDPU)
- [How I use LLMs — Andrej Karpathy](https://www.youtube.com/watch?v=EWvNQjAaOHw)

## Applied to people

*Formerly the standalone idea **The Connection**.* A team-building and synergy analysis platform that uses personality traits (MBTI) and Machine Learning (Graphs) to predict and optimize group dynamics. Leveraging Graph ML to move from 1:1 matching to optimized 1:N team synergy is a unique wedge in HR Tech.

### Key Features
- **Synergy Analysis**: Not just 1:1 matching, but 1:N team synergy.
- **Data Sources**: Survey results combined with social activity (Instagram, etc.) for deeper analysis.
- **Simulation**: Indirect experience/simulation of team performance before committing.

### Technical Roadmap
- **Machine Learning with Graphs**: Reference [Stanford CS224W](https://web.stanford.edu/class/cs224w/).
- **Concrete backbone** → [[../research/system/graphrag-connection-engine|GraphRAG & the Connection Engine]]. A team is a graph of people, so the same machinery applies directly:
  - **Community detection (Leiden)** — find natural sub-teams / cliques.
  - **Betweenness & brokerage (Burt's structural holes)** — surface the *connectors* who bridge sub-groups; the highest-synergy people that a naive 1:1 matcher misses.
  - **Personalized PageRank (HippoRAG's trick)** — "seed on one person → who complements them across the network?"
  - **Link prediction (Adamic-Adar)** — "which two un-paired people would work well together given the rest of the graph?" = the core prediction, as a named, benchmarked task.
- **Validation**: Compare survey-based analysis with real-world outcomes.

### Challenges
- **Survey Professionalism**: Moving beyond simple, non-professional surveys for personality analysis.
- **Accuracy**: Quantifying "synergy" in a meaningful way.

## 🔗 Connections

### ⬆ Pipeline
- Back ← [[ideation]] — tracked on the active ideation board
- Grounded by → [[../research/system/connecting_the_dot|Connecting the Dots — The Field]] — the theory this project turns into a system
- Draws on → [[../research/system/graphrag-connection-engine|GraphRAG & the Connection Engine]] — the graph algorithms that give both graphs a real technical spine
- Draws on → [[../research/system/graph-theory-foundations|Graph Theory Foundations]] — the traversals `graph_analysis.py` already runs on the vault
- Challenged by → [[../research/system/two-kinds-of-connection|Two Kinds of Connection]] — the engine finds analogy; the connections I care most about are a different kind
- Builds → [[../../LINKING.md|LINKING standard]] — the notes-graph half, already live in this vault
- Hub → [[../index|Master Index]]

<!-- AUTO-CONCEPTS:START -->
### 🔀 Concepts (auto-generated — do not edit)
- **multi-signal-fusion** → [[Advance Planner]] (system), [[Atlas - One Map Over Every App]] (product), [[Been There]] (system), [[Chronicle - Personal Topic Timeline]] (product), [[Company Fit Finder - Where to Work]] (system), [[Meeting Line - Before, During, After]] (product), [[Taste Detector]] (system), [[Triathlon Photo Finder]] (system), [[Wine Value Advisor]] (system), [[../projects/Michelin Filter]] (system), [[../projects/Trip Guide - Shareable Restaurant Map]] (travel), [[../projects/prd/Chronicle_prd]] (product), [[../research/cooking/selected-restaurants]] (cooking), [[../research/system/connecting_the_dot]] (system), [[../research/system/graph-theory-foundations]] (system), [[../research/system/graphrag-connection-engine]] (system), [[../research/system/linking-algorithms-survey]] (system)
- **interpretation-over-artifact** → [[Chronicle - Personal Topic Timeline]] (product), [[Company Fit Finder - Where to Work]] (system), [[Finding What You Like - Rekindling Passion & Curiosity]] (system), [[Keep in Touch - Relationship Chronicle]] (system), [[Meeting Line - Before, During, After]] (product), [[Private Space - The Bedroom Moved Online]] (music), [[Show Your Way - Instagram for Personal Methods]] (consumer), [[Unified-Media-Insight-Capture-Tool]] (product), [[../projects/prd/Chronicle_prd]] (product), [[../projects/prd/Constellate_prd]] (product), [[../research/career/Creative-Tech-Trends]] (career), [[../research/vibecoding/karpathy-llm-wiki]] (vibecoding)
- **ai-as-enabler-not-replacer** → [[Been There]] (system), [[Finding What You Like - Rekindling Passion & Curiosity]] (system), [[Return to Basics]] (system)
- **bridging-structural-holes** → [[Atlas - One Map Over Every App]] (product), [[../projects/prd/Constellate_prd]] (product), [[../research/system/AI-Industry-Map-2026]] (system), [[../research/system/connecting_the_dot]] (system), [[../research/system/graph-theory-foundations]] (system), [[../research/system/graphrag-connection-engine]] (system), [[../research/system/linking-algorithms-survey]] (system), [[../research/system/two-kinds-of-connection]] (system)
<!-- AUTO-CONCEPTS:END -->

---
- **Subject**: [[Startup & Side Projects]]
- **Source**: `raw/obsidian/startup/idea/The Connection.md`
