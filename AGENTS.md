# Agentic OS: Unified Research & Ideation Manual

This workspace is a combined engine for fact-based research (observing/mapping) and business ideation/prototyping (synthesizing/acting). It utilizes the GStack framework globally in Cursor/Gemini for execution tasks and Obsidian for visual organization.

## 📁 Repository Conventions

### 1. File Structure
- `/raw/`: Immutable raw source materials (CSV, txt, etc.)
- `/scripts/`: Execution scripts, parsers, and scrapers (Python)
- `/docs/`: Specs and design documents
- `/wiki/`: Processed knowledge base
  - `/wiki/index.md`: Master index (categorized)
  - `/wiki/stream.md`: Capture — the user's raw thought dumps, append-only, newest first (see "Connect pass")
  - `/wiki/log.md`: Main vault change log **and** prompt history (Prompt Log section)
  - `/wiki/research/`: Hierarchical research folders (career, cooking, etc.)
  - `/wiki/ideation/`: Active ideation lists and status boards
  - `/wiki/projects/`: Product requirements (PRDs), specs
  - `/wiki/concepts/`: Concept atoms — reusable underlying patterns that link pages across categories (horizontal axis)

### 2. Mandatory Frontmatter (Wiki Files)
Every wiki file (Markdown/JSON) must include YAML frontmatter.
- **The `stage` property must be the FIRST property.**
- The `category` property must be second.
- Determine `stage` based on directory:
    - `wiki/research/` -> `research`
    - `wiki/ideation/` -> `ideation`
    - `wiki/projects/` -> `projects`
    - `wiki/cooking/` -> `cooking`
    - Others -> `general`
    - Files representing raw inspiration -> `input`

Example:
```markdown
---
stage: input
category: inspiration
---
```

## 🔄 The Loop

One unified loop for everything the user is curious about. **Career is a research category, not a separate track** — its purpose is understanding the AI/job market to find the right role. Outputs are diverse: startup ideas, career decisions, writing.

**Capture → Research → Synthesize → Ideate → Build → Reflect ↺**

1. **Capture (`wiki/stream.md`, `/raw/`)**: `stream.md` is the front door for the user's own raw, unorganized thoughts on any topic — append-only, newest first, **zero structure required of the user**. `/raw/` holds immutable external source material (videos, articles, quotes, datasets).
2. **Research (`wiki/research/{category}/`)**: Fact-gathering and structuring, any category. Every note starts with a "Key Takeaway" callout.
3. **Synthesize (`wiki/concepts/`)**: The bridge from Research to Ideation. Tag each note with the concept atoms it instances; notes from *different categories* sharing an atom are the raw material for new ideas. This stage is where cross-domain insight is produced deliberately instead of by memory. See `LINKING.md`.
4. **Ideate (`wiki/ideation/`)**: Candidates graduate onto the board (`ideation.md`) with a status; strong ones move to specs.
5. **Build (`wiki/projects/` → `scripts/`)**: Formulate specs/PRDs (`template.md`) past the "Stop and Think" gate, then write execution code.
6. **Reflect (`wiki/log.md`)**: Record outcomes *and feed learnings back* into research and ideation — the loop closes here; the log is not just an archive.

### Idea lifecycle

Every idea/project note carries a **`lifecycle:`** frontmatter field (distinct from `status:`, which is document state). It moves in one direction, with two off-ramps:

`spark → researching → validated → building → shipped`  ·  off-ramps: `parked`, `killed`

| lifecycle | meaning |
|---|---|
| `spark` | raw capture, still an entry in `wiki/stream.md` |
| `researching` | actively gathering evidence |
| `validated` | passed the "Stop and Think" forcing-question gate |
| `building` | spec/PRD or code underway |
| `shipped` | launched / live |
| `parked` | paused — **requires `lifecycle_reason:`** + a revisit trigger |
| `killed` | abandoned — **requires `lifecycle_reason:`** (the post-mortem) |

**The kill/park reason is the Reflect step made concrete.** A killed idea without a reason is wasted learning; the *why it died* is the reusable, cross-domain insight. All `parked`/`killed` ideas are listed with their reason in the Graveyard section of `wiki/ideation/ideation.md`.

### Connect pass (`wiki/stream.md`)

`stream.md` is an **append-only log of freeform entries**, newest first, and intentionally the one page with **no standards applied to the user's input**. Entries are random thoughts, short diary notes, ideas, complaints/blame, questions — anything, any length, any topic, any mood. The user dumps raw and unorganized by design: **never ask them to categorize, tag, tidy, or justify an entry.** Structuring is the agent's job, done later, on request ("connect pass").

**Entry shape** — `## YYYY-MM-DD <kind emoji> <gist>`, a status line, freeform body, then `---`. The `##` headings are the index: Obsidian's Outline panel turns them into a clickable list, so the gist in the heading is what makes the log scannable. **No table** — a table taxes writing (no Enter, `|` breaks rows) to buy scanning that the Outline panel already gives free, and this page exists to make writing frictionless.

**Division of labour:** the user writes the **date heading + body**. The agent adds the **kind emoji, status, and `Connects:` line**. If the user pastes a thought into chat, the agent writes the entry — don't send them to the file.

