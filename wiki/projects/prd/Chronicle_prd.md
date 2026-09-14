---
stage: projects
category: product
tag: projects
created: 2026-07-24
industry: Productivity / Tooling
status: active
lifecycle: researching
concepts: [interpretation-over-artifact, multi-signal-fusion]
topic:
- PRD
- Product
- Chronicle
type: resource
---

> [!IMPORTANT] Key Takeaway
> **Why this matters:** Chronicle lets you archive any topic by time through your own frame, so you can read a subject's 연대기 and eventually analyze how it (and your view of it) evolved. Its deepest purpose is **linking — finding 의외의 연결성 (unexpected connections) both within a subject and across subjects**. v1 ships a lightweight version of that linking so the moat is visible from day one.
> **How to use it:** Source of truth for building v1 — and the brief to paste into Figma Make to generate the initial design. Structured to the Figma PRD guide (overview → users → features → flows → success).
> **Informs:** Implementation, feature prioritization, and the Chronicle idea page roadmap.

# PRD — Chronicle (v1: Archive + Lightweight Linking)

> [!WARNING] Superseded by [[Constellate_prd|Constellate PRD]] (2026-09-04)
> The product absorbed this one and grew: macOS desktop instead of web PWA, SQLite instead of IndexedDB,
> a reading surface with highlights, media types as first-class, trend promoted from Phase 2 to v1 core,
> and Projects as a second container. **This document is still live as a source** — its design system (§6.1),
> component inventory (§6.3), seed content (§6.6) and linking engine (§7) are inherited unchanged by v2.

## Product Details
| | |
|---|---|
| **Project** | Chronicle — personal, time-ordered, cross-subject-linking archive |
| **Target release** | v1.0 (web-first PWA) |
| **Document owner** | Seungjo Han (한승조) |
| **PM / Designer / Developer** | Seungjo Han (solo) |
| **Version** | 0.5 — added Inspiration page + dedicated Tag pages (design iteration from Figma Make) |
| **Updated** | July 24, 2026 |
| **Status** | Researching → drafting spec |

---

## 1. Overview

**Elevator pitch:** Paste a URL; Chronicle enriches it (title, summary, keywords), files it under a subject you choose, and lists it by date. Read any topic as a chronology (연대기), and see related items — within the same subject *and* across others — so you notice connections you'd otherwise miss.

**Value proposition:**
- **Read a topic over time, not just its latest snapshot** — grasp the 시대적 흐름 (how the story, and your view of it, evolved).
- **Your frame, not an algorithm's** — you choose what enters and under which subject.
- **Connect the dots** — the Related panel surfaces 의외의 연결성 (unexpected connections) across your subjects. *This is the moat.*

**Strategic context (why this, why now):** The capture loop (URL → metadata → folders → tags → search) is commoditized — Zotero, Raindrop, Readwise, Instapaper all do it well, and all silo by folder. None make **time the reading axis** or surface **cross-subject connections**. Chronicle's differentiation is exactly there: the *reading* (chronology) and the *linking* (연결성), not the capture. It productizes the "connect the dots" instinct curiosity-lab already runs on.

---

## 2. Goals & Principles

**v1 goals — do these four well:**
1. **Frictionless capture** — paste a URL, get a clean enriched card with near-zero effort.
2. **Category-scoped, date-ordered reading** — each subject its own space; within it, items read as a chronology.
3. **Fast retrieval** — scoped search so nothing archived is ever lost.
4. **Lightweight linking (the moat, cheap version)** — a Related panel on each item showing keyword/hashtag-overlap relations, within and across subjects.

**North-star principle — Linking (연결성):** the reason Chronicle exists is to connect the dots. v1 delivers the *mechanism* (keyword-overlap panel — finds *obvious* relations); Phase 2 delivers the *magic* (semantic embeddings — finds *surprising*, word-independent relations). v1 is built so Phase 2 slots in without a rewrite.

---

## 3. Users & Personas

**Primary persona — "The Curious Archivist" (the v1 user):**
- A PM/builder who actively follows many topics — news, tech, economy, music, books.
- **Goal:** understand how each topic *develops over time*, and notice connections *between* topics.
- **Frustration:** existing tools show only the latest snapshot and silo saves by folder; the throughline and the cross-topic links are invisible.
- **Behavior:** saves links constantly; thinks in "connect the dots"; wants a personal memory, not a feed.

