# Knowledge OS: Linking Standard (Canonical)

> Single source of truth for how pages connect in curiosity-lab.
> `AGENTS.md` points here; do not duplicate these rules elsewhere.

The vault connects along **two axes**. Every page can carry both.

```
   VERTICAL AXIS — the pipeline (your spine)
   Reference/Input ─▶ Research ─▶ Idea (ideation) ─▶ Project
        │              │            │                  │
        └──────────────┴─────┬──────┴──────────────────┘
                             │
   HORIZONTAL AXIS — concepts (the connective tissue)
   page ─▶ [[concept]] ◀─ page      (crosses categories, finds common parts)
```

- **Vertical links are hand-written** — they encode *your* judgment about what feeds what.
- **Horizontal links are auto-generated** — a script derives them from each page's `concepts:` frontmatter, so they never drift.

---

## 1. Frontmatter

Strict order. `concepts` is optional but is what powers the horizontal axis.

```yaml
---
stage: research          # research | ideation | projects | concept | general | input
category: cooking        # subject domain (cooking, career, music, system, …)
tag: cooking             # matches the category/folder for filtering
concepts: [high-signal-filter, multi-signal-fusion]   # inline list; the atoms this page instances
---
```

`stage` is inferred from the folder: `wiki/research/`→research, `wiki/ideation/`→ideation, `wiki/projects/`→projects, `wiki/concepts/`→concept, raw inspiration→input, else general.

---

## 2. Vertical axis — the pipeline (hand-written)

The workflow is **Reference → Research → Idea → Project**. Under `## 🔗 Connections`, keep a `### ⬆ Pipeline` block with directional, annotated links:

```markdown
### ⬆ Pipeline
- Source ← [[../../raw/michelin_wine_list.csv]] — raw award data feeding this note
- Feeds → [[../../projects/Michelin Filter]] — supplies the filter's ranking signals
```

Rules:
- **Research** notes link *forward* to the ideas/projects they inform (`Feeds →`) and *back* to their raw source (`Source ←`).
- **Idea** notes link *back* to originating research and *forward* to promoted projects.
- **Project** specs link *back* to BOTH parent ideas and the research that grounds them.
- Every link gets a one-sentence "why," and uses **relative paths** always (`[[../research/cooking/index]]`).

---

## 3. Horizontal axis — concepts (auto-generated)

A **concept atom** is the underlying pattern/mechanism a page is an *example of* — not its topic. Two pages that share a concept **from different categories** are the valuable, non-obvious link (의외의 연결성).

### Concept nodes
Live in `wiki/concepts/`. One file per atom. Kept short:

```markdown
---
stage: concept
category: system
axis: bits-vs-atoms      # optional: names a polarity for tension detection
---

# Abundance flips value
When something floods to near-free, its opposite becomes the scarce premium.

<!-- AUTO-INSTANCES:START -->
<!-- filled by scripts/build_connections.py -->
<!-- AUTO-INSTANCES:END -->
```

### On each page
1. Add the atoms to `concepts:` in frontmatter.
2. The script renders a delimited block inside `## 🔗 Connections`:

```markdown
<!-- AUTO-CONCEPTS:START -->
### 🔀 Concepts (auto-generated — do not edit)
- **high-signal-filter** → [[../music/music-social-media]] (music), [[../../projects/Michelin Filter]] (system)
<!-- AUTO-CONCEPTS:END -->
```

Never hand-edit between the `AUTO-` markers — rerun the script instead:
`python scripts/build_connections.py`

---

## 4. Quality bar

Only assign a concept (or write a vertical link) if you can finish:

> "This connects because **[specific mechanism]**, not just because they share a topic."

- "Both are about product strategy" → too vague, skip.
- "Both reduce an overwhelming set to the few that matter via a distinctive key" → that's a concept.

Keep the concept vocabulary **small and reused**. A concept with only one instance isn't a link yet — it's a candidate. A concept that keeps accumulating instances is a research theme ripe to graduate into an idea.

---

## 5. Scope: concept-tag by note quality, not by folder

There is **one** research system; every category (including career) flows through the same loop. Whether a page gets concept tags depends on the *note*, not its folder:

- **Concept-tag** any note that carries a **transferable insight** — a mechanism, pattern, or thesis that could recur in another domain. This includes ideas, projects, cross-domain research (cooking, music, planting, personal), and industry/trend notes in career (`AI-Industry-Map-2026`, `Creative-Tech-Trends`, `Edge-AI-Infrastructure-2026`).
- **Skip** boilerplate **profile/database pages** — individual company profiles, vocabulary lists, raw reference tables. Linking ~90 near-identical company pages by shared concepts is noise; they stay organized by same-entity links and their MOC hubs (country maps, `AI-Industry-Map-2026`).

Rule of thumb: *"If I recall this note six months from now, is it because of a reusable idea (tag it) or just a fact I looked up (don't)?"*

---

## 6. Logging
All changes and prompts are logged in `wiki/log.md` (Change Log + Prompt Log). See `AGENTS.md`.
