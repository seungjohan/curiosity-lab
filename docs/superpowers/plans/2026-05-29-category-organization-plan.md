# Category-Based Organization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Standardize a mandatory `category` property as the first field in the YAML frontmatter of all wiki files for improved organization and Obsidian Graph View filtering.

**Architecture:** 
1. Update `GEMINI.md` to establish the new schema.
2. Develop a Python migration script to safely inject/reorder properties in all `.md` files in `/wiki/`.
3. Execute migration and verify consistency.

**Tech Stack:** Python (for migration), Markdown/YAML (system schema).

---

### Task 1: Update System Manual (GEMINI.md)

**Files:**
- Modify: `GEMINI.md`

- [ ] **Step 1: Update Page Schema**
Modify the "Page Schema" section to include `category` as the first property.

- [ ] **Step 2: Update Company Page Schema**
Modify the "Company Page Schema" section to include `category` as the first property.

- [ ] **Step 3: Commit**
```bash
git add GEMINI.md
git commit -m "docs: update system manual with mandatory category property"
```

### Task 2: Create Migration Script

**Files:**
- Create: `scripts/migrate_categories.py`

- [ ] **Step 1: Write the migration script**
The script must:
1. Iterate through all `.md` files in `wiki/`.
2. Parse the YAML frontmatter.
3. Determine the category based on filename and tags.
4. Rewrite the file with `category` as the FIRST property.

```python
import os
import yaml
import re

WIKI_DIR = "wiki"
CATEGORIES = ["career", "stock market", "cooking", "system"]

def get_category(filename, content, tags):
    if filename in ["index.md", "log.md", "AI-Industry-Map-2026.md"]:
        return "system"
    if "company" in tags or "-PM" in filename or "-Map" in filename:
        return "career"
    # Default to career for now as per vault contents
    return "career"

def migrate_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not match:
        # Handle files without frontmatter
        filename = os.path.basename(filepath)
        category = get_category(filename, "", [])
        new_content = f"---\ncategory: {category}\n---\n\n" + content
    else:
        frontmatter_raw = match.group(1)
        body = match.group(2)
        try:
            frontmatter = yaml.safe_load(frontmatter_raw) or {}
        except yaml.YAMLError:
            print(f"Error parsing YAML in {filepath}")
            return

        filename = os.path.basename(filepath)
        tags = frontmatter.get('tags', [])
        if isinstance(tags, str): tags = [tags]
        
        category = frontmatter.get('category') or frontmatter.get('subject') or get_category(filename, content, tags)
        
        # Remove old keys if any
        frontmatter.pop('subject', None)
        frontmatter['category'] = category
        
        # Reconstruct YAML with category first
        ordered_keys = ['category'] + [k for k in frontmatter.keys() if k != 'category']
        new_yaml = ""
        for k in ordered_keys:
            # Simple manual dump to ensure order and style
            val = frontmatter[k]
            if isinstance(val, list):
                new_yaml += f"{k}: [{', '.join(val)}]\n"
            else:
                new_yaml += f"{k}: {val}\n"
        
        new_content = f"---\n{new_yaml}---\n{body}"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == "__main__":
    for filename in os.listdir(WIKI_DIR):
        if filename.endswith(".md"):
            migrate_file(os.path.join(WIKI_DIR, filename))
```

- [ ] **Step 2: Commit script**
```bash
git add scripts/migrate_categories.py
git commit -m "feat: add category migration script"
```

### Task 3: Execute Migration and Verify

- [ ] **Step 1: Run migration script**
Run: `python3 scripts/migrate_categories.py`

- [ ] **Step 2: Verify a sample file (e.g., Upstage.md)**
Run: `head -n 5 wiki/Upstage.md`
Expected: `category: career` is the first line after `---`.

- [ ] **Step 3: Verify system files (e.g., index.md)**
Run: `head -n 5 wiki/index.md`
Expected: `category: system` is the first line.

- [ ] **Step 4: Commit changes**
```bash
git add wiki/*.md
git commit -m "refactor: apply category property to all wiki pages"
```
