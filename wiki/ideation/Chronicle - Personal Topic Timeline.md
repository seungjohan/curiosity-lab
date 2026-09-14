---
stage: ideation
category: product
concepts: [interpretation-over-artifact, multi-signal-fusion]
lifecycle: building
---

> [!IMPORTANT] Key Takeaway
> **Why this matters:** Existing news-timeline products are editorial and someone-else-curated. There's no tool where *you* archive any topic by time, through *your own* frame — so you can read a subject's 연대기 (chronology) and feel how it (and your own view of it) evolved. And the deepest value is **linking**: finding **의외의 연결성 (unexpected connections)** — common points not just *within* a subject but *across* subjects. This is curiosity-lab's own "connect the dots" philosophy turned into a product.
> **How to use it:** Build a spec + prototype for a URL-in → auto-enriched, date-ordered, category-scoped archive. Instapaper-like UI, hashtags, strong search — designed so cross-subject linking can grow on top.
> **Informs:** Desktop app + mobile app product direction.

# Chronicle — Personal Topic Timeline

## Problem Statement
When I follow a topic — news, tech, economy, music — I only ever see the *latest* snapshot. I can't easily read it in time order to grasp the **시대적 흐름**: how the story developed, how my own point of view shifted, and where it might go next. Editorial timeline apps exist but they curate for me. I want to archive through **my frame, my interest, my lens** — and later analyze the trend and even predict the future from my own archive.

