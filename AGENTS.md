# Agentic OS: Unified Research & Ideation Manual

This workspace is a combined engine for fact-based research (observing/mapping) and business ideation/prototyping (synthesizing/acting). It utilizes the GStack framework globally in Cursor/Gemini for execution tasks and Obsidian for visual organization.

## 📁 Repository Conventions

### 1. File Structure
- `/raw/`: Immutable raw source materials (CSV, txt, etc.)
- `/scripts/`: Execution scripts, parsers, and scrapers (Python)
- `/docs/`: Specs and design documents
- `/wiki/`: Processed knowledge base
  - `/wiki/index.md`: Master index (categorized)
  - `/wiki/log.md`: Main vault change log
  - `/wiki/research/`: Hierarchical research folders (career, cooking, etc.)
  - `/wiki/ideation/`: Active ideation lists and status boards
  - `/wiki/projects/`: Product requirements (PRDs), specs

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

Example:
```markdown
---
stage: research
category: career
---
```

## 🔄 The Thinking Flow (Information Loop)

1. **Research (`wiki/research/{category}/`)**: Fact-gathering and structuring. Every note starts with a "Key Takeaway" callout.
2. **Ideation (`wiki/ideation/`)**: List and catalog ideas in the central board (`wiki/ideation/ideation.md`).
3. **Specs (`wiki/projects/`)**: Formulate specs/PRDs (using `template.md`) before writing code.
4. **Execution (`scripts/`)**: Create Python scripts, scrapers, and execution logic here.
5. **Log & Learnings (`wiki/log.md`)**: Track changes and outcomes.

## 📝 Page Schemas

### Standard Page
```markdown
---
stage: [research/ideation/projects/cooking/general]
category: [career/stock market/cooking/system/etc]
---

> [!IMPORTANT] Key Takeaway
> **Why this matters:** {Insight}
> **How to use it:** {Action/Decision}
> **Informs:** {Future project/intuition}
```

## 🔗 Linking Philosophy

### Connection types

Every page can hold five types of connections. The LLM finds and writes
all of them on every ingest.

| Type | Label | Meaning |
|---|---|---|
| 1 | `same-entity` | Both pages mention the same person, company, concept, or term |
| 2 | `supports / contradicts` | One page's claim strengthens or challenges another's |
| 3 | `feeds-into` | Research → Ideation → Spec (vertical chain) |
| 4 | `analogical` | Different domains, same underlying pattern or structure |
| 5 | `tension` | Two pages pull in opposite directions of value or direction |

Types 4 and 5 are the priority — they produce unexpected insight (의외의 연결성).

---

### Two places connections live

#### 1. Inline keyword links (body text)
Wrap key terms in Obsidian links when a corresponding page exists.
Link on first mention only. Use relative paths always.

> "This mirrors how [[../research/biology/mycelium]] distributes nutrients..."

#### 2. `## 🔗 Connections` section (bottom of every page)

```markdown
## 🔗 Connections

### Same entity
- [[../research/category/page]] — both discuss `X`

### Supports / contradicts
- [[../research/category/page]] — supports the claim that `Y`
- [[../ideation/page]] — contradicts: argues against `Z`

### Feeds into
- [[../projects/page]] — this research grounds this spec

### Analogical ✦
- [[../research/other-domain/page]] — same pattern: both [shared structure]
  > "X in [domain A] mirrors Y in [domain B] because [mechanism]"

### Tension ✦
- [[../ideation/page]] — pulls against: this argues for [opposite direction]
```

✦ = unexpected connections. Always attempt these. If none found, write:
`- none identified yet`

---

### Ingest connection pass (run after every new source)

**Step 1 — Types 1, 2, 3**
Read `wiki/index.md`. For each page whose summary shares an entity,
claim, or topic with the new source → open it, update its Connections
section, add inline links where relevant.

**Step 2 — Type 4 (analogical)**
Scan index.md categories *other than* the current one.
Ask: "What pattern or structure does this source share with pages
in a completely different domain?"
Write the shared mechanism explicitly — not just that they're similar.

**Step 3 — Type 5 (tension)**
Ask: "Which existing pages argue for the opposite direction or value?"
Look especially across `wiki/research/` ↔ `wiki/ideation/` boundaries.

**Step 4 — Backlinks**
For every connection found, add a reciprocal entry in the
target page's Connections section pointing back to the new page.

---

### Connection quality bar

Only write a connection if you can complete this sentence:

> "This connects to [[page]] because **[specific reason]**,
> not just because they share the same topic."

"Both are about product strategy" → too vague, skip.
"Both describe how scarcity drives urgency in user decisions" → write it.

---

### Paths
Use relative paths: `[[../research/career/AI-Industry-Map-2026]]`
or `[[../projects/Michelin-Filter]]` to maintain vault compatibility.