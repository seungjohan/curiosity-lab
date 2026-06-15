# Batch Lint Fix Wiki Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix linting errors across 28 wiki files by ensuring correct frontmatter (category first), adding Key Takeaway callouts, and providing consistent Connections sections.

**Architecture:** Surgical updates to markdown files using `replace` to preserve existing content while adding missing sections and fixing frontmatter.

**Tech Stack:** Markdown, Python (for linting verification).

---

### Task 1: Fix Double Frontmatter in Projects

**Files:**
- Modify: `wiki/projects/Dreams & Hobbies.md`
- Modify: `wiki/projects/Favorite Foods.md`
- Modify: `wiki/projects/Idea Stream.md`
- Modify: `wiki/projects/Inspiration Sources.md`
- Modify: `wiki/projects/Market Analysis.md`

- [ ] **Step 1: Fix Dreams & Hobbies.md**
  - Remove redundant `---` blocks and merge.
  - Ensure `category: system` is the first property.
- [ ] **Step 2: Fix Favorite Foods.md**
  - Remove redundant `---` blocks and merge.
  - Ensure `category: cooking` is the first property.
- [ ] **Step 3: Fix Idea Stream.md**
  - Remove redundant `---` blocks and merge.
  - Ensure `category: system` is the first property.
- [ ] **Step 4: Fix Inspiration Sources.md**
  - Remove redundant `---` blocks and merge.
  - Ensure `category: system` is the first property.
- [ ] **Step 5: Fix Market Analysis.md**
  - Remove redundant `---` blocks and merge.
  - Ensure `category: system` is the first property.

### Task 2: Fix Remaining Projects

**Files:**
- Modify: `wiki/projects/Michelin Filter.md`
- Modify: `wiki/projects/PRD.md`
- Modify: `wiki/projects/Personal Blog & Portfolio.md`
- Modify: `wiki/projects/Relationship Lessons.md`
- Modify: `wiki/projects/Self-Reflection.md`
- Modify: `wiki/projects/Social Interactions.md`
- Modify: `wiki/projects/Startup Insights.md`
- Modify: `wiki/projects/The Connection.md`
- Modify: `wiki/projects/Triathlon Photo Finder.md`
- Modify: `wiki/projects/Webeing.md`

- [ ] **Step 1: Fix Michelin Filter.md**
  - Add `category: system` to frontmatter.
  - Add Key Takeaway block.
  - Add `## 🔗 Connections` with index link.
- [ ] **Step 2: Fix PRD.md**
  - Add `category: system` to frontmatter.
  - Add Key Takeaway block.
  - Add `## 🔗 Connections` with index link.
- [ ] **Step 3: Fix Personal Blog & Portfolio.md**
  - Add `category: system` to frontmatter.
  - Add Key Takeaway block.
  - Update `## 🔗 Connections` to include index link.
- [ ] **Step 4: Fix Relationship Lessons.md**
  - Add `category: system` to frontmatter.
  - Add Key Takeaway block.
  - Add `## 🔗 Connections` with index link.
- [ ] **Step 5: Fix Self-Reflection.md**
  - Add `category: system` to frontmatter.
  - Add Key Takeaway block.
  - Add `## 🔗 Connections` with index link.
- [ ] **Step 6: Fix Social Interactions.md**
  - Add `category: system` to frontmatter.
  - Add Key Takeaway block.
  - Add `## 🔗 Connections` with index link.
- [ ] **Step 7: Fix Startup Insights.md**
  - Add `category: system` to frontmatter.
  - Add Key Takeaway block.
  - Add `## 🔗 Connections` with index link.
- [ ] **Step 8: Fix The Connection.md**
  - Add `category: system` to frontmatter.
  - Add Key Takeaway block.
  - Add `## 🔗 Connections` with index link.
- [ ] **Step 9: Fix Triathlon Photo Finder.md**
  - Add `category: system` to frontmatter.
  - Add Key Takeaway block.
  - Add `## 🔗 Connections` with index link.
- [ ] **Step 10: Fix Webeing.md**
  - Add `category: system` to frontmatter.
  - Add Key Takeaway block.
  - Add `## 🔗 Connections` with index link.

### Task 3: Fix AI Maps (Add Key Takeaway)

**Files:**
- Modify: `wiki/research/career/Bay-Area-AI-Map.md`
- Modify: `wiki/research/career/Ireland-AI-Map.md`
- Modify: `wiki/research/career/NYC-AI-Map.md`
- Modify: `wiki/research/career/UK-AI-Map.md`
- Modify: `wiki/research/career/USA-AI-Map.md`

- [ ] **Step 1: Add Key Takeaway to Bay-Area-AI-Map.md**
- [ ] **Step 2: Add Key Takeaway to Ireland-AI-Map.md**
- [ ] **Step 3: Add Key Takeaway to NYC-AI-Map.md**
- [ ] **Step 4: Add Key Takeaway to UK-AI-Map.md**
- [ ] **Step 5: Add Key Takeaway to USA-AI-Map.md**

### Task 4: Fix Misc Research

**Files:**
- Modify: `wiki/research/personal/Blog Portfolio - Codex Prompts.md`
- Modify: `wiki/research/planting/index.md`
- Modify: `wiki/research/planting/vocabulary.md`
- Modify: `wiki/research/resume/section_education.md`
- Modify: `wiki/research/resume/section_experience.md`
- Modify: `wiki/research/resume/section_others.md`
- Modify: `wiki/research/resume/section_projects.md`
- Modify: `wiki/research/travel/guidelines.md`

- [ ] **Step 1: Fix Blog Portfolio - Codex Prompts.md**
  - Add `category: system` to frontmatter.
  - Add Key Takeaway block.
  - Add `## 🔗 Connections` with index link.
- [ ] **Step 2: Add Key Takeaway to planting/index.md**
- [ ] **Step 3: Add Key Takeaway to planting/vocabulary.md**
- [ ] **Step 4: Fix resume/section_education.md**
  - Add Key Takeaway block.
  - Add `## 🔗 Connections` with index link.
- [ ] **Step 5: Fix resume/section_experience.md**
  - Add Key Takeaway block.
  - Add `## 🔗 Connections` with index link.
- [ ] **Step 6: Fix resume/section_others.md**
  - Add Key Takeaway block.
  - Add `## 🔗 Connections` with index link.
- [ ] **Step 7: Fix resume/section_projects.md**
  - Add Key Takeaway block.
  - Add `## 🔗 Connections` with index link.
- [ ] **Step 8: Add Key Takeaway to travel/guidelines.md**

### Task 5: Final Verification

- [ ] **Step 1: Run linter**
  - Run: `python3 scripts/lint_wiki.py`
  - Expected: Zero or minimal remaining errors.
