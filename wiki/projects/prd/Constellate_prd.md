---
stage: projects
category: product
tag: projects
created: 2026-09-04
industry: Productivity / Tooling
status: active
lifecycle: building
concepts: [interpretation-over-artifact, bridging-structural-holes, high-signal-filter]
topic:
- PRD
- Product
- Constellate
type: resource
---

> [!IMPORTANT] Key Takeaway
> **Why this matters:** This supersedes the v1 archive PRD. The product is no longer "an archive with linking" — it is a **personal media archive you also read in**, built around one question: *where is this subject going next?* Media enters by URL, is filed under a subject, and is read **in published-date order** so the movement of a topic is visible; a dated **Trend Read** turns that movement into an explicit, checkable prediction. A second container — **Projects** — collects references for things you actually make (music first).
> **How to use it:** Source of truth for the Figma prototype and the build. Everything here is ranked against the core; anything Readwise does that doesn't serve it is in §16, not §5.
> **Informs:** The Figma extension of Chronicle v4, and the build in a separate repo.

# PRD — Constellate (Archive · Read · Trend · Projects)

## Product Details
| | |
|---|---|
| **Project** | **Constellate** — personal media archive, read chronologically, for trend inference |
| **Target release** | v1.0 — **macOS desktop app** |
| **Document owner** | Seungjo Han (한승조) |
| **PM / Designer / Developer** | Seungjo Han (solo) |
| **Version** | 1.2 — supersedes `Chronicle_prd.md` (v0.5) |
| **Updated** | September 4, 2026 |
| **Status** | Spec drafted → Figma prototype → build |
| **Name** | **Constellate** — decided 2026-09-04. A constellation is scattered points that only become a figure once someone draws the line between them, which is exactly §7.4. **"Chronicle" survives as the name of the timeline view** inside it; the shipped v1 app, the Figma file "Chronicle · Version 4", and `Chronicle_prd.md` keep their historical names. |

---

## 0. What this changes from v1 — read this first

`Chronicle_prd.md` (v0.5, Jul 24) is **superseded**, not deleted. Nine decisions changed:

| # | v1 said | v2 says | Why |
|---|---|---|---|
| 1 | Web-first PWA | **macOS desktop app** | Owner's decision. Buys local-first storage, no hosting, no auth, and native file writes into curiosity-lab. |
| 2 | IndexedDB via Dexie | **SQLite** in Application Support + **markdown export** of highlights/notes into the vault | Full-text search over article bodies; outflow without vault bloat. |
| 3 | Archive only — no reading surface | **Reading mode with highlights** | Owner reads and highlights daily; v1's detail panel showed a summary, not the article. |
| 4 | URLs → enriched cards | **Articles, PDFs, videos, tracks, podcasts** as distinct types | "Archiving media's articles, URL, PDF, or whatever, from so many resources." |
| 5 | Trend + foresight = **Phase 2** | **Trend is v1 core** (§7.2) | The *goal* is the owner's, stated twice: "I wanna keep track of the movement of the trend or the next step based on the past steps" and "go back to the past and keep track of those movements and imagine or think about the future step." The **Trend Read mechanism** in §7.2 — four fixed sections, mandatory falsifier, saved as a dated item — is the author's design and needs confirming. |
| 6 | One container: Category | **Two: Subject and Project** (§7.3) | "I have several projects I like to keep running… music." Observation and production are different jobs. |
| 7 | — | **Triage states** Inbox / Later / Archive | Named as load-bearing. |
| 8 | `publishedAt ?? savedAt`, sort toggle | **Published date is the default axis and is user-editable** | The 연대기 dies if the timeline is really a save-order list. Enrichment gets dates wrong; editing is not cosmetic. |
| 9 | Vercel serverless + Claude for enrichment | **Direct API call from the app**, key in app settings | No server in a desktop app. |

**Unchanged from v1:** paste-a-URL as the only capture path; scoped search; the Related panel (keyword overlap in v1, semantic later); hashtags; Tags page and Tag pages; the Inspiration page; the seungjohan.com editorial-minimal design system; JSON export.

**Explicitly still out:** browser extension, newsletter address, RSS/Feed, mobile, Readwise API import. v1 ingest is **paste a URL, and nothing else**.

---

## 1. Overview

**Elevator pitch.** Paste any media URL — article, PDF, video, track, podcast. Constellate enriches it, files it under a subject, and lists it **by the date it was published**. Read a subject forward through time to see how it actually moved, then ask it for a **Trend Read**: a dated, saved statement of where it's heading and what would prove it wrong. Separately, **Projects** collect references for the things you make.

**The core thesis — two directions of time.** The same archive does two jobs, and both fail in Readwise for the same reason:

- **Subjects look backward to infer forward.** Archive everything on AI in published order, scroll from 2016 to now, and the *shape* of the movement becomes visible — that shape is the basis for guessing the next step. Readwise orders by **save date**, which destroys this: a 2016 article saved today sits at the top, next to yesterday's news.
- **Projects look outward to gather material for something you'll make.** Composing works by collecting many references and bending them into your own — so the references need to be *findable by why you saved them*, not by when. Readwise has no notion of *why* a thing was saved.

**What holds them together:** every item carries **your interpretation** — a note, a highlight, a reason. That is what gets retrieved later, not the artifact. Subjects and Projects are two views over one archive of interpreted media.

**Strategic context.** Capture is commoditized. Reading is commoditized. What nobody sells is **an archive whose primary axis is when things happened, and which will tell you what it thinks comes next — and remember that it told you.**

---

## 2. Goals & Principles

**v1 goals — five, in priority order:**
1. **Capture anything** — paste a URL of any supported type, near-zero effort, correct published date.
2. **Read a subject as a chronology** — published-date ordering as the default and defining view.
3. **Read and highlight text in-app** — articles and PDFs, with highlights that leave the app as markdown.
4. **Trend Read** — an explicit, dated, saved inference about a subject's direction (§7.2).
5. **Projects** — reference collections that serve making things, music first (§7.3).

**Principles:**
- **Published date is sacred.** Every design decision that would degrade the published-date axis loses. It is the product.
- **A prediction that isn't written down and dated isn't a prediction.** Trend Reads are saved artifacts on the same timeline as their evidence, so they can be checked later.
- **Your interpretation outranks the LLM's.** Every enriched field is editable. The note is yours.
- **One user, no configuration.** No saved-view builders, no settings panes for things one person decides once. Cut it.
- **Calm and print-like.** Inherit the seungjohan.com editorial minimalism from v4. No AI-slop gradients, no drop shadows.

