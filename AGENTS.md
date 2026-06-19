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

1. **Horizontal Patterning:** Build a network of thinking, not isolated notes. Every new page must link to at least one existing page.
2. **Vertical Linking:** Every note in `/wiki/projects/` must include a `## 🔗 Connections` section pointing to the underlying research inside `/wiki/research/{category}/`.
3. **Paths:** Use relative paths (e.g., `[[../research/career/AI-Industry-Map-2026]]` or `[[../projects/Michelin-Filter]]`) to maintain vault compatibility.
