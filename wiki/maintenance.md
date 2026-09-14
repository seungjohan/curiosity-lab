---
stage: general
category: system
tag: system
type: index
---

> [!IMPORTANT] Key Takeaway
> **Why this matters:** Tracks link health and the backlog of pages implied by existing links but not yet written — so intent captured in a `[[link]]` isn't lost.
> **How to use it:** Run the scan periodically; create pages from the backlog when you actually want to write them (don't pre-create empty stubs — they add graph noise).
> **Informs:** What research/content to write next.

# 🩺 Link Maintenance & Content Backlog

Generated 2026-07-13 from a vault-wide unresolved-wikilink scan. See [[../LINKING.md|Linking Standard]].

## 🟢 Backlog — pages worth creating (implied by existing links)

**AI company profiles** — from [[research/career/Bay-Area-AI-Map]], [[research/career/USA-AI-Map]]
- Cognition-AI · Sierra · Cursor

**Cooking** — from [[research/cooking/index]], [[research/cooking/Favorite Foods]]
- Regions: south-america · indonesia · middle-east
- Dishes: Fideuá · 海鮮丼 (Kaisendon)

**Research deep-dives** — from [[ideation/research_board]] (this board *is* the to-write list)
- Music Composition & Orchestration · Graph Machine Learning · Startup Ecosystems · Triathlon & Endurance Sports · World History & Renaissance · Fine Dining Data · Language Learning

**Vibecoding workflow sub-pages** — from [[research/vibecoding/index]]
- workflow-prompting · workflow-generation · workflow-refinement · workflow-orchestration

## 🔴 Open — links to a note that was deliberately deleted

**`research/career/Finding-Dream-Services`** — 5 references, from [[ideation/Company Fit Finder - Where to Work]] (3) and [[ideation/Finding What You Like - Rekindling Passion & Curiosity]] (2), both citing it as `Seed ←`. The file was removed in commit `2ca404d` along with the ~80 company-profile notes. **Not auto-fixed:** both notes describe it as the research they were *promoted and narrowed from*, so the text is historically true and there is no surviving note to repoint to. Decide which you want — restore it from `git show 2ca404d^:wiki/research/career/Finding-Dream-Services.md`, repoint the links at [[research/career/Job-Search-Next-Step]], or rewrite the two `Seed ←` lines to name the deletion. Related: the same commit removed the "80+ hand-built company deep-dives" that [[ideation/Company Fit Finder - Where to Work]] cites as its proof and starter dataset.

**URLs written as wikilinks** — 5 in [[ideation/Unified-Media-Insight-Capture-Tool]] (`[[https://read.readwise.io/]]` and four more). Obsidian renders these as broken *internal* links; they want to be `[label](url)` markdown links. Cosmetic, left alone pending your call.

## ✅ Stale links fixed (2026-08-16)
Vault-wide scan during an ingest + lint pass. 87 links repointed; the vault went from **10 connected components and 9 orphan notes to 1 component, 0 orphans**.
- **66 vault-absolute `[[wiki/...]]` links → relative paths** (LINKING.md §2 requires relative). Most were pre-reorg `[[wiki/cooking/...]]` targets left behind when cooking moved under `research/` — that one stale prefix was what orphaned all 7 recipe notes.
- **14 `[[../index|Master Index]]` links** in depth-2 research notes resolved to a nonexistent `wiki/research/index` → `[[../../index]]`. (The same link is *correct* from `ideation/` and `projects/`, which is why it survived earlier scans.)
- `[[../cooking/baking/index]]` → `[[../research/cooking/baking/index]]` in [[ideation/Return to Basics]]; two `raw/` CSV links in [[research/cooking/selected-restaurants]] were one directory short; four `file://` links there pointed at `~/Obsidian/research/raw`, a path that does not exist.
- **`[Personal Blog & Portfolio](projects/Personal Blog & Portfolio.md)`** in [[index]] — stale since the file was renamed to `seungjohan.com.md` in `2ca404d`.

## ✅ Stale links fixed (2026-07-13)
- `karpathy-vibecoding` → `karpathy-llm-wiki` (deleted file)
- `GEMINI` → `AGENTS`, `Log` → `log`, `brainstorming` → `ideation` (renamed; in [[llm-wiki-pattern]])
- Data files repointed to `raw/`: `Blog Portfolio - Figma Prompts.json`, `AI-Startups-Korea-Top30.csv`, `Global-AI-Companies-Index-2026.csv`, `michelin_wine_list.csv`
- `research` → `research_board` (in AI in Education)

## ⏭️ Intentionally left alone
- Historical narrative in [[ideation/brainstorming_history_log]] (`brainstorming`, `interests`, `research`) — a past-tense record; not rewritten.
- Date notes (e.g. `2026-05-15`) — daily-note style placeholders.
- Doc examples in `LINKING.md` / `AGENTS.md` / `template.md` (`[[concept]]`, `[[relative/path]]`, `{category}/{file}`).

## 🔗 Connections
- [[index|Master Index]]
- [[log|System Log]]