---

## 3. User

**Sole user — the owner.** A PM/builder who follows several subjects seriously (AI/tech, economy), composes music as a hobby, and runs a handful of side projects. Saves constantly across formats. Currently splits this across Readwise Reader (reading), a hand-maintained markdown table in `wiki/research/music/composing/references.md` (music references), and browser bookmarks.

**The behaviour that proves it works:** he stops maintaining the markdown table by hand, and he goes back to a subject's timeline *on purpose* to think about what's next.

No secondary personas in v1. Multi-user is Phase 3 and shapes nothing here.

---

## 4. User Stories

**Capture**
- As the archivist, I paste a URL of any type and get a correct, editable card, so capturing is one gesture.
- As the archivist, I fix a wrong published date in one click, because the date is what the timeline is built on.
- As the archivist, I save a YouTube video or a Spotify track with a note about *why*, without the app trying to play it.

**Read chronologically (the core)**
- As the reader, I open a subject and see items grouped by the year and month they were published — not when I saved them.
- As the reader, I flip oldest-first to read a subject's story forward from its beginning.
- As the reader, I see at a glance which periods were dense and which were quiet, so acceleration is visible.

**Trend (the core)**
- As the analyst, I ask for a Trend Read on a subject and a date range, and get: what changed, the direction, what must hold, what would break it.
- As the analyst, that Read is **saved into the subject, dated today**, so six months later I find it sitting on the timeline next to what actually happened.
- As the analyst, I can tell at a glance which items on a timeline are evidence and which are my own past reads.

**Read & highlight**
- As the reader, I read an article or PDF in a clean column and highlight as I go.
- As the reader, my highlights and notes collect in a Notebook tab per item.
- As the owner, my highlights land in curiosity-lab as markdown, so they join the rest of my thinking.

**Projects**
- As the composer, I collect references for a piece — video, track, article — into a project, each with a note on *why* (the instrument, the beat, the idea).
- As the composer, I browse a project as a board of references, not a timeline, because chronology is irrelevant to a reference pile.
- As the builder, I spin up a new project space whenever I start something, without ceremony.

**Connect & retrieve**
- As the connector, each item shows related items within and across subjects, with cross-subject links highlighted.
- As the searcher, I search with a scope (overall / title / hashtag / description / date range) and find anything instantly.

---

## 5. Features & Functionality (v1)

Ranked by service to the core. Everything Readwise does that isn't here is in §16 with the reason.

### 5.1 Capture
- **Paste a URL** — single input, global shortcut. The primary ingest path.
- **Drop a local file** — drag-and-drop or file picker, for **PDF** at minimum (plus audio and image, which Projects need). *Added in v1.2: the owner named "articles, URL, PDF, or whatever" and §11 gates release on PDF capture, but most PDFs he holds are files on disk, not URLs. URL-only ingest made that release criterion unsatisfiable.*
- **Type detection** → `article` · `pdf` · `video` · `track` · `podcast` · `note` · `page` (fallback).
- **A note with no source** — `type: note`, no URL required. An idea, a fragment, something that struck him. See §5.5 on why this exists.
- **Enrichment** — title, source/channel/artist, **author**, **published date**, summary, keywords, cover image.
- **Editable enriched card** before save: every field, plus subject picker, hashtags, note.
- **Every field stays editable after save**, in the Info tab (§5.7). There is no separate "edit metadata" dialog.
- **Published-date correction** — inline, one click, always available. First-class, not buried in a dialog.
- **Duplicate detection** — re-adding a known URL surfaces the existing item.
- **Full text stored** for `article` and `pdf` (enables reader mode + search over bodies).

### 5.2 Organize
- **Tags** — **a first-class organising axis, not a decoration.** The owner names tags and time as his two axes: *"I wanna collect inspirations or medias that I wanna archive **by tag and by time order**."* So: a tag filter on every list, a Tags page (chip cloud + counts), and a Tag page per tag — a date-ordered feed of everything carrying it, across all subjects. **A Tag page is a timeline in its own right**, which means a tag is a valid way to read a chronology without a subject existing at all.
- **Subjects** — sidebar containers; create/rename/reorder/colour. An item has **at most one**; `subjectId` is nullable and unfiled items live in **Unfiled**. Requiring a subject at capture would tax the one gesture that has to stay frictionless.
- **Projects** — a second sidebar group; an item can belong to many (§7.3).
- **Triage** — Inbox / Later / Archive tabs on any list, with per-row hover actions.
- **Type filter chip** — narrow any list to articles / videos / tracks / PDFs / podcasts / notes. This is where "beyond text" lives.
- **Delete** — from any list row or the detail panel, with a single-level undo toast (~10s) before the row goes. Cascades to that item's `highlight`, `timestamp` and `item_project` rows. *This is what §16's "Trash — delete with undo is enough" was assuming; it was never actually specified.*

### 5.3 Read (chronology — the core)
- **Timeline view** — the default for a subject. Grouped by published **year**, then month. Oldest ↔ newest toggle.
- **Density strip** — a thin bar per period showing item count. Acceleration made visible, no LLM required.
- **Reading mode** — clean serif column, `Aa` typography control, document outline in the left rail, for `article` and `pdf`.
- **Highlighting** — select → highlight; highlights render with a left border + tint; each can carry a note.
- **Notebook tab** — all highlights and notes for the open item, with a count badge.
- **Media items** — no reader. A reference card: cover, source/artist, duration, published date, your note, hand-typed timestamps, "Open original."

### 5.4 Trend (the core) — §7.2
- **Trend Read** — pick subject + date range → a dated, saved, four-section inference.
- **Reads live on the timeline** they analyse, visually distinct from evidence.

### 5.5 Connect
- **Related panel** — Same subject / **Other subjects** (highlighted amber, 의외의 연결성), each row showing the shared key(s). Keyword + hashtag overlap in v1; engine swappable later. **Read §7.4 before building on this — the owner has already concluded this engine finds the wrong kind of connection.**
- **Inspiration page** — the push surface: surfaced cross-subject connections, plus recent Trend Reads.

> **⚠ "Inspiration" means two different things and this PRD only builds one of them.**
> In the owner's four opening words — *music · inspiration · basic idea of chronicle · archiving with tags* — "inspiration" is **a kind of thing he saves**, not a page. `wiki/research/inspiration.md` is a hand-kept table of exactly that: *"A running shelf of media (videos, articles, URLs) that sparked something — captured with enough metadata to find and reuse later, before the spark fades,"* with columns `Date Added · Title · Subject · Media · Source/Channel · URL · Notes / Why it caught me`.
> Chronicle v4's sidebar **Inspiration** is something else entirely — a results surface where the engine pushes connections *to* him.
> Same word, two meanings. The saved-item reading is served by `type: note` (§5.1) plus the note field; the page keeps its v4 name. **Open question in §14: should the page be renamed to free the word?**

