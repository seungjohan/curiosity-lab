# Knowledge OS: Design & Linking Standards

This document establishes the structural and connection standards for the curiosity-lab vault. It ensures the vault serves as a highly connected, easily navigable digital garden.

## 1. Frontmatter Structure
All wiki pages must begin with standard frontmatter in the following strict order:
1. **stage**: Inferred by parent folder (research, ideation, projects, cooking, general).
2. **category**: High-level subject domain (cooking, career, music, system, etc.).
3. **tag**: String property matching the folder/category name for filtering.

Example:
```yaml
---
stage: research
category: cooking
tag: cooking
country: France
---
```

## 2. Horizontal (Intra-Stage) Connections: MOC Hubs
* Peer-to-peer pages within the same stage (e.g., two research pages) should link to each other horizontally to form context-specific threads.
* Each major category must maintain a **Map of Content (MOC)** index page (e.g., `wiki/research/cooking/index.md`) that serves as a central hub linking to all category pages.

## 3. Vertical (Cross-Stage) Connections: Hybrid Pipeline
To support the **Research ➔ Ideation ➔ Projects** workflow:
* **Research notes** link forward to relevant ideation boards or project specs.
* **Ideation notes** link back to originating research notes, and forward to promoted projects.
* **Project specs** must have a `## 🔗 Connections` section linking back to BOTH parent ideation boards and relevant research notes.

## 4. Link Formatting Rules
* **Relative Paths:** Always use relative links (e.g., `[[../research/cooking/france]]`) instead of naked filenames to guarantee link portability in Obsidian, VS Code, GitHub, and Python scripts.
* **Annotated Links:** Under the `## 🔗 Connections` section of a file, every link must include a brief, one-sentence description explaining *why* it is connected.
  * *Example:* `- [[../research/cooking/france]] — provides the technical foundation for the braising methods used here.`