**Secondary (deferred to the product phase):** knowledge workers, researchers, and learners who want a personal, chronological, connected memory. Not a v1 target — informs Phase 3 (see §15).

---

## 4. User Stories

- As the **archivist**, I want to save a page by pasting its URL, so capturing is one action.
- As the **archivist**, I want each item auto-titled, summarized, and keyworded, so I never hand-type metadata.
- As the **archivist**, I want to file each item under a subject I pick, so every topic has its own space.
- As the **archivist**, I want to edit any enriched field and add hashtags, so my frame wins over the LLM's.
- As the **reader**, I want a category's items listed by date, so I can read the topic's chronology (연대기).
- As the **reader**, I want to flip newest ↔ oldest, so I can read the story forward or catch up backward.
- As the **searcher**, I want scoped search (overall / title / hashtag / description / date-range), so I can find any item fast.
- As the **connector**, I want each item to show related items — within and across subjects — so I notice connections I'd forget.
- As the **connector**, I want cross-subject relations highlighted, so the surprising links stand out from the obvious.
- As the **connector**, I want an **Inspiration page** that gathers the connections and trends across my whole archive, so I have somewhere to go be surprised and see the big picture.
- As the **searcher**, I want clicking a hashtag to open a **page of every item with that tag**, so I can read a theme across all subjects at once.
- As the **owner**, I want to export/import my archive as JSON, so my data is never trapped in one browser.
- As the **mobile user**, I want to install it as an app and read offline, so I can use it anywhere.

---

## 5. Features & Functionality (v1)

**Capture**
- Add an item by pasting a URL (single input + "Add" button)
- Auto-enrichment: title, source, publish date, keywords, summary
- Pick a category on save; edit any field; add hashtags
- Duplicate detection (re-adding a known URL surfaces the existing item)

**Organize & read**
- Category spaces in a sidebar — one per subject; create / rename / reorder
- Date-ordered card list per category (newest ↔ oldest toggle)
- Item detail view: full summary, editable fields, note, "open original"

**Search**
- Scoped search: Overall / Title / Hashtag / Description / Date-range
- Search the current category or all categories

**Link (the moat — cheap keyword version)**
- Related panel on each item: related items by keyword / hashtag overlap
- Grouped into "Same subject" and "Other subjects" (cross-subject highlighted)
- Each related row shows the shared key(s)

**Discover**
- **Tags page** — all hashtags (chip cloud with counts); clicking a hashtag opens its own **Tag page** (every item with that tag, across subjects). Hashtags live on their own pages, not in the sidebar.
- **Inspiration page** — a dedicated "results" surface: surfaced cross-subject connections + simple trends now (from the keyword engine); trend summaries + foresight later (§6.7).

**Foundation**
- JSON export / import (durability — the personal-era backup)
- Installable PWA (desktop + mobile), offline reading of saved items

*Feature priority:* Capture → Read → Search → Related panel → Foundation (see Build Plan §12).

---

## 6. Design, Layout & User Flows

### 6.1 Design system (reuse seungjohan.com)
Chronicle reuses the existing seungjohan.com design system — **editorial minimalism**. It's a perfect fit for a reading-first archive.
- **Philosophy:** clarity first, typographic restraint, calm interaction. No decorative gradients, shadows, or illustrations. Color carries meaning, not decoration.
- **Palette (Tailwind):** page `bg-white`; primary text `text-gray-900`; body `text-gray-700`; muted `text-gray-500`; label/meta (dates) `text-gray-400`; borders `border-gray-100`; primary CTA `bg-black text-white`. One optional accent per category (small color dot on the CategoryBadge).
- **Type:** editorial, precise sizes (no default Tailwind text-size classes for headings/body). Titles carry hierarchy by weight/size, not color.
- **Motion:** subtle + fast — entry `opacity 0→1, y 20→0`, ~0.7s, ease `[0.22,1,0.36,1]`. Nothing bounces or pulses.

> **For Figma Make:** do NOT use generic AI aesthetics — no Inter/Roboto, no purple gradients, no drop shadows. This is a calm, monochrome, print-like reading room.

