# Agentic OS: Unified Research & Ideation Manual

This workspace is a combined engine for fact-based research (observing/mapping) and business ideation/prototyping (synthesizing/acting). It utilizes the GStack framework globally in Cursor/Gemini for execution tasks and Obsidian for visual organization.

## 👤 User Profile & Workspace Purpose
- **User Role:** Journalist, Researcher, 0→1 Product Manager, Composer, and Writer.
- **Focus:** Building products from scratch, fact-gathering, product intuition, musical expression, and cross-domain synthesis.
- **Research:** Fact-gathering, company profiling, culinary databases, industry indexing.
- **Ideation & Prototyping:** Transforming research into startup concepts, PRDs, and tools.

## 🔄 The Thinking Flow (Information Loop)

The agent must maintain a continuous loop from observation to action:

1. **Research (`wiki/research/{category}/`)**: Fact-gathering and structuring. Every note starts with a "Key Takeaway" callout.
2. **Ideation (`wiki/ideation/`)**: List and catalog ideas in the central board (`wiki/ideation/ideation.md`).
3. **Specs (`wiki/projects/`)**: Formulate specs/PRDs (using `template.md` to answer forcing questions) before writing code.
4. **Execution (`scripts/`)**: Create Python scripts, scrapers, and execution logic here.
5. **Log & Learnings (`wiki/log.md`)**: Track changes and outcomes.

## 📁 System Structure

- `/raw/`: Immutable raw source materials (CSV, txt, etc.)
- `/scripts/`: Execution scripts, parsers, and scrapers
- `/docs/`: Specs and design documents
- `/wiki/`: Processed knowledge base
  - `/wiki/index.md`: Master index (categorized)
  - `/wiki/log.md`: Main vault change log
  - `/wiki/research/`: Hierarchical research folders (career, cooking, personal, planting, resume, system, travel, vibecoding, vocabulary)
  - `/wiki/ideation/`: Active ideation lists and status boards
  - `/wiki/projects/`: Product requirements (PRDs), specs, and project files

## 📝 Page Schemas

Every wiki page must follow this structure. The `category` property is **mandatory** and must be the first property in the YAML frontmatter.

### Standard Page
```markdown
---
category: [career/stock market/cooking/system/etc]
---

> [!IMPORTANT] Key Takeaway (from my product & creative perspective)
> **Why this matters:** {Insight}
> **How to use it:** {Action/Decision}
> **Informs:** {Future project/intuition}

# {Title}

{Structured Content}

## 🔗 Connections
- [[Related Page 1]]
- [[Related Page 2]]
```

### 🏢 Company Page (Analyst Mode)
For pages specifically analyzing a company. The `category` property is **mandatory** and must be the first property.

```markdown
---
category: system
industry: [Primary, Secondary]
scale: [Startup/Scale-up/Unicorn/Public]
hq: City, State/Province
country: CountryName
tags: [company, PillarName, SpecificTag]
about: One-sentence summary.
---
```
**Mandatory for Companies:**
- Use `#company` tag.
- Include explicit `country` for easier filtering.
- Link to the relevant pillar in [[AI-Industry-Map-2026]].

### 🍳 Culinary Page (Dish & Region Mode)
For pages exploring dishes, ingredients, or regional cuisines. The `category` property is **mandatory** and must be `cooking`.

```markdown
---
category: cooking
country: [France/Italy/Spain/Japan/China/Korea/Vietnam/Mexico/USA]
region: [Specific region if applicable]
type: [Dish/Ingredient/Technique/Restaurant]
tags: [cooking, CuisineType, MainIngredient]
---
```
**Mandatory for Cooking:**
- Use `#cooking` tag.
- Specify the `country` for vault-wide organization.
- Include a "Key Takeaway" focusing on the product/creative essence of the dish.

## 🔗 Linking Philosophy

1. **Horizontal Patterning:** Prioritize patterns across domains (e.g., Product ↔ Music). Build a network of thinking, not isolated notes. Every new page must link to at least one existing page.
2. **Vertical Linking:** Every note in `/wiki/projects/` must include a `## 🔗 Connections` section pointing to the underlying research inside `/wiki/research/{category}/`.
3. **Graduation:** Ideation boards (`ideation.md`) must link directly to the spec files in `/wiki/projects/`.
4. **Paths:** Use relative paths (e.g., `[[../research/career/AI-Industry-Map-2026]]` or `[[../projects/Michelin-Filter]]`) to maintain vault compatibility.
