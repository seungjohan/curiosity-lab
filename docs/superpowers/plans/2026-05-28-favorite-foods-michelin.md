# Favorite Foods Wiki & Michelin Scraper Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a categorized "Favorite Foods" wiki page and scrape Michelin Guide "Interesting Wine List" data into a CSV.

**Architecture:** Use the "Categorized Registry" pattern for the wiki page and a @generalist subagent for web scraping.

**Tech Stack:** Markdown, CSV, @generalist (web_fetch)

---

### Task 1: Create Favorite Foods Wiki Page

**Files:**
- Create: `wiki/Favorite Foods.md`

- [ ] **Step 1: Create the file with initial content**

```markdown
# Favorite Foods

## Related
- [[Michelin Filter]]

## Overview
A curated registry of favorite dishes and flavors to reference when choosing restaurants.

## Spain
| Food Name | Type | Basic Ingredient | Notes |
| :--- | :--- | :--- | :--- |
| **[[Fideuá]]** | Main Dish | Seafood, Noodles | Often compared to Paella but uses short noodles. |

## Korea
| Food Name | Type | Basic Ingredient | Notes |
| :--- | :--- | :--- | :--- |
| | | | |

## Japan
| Food Name | Type | Basic Ingredient | Notes |
| :--- | :--- | :--- | :--- |
| | | | |
```

- [ ] **Step 2: Commit**

```bash
git add "wiki/Favorite Foods.md"
git commit -m "feat: add Favorite Foods wiki page"
```

---

### Task 2: Wiki Integration (Index & Michelin Filter)

**Files:**
- Modify: `wiki/index.md`
- Modify: `wiki/Michelin Filter.md`

- [ ] **Step 1: Update Wiki Index**

Modify `wiki/index.md` to include the new page under a "Culinary & Dining" category.

```markdown
### 🍴 Culinary & Dining
- [[Favorite Foods]] - Registry of personal favorite dishes.
- [[Michelin Filter]] - Strategy for finding reasonable fine dining.
```

- [ ] **Step 2: Update Michelin Filter**

Modify `wiki/Michelin Filter.md` to link to Favorite Foods.

```markdown
## Related
- [[Favorite Foods]]
```

- [ ] **Step 3: Commit**

```bash
git add wiki/index.md "wiki/Michelin Filter.md"
git commit -m "refactor: integrate Favorite Foods into wiki"
```

---

### Task 3: Scrape Michelin "Interesting Wine List" Data

**Files:**
- Create: `raw/michelin_wine_list.csv`

- [ ] **Step 1: Dispatch @generalist to scrape data**

Dispatch a subagent with the following prompt:
"Scrape the Michelin Guide website for restaurants awarded the 'Interesting Wine List' award. Extract data for at least 50 restaurants (focus on Spain, Japan, Korea, and France first). 
Format the output as a CSV with these columns:
Name,Address,Location,Price,Cuisine,Longitude,Latitude,PhoneNumber,Url,WebsiteUrl,Award,GreenStar,FacilitiesAndServices,Description
Save the result to `raw/michelin_wine_list.csv`."

- [ ] **Step 2: Verify CSV existence and content**

Run: `head -n 5 raw/michelin_wine_list.csv`
Expected: CSV headers followed by restaurant data.

- [ ] **Step 3: Commit**

```bash
git add raw/michelin_wine_list.csv
git commit -m "data: ingestion of Michelin Interesting Wine List restaurants"
```

---

### Task 4: Log Update

**Files:**
- Modify: `wiki/Log.md`

- [ ] **Step 1: Add entry to Log.md**

```markdown
## [2026-05-28] Favorite Foods & Michelin Data
- Created [[Favorite Foods]] wiki page with Spain (Fideuá) entry.
- Integrated Culinary & Dining category into [[index]].
- Ingested 50+ Michelin "Interesting Wine List" restaurants into `raw/michelin_wine_list.csv`.
```

- [ ] **Step 2: Commit**

```bash
git add wiki/Log.md
git commit -m "docs: update log for Favorite Foods and Michelin data"
```