### 6.2 Layout
- **Left sidebar (nav):** **Home** · **Category** · **Tags** · **Inspiration**. Home = the full cross-category feed; Category expands to the subject spaces; Tags opens a Tags page; Inspiration opens the insights page (§6.7). A global "Add URL" button sits here too.
- **Tags behavior (updated):** the sidebar **Tags** item does **not** expand a hashtag list inside the sidebar. It opens a **Tags page** (all hashtags, e.g. a chip cloud with counts). Clicking any hashtag — from the Tags page *or* from a card — opens a dedicated **Tag page**: a date-ordered feed of every item carrying that hashtag, across all subjects. Hashtags never live inline in the sidebar.
- **Main area — top:** a **search bar** (with scope selector).
- **Main area — below:** an **Instapaper-style media list** — a vertical stack of cards, each showing **title, summary, and hashtags** (plus source + date, muted). Generous whitespace; hairline dividers.
- **Responsive:** desktop = persistent sidebar + feed; mobile = sidebar collapses to a drawer (hamburger), feed goes single-column, search bar sticks to top.

### 6.3 Component inventory (for Figma Make)
`AppShell` (sidebar + main) · `Sidebar` (Home / Category / Tags / Inspiration nav + AddUrlButton) · `SearchBar` + `ScopeChips` · `ItemCard` (title, summary, hashtags, source, date) · `ItemList` (Instapaper feed) · `DateDivider` · `HashtagChip` · `CategoryBadge` · `AddUrlModal` → `EnrichedCardEditor` (editable fields + category picker) · `ItemDetail` (full summary, note, "open original") · `RelatedPanel` + `RelatedRow` (title, category badge, "shares: …") · `TagsOverview` (all hashtags, chip cloud) · `TagPage` (feed for one hashtag) · `InspirationPage` · `ConnectionCard` (a surfaced cross-subject link) · `TrendCard` · `EmptyState` · `EnrichingState` · `PartialEnrichmentBanner`.

### 6.4 Flows
- **Capture:** paste URL → "enriching…" → editable enriched card (title, source, date, summary, keywords, category picker, hashtags) → save → card lands at its date position.
- **Browse:** open Home or a category → date-ordered Instapaper feed → sort toggle (newest ↔ oldest).
- **Search:** type → pick scope (chips) → optional date range → same feed, filtered; active scope + range shown as removable chips.
- **Related (the moat):** open an item → Related panel shows **Same subject** (threads the chronology) and **Other subjects** (highlighted 의외의 연결성); each row: title, category badge, shared key(s); click → jump.
- **Tags:** click **Tags** in the sidebar → Tags page (all hashtags as a chip cloud with counts) → click a hashtag → **Tag page** (date-ordered feed of every item with that tag). A hashtag on any card links straight to its Tag page.
- **Inspiration:** click **Inspiration** in the sidebar → the insights page (§6.7): a place to *go be surprised* — surfaced cross-subject connections + simple trends now, richer trend summaries + foresight later.

### 6.5 States & microcopy
- **Empty (first run):** "Nothing here yet — paste a URL to start this timeline."
- **Enriching:** inline spinner + "Reading the page…"
- **Partial enrichment:** banner "Couldn't fully read this page — check the title and summary."
- **No related items:** "No connections yet. Add more and they'll start linking."
- **Key labels:** "Add URL", "Related · Other subjects", "shares: incentives", sort toggle "Newest / Oldest".

### 6.6 Sample seed content — category **"Tech"** (use as real design data, not lorem-ipsum)
This set doubles as a demo of the 연대기 (AI, 2016 → 2026) and of linking — note **"Fable"** appears in two items, so the Related panel should link them.

| Date | Title | Source | Summary | Hashtags |
|---|---|---|---|---|
| 2016-03-13 | 이세돌의 인간 승리… '바둑 괴물' 알파고도 '백기' | 연합뉴스 (Yonhap) | Lee Sedol beat AlphaGo in Game 4 of the Google DeepMind Challenge Match (resignation at move 180) — AlphaGo's first loss to a human after a 499–1 record. | #ai #go #deepmind |
| 2026-06-30 | US to lift export controls on Anthropic's Fable AI model, source says | Reuters | The US will lift export controls on Anthropic's Fable AI model, per a source. | #ai #policy #anthropic |
| 2026-07-14 | OpenAI's first device will be a moveable, screenless speaker built as an AI companion | Bloomberg | OpenAI's first hardware device is reportedly a moveable, screenless speaker designed as an AI companion. | #ai #hardware #openai |
| 2026-07-21 | Kimi K3 Fable — K3 is competitive with Fable; K3 + Fable is SoTA | Fireworks AI | Benchmarked open Kimi K3 vs closed Fable 5 on ~1,000 agentic tasks; routing between them hit 93% accuracy at up to ~50× lower cost. Thesis: don't pick a model, route. | #ai #models #routing |

