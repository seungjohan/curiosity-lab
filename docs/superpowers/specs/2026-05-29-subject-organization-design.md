# Design Spec: Category-Based Organization

**Date:** 2026-05-29
**Topic:** Wiki Categorization via Properties
**Status:** Validated

## 1. Overview
The goal is to implement a clear categorization system for the "Knowledge OS" using Obsidian properties instead of physical subfolders. This maintains a flat directory structure for ease of search and linking while allowing for thematic grouping and visual distinction in Obsidian's Graph View.

## 2. Requirements
- Standardize a `category` property in the YAML frontmatter of all `/wiki/` files.
- **Mandatory:** The `category` property must be the **first** property in the YAML block.
- Ensure all existing files are migrated to include the appropriate `category`.
- Update the system's "Operating Manual" (`GEMINI.md`) to enforce this property for all future content.
- Support at least three initial categories: `career`, `stock market`, and `cooking`.

## 3. Design Details

### 3.1 YAML Schema
Every wiki page must include the following in its frontmatter, starting with the `category` field:

```yaml
---
category: [career | stock market | cooking | system]
tags: [existing tags]
about: One-sentence summary.
---
```

### 3.2 Operating Manual Updates (`GEMINI.md`)
The `Page Schema` and `Company Page Schema` sections will be updated to include `category` as the first mandatory field.

### 3.3 Mapping of Initial Categories
- **Career:** All company profiles, industry maps, job search logs, and PM-related notes.
- **Stock Market:** Finance-related research, stock analysis, market trends.
- **Cooking:** Recipes, culinary techniques, food science.
- **System:** Index files (`index.md`), change logs (`log.md`), and system-wide maps.

## 4. Migration Strategy
1. **Automation:** Use a batch update script to inject the `category` property as the first line of the YAML frontmatter in existing `.md` files in `/wiki/`.
2. **Classification Logic:** 
   - Files ending in `-PM`, `-Map`, or containing company tags -> `category: career`.
   - Index/Log -> `category: system`.
   - All others -> TBD or default to `career` based on current vault contents.

## 5. Success Criteria
- All 80+ files in `/wiki/` have a `category` property as the first entry in their frontmatter.
- `GEMINI.md` reflects the new mandatory schema.
- Obsidian Graph View can successfully group and color nodes using the "category" property.

