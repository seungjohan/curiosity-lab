# Planting Category Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Establish a new "planting" category for botanical and gardening knowledge, including a specialized vocabulary page.

**Architecture:** 
- New folder `wiki/planting/` for category content.
- New vocabulary file `wiki/planting/vocabulary.md`.
- Updated master index `wiki/index.md` and system log `wiki/log.md`.

**Tech Stack:** Markdown (Knowledge OS)

---

### Task 1: Create Planting Vocabulary

**Files:**
- Create: `wiki/planting/vocabulary.md`

- [ ] **Step 1: Write the vocabulary file**

```markdown
---
category: planting
tags: [vocabulary, botany, planting]
---

# 🌿 Planting Vocabulary

This page consolidates terms related to botany, gardening, and plant life cycles.

## 🇬🇧 English
| Word | Meaning | Example |
| :--- | :--- | :--- |
| **Wilt** | Loss of turgor pressure in plants, causing them to go limp. | "The seedlings began to wilt in the direct sun." |
| **Fruiting** | The phase where a plant produces fruit. | "The tomato plants are finally fruiting." |

## 🔗 Connections
- [[wiki/planting/index.md|Planting Index]]
- [[wiki/cooking/vocabulary.md|Cooking Vocabulary]]
```

- [ ] **Step 2: Commit**

```bash
git add wiki/planting/vocabulary.md
git commit -m "feat: add planting vocabulary page"
```

---

### Task 2: Create Planting Index

**Files:**
- Create: `wiki/planting/index.md`

- [ ] **Step 1: Write the planting index file**

```markdown
---
category: planting
---

# 🌿 Planting & Horticulture: Master Index

Research and notes on botany, gardening, and plant life cycles.

## 📖 Vocabulary & Fundamentals
- [[wiki/planting/vocabulary.md|Planting Vocabulary]]

## 🔗 Connections
- [[wiki/index.md|Main Index]]
```

- [ ] **Step 2: Commit**

```bash
git add wiki/planting/index.md
git commit -m "feat: add planting master index"
```

---

### Task 3: Update Master Index

**Files:**
- Modify: `wiki/index.md`

- [ ] **Step 1: Add Planting section to Master Index**

```markdown
## 🌿 Planting & Horticulture
- [[wiki/planting/index.md|Planting & Horticulture: Master Index]] - Botany, gardening, and life cycle tracking.
```

- [ ] **Step 2: Commit**

```bash
git add wiki/index.md
git commit -m "feat: link planting category in master index"
```

---

### Task 4: Update System Log

**Files:**
- Modify: `wiki/log.md`

- [ ] **Step 1: Record the system expansion**

```markdown
- **2026-06-09:** Added `planting` category and vocabulary.
```

- [ ] **Step 2: Commit**

```bash
git add wiki/log.md
git commit -m "chore: log planting category addition"
```