**Match-keys illustrated:** items 2 and 4 share `fable` → they appear in each other's Related panel (Same subject: Tech). Across categories, `ai` would bridge Tech ↔ any other subject where it appears. This is exactly the connection the panel exists to surface.

### 6.7 Inspiration page (the "results" surface)
A dedicated page (sidebar: **Inspiration**) where the archive's *output* lives — the counterpart to the per-item Related panel. The Related panel is **pull** (links you find while reading one item); Inspiration is **push** (Chronicle brings the connections and trends to you). It's the home for what was the deferred feed/digest surface (§16).

- **v1 (cheap, from the keyword engine):**
  - **Surfaced connections** — a feed of `ConnectionCard`s: cross-subject links the keyword engine found (item A in one subject ↔ item B in another, with the shared key). The "unexpected links" feed, made real cheaply.
  - **Simple trends** — a few `TrendCard`s: most-used keywords/hashtags, most-connected subjects, recent activity.
- **Phase 2 (the upgrade):** semantic "surprise" connections; LLM-written per-category trend summaries (연대기 arc); cross-category common threads; foresight.
- **Feel:** a calm "discover" page, not a dashboard — a place to wander and be surprised. Same editorial minimalism.

---

## 7. The Linking Engine (the moat)

The product bets on this. v1 ships the cheap keyword version; Phase 2 upgrades it to semantic. Same surface (the Related panel), smarter engine.

- **Surface:** the Related panel (§6), two groups — Same subject / Other subjects (highlighted).
- **v1 detection (keyword/hashtag overlap):** for the open item, find others sharing ≥1 match-key or hashtag; score by shared-key count (hashtags weighted higher), multiply by a **cross-category boost** (a shared key across subjects is more surprising), recency tiebreak; exclude self; cap N per group. Computed on demand (personal-scale = fast).
- **Honest limit:** keyword overlap finds relations that *share vocabulary* — obvious + semi-obvious. It is blind to the *truly surprising* links that mean the same thing in different words ("rate cuts" ↔ "vinyl boom" via discretionary spending). Those need **Phase 2 semantic embeddings** — that's the upgrade, in the same panel.

---

## 8. Data Model (the "how" — kept minimal)

Local-first for v1, shaped for future multi-user sync (`userId` included now).

- **Item:** `id`, `userId`, `url`, `canonicalUrl` (dedup key), `title`, `source`, `summary`, `keywords[]` (display), `matchKeys[]` (normalized, for linking), `hashtags[]`, `categoryId`, `publishedAt | null`, `savedAt`, `enrichment` (full/partial/failed), `note?`. *(Phase 2: additive `embedding?` — no migration.)*
- **Category:** `id`, `userId`, `name`, `color?`, `createdAt`, `order`. A first-class container, not a tag.
- **Two-layer keywords:** `keywords` are free-form for display; `matchKeys` are derived (lowercase → de-pluralize → alias-map) so "AI" / "artificial intelligence" / "A.I." actually match. A small alias map (in IndexedDB) grows over time; changing it triggers a cheap rebuild pass.
- **Time axis:** `publishedAt ?? savedAt` — sorting a category by this is the 연대기 view.
- Links are **computed over** items, not stored on them.

---

## 9. Non-Functional Requirements

- **Durability:** ship JSON export/import in v1 (IndexedDB is per-browser; this is the backup until sync exists).
- **Privacy:** enrichment sends URL + extracted text to a hosted LLM — fine for personal use; flag for the product phase (may need a privacy mode).
- **Offline:** PWA caches shell + saved items for offline reading; capture needs connectivity.
- **Performance:** all reads/search/linking are local, personal-scale — target instant (<100ms). Only enrichment is network-bound.
- **Security:** the Claude API key lives only in the serverless function, never the client.

---

## 10. Assumptions, Dependencies & Constraints