When asked for a connect pass, for each entry marked `🌱 raw`:

1. **Read it charitably.** A fragment, a bad mood, or an unfinished sentence is valid input, not an error. Never edit, rewrite, correct, or "clean up" the user's words — the raw text is the record. Add to the heading and the `Connects:` line only.
2. **Set the kind emoji** (💭 random · 📔 diary · 💡 idea · 😤 blame · ❓ question), and sharpen the heading gist only if the user left it blank. **😤 blame entries are prime idea material** — a complaint is a problem statement with the emotion still attached, and friction the user hit personally is exactly the kind worth solving. Mine them for latent ideas; don't dismiss them as venting.
3. **Search the vault for real relationships** — related research notes, existing ideas, and concept atoms in `wiki/concepts/`. Prefer connections the user is *unlikely to have noticed themselves* (a cooking note sharing an atom with a music note); that surprise is the whole value.
4. **Add a `**Connects:**` line** with wikilinks. Apply the same quality bar as all linking: only link if you can finish *"connects because **[specific mechanism]**"* — not just a shared topic. **An entry with no honest connection gets none.** A fabricated link is worse than an empty one, because it poisons the graph the user is learning to trust.
5. **Flip `🌱 raw` → `🔗 connected`.** Leave a genuinely inert entry as `🪦 dropped` rather than forcing a link.
6. **Surface candidates.** Report which entries recur or attract many links — those are graduation candidates. Recommend; don't graduate unasked.

**If the stream outgrows one file** (filtering by kind/date becomes the real need, not just scanning): the upgrade is one file per thought under `wiki/stream/` with `kind:`/`lifecycle:` frontmatter, and a Dataview `TABLE` block in `stream.md` rendering the view. Dataview is installed and the user has used this pattern before. Graduation then costs nothing — the thought file *becomes* the idea note by gaining `concepts:`. **Don't pre-build this**; the single file is correct until the volume justifies the machinery.

**Graduating an entry:** create the note in `wiki/ideation/` with `concepts:` + `lifecycle: spark`, add it to the board, then set the entry's status line to `🎓 → [[the new note]]`. **Never delete the original entry** — it is the origin record of the idea.

Raw entries carry **no `concepts:` frontmatter** (`LINKING.md` §5: tag transferable insight, not raw capture). Graduation is how a thought earns its concepts. `stream.md` itself is therefore never processed by `scripts/build_connections.py`.

## 📝 Page Schemas

### Standard Page
```markdown
---
stage: [input/research/ideation/projects/cooking/general]
category: [career/stock market/cooking/system/etc]
---

> [!IMPORTANT] Key Takeaway
> **Why this matters:** {Insight}
> **How to use it:** {Action/Decision}
> **Informs:** {Future project/intuition}
```

## 🔗 Linking Philosophy

**The full standard lives in `LINKING.md` (canonical). Read it before any ingest.** Summary:

The vault connects on **two axes**:

1. **Vertical — the pipeline (hand-written):** `Reference → Research → Idea → Project`. Under `## 🔗 Connections`, a `### ⬆ Pipeline` block holds directional annotated links (`Feeds →`, `Source ←`, `Back ←`). This encodes your judgment about what informs what.
2. **Horizontal — concepts (auto-generated):** each page lists the underlying atoms it instances in `concepts:` frontmatter; `scripts/build_connections.py` renders the `### 🔀 Concepts` block between `AUTO-` markers. Two pages sharing a concept across different categories = the valuable, non-obvious link (의외의 연결성). Never hand-edit between the markers.

**Quality bar:** only add a concept or vertical link if you can finish — *"connects because **[specific mechanism]**, not just a shared topic."* Keep the concept vocabulary small and reused (`wiki/concepts/`).

**Ingest pass after every new source:**
1. Write the vertical `### ⬆ Pipeline` links (forward + back), with a one-sentence why each.
2. Assign 1–4 concepts in frontmatter — reuse existing atoms in `wiki/concepts/` where possible; create a new node only for a genuinely new, reusable pattern.
3. Run `python scripts/build_connections.py` to regenerate horizontal links and concept-node instance lists.
4. Add inline `[[relative/path]]` links on first mention of a key term in body text.

Use **relative paths always** (`[[../research/career/AI-Industry-Map-2026]]`).

**Scope:** the concept axis is for idea-generating notes (`ideation/`, `projects/`, cross-domain `research/`). The career company DB (`research/career/`) stays organized by MOC hubs, not concepts — see `LINKING.md §5`.

### Prompt & History Logging

All interactions must be logged in `wiki/log.md` to maintain transparency and traceability of architectural decisions:
1. **Change Log** (top table): All significant actions or changes — `Date | Action | Page | Description`.
2. **Prompt Log** (second table): All significant user prompts — `Date | User Prompt | Outcome | Agent`. Always record which AI agent handled the prompt (e.g. `Claude Code (Opus 4.8)`, `gemini-3.1-flash-lite`).
3. **Agent Accountability**: If multiple agents are used, each agent is responsible for recording its own actions and prompts in `wiki/log.md` to maintain a unified history.