### 5.6 Retrieve
- **Scoped search** — Overall / Title / Hashtag / Description / Date range. Scoped to current space or everything. Searches article bodies too.

### 5.7 Foundation
- **Right panel, tabbed:** **Related** (default) · **Info** · **Notebook**. The panel persists across browse and read mode.
  - **Info** — the item's metadata *and the only post-save edit surface*: type · source/channel/artist · author · **published date** (inline `PublishedDateEditor`) · saved date · subject · hashtags · duration (media only) · enrichment status (`full|partial|failed`) · **a visible flag when the timeline fell back to `savedAt`** · Open original. Every field edits inline; there is no "Edit metadata" dialog.
  - **Notebook** — the **note** at the top (placeholder "Add a personal note…", always editable), then the item's highlights beneath it, with a count badge on the tab. *The note is the field §1 calls the whole point of the archive; when the panel became tabbed it lost its home, and this is it.*
- **Home** — the all-subjects view: every item across every subject, triage tabs and scope chips as elsewhere, grouped by published date. The only cross-subject list, and Constellate's answer to Readwise's "Recently added".
- **Settings** — one minimal pane, not a sidebar section: model API key (OS keychain), the markdown-export destination inside curiosity-lab, JSON export/import. Nothing else. *§2's "no settings panes" principle means no **view-configuration** panes; the key has to live somewhere.*
- **Markdown export** — highlights and notes written into curiosity-lab as notes.
- **JSON export/import** — full-archive durability.

---

## 6. Design & Layout

### 6.1 Design system
Inherit **Chronicle v4** unchanged — the seungjohan.com editorial minimalism, its palette, type scale, and the `ENTRY` / `SLIDE` / `FADE` motion patterns. v4's design documentation carries a *"what this design is not"* constraints list; adding reading mode must not violate it.

**One colour rule survives from v4 and must not be diluted:** the amber used for cross-subject connections is load-bearing. It marks the surprise. It is not decoration and must not be reused elsewhere.

**Consequence for reading mode:** the highlight mark introduced in §5.3 — tinted background plus coloured left border — **must not be amber.** Highlights take a neutral secondary token. Amber appears only on cross-subject Related rows and on the Inspiration page. This is the one inviolable rule in the design, and reading mode is exactly where it would break by accident.

### 6.2 One shell, two modes

| | Left rail | Centre | Right panel |
|---|---|---|---|
| **Browse** | Home · Subjects · Projects · Tags · Inspiration · **+ Add URL** | Triage tabs → search + scope chips → date-grouped list (+ density strip) | Related · Info · Notebook |
| **Read** | Document outline (TOC) | The article: serif column, `Aa`, reading progress hairline | *unchanged — same panel* |

Clicking an item enters Read mode; `Esc` returns. The right panel persists across both — that continuity is what makes Related feel like part of reading rather than a separate feature.

### 6.3 Four axes, four homes
Resolved so they stop competing for the sidebar:
- **Time** (published date) → **the grouping of every list.** The default and the product.
- **Tag** → **a filter on every list**, plus the Tags page and per-tag Tag pages. Co-equal with time, per the owner's own phrasing ("by tag and by time order") — *v1.1 omitted this axis entirely and put Type in its place.*
- **Container** (Subject / Project) → **sidebar sections**
- **State** (Inbox/Later/Archive) → **tabs on the list**
- **Type** (article/video/track/pdf/podcast/note) → **filter chip above the list**

### 6.4 Component inventory (delta on v4)
v4 already has: `AppShell`, `Sidebar`, `SearchBar` + `ScopeChips`, `ItemCard`, `ItemList`, `DateDivider`, `HashtagChip`, `CategoryBadge`, `AddUrlModal` → `EnrichedCardEditor`, `ItemDetail`, `RelatedPanel` + `RelatedRow`, `TagsOverview`, `TagPage`, `InspirationPage`, `ConnectionCard`, `TrendCard`, `EmptyState`, `EnrichingState`, `PartialEnrichmentBanner`.