- **Assumptions:** most pages expose enough metadata/text to enrich; personal-scale data (hundreds–low thousands of items) fits IndexedDB + client-side search; single user in v1.
- **Dependencies:** Claude API (enrichment); a serverless host (Vercel); the keyword alias map (linking quality).
- **Constraints:** local-first (no cloud sync in v1); capture requires connectivity; API key server-side only; keep v1 scope tight — resist feature creep (the backlog, §16, absorbs it).

---

## 11. Release Criteria (ship v1 when all true)

- Capture → enrich → save works reliably, including the partial-enrichment fallback.
- A category reads correctly by date; sort toggle works.
- Search returns correct results across all five scopes + date range.
- Related panel shows correct Same-subject / Other-subject relations with shared keys shown.
- Export → import round-trips with no data loss.
- Installs as a PWA; offline reading works.

---

## 12. Build Plan / Milestones (v1)

Thin vertical slices; each usable on its own.

| # | Milestone | Delivers |
|---|---|---|
| M1 | Capture + enrich | URL → `/api/enrich` → editable card saved to IndexedDB. The core loop. |
| M2 | Categories + date list | Sidebar, category CRUD, date-ordered list + sort toggle. |
| M3 | Search | Scoped search (all 5 scopes) via FlexSearch. |
| M4 | Related panel | match-key derivation + alias map + overlap engine (§7) + panel UI. The moat, minimum version. |
| M5 | Durability + PWA | JSON export/import, PWA install/offline, empty/loading/partial states. |

**Tech (proposed):** Vite + React 18 + TypeScript, Tailwind v4, IndexedDB via Dexie, FlexSearch, React Router v7; enrichment via a Vercel serverless function calling Claude (`claude-haiku-4-5` default). Matches the existing seungjohan.com stack for reuse.

---

## 13. Success Metrics / Evaluation Plan

Personal-use signals (v1 is for one user — measure usefulness, not scale):
- **Capture friction:** I add items without hesitation; capture feels like one gesture.
- **Enrichment quality:** the auto title/summary/keywords are "good enough to not edit" most of the time.
- **Linking value:** the Related panel surfaces at least one genuinely useful connection per session that I wouldn't have recalled.
- **Behavior change:** I reach for Chronicle instead of a browser bookmark / Instapaper when following a topic.
- **The feeling:** reading a category chronologically actually gives me the 시대적 흐름 — the sense of a topic's arc.

---

## 14. Risks & Open Questions

