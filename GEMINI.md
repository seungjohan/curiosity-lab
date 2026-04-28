# Knowledge OS: Operating Manual

This document defines the rules, schemas, and workflows for the Product Thinking-based Knowledge OS.

## 👤 User Profile
- **Role:** 0→1 Product Manager, Composer, Writer.
- **Focus:** Building products from scratch, product intuition, musical expression, cross-domain synthesis.

## 📁 System Structure
- `/raw/`: Incoming raw materials (read-only for Gemini).
- `/wiki/`: Processed, structured knowledge (Gemini-managed).
- `/wiki/index.md`: Master index organized by themes.
- `/wiki/log.md`: Change log for all updates.
- **Rule:** Flat structure inside `/raw/` and `/wiki/`. No subfolders.

## 🔄 Workflows

### 1. Adding Knowledge (`input` → `structured wiki`)
- **Trigger:** New material added to `/raw/` or provided in chat.
- **Process:**
  1. Extract key ideas.
  2. Create/Update page in `/wiki/` using Markdown.
  3. **Mandatory:** Start with the "Key Takeaway" callout block.
  4. Use `[[wiki links]]` to connect with existing pages.
  5. Update `/wiki/index.md` if a new theme emerges.
  6. Record the change in `/wiki/log.md`.

### 2. Asking Questions (`query` → `synthesized answer`)
- **Trigger:** User asks a question about stored knowledge.
- **Process:**
  1. Search `/wiki/` for relevant concepts.
  2. Synthesize an answer that improves decision-making or creative intuition.
  3. Reference specific wiki pages using `[[links]]`.

### 3. System Health Check
- **Trigger:** User request or scheduled maintenance.
- **Process:**
  1. Identify "orphan" pages (no incoming/outgoing links).
  2. Surface contradictions or outdated product assumptions.
  3. Suggest new connections between Product, Music, and Learning.

## 📝 Page Schema
Every wiki page must follow this structure:

```markdown
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

## 🔗 Linking Philosophy
- Prioritize patterns across domains (e.g., Product ↔ Music).
- Build a network of thinking, not isolated notes.
- Every new page must link to at least one existing page.
