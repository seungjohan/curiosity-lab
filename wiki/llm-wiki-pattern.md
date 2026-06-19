---
stage: general
category: system
tag: system
created: 2026-05-14
industry: N/A
status: active
topic:
- Wiki
- LLM
- Structure
type: meta
---

> [!IMPORTANT] Key Takeaway
> **Why this matters:** The architectural blueprint for this system, where LLMs manage interlinked markdown files to create a compounding, persistent knowledge artifact.
> **How to use it:** Follow these patterns when ingesting new sources or querying the system.
> **Informs:** [[index|Master Index]], [[log|System Log]]

# LLM Wiki Pattern

The **LLM Wiki Pattern** is a method for building personal knowledge bases where an LLM incrementally builds and maintains a persistent wiki of interlinked markdown files.

## Core Philosophy
- **Persistent Artifact**: Unlike standard RAG which re-derives knowledge every time, the wiki is a compounding artifact where synthesis and cross-references are maintained over time.
- **LLM as Programmer, User as Architect**: The user provides sources and asks questions; the LLM handles the "grunt work" of summarizing, cross-referencing, and bookkeeping.
- **Compounding Knowledge**: Every new source and every insight from a query is folded back into the wiki.

## Architecture
- **Raw Sources**: Immutable source documents.
- **The Wiki**: Managed interlinked markdown files.
- **The Schema**: Rules (like [[GEMINI]]) that define how the LLM maintains the wiki.

## Key Files in this Project
- [[index]] - Content-oriented catalog.
- [[Log]] - Chronological record of operations.
- [[brainstorming]] - Focused list for startup/project ideas.

## References
- Source: `llm-wiki.md`
- Original Gist: [karpathy/llm-wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

## 🔗 Connections
- [[index|Master Index]]
- [[log|System Log]]