- **Keyword quality is load-bearing (v1).** The Related panel is only as good as `matchKeys` — how aggressively to normalize, and how the alias map grows (manual vs LLM-proposed). *Resolve during M4.*
- **Enrichment reliability** — paywalled / JS-rendered pages resist server-side fetch; how far before falling back to metadata-only?
- **Publish-date detection** — not all pages expose a date; `savedAt` fallback — good enough, or prompt the user?
- **Solution favoritism (Figma's warning):** don't over-commit to keyword-only linking — Phase 2 semantic is where the real value is; keep the panel engine swappable.
- **Sibling boundary** — where does Chronicle end and the Unified-Media-Insight-Capture-Tool begin? (This archives whole media by time; that captures the moment of insight inside media.)

---

## 15. Roadmap

- **Phase 1 — Archive + Lightweight Linking** *(this PRD)*: capture, categories, date lists, hashtags, scoped search, keyword-overlap Related panel. Web-first PWA, local-first, LLM enrichment.
- **Phase 2 — Semantic Linking & Analysis** *(the differentiator)*: embedding-based "surprise" links, per-category trend summary (연대기 arc), cross-category common threads, foresight.
- **Phase 3 — Native Apps & Product**: native desktop + mobile (share-sheet capture); personal tool → multi-user product (accounts, sync, billing).

---

## 16. Build-Later Backlog (deferred — captured so nothing is forgotten)

**Linking — Phase 2:**
- [ ] Semantic / embedding "surprise" links (word-independent connections). *The upgrade that makes the panel truly 의외의.*
- [ ] Link-score refinement (cross-category boost, thresholds, the high-semantic + low-lexical highlight).
- [ ] Richer Inspiration-page surfaces: weekly connect-pass digest, connection graph. *(The "unexpected-links feed" is no longer deferred — it's the v1 Inspiration page's surfaced-connections list, §6.7.)*

**Analysis — Phase 2:**
- [ ] Per-category trend summary (연대기 arc).
- [ ] Cross-category common-thread analysis.
- [ ] Foresight / prediction (hardest; honest limits).

**Platform & product — Phase 3:**
- [ ] Native desktop app (Tauri/Electron).
- [ ] Native mobile app + share-sheet capture.
- [ ] Browser extension (one-click capture).
- [ ] Multi-user product (accounts, hosted sync, billing).

**Maybe / later:**
- [ ] Controlled-vocabulary keyword mode (evolve match-keys toward the concept-atom model).
- [ ] Bulk import (Raindrop / Instapaper / Zotero / Pocket export).
- [ ] Reader mode / full article body storage.

---

## 17. Changelog

| Version | Date | Changes |
|---|---|---|
| 0.5 | Jul 24, 2026 | Design iteration after the first Figma Make build. Added an **Inspiration page** (sidebar) as the push-based "results" surface (surfaced connections + trends; §6.7) — absorbs the deferred unexpected-links feed. Moved hashtags off the sidebar: **Tags** now opens a Tags page, and a hashtag opens its own **Tag page**. Updated layout, components, flows, features, user stories, backlog. |
| 0.4 | Jul 24, 2026 | Expanded §6 into Design, Layout & User Flows: reused seungjohan.com design system, the sidebar (Home/Category/Tags) + search + Instapaper feed layout, a component inventory, states + microcopy, and a real seeded **Tech** category (AlphaGo 2016 → Fable/Kimi/OpenAI 2026) that also demos the linking. |
| 0.3 | Jul 24, 2026 | Restructured to the Figma PRD guide for Figma Make. Added Product Details, Overview + value prop + strategic context, User Personas, User Stories, User Flows & UX Notes, Assumptions/Dependencies/Constraints, Release Criteria, Success Metrics. Body kept plain-text (no wikilinks) for pasting. |
| 0.2 | Jul 24, 2026 | Deep-dive upgrade. v1 gained a keyword-overlap Related panel; two-layer keyword model; Linking Engine, Non-Functional, Build Plan, Build-Later Backlog sections. |
| 0.1 | Jul 24, 2026 | Initial draft. v1 scope (archive, web-first, LLM enrichment, personal-first). |

## 🔗 Connections
- [[../../ideation/Chronicle - Personal Topic Timeline|Chronicle — Idea Page]] — the researched idea + roadmap this PRD implements
- [[../../ideation/Unified-Media-Insight-Capture-Tool|Unified-Media-Insight-Capture-Tool]] — sibling capture idea
- [[../../ideation/ideation|Ideation Board]]
- [[../../index|Master Index]]

<!-- AUTO-CONCEPTS:START -->
### 🔀 Concepts (auto-generated — do not edit)
- **interpretation-over-artifact** → [[../../ideation/Chronicle - Personal Topic Timeline]] (product), [[../../ideation/Company Fit Finder - Where to Work]] (system), [[../../ideation/Finding What You Like - Rekindling Passion & Curiosity]] (system), [[../../ideation/Keep in Touch - Relationship Chronicle]] (system), [[../../ideation/Private Space - The Bedroom Moved Online]] (music), [[../../ideation/The Connection]] (system), [[../../ideation/Unified-Media-Insight-Capture-Tool]] (product), [[Constellate_prd]] (product), [[../../research/career/Creative-Tech-Trends]] (career), [[../../research/vibecoding/karpathy-llm-wiki]] (vibecoding)
- **multi-signal-fusion** → [[../../ideation/Advance Planner]] (system), [[../../ideation/Been There]] (system), [[../../ideation/Chronicle - Personal Topic Timeline]] (product), [[../../ideation/Company Fit Finder - Where to Work]] (system), [[../../ideation/Taste Detector]] (system), [[../../ideation/The Connection]] (system), [[../../ideation/Triathlon Photo Finder]] (system), [[../../ideation/Wine Value Advisor]] (system), [[../Michelin Filter]] (system), [[../Trip Guide - Shareable Restaurant Map]] (travel), [[../../research/cooking/selected-restaurants]] (cooking), [[../../research/system/connecting_the_dot]] (system), [[../../research/system/graph-theory-foundations]] (system), [[../../research/system/graphrag-connection-engine]] (system)
<!-- AUTO-CONCEPTS:END -->
