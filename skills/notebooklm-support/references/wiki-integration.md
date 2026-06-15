# Wiki Integration Patterns for NotebookLM

This reference defines how to map NotebookLM content to the structured Obsidian Wiki.

## Mapping Content Types

| NotebookLM Output | Wiki Folder | Page Type |
| :--- | :--- | :--- |
| Project Summary | `wiki/research/{cat}/` | Concept |
| Entity Analysis | `wiki/research/career/` | Company Page |
| Technical Explanation | `wiki/research/system/` | Reference |
| Culinary Deep-Dive | `wiki/research/cooking/` | Technique/Dish |
| Ideation/Brainstorm | `wiki/ideation/` | Idea Entry |

## Schema Compliance

Every page generated from NotebookLM data MUST adhere to the **[[AGENT.md]]** standards:

### 1. Frontmatter
Include the mandatory `category` property.
```yaml
---
category: research
tags: [notebooklm, synthesized]
---
```

### 2. Key Takeaway Block
Start the page with a high-signal callout.
```markdown
> [!IMPORTANT] Key Takeaway
> **Why this matters:** {Synthesized insight from NotebookLM}
> **How to use it:** {Practical application}
> **Informs:** {Future project or intuition}
```

### 3. Citations
Always note the NotebookLM notebook ID or the specific sources used for the synthesis in a `## Sources` section at the bottom.

## Automated Filing Workflow
1. Run `notebooklm ask` with a prompt asking for "Obsidian-compatible markdown output".
2. Capture the output.
3. Use the `write_file` tool to save to the appropriate path.
4. Update `wiki/log.md` with the new entry.