**New for v2:**
`TriageTabs` · `TypeFilterChip` · `DensityStrip` · `ReaderView` (serif column + `Aa` + progress hairline) · `DocumentOutline` · `Highlight` (rendered mark) · `HighlightPopover` · `NotebookPanel` · `RightPanelTabs` · `MediaReferenceCard` (cover, artist/channel, duration, timestamps, Open original) · `TimestampRow` · `ProjectBoard` + `ProjectCard` · `TrendReadModal` (subject + range picker) · `TrendReadItem` (a Read rendered on the timeline) · `PublishedDateEditor` · `InfoPanel` (the Info tab's body) · `UndoToast` · `SettingsPane` · `TagFilter` · `FileDropZone` · `CausalCardEditor` (§7.4, if Kind-2 is taken up).

### 6.5 States & microcopy (delta)
- **Empty subject:** "Nothing here yet — paste a URL to start this timeline."
- **Empty project:** "No references yet. Add the first thing that inspired this."
- **Enriching:** "Reading the page…"
- **Partial enrichment:** "Couldn't fully read this page — check the title and the date."
- **Missing published date:** "No date found — set one, or this item won't sit correctly on the timeline."
- **Media item, read mode attempted:** *(there is no read mode)* → "Open original"
- **Trend Read running:** "Reading 34 items, 2016 → 2026…"
- **Too few items for a Read:** "Only {n} items in this range — a Trend Read needs at least 8."
- **No related items:** "No connections yet. Add more and they'll start linking."

---

## 7. The Three Engines

### 7.1 Linking (inherited from v1, unchanged)
Two-layer keywords: `keywords` free-form for display; `matchKeys` normalized (lowercase → de-pluralize → alias map) so "AI" / "artificial intelligence" / "A.I." match. Score by shared-key count (hashtags weighted higher) × **cross-subject boost**, recency tiebreak, capped per group, computed on demand. Honest limit: this finds relations that *share vocabulary*. Word-independent surprise needs embeddings — Phase 2, same panel.

### 7.2 Trend Read — the differentiator

Chronicle v1 deferred foresight and admitted it "needs a real method, not just a prompt." This is the method, and its value is structural rather than clever.

**Mechanism**
1. Pick a **subject** and a **date range**.
2. The app assembles those items' **summaries in published order** (summaries, not full bodies — bounded cost).
3. One model call returns four fixed sections:
   - **What changed** — the movement across the period, in order.
   - **The direction** — where the vector points now.
   - **What must be true** for it to continue.
   - **What would break it** — the falsifier.
4. The result is **saved as an item in that subject**, dated **today**, typed `trend_read`, tagged `#trend-read`.

**Why saving it is the whole point.** A Read is dated and sits on the same timeline as its evidence. Six months later, scrolling that subject, you pass your own past prediction on the way to what actually happened. Foresight becomes **checkable** instead of a feeling. No read-later tool does this, and it costs one model call plus a row.

**Deliberate constraints**
- Never automatic. A Read is always an explicit act, so it stays a considered judgement.
- **Refuses to run on fewer than 8 items** in the selected range. A trend over three articles is noise.
- The four sections are fixed. The falsifier is mandatory: a prediction with no way to be wrong isn't one.
- Rendered visually distinct on the timeline. Evidence and inference must never blur.

### 7.3 Subjects vs Projects — two containers, one archive

**Confirmed by the owner** (v1.1 wrongly flagged this as the author's invention): *"I have several projects I like to keep running. Uh, the first one is music… I'm going to also categorize or save archive resources based on the projects I will run."* The two-container split below is still the author's structuring of that statement.

They are the same primitive with different defaults, because building two systems for one user doubles the work:

| | **Subject** | **Project** |
|---|---|---|
| Purpose | Observe how something moves | Gather material for something you make |
| Default view | **Timeline** (published date) | **Board** (grid, grouped by tag) — *toggleable to Timeline* |
| Sort | Published date | Published date, or date-added, or manual |
| Trend Read | Yes | No |
| Membership | An item has **at most one** | An item can be in **many** |
| Lifecycle | Long-lived | `active` → `archived`; the sidebar shows active, past projects collapse |
| Example | AI · Economy | Music composing · a side project |

An item's **home is a subject** (or Unfiled); it can be *pulled into* any number of projects. This mirrors how curiosity-lab already works — a note lives in one folder and links to many things — and it means a reference can be both evidence of a trend and material for a piece, without duplication.

**A project is not sorted by save order.** v1.1 gave projects date-added sort and no timeline, which is precisely the failure this PRD condemns Readwise for. The owner's phrase — *"archive **by tag and by time order**"* — was about his inspirations, which live in projects. Board is the default because a reference pile is usually browsed rather than read forward, but the timeline is one click away.

**Projects are created continuously.** *"I will keep updating projects which I am going to run."* So the container needs an `archived` state, or the sidebar only ever grows.

**The music project, concretely.** [`wiki/research/music/composing/references.md`](../../research/music/composing/references.md) is this feature, maintained by hand. Its hand-chosen columns are the spec:

| His column | Field |
|---|---|
| Media Title | `title` |
| **About** | **`note`** — his own words on why it matters |
| Media | `type` |
| Channel Name | `source` |
| URL | `url` |

The one thing the table can't do is capture *why* in a structured, filterable way — "because of the instrument," "because of the beat." v1 handles that with **hashtags + note**. A per-project facet vocabulary (`instrument:` / `beat:` / `mood:`) is in §16 — worth building only after the freeform tags prove insufficient.

**The workflow ends in using, not collecting.** *"The core part of the music composing is to collect lot of references and **use it or customize it or change it into my way**."* Collecting is the means; making the piece is the end. v1 marks the end of that arc minimally: `item_project` carries **`usedAt`** and **`usedNote`** ("took the drum pattern, halved the tempo"), and a project board filters **Used / Unused**. That is the smallest thing that closes the loop — a reference pile you never mark up is indistinguishable from a pile you never used. Anything richer (linking a reference to the finished piece, an output register) is §16.

### 7.4 ⚠ The Related panel finds the wrong kind of connection

**This is the most serious open problem in the spec, and the owner already diagnosed it himself.**

[`wiki/research/system/two-kinds-of-connection.md`](../../research/system/two-kinds-of-connection.md), written 2026-08-06, splits "unexpected connection" in two:

| | **Kind 1 — analogy** | **Kind 2 — hidden shared variable** |
|---|---|---|
| The link is | the same abstract *shape* | both wired to the same *third thing* |
| The two things are | alike underneath | often totally unalike, even opposite |
| You find it by | going **up** — abstract until they meet | going **sideways** — into what each one touches |
| Example | Michelin filter ≈ music discovery | Nike ⇄ Nintendo (both hang on free time) |

His verdict: *"The connections that actually excite me (Nike vs Nintendo, Covid → travel/dining) are **not** the kind the engine finds… **The engine is structurally blind to Kind 2.** We've been perfecting the half that finds analogies while the connections that thrill me are mostly the other half."*

**This lands directly on §7.1 and §5.5.** Keyword overlap is a similarity measure. Embeddings — the "Phase 2 upgrade" — are *also* a similarity measure. So the roadmap's headline improvement is a better version of the half he already ruled out. Nike and Nintendo share no vocabulary and no embedding neighbourhood; no amount of semantic upgrading will ever surface that pair.

**His sketched fix — the shadow method.** Don't compare two items. Give each a **causal card**: `{consumes, depends_on, produces, competes_with, threatened_by}`. Nike `depends_on → free time spent outdoors`; Nintendo `consumes → free time`. They never look alike, but their cards **collide on "free time" with opposite signs**, and that collision *is* the connection. Three sub-types: **substitutes** (compete for a resource, opposite sign), **complements** (rise together, same sign), **common-cause** (one upstream node, many effects — Covid).

**Why this belongs in this PRD rather than a research note.** The causal card is the same substrate the Trend Read needs. §7.2 asks what drives a subject and what would break it; a card that already names what each item consumes, depends on and threatens is exactly the input for that. Kind-2 linking and foresight are one feature wearing two hats, and building either one alone pays for the other.

**Status: not scheduled.** v1 ships the Kind-1 panel because it already works (§10.1) — but §5.5 must not be described as the moat while it finds only the obvious half. See §14 for the decision this needs.

---

## 8. Data Model

SQLite. `userId` retained for a possible multi-user future; it costs nothing now.

**`item`** — `id`, `url`, `canonicalUrl` (dedup), `type` (`article|pdf|video|track|podcast|page|trend_read`), `title`, `source`, `author`, `summary`, `body` (nullable — text types only), `coverUrl`, `keywords[]`, `matchKeys[]`, `hashtags[]`, `subjectId`, `publishedAt` (nullable, **user-editable**), `savedAt`, `state` (`inbox|later|archive`), `note`, `enrichment` (`full|partial|failed`), `durationSec` (media), `embedding` (nullable — Phase 2, additive).

**`space`** — `id`, `name`, `kind` (`subject|project`), `color`, `order`, `createdAt`, `brief` (nullable — a project's own description).

**`item_project`** — `itemId`, `projectId`, `addedAt`. Many-to-many; subjects use `item.subjectId` instead.

**`highlight`** — `id`, `itemId`, `text`, `startOffset`, `endOffset`, `note`, `createdAt`, `exportedAt` (nullable — drives incremental markdown export).

**`timestamp`** — `id`, `itemId`, `positionSec`, `label`, `note`, `createdAt`. Hand-typed media markers.

**`trend_read`** — stored as an `item` with `type = trend_read`, its four sections in `body`, `subjectId` set, `publishedAt = today`. **No separate table** — this is what puts Reads on the same timeline as their evidence.

**Time axis:** `publishedAt ?? savedAt`, with a visible flag when it fell back, so the timeline never lies silently.

**`alias`** — `alias` (PK), `canonical`. **Omitted from v1.1 and load-bearing:** §7.1's match-key derivation, the shipped `matchKeys.ts`, and the JSON backup all depend on it. Grown from enrichment proposals; a write triggers a `matchKeys` rebuild across all items. The JSON export must round-trip it or every learned alias is lost on import.

**Search:** SQLite FTS5 over `title`, `summary`, `source`, `author`, `body`, `note`, `hashtags`. *`source` was dropped in v1.1 — the shipped search indexes it, so porting v1.1 literally would have been a search regression.* Scope mapping: Overall = title+summary+source+author+hashtags · Title = title · Description = summary+body · Hashtag = hashtags.

**Duplicate detection and Trend Reads.** `canonicalUrl` is the global dedup key, but a Trend Read has no URL — so every Read would collide with every other and import would silently keep only the first. Rule: `url`/`canonicalUrl` are **nullable**, and dedup **excludes `type IN ('trend_read','note')`**. The M2 unique index and the M6 writer must both honour this, and §11 gates on an archive with ≥2 Reads round-tripping.

**Backup format.** `ArchiveBackup` goes to `version: 2` — `categories` → `spaces`, `categoryId` → `subjectId`, plus `alias`, `item_project`, `highlight`, `timestamp`. The importer must accept v1 files and map them forward, or the existing archive is stranded.

**Links are computed, never stored.**

---

## 9. Non-Functional Requirements

- **Local-first.** No server, no account, no network except enrichment and Trend Reads.
- **Durability.** JSON export/import; SQLite file is user-visible and backup-able.
- **Performance.** Reads, search, and linking are local and personal-scale — target instant (<100ms). FTS5 handles bodies.
- **Key handling.** The model API key lives in app settings (OS keychain), never in the repo.
- **Privacy.** Enrichment sends page text to a model provider. Acceptable for personal use; note it.
- **Offline.** Everything already saved is fully readable offline. Capture and Trend Reads need connectivity.

---

## 10. Assumptions, Dependencies & Constraints

**Assumptions:** most pages expose enough metadata to enrich; personal scale (hundreds–low thousands of items); one user; media platforms keep working oEmbed/metadata endpoints.

**Dependencies:** a model API for enrichment and Trend Reads; a readability/extraction library for article bodies; a PDF text extractor.

**Constraints:**
- **⚠ No working generation quota today — but the code path already exists.** [`TODOS.md`](../../../TODOS.md) records that the vault's `GEMINI_API_KEY` has `generate_content_free_tier_requests, limit: 0`; embeddings work, generation does not. The shipped v1 already abstracts this: `api/_core/llm.ts` defines `Provider = 'anthropic' | 'gemini'`, picks whichever key is present, and defaults Anthropic to `claude-haiku-4-5-20251001`. **So M0 is not "build provider support" — it is: add an `ANTHROPIC_API_KEY` and make one real call**, since that branch has only ever run against a mocked `fetch`.
- Desktop-only. Anything found on a phone must survive until you're at the Mac (see §14).
- Paste-a-URL is the only ingest. No extension, no RSS, no email.

**Stack — chosen by the owner, and proven at M1.** **Tauri v2** (Rust core, system webview) wrapping the existing React 18 + TypeScript + Tailwind v4 front end; chosen over Electron for size, memory and first-party SQLite. SQLite via `tauri-plugin-sql` with FTS5. Enrichment stays on the existing provider abstraction: a small fast model per item, a stronger one for Trend Reads, which are rare and matter more. *Electron remains only a contingency if a Tauri blocker appears — M1 found none.*

### 10.1 Inherited codebase — this is a port, not a greenfield build

**`~/Cursor/chronicle/` was the shipped v1.** Its `roadmap.md` reads *"v1 shipped — capture, categories, chronological reading, scoped search."* Vite + React 18 + TypeScript + Tailwind v4, Dexie/IndexedDB, FlexSearch, react-router 7, `motion`, `lucide-react`, `@anthropic-ai/sdk`, `vite-plugin-pwa`. It was never a git repository.

**The codebase of record is now `~/Cursor/Constellate`** — a git repo holding that source plus the M0 test net and the M1 Tauri shell. Treat `~/Cursor/chronicle/` as read-only reference.

**Carries over close to unchanged:**
- `src/lib/matchKeys.ts`, `linking.ts`, `search.ts`, `url.ts`, `format.ts` — pure functions over plain data. The §7.1 linking engine is *already built*.
- `api/_core/` — `extract.ts`, `enrich.ts`, `llm.ts`, `types.ts`. The enrichment **logic** carries over. Its **transport does not**: it is a Vercel function reachable only through the Vite `devApi()` plugin, so it does not exist in a packaged Tauri app. Must be rehosted as a Tauri command — see M3a.
- The component layer (`AddUrlModal`, `ItemCard`, `ItemDetail`, `SearchBar`, `Sidebar`, `HashtagEditor`, `atoms`), the page layer (`FeedPage`, `TagPage`, `TagsOverviewPage`, `InspirationPage`), `motion.ts`, and `src/styles/` design tokens.
- `SEED_CATEGORIES` / `SEED_ITEMS` in `db.ts` — the seed content from §6.6 of the **superseded** `Chronicle_prd.md`, already coded.

**The data model is already 80% of §8.** `src/lib/types.ts` `Item` matches field-for-field on `id`, `userId`, `url`, `canonicalUrl`, `title`, `source`, `summary`, `keywords`, `matchKeys`, `hashtags`, `categoryId`, `publishedAt`, `savedAt`, `enrichment`, `note`, `embedding?`. v2 adds `type`, `body`, `coverUrl`, `author`, `state`, `durationSec`; renames `Category` → `Space` (+ `kind`, `brief`, `state`); and adds tables `alias`, `item_project`, `highlight`, `timestamp`. **Additive except one rename that is not:** `item.categoryId` → `subjectId` touches `linking.ts`, `db.ts`, `search.ts`, `ArchiveContext.tsx`, `FeedPage.tsx` and the routes, and breaks the v1 JSON backup format that §11 requires to round-trip — hence `ArchiveBackup version: 2` in §8.

**Must be replaced:** `src/lib/db.ts` — Dexie/IndexedDB → SQLite + FTS5. The only genuinely invasive change. Its Dexie index declarations map onto SQLite indexes directly; the query call-sites are the work.

**Debt that transfers (from `roadmap.md`), ordered by how much it will hurt here:**
1. **~~No automated tests anywhere.~~ Closed by M0.** 75 tests now cover `matchKeys`, `linking`, `search`, `url`, the db import/export round trip and provider selection — mutation-verified 12/12. What remains untested is the **UI layer and the enrichment chain**. The standing rule: run `npm test` after every step of the storage port.
2. **The Anthropic path is stub-verified only.** See M0.
3. **The search index rebuilds on every archive change** (`ArchiveContext.tsx`). Tolerable at hundreds of items; v2 makes it worse by adding full article `body` to the index. This graduates from "later" to "fix during the SQLite port," where FTS5 makes it incremental for free.
4. **Multi-word match keys** — "AI policy" normalises to the dead key `ai policy`. Degrades the Related panel.
5. **Enrichment fails on JS-rendered and paywalled pages.** Unresolved in v1, inherited whole; worse in v2 because `body` is now stored and read.
6. **Connection scoring is unranked and quadratic.** Generic keys like `ai` dominate every Related panel, and `getAllConnections()` scans all pairs. v1's own roadmap Stage A — IDF rarity weighting, a stop-key threshold, time-span bonus, per-key cap — is a **prerequisite for §5.5 being useful at all**, not a later nicety. §12 lists the Related panel as "already built"; it is built but not yet good.
7. No accessibility pass; bundle ~490 KB (159 KB gzipped).

**One inherited question, now answered.** v1's debt list asks whether "duplicate detection is global, so filing one page under two subjects is impossible by design" is wanted. **It is.** §7.3 gives an item exactly one subject and many projects — global dedup is correct and stays.

---

## 11. Release Criteria

Ship when all are true:
- Paste → enrich → save works for **each type**: article, PDF, video, track, podcast.
- Published date is correct or correctable in one click; the timeline groups by it.
- A subject reads as a chronology, oldest↔newest, with the density strip.
- Reading mode renders articles and PDFs; highlighting works; highlights appear in Notebook.
- Highlights export to curiosity-lab as markdown without duplicating on re-export.
- A Trend Read produces four sections and is saved as a dated item in its subject.
- A project holds references, displays as a board, and an item can sit in a subject and a project at once.
- Scoped search returns correct results across all five scopes, including article bodies.
- Related panel shows correct Same-subject / Other-subject rows with shared keys.
- JSON export → import round-trips with no loss.

---

## 12. Build Plan

Thin vertical slices; each usable alone.

| # | Milestone | Status | Delivers | Depends on |
|---|---|---|---|---|
| **M-1** | **Figma prototype** | ⬜ **next** | Extend Chronicle v4 with the two-mode shell, reader, Notebook, Info tab, density strip, tag filter. Design sign-off gates M4–M9. | — |
| **M0a** | Test net | ✅ **done** | 75 tests over the pure-function engines, mutation-verified 12/12. Commit `af07419`. | — |
| **M0b** | One live Anthropic call | ⛔ **blocked** | Closes the stub-verified gap. Needs `ANTHROPIC_API_KEY`. | a key |
| **M1** | Tauri shell | ✅ **done** | Tauri v2 wrapping the existing app as a Mac desktop app, still on Dexie. Commit `c972250`. | M0a |
| **M2** | **Storage port** | ⬜ | `db.ts` → SQLite + FTS5; `Category` → `Space`; `categoryId` → `subjectId`; new `alias` / `item_project` / `highlight` / `timestamp` tables; `ArchiveBackup v2` with a v1 importer. Search becomes incremental. | M0a, M1 |
| **M3** | Types + capture | ⬜ | `type` detection; **local-file drop for PDF**; `body` storage; cover art; media reference card; **published-date editor**; Info tab. | M2 |
| **M3a** | **Enrichment transport** | ⬜ | Move `extract`+`enrich`+`llm` out of the Vite `devApi()` plugin into a Tauri command; key from the OS keychain; `enrichClient` switches `fetch('/api/enrich')` → `invoke()`. **Without this a packaged app cannot capture at all.** | M1 |
| **M4** | Subjects + timeline | ⬜ | Published-date grouping (year → month), oldest↔newest, density strip, tag filter on every list. | M2, M-1 |
| **M5** | Reading + highlights | ⬜ | Reader view, `Aa`, document outline, highlighting, Notebook tab + note. **The largest genuinely new build.** | M3, M-1 |
| **M6** | **Trend Read** | ⬜ | Range picker, four-section generation, ≥8-item gate, saved as a dated item on the timeline. | M4, M0b |
| **M7** | Triage + type filter | ⬜ | Inbox / Later / Archive tabs, type filter chip, delete + undo. | M4 |
| **M8** | Projects | ⬜ | Project spaces, board ↔ timeline toggle, many-to-many, `usedAt`/`usedNote`, archived state. | M2, M4 |
| **M9** | Outflow + durability | ⬜ | Markdown export into the vault, JSON export/import, Settings pane, all empty/error states. | M5 |
| **—** | *Already built* | ✅ | Enrichment **logic** · scoped search · hashtags / Tags page / Tag page · Related panel (§7.1, but see debt #6) · Inspiration page · JSON backup · seed content · design tokens. Port, don't rebuild. | — |

**Order notes.**
- **M-1 first.** The owner's stated sequence is prototype, then build. M2/M3a are plumbing and can run alongside it; M4–M9 wait on design sign-off.
- ~~M0 first, without exception.~~ **Done.** The test net exists and mutation-verified; the rule it enforced now reads: run `npm test` after every step of M2.
- **M3a is not optional.** §0 row 9 decided enrichment is a direct call from the app, but the inherited chain only runs behind the dev server. Until M3a ships, a packaged build has no capture.
- **M6 before M7/M8.** Trend is the stated core. If the build stalls after M6, what exists is still the product that justifies existing.
- Against the **superseded v1 plan** (`Chronicle_prd.md` §12), roughly **M1–M4 plus the JSON-export half of M5 are done**: capture, enrichment, categories, chronological reading, scoped search and the linking engine all work today.

---

## 13. Success Metrics

One user — measure usefulness, not scale.
- **The table dies.** `music/composing/references.md` stops being updated by hand because the app is better.
- **The timeline gets used on purpose.** You open a subject chronologically to think, not just to retrieve.
- **A Trend Read gets checked.** At least once, you scroll back to a past Read and compare it to what happened. This is the metric that proves the core idea.
- **Capture is thoughtless.** Pasting a URL never feels like a chore.
- **Dates are right.** You rarely need to correct a published date.
- **Behaviour change.** You reach for this instead of Readwise.

---

## 14. Risks & Open Questions

**Risks**
- **⚠ Foresight can become horoscope.** Four confident-sounding sections about the future are easy to generate and easy to over-trust. The mandatory falsifier and the dated saving are the guardrails; if Reads start reading as generic, the feature has failed and should be cut rather than tuned.
- **Published-date detection is load-bearing and unreliable.** Many pages don't expose a date; some lie. The whole product rests on this field. Mitigation: the date editor is first-class and a fallback is always visibly flagged.
- **Two containers may be one too many.** If projects go unused after a month, collapse them into tagged subjects.
- **Desktop-only breaks the phone half of the habit** — see below.
- **⚠ The Related panel finds the wrong kind of connection.** §7.4. The panel is sold as the moat but is structurally blind to the Kind-2 links the owner says are the ones that excite him — and the planned semantic upgrade does not fix it. **The largest unresolved problem in this spec.**
- **Porting code whose UI layer is untested.** The engines are covered (75 tests, M0a); the components, the enrichment chain and the Tauri boundary are not. M2 rewrites storage beneath them.
- **A packaged build cannot capture until M3a.** The enrichment endpoint only exists behind the dev server.
- **The search index rebuild gets worse before it gets better.** v1 rebuilds the whole FlexSearch index on every archive change; v2 adds full article bodies to it. Must be fixed *during* the SQLite port (FTS5 makes it incremental), not deferred.
- **Scope.** This is Readwise + Chronicle + a trend engine, solo. §12's ordering is the defence: stop after M6 and you still have the thing worth having.

**Open questions — need your answers**
1. **⚠ Kind-2 connection (§7.4) — the big one.** Three options: (a) ship the Kind-1 panel in v1 and schedule the causal card for the next release; (b) build a minimal causal card *now*, since the Trend Read needs the same substrate anyway; (c) accept that Kind-1 is all this product does and stop calling the Related panel the moat. **This decides whether §5.5 is the differentiator or a commodity feature.**
2. **Phone capture.** Desktop-only means anything found on a phone must wait. Keep Readwise as the phone inbox and paste in later, mail links to yourself, or accept the gap for v1?
3. **Which projects, besides music?** You said "several projects I keep running" but named only music. Two or three more would confirm Project-as-container rather than tags.
4. **Music facets.** Are `instrument` / `beat` / `mood` worth structuring in v1, or do freeform hashtags earn their keep first?
5. **Trend Read scope.** Subject-wide only, or also across subjects ("what do AI and Economy jointly suggest")? Cross-subject is the more interesting question and the harder one. *Note: a cross-subject Trend Read is close to Kind-2 linking — Q1 may answer this one too.*
6. **Trend Read mechanism.** The goal is yours; the four-section-plus-falsifier-saved-as-a-dated-item design is the author's (§0 row 5). Confirm before M6's ordering rests on it.
7. **Does the Inspiration page keep its name?** §5.5 — "inspiration" means a saved thing to you and a results page to v4. One of them should probably give up the word.

*Retired: naming — **decided 2026-09-04: Constellate.** See Product Details.*

---

## 15. Roadmap

*Numbered by release, not by "v" — "v2" already means this document.*

- **Release 1 (this PRD)** — capture all types · subject timelines · tags as an axis · reading + highlights · Trend Read · projects · related panel · markdown outflow. macOS, local-first.
- **Release 2 — ingest & reach.** Browser extension, mobile capture (share sheet), Feed (RSS + newsletter address) with Library-vs-Feed promotion.
- **Release 3 — connection & analysis.** The **causal card and Kind-2 linking (§7.4)**; embedding-based Kind-1 links; cross-subject trend threads; Trend Reads that cite prior Reads and score their own accuracy.
- **Release 4 — product.** Multi-user, sync, accounts. Shapes nothing before it arrives.

---

## 16. Backlog — cut, with reasons

**Cut from Readwise (seen in the screenshots, deliberately not built):**
- [ ] **Feed / RSS / newsletter address / UNSEEN-SEEN** — depends on the ingest infrastructure v1 removed. → v2.
- [ ] **Reading progress *as a queue metric*** — the ring on cards, %-complete and time-left in metadata, the "Continue reading" shelf. Serves finishing a queue, not seeing a trend, and is meaningless for media. **The in-reader scroll hairline (§6.2) stays** — that is position feedback, not a completion score. *Open: is scroll position persisted per item so a part-read article reopens where you left it? For a daily reader, probably yes; it needs a `readPosition` field if so.*
- [ ] **Smart views / Shortlist / "Manage views" / Configure** — a configuration surface for a one-person tool.
- [ ] **Text-to-speech** — large build, unrelated to the core.
- [ ] **Ghostreader-style chat over the library** — the Trend Read is the focused version of this. Revisit only if Reads prove valuable.
- [ ] **Books / EPUB, Tweets, Emails** — add a type when you actually save one. *`note` and local-PDF drop were added to v1 (§5.1) because your own words named them.*
- [ ] **Trash (a recoverable bin)** — delete with undo is enough, and that undo is now actually specified in §5.2.
- [ ] **Keyboard-shortcut system** — beyond the basics (add URL, escape, next/prev), later.

**Deferred from Chronicle v1:**
- [ ] Semantic / embedding surprise links — **but see §7.4: these are still Kind-1.** Link-score refinement (v1 roadmap Stage A: IDF rarity weighting, stop-key threshold, time-span bonus) is a *prerequisite for §5.5 being useful*, not a deferral.
- [ ] Cross-subject common-thread analysis; connection graph; weekly digest.
- [ ] Controlled-vocabulary keywords (evolving matchKeys toward concept atoms).
- [ ] Bulk import (Raindrop / Instapaper / Zotero / Pocket).
- [ ] PWA / web build; native mobile.

**New ideas, parked:**
- [ ] **Per-project facet vocabulary** — `instrument:` / `beat:` / `mood:` for music. Only after freeform tags fail.
- [ ] **Trend Read accuracy scoring** — later Reads grade earlier ones against what happened. The natural endgame of §7.2, and the thing that would make this genuinely unusual.
- [ ] **Vault concept-atom integration** — reuse `wiki/concepts/` atoms as a shared vocabulary between app and vault. Explicitly *not* chosen for v1: you picked "beyond text" as the only direction to broaden in.
- [ ] **Daily highlight review** — the resurfacing half of the fourth Readwise pillar you named load-bearing. Deferred to Release 2 rather than cut: it needs a body of highlights to be worth anything, and there are none yet. Cheap when it lands — N random past highlights on one screen, over the existing `highlight` table.
- [ ] **Reference → output linkage** — which finished piece a reference actually fed. `usedAt`/`usedNote` in §7.3 is the v1 stub; a real output register is later.
- [ ] **`language` metadata** — one user, one set of languages. Not worth a field.

---

## 17. Changelog

| Version | Date | Changes |
|---|---|---|
| 1.3 | Sep 4, 2026 | **Named Constellate.** Product renamed from the working title; the timeline *view* keeps the name Chronicle. Historical names untouched: the shipped v1 app, the Figma file "Chronicle · Version 4", and the superseded `Chronicle_prd.md`. Build folder `~/Cursor/Constellate` → `~/Cursor/Constellate`. |
| 1.2 | Sep 4, 2026 | **Fidelity pass against the owner's own words, a five-lens audit, and the shipped state.** Added **§7.4** — the Related panel is a Kind-1 similarity engine and the owner's `two-kinds-of-connection.md` concludes Kind 2 is what actually excites him, so the planned semantic upgrade improves the wrong half; his causal-card sketch is also the Trend Read's natural substrate. Promoted **tags to a first-class axis** (§5.2, §6.3) per "by tag and by time order"; made `subjectId` nullable. Corrected §7.3 — **Projects are the owner's idea, not the author's** — and gave them a timeline toggle, published-date sort, an `archived` state, and `usedAt`/`usedNote` for the "use it or change it into my way" step. Disambiguated **"inspiration"** (a saved thing vs. v4's results page) and added `type: note` plus **local-file/PDF drop**, since URL-only ingest made §11's PDF gate unsatisfiable. Specified the previously unbuilt **Info tab, note field home, Home view, Settings pane, delete + undo**; deferred daily review explicitly. Fixed data-model bugs: missing **`alias` table**, **Trend Reads colliding on the `canonicalUrl` dedup key**, `source`/`author` dropped from FTS5, and the `categoryId` → `subjectId` rename wrongly called additive (now `ArchiveBackup v2`). Added **M-1 Figma gate** and **M3a enrichment transport** (without which a packaged app cannot capture); marked M0a/M1 done and M0b blocked. Ruled the highlight mark must not be amber. Renumbered the roadmap by release. |
| 1.1 | Sep 4, 2026 | **Rewritten as a port after finding the shipped v1 at `~/Cursor/chronicle/`.** Added §10.1 (inherited codebase: what carries over, what's replaced, the debt that transfers); rewrote §12's build plan — tests and Tauri shelling now precede the storage port, and the previous plan's M1/M2/M7 are already done; narrowed the M0 blocker (the provider abstraction and `claude-haiku-4-5` default already exist — it needs a key and one live call, not a build); resolved v1's open question on one-URL-in-two-subjects (global dedup is correct); added the untested-port and search-index risks; recorded the "Rootnote" naming lean. |
| 1.0 | Sep 4, 2026 | Supersedes v0.5. Platform → macOS desktop; storage → SQLite + markdown outflow; added reading mode + highlights; media types as first-class; **trend promoted from Phase 2 to v1 core** as the dated, saved Trend Read (§7.2); **Projects** added as a second container (§7.3); triage states; published date made editable and load-bearing; three-axis layout resolution; Readwise features ranked and cut with reasons (§16). |

## 🔗 Connections

### ⬆ Pipeline
- Source ← [[Chronicle_prd|Chronicle PRD v1]] — the v0.5 archive spec this supersedes
- Back ← [[../../ideation/Chronicle - Personal Topic Timeline|Chronicle — Idea Page]] — the researched idea
- Back ← [[../../ideation/Unified-Media-Insight-Capture-Tool|Unified Media Insight Capture Tool]] — the sibling idea; its "capture the moment of insight" is answered here by notes, highlights and hand-typed timestamps
- Source ← [[../../research/products|Products I Admire]] — the Readwise Reader row this product replaces
- Source ← [[../../research/music/composing/references|Composing: References]] — the hand-maintained table the Projects feature replaces
- Hub → [[../../index|Master Index]]

<!-- AUTO-CONCEPTS:START -->
### 🔀 Concepts (auto-generated — do not edit)
- **interpretation-over-artifact** → [[../../ideation/Chronicle - Personal Topic Timeline]] (product), [[../../ideation/Company Fit Finder - Where to Work]] (system), [[../../ideation/Finding What You Like - Rekindling Passion & Curiosity]] (system), [[../../ideation/Keep in Touch - Relationship Chronicle]] (system), [[../../ideation/Private Space - The Bedroom Moved Online]] (music), [[../../ideation/The Connection]] (system), [[../../ideation/Unified-Media-Insight-Capture-Tool]] (product), [[Chronicle_prd]] (product), [[../../research/career/Creative-Tech-Trends]] (career), [[../../research/vibecoding/karpathy-llm-wiki]] (vibecoding)
- **bridging-structural-holes** → [[../../ideation/The Connection]] (system), [[../../research/system/AI-Industry-Map-2026]] (system), [[../../research/system/connecting_the_dot]] (system), [[../../research/system/graph-theory-foundations]] (system), [[../../research/system/graphrag-connection-engine]] (system), [[../../research/system/two-kinds-of-connection]] (system)
- **high-signal-filter** → [[../../ideation/Company Fit Finder - Where to Work]] (system), [[../../ideation/Wine Value Advisor]] (system), [[../Michelin Filter]] (system), [[../Trip Guide - Shareable Restaurant Map]] (travel), [[../../research/cooking/selected-restaurants]] (cooking), [[../../research/music/music-social-media]] (music)
<!-- AUTO-CONCEPTS:END -->