## Core Product Thesis
A low-feature, high-focus archive tool. The magic isn't features — it's the **chronological + personal-frame** framing, and above all the **linking**:
1. **My lens** — I choose what enters and under which subject. The collection reflects *my* interest, not an algorithm's.
2. **Time as the primary axis** — everything lists newest/oldest by date, so a topic reads as a 연대기.
3. **Trend + foresight** — because it's dated and mine, I can summarize the arc of my own thinking and forecast where the topic is heading.
4. **Connecting the dots (연결성) — the main point.** The deepest value is finding **의외의 연결성 (unexpected connections)**. When I add an item under one subject, Chronicle should surface common points **not only within that subject, but across other subjects** — an economy shift that echoes a music trend, a tech idea that rhymes with a news event, a book that reframes something I saved months ago in a different category. Knowledge compounds when dots connect *across* domains, not inside silos. This is [[../../LINKING|curiosity-lab's linking system]] turned into a product: the same "find the surprising link" instinct this vault runs on.

> *Decided (2026-07-24 brainstorm): the linking surface is a **Related panel** on each item, showing related items **within the same subject and across other subjects** (cross-subject = the highlighted surprise). **v1 ships a cheap keyword-overlap version** of it; semantic "surprise" links come in Phase 2. Other surfaces (feed / connect-pass digest / graph) are deferred. See [[../projects/prd/Chronicle_prd|the PRD]] §6 + §12.*

## Core User Flow
1. **Paste a URL** — single input.
2. **Auto-enrich** — the product fetches and extracts: media **title**, source URL, **metadata**, **core keywords**, and a **summary**.
3. **Categorize** — the item lands in a subject I pick (e.g. News, Music, Tech, Economy) — each its own page/space.
4. **Tag** — add hashtags for cross-cutting retrieval.
5. **Browse** — items list **ordered by date** within a category (Instapaper-style card list).
6. **Search** — scoped search (see below).
7. **Analyze** — later, combine categories and surface **common threads / trends** across them; summarize the arc; project forward.

## Features (intentionally minimal)
- **URL archiving** with automatic enrichment (title, metadata, keywords, summary).
- **Category pages** — one space per subject (news-only, music-only, tech-only, economy-only). This is the *most important* organizing primitive.
- **Date ordering** — the default and defining view; date is a first-class axis.
- **Hashtags** — flexible cross-category labels.
- **Scoped search** — user picks the scope:
  - Search **overall**
  - Search in **title**
  - Search by **hashtag**
  - Search in **description / summary**
  - **Date range** (from-date → to-date period filter)
- **Related panel (v1, cheap)** — on each item, related items by keyword/hashtag overlap, within *and* across categories (cross-category highlighted). The moat's minimum version.
- **Semantic linking + trend/foresight analysis (Phase 2)** — embedding-based surprise links, per-category 연대기 summaries, cross-category common threads, forward-looking reads.

## UI Reference
- **Instapaper** — the target look and feel exactly: clean, list-of-cards reading archive.

## Roadmap
Ship the archive first as a solid wedge; the analysis (the real differentiator) and native apps bolt on later. The v1 data model is designed so nothing below requires a rewrite.

### Phase 1 — Archive + Lightweight Linking (v1, in PRD)
- **Platform:** Web-first (installable PWA — works on desktop + mobile browsers).
- URL-in → **LLM-powered** enrichment (title, metadata, keywords + normalized match-keys, summary).
- Category spaces (news / music / tech / economy…), date-ordered card list (Instapaper UI).
- Hashtags + scoped search (overall / title / hashtag / description / date-range).
- **Related panel (the moat, cheap version)** — keyword/hashtag-overlap related items, within *and* across categories (cross-category highlighted). Finds the *obvious* dots; the surprising ones come in Phase 2.
- Personal now (single-user, local-first) but architected to become multi-user later.

### Phase 2 — Semantic Linking & Analysis (the differentiator)
- **Semantic linking (의외의 연결성) — the headline upgrade.** Embedding-based links that catch **unexpected connections sharing no words** (different words, same idea, different subject) — the thing keyword overlap is blind to. Upgrades the same Related panel.
- **Per-category trend summary** — LLM reads a category's dated items and summarizes the 연대기: how the topic (and my view of it) evolved.
- **Cross-category common threads** + **foresight** — project where a topic is heading, grounded in my own archive. *(Hardest piece; needs a real method, not just a prompt.)*
- *Deferred surfaces:* unexpected-links feed, connect-pass digest, connection graph.

### Phase 3 — Native Apps & Product
- **Native desktop app** (Tauri/Electron) and **native mobile app** (with share-sheet "save to Chronicle").
- Open up from personal tool → **multi-user product**: accounts, hosted sync, billing.

## Market Landscape
- **Timeline** (news app, ~2015, now defunct) — the closest concept: dated "cards" showing a story's history. But editorial and news-only, curated *for* the reader. Validates demand; leaves the personal/any-topic space open. [TechCrunch](https://techcrunch.com/2015/01/15/timeline-launches-news-app-to-give-you-the-context-behind-the-days-headlines)
- **Google News Timeline** (Google Labs, defunct) — search a topic, see it over day-columns. Same gap: not personal, not self-curated.
- **NewsWhip Timeline** — real-time story-trajectory tracking, but a pro media-monitoring analytics tool, not a personal archive.
- **Kagi** users have openly requested a "topic timeline over a long period" view — wanted-but-unbuilt even now. [Kagi feedback](https://kagifeedback.org/d/836-timeline-view-show-important-news-stories-on-a-topic-over-a-longer-period-of-time)
- **Instapaper / Readwise Reader / Are.na / mymind** — great "save anything" archives, but organized by save-order/collection, *not* by a topic's chronology-as-the-point, and not built around trend analysis of your own frame.

**Gap:** personal + any-topic + self-curated + time-as-the-point + trend/foresight + **cross-subject linking**. The capture loop is commoditized (Zotero, Raindrop, Readwise, Instapaper all do URL→metadata→folders→tags→search well); the moat is the *reading* (chronology) and the *linking* (의외의 연결성) — not the capture. Nobody occupies all six.

## Open Questions
- **Cross-subject linking — surface & staging now decided** (2026-07-24): a **Related panel** (within + across categories), keyword-overlap in v1, semantic embeddings in Phase 2. Remaining questions: (v1) how good `matchKeys`/alias-map normalization needs to be for the panel to feel useful; (Phase 2) which embedding method + how to score the *surprising* quadrant. See [[../projects/prd/Chronicle_prd|PRD]] §6, §12, §13.
- How is the auto-summary / keyword extraction done — on-device, or a hosted LLM? Cost per URL at scale?
- "Predict the future from my archive" — how far does the analysis go? Summary of the arc (easy) vs. genuine forecasting (hard, needs a real method).
- Paywalled / JS-heavy pages: can enrichment reliably fetch title/metadata/summary?
- Where does this end and [[Unified-Media-Insight-Capture-Tool]] begin? (This archives the *whole media by time*; that captures the *moment of insight inside* media.) Same product, or two?

## 🔗 Connections

### ⬆ Pipeline
- Back ← [[sparks|✨ Spark List]] — promoted from the `Topic time-archive` spark (2026-07-24)
- Back ← [[ideation]] — tracked on the active ideation board
- Spec → [[../projects/prd/Chronicle_prd|Chronicle PRD]] — v1 (the archive) product requirements
- Spec → [[../projects/prd/Constellate_prd|Constellate PRD]] — the current spec: archive · read · trend · projects (supersedes v1)
- Sibling → [[Unified-Media-Insight-Capture-Tool]] — the moment-of-insight capture cousin; this one archives whole media chronologically
- Hub → [[../index|Master Index]]

<!-- AUTO-CONCEPTS:START -->
### 🔀 Concepts (auto-generated — do not edit)
- **interpretation-over-artifact** → [[Company Fit Finder - Where to Work]] (system), [[Finding What You Like - Rekindling Passion & Curiosity]] (system), [[Keep in Touch - Relationship Chronicle]] (system), [[Private Space - The Bedroom Moved Online]] (music), [[The Connection]] (system), [[Unified-Media-Insight-Capture-Tool]] (product), [[../projects/prd/Chronicle_prd]] (product), [[../projects/prd/Constellate_prd]] (product), [[../research/career/Creative-Tech-Trends]] (career), [[../research/vibecoding/karpathy-llm-wiki]] (vibecoding)
- **multi-signal-fusion** → [[Advance Planner]] (system), [[Been There]] (system), [[Company Fit Finder - Where to Work]] (system), [[Taste Detector]] (system), [[The Connection]] (system), [[Triathlon Photo Finder]] (system), [[Wine Value Advisor]] (system), [[../projects/Michelin Filter]] (system), [[../projects/Trip Guide - Shareable Restaurant Map]] (travel), [[../projects/prd/Chronicle_prd]] (product), [[../research/cooking/selected-restaurants]] (cooking), [[../research/system/connecting_the_dot]] (system), [[../research/system/graph-theory-foundations]] (system), [[../research/system/graphrag-connection-engine]] (system)
<!-- AUTO-CONCEPTS:END -->

### Tension ✦ (hand-picked)
- [[Return to Basics]] — pulls against: this tool deepens digital capture/curation, while Return to Basics argues value is migrating to physical, non-digital grounding.

---
- **Subject**: [[Startup & Side Projects]]
- **Source**: User Brainstorming — promoted from spark `Topic time-archive`
