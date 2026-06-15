# Agentic OS: Unified Research & Ideation Manual

This workspace is a combined engine for fact-based research (observing/mapping) and business ideation/prototyping (synthesizing/acting). It utilizes the GStack framework globally in Cursor/Gemini for execution tasks and Obsidian for visual organization.

## 👤 User Profile & Workspace Purpose
- **User Role:** Journalist, Researcher, and 0→1 Product PM/Developer.
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

## 🔗 Linking Philosophy

1. **Vertical Linking:** Every note in `/wiki/projects/` must include a `## 🔗 Connections` section pointing to the underlying research inside `/wiki/research/{category}/`.
2. **Graduation:** Ideation boards (`ideation.md`) must link directly to the spec files in `/wiki/projects/`.
3. **Paths:** Use relative paths (e.g., `[[../research/career/AI-Industry-Map-2026]]` or `[[../projects/Michelin-Filter]]`) to maintain vault compatibility.
