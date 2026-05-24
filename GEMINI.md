# Brainstorming Wiki Management Rules (Schema)

This project is a personal knowledge base for brainstorming startup and side project ideas. It follows the "LLM Wiki" pattern where the LLM (Gemini) maintains a persistent, interlinked collection of markdown files.

## Project Structure

- `raw/`: Immutable raw source materials. This is where the user provides resources, data, or inspirations (market research, thoughts, history, etc.).
- `wiki/`: Structured, interlinked knowledge base maintained by Gemini.
  - `wiki/index.md`: Central Table of Contents, categorized.
  - `wiki/Log.md`: Chronological log of all operations.
  - `wiki/ideation.md`: Central hub for startup ideas, formatted as a table with properties (Industry, Competitors, Status, etc.).
  - `wiki/research.md`: List of deep-dive research topics and market analysis.
  - All other files are flat within `wiki/`.

## Evolution & Instruction Updates
- **Global Orders**: Whenever the user provides a "global order" (e.g., a new rule, workflow change, or schema update), Gemini must immediately adjust and update this `GEMINI.md` file to reflect the change.

## Core Operations

### 1. Data Entry
- **Trigger**: User adds a file to `raw/` or provides new information.
- **Workflow**:
  1. Read the new data.
  2. Summarize key insights and connect them to existing knowledge.
  3. Create or update relevant pages in `wiki/`.
  4. Use `[[WikiLink]]` for cross-references.
  5. Update `wiki/index.md` with the new/updated pages.
  6. Update `wiki/ideation.md` or `wiki/research.md` as appropriate.
  7. Append an entry to `wiki/Log.md`.

### 2. Querying
- **Trigger**: User asks a question or asks to "deep dive" into a topic.
- **Workflow**:
  1. Search `wiki/index.md` and relevant wiki pages.
  2. Synthesize an answer, citing specific wiki pages or raw sources.
  3. If the insight is valuable, offer to create a new wiki page for it (compounding knowledge).

### 3. Health Check
- **Trigger**: Periodic maintenance or user request.
- **Workflow**:
  1. Check for broken `[[WikiLink]]`s.
  2. Identify orphan pages (no inbound links).
  3. Detect contradictions between old and new data.
  4. Suggest new areas for exploration or data gaps to fill.

## Conventions
- **Flat Wiki**: No subdirectories inside `wiki/`.
- **Linking**: Always use `[[Page Name]]` for internal references.
- **Categorization**: Managed exclusively in `wiki/index.md`.
- **Consistency**: Gemini is responsible for maintaining the integrity and interlinking of the wiki.
- **Language**: All content must be in English.

## Skill Usage
- **Superpowers Skills**: In this directory, you are **AUTHORIZED** to use all "superpowers" skills (brainstorming, writing-plans, etc.) as they are highly relevant to the ideation and research workflows here. This overrides the workspace-level restriction.
