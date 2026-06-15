---
name: notebooklm-support
description: Manage Google NotebookLM notebooks, add sources, ask questions, and generate audio overviews (podcasts) using the notebooklm-py CLI tool. Use when the user wants to leverage NotebookLM for research synthesis or audio content.
---

# NotebookLM Support

This skill enables interaction with Google NotebookLM via the `notebooklm-py` CLI. It allows for advanced research synthesis, batch processing of sources, and automated "Deep Dive" podcast generation.

## Prerequisite Setup
Before using this skill, the following steps must be completed:
1. **Installation:** `pip install "notebooklm-py[browser]"` and `playwright install chromium`.
2. **Authentication:** Run `notebooklm login`. This opens a browser window for Google authentication.
3. **Verification:** Check current notebooks with `notebooklm notebooks list`.

## Workflows

### 1. Project & Notebook Management
- **Create:** `notebooklm notebooks create "<name>"`
- **List:** `notebooklm notebooks list`
- **Delete:** `notebooklm notebooks delete <id>`

### 2. Sourcing Materials
Add research materials to a notebook corpus.
- **Add URL or File:** `notebooklm sources add <target> --notebook-id <id>`
- **Add YouTube Video:** `notebooklm sources add <youtube-url> --notebook-id <id>`
- **List Sources:** `notebooklm sources list --notebook-id <id>`

### 3. Synthesis & Querying
Analyze the corpus and extract insights.
- **Ask a Question:** `notebooklm ask "<question>" --notebook-id <id>`
- **Batch Export:** Use `notebooklm sources list` to identify sources and fetch structured content.

### 4. Audio Overviews (Podcasts)
Generate and download the AI-generated "Deep Dive" audio conversation.
- **Generate:** `notebooklm artifacts generate audio --notebook-id <id>`
- **Wait for Completion:** Audio generation can take several minutes.
- **Download:** `notebooklm artifacts download audio --notebook-id <id> --output <path>`

### 5. LLM Wiki Integration
When processing NotebookLM results, you MUST follow the **[[AGENT.md]]** schema for the workspace wiki.

- **Filing:** Move summaries and extracted insights to the appropriate `wiki/research/{category}/` subfolder.
- **Mandatory Schema:** 
    - Every new page MUST have a `category` property in the YAML frontmatter.
    - Every page MUST start with a `> [!IMPORTANT] Key Takeaway` callout block.
- **Horizontal Patterning:** Ensure the new page links to at least one existing page in the wiki to maintain structural integrity.

## Resources
- **CLI Reference:** See [references/cli-reference.md](references/cli-reference.md) for a full command list.
- **Integration Patterns:** See [references/wiki-integration.md](references/wiki-integration.md) for mapping content types to the wiki.
