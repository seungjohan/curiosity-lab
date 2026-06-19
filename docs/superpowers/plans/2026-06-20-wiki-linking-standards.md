# Wiki Linking and Organization Standards Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Clean up the restaurant database files, automate frontmatter formatting to add the `tag` property and enforce mandatory property order across all wiki files, and document new linking standards in `DESIGN.md`.

**Architecture:** 
1. Establish a test suite `tests/test_wiki_structure.py` to assert vault integrity, folder deletion, frontmatter ordering (`stage` first, `category` second, `tag` third), tag correctness, and `DESIGN.md` existence.
2. Automate frontmatter updates using a Python script `scripts/add_tag_property.py`.
3. Create the `DESIGN.md` guidelines at the root level and verify that all assertions pass.

**Tech Stack:** Python 3, PyYAML, pytest

---

## File Structure

- Create: `tests/test_wiki_structure.py` — Test suite asserting folder structure, frontmatter schemas, tag rules, and DESIGN.md content.
- Create: `scripts/add_tag_property.py` — Frontmatter migration script.
- Create: `DESIGN.md` — Root-level Markdown standards document.
- Delete: `wiki/research/cooking/restaurants/` — Bloated restaurant folder.

---

### Task 1: Create the Regression and Validation Test Suite

**Files:**
- Create: `tests/test_wiki_structure.py`

- [ ] **Step 1: Write the validation tests**
Write a pytest test suite to verify the folder deletion, frontmatter constraints, tag mapping, and DESIGN.md existence.

Write the code to `tests/test_wiki_structure.py`:
```python
import os
import re
import yaml
from pathlib import Path

WIKI_DIR = Path("wiki")

def get_frontmatter(content):
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not match:
        return None, content
    raw_yaml = match.group(1)
    body = content[match.end():]
    try:
        data = yaml.safe_load(raw_yaml)
        return data, body
    except yaml.YAMLError:
        return None, content

def test_restaurants_deleted():
    """Verify that the restaurants folder and its markdown files are deleted."""
    rest_dir = WIKI_DIR / "research" / "cooking" / "restaurants"
    assert not rest_dir.exists(), "wiki/research/cooking/restaurants directory should be deleted"

def test_frontmatter_rules():
    """Verify all wiki files follow frontmatter constraints: stage first, category second, tag third."""
    assert WIKI_DIR.exists(), "wiki directory must exist"
    
    # Exclude system/temporary directories or paths
    md_files = [p for p in WIKI_DIR.rglob("*.md") if "restaurants" not in p.parts]
    
    for filepath in md_files:
        content = filepath.read_text(encoding="utf-8")
        data, _ = get_frontmatter(content)
        
        # Files must have frontmatter
        assert data is not None, f"File {filepath} must contain valid YAML frontmatter"
        
        # Verify order of properties
        keys = list(data.keys())
        assert len(keys) >= 3, f"File {filepath} must have at least stage, category, and tag properties"
        assert keys[0] == "stage", f"File {filepath}: first key must be 'stage', got '{keys[0]}'"
        assert keys[1] == "category", f"File {filepath}: second key must be 'category', got '{keys[1]}'"
        assert keys[2] == "tag", f"File {filepath}: third key must be 'tag', got '{keys[2]}'"
        
        # Verify tag matches folder/category name rules
        expected_tag = None
        parts = filepath.relative_to(WIKI_DIR).parts
        
        if len(parts) >= 2 and parts[0] == "research":
            # wiki/research/{subfolder}/...
            expected_tag = parts[1]
        elif len(parts) >= 1 and parts[0] == "cooking":
            # wiki/cooking/...
            expected_tag = "cooking"
        elif len(parts) >= 1 and parts[0] == "projects":
            # wiki/projects/...
            expected_tag = "projects"
        elif len(parts) >= 1 and parts[0] == "ideation":
            # wiki/ideation/...
            expected_tag = "ideation"
        else:
            # Root wiki files
            expected_tag = "system"
            
        assert data["tag"] == expected_tag, f"File {filepath}: expected tag '{expected_tag}', got '{data['tag']}'"

def test_design_md_exists():
    """Verify root-level DESIGN.md exists and contains expected sections."""
    design_file = Path("DESIGN.md")
    assert design_file.exists(), "Root-level DESIGN.md must exist"
    
    content = design_file.read_text(encoding="utf-8")
    assert "# Knowledge OS: Design & Linking Standards" in content, "DESIGN.md must have standard title header"
    assert "Horizontal (Intra-Stage) Connections: MOC Hubs" in content, "DESIGN.md must document MOC Hubs"
    assert "Vertical (Cross-Stage) Connections: Hybrid Pipeline" in content, "DESIGN.md must document hybrid workflow connections"
    assert "Relative Paths" in content, "DESIGN.md must document relative paths"
    assert "Annotated Links" in content, "DESIGN.md must document annotated links"
```

- [ ] **Step 2: Run tests to verify they fail**
Run: `pytest tests/test_wiki_structure.py -v`
Expected output: Fails (restaurants directory exists, tag properties are missing, DESIGN.md is missing).

- [ ] **Step 3: Commit initial test file**
Run:
```bash
git add tests/test_wiki_structure.py
git commit -m "test: add wiki linking and frontmatter validation tests"
```

---

### Task 2: Delete the Restaurants Folder

**Files:**
- Delete: `wiki/research/cooking/restaurants/`

- [ ] **Step 1: Delete the folder**
Run: `rm -rf wiki/research/cooking/restaurants`

- [ ] **Step 2: Run pytest to check test output**
Run: `pytest tests/test_wiki_structure.py -k test_restaurants_deleted -v`
Expected output: `test_restaurants_deleted` passes. Other tests still fail.

- [ ] **Step 3: Commit deletion**
Run:
```bash
git add wiki/research/cooking/restaurants/ || true
git commit -m "style: remove individual restaurant pages from csv data to avoid bloat"
```

---

### Task 3: Implement Frontmatter Automation Script

**Files:**
- Create: `scripts/add_tag_property.py`

- [ ] **Step 1: Write migration script**
Write a Python script that iterates over every markdown file, parses the frontmatter, populates `stage`, `category`, and `tag` properties matching our folder rules, and structures them in the correct order.

Write code to `scripts/add_tag_property.py`:
```python
import os
import re
import yaml
from pathlib import Path

WIKI_DIR = Path("wiki")

def get_frontmatter(content):
    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not match:
        return None, content
    raw_yaml = match.group(1)
    body = content[match.end():]
    try:
        data = yaml.safe_load(raw_yaml)
        return data, body
    except yaml.YAMLError:
        return None, content

def get_stage_and_tag(filepath: Path):
    parts = filepath.relative_to(WIKI_DIR).parts
    
    if len(parts) >= 2 and parts[0] == "research":
        return "research", parts[1]
    elif len(parts) >= 1 and parts[0] == "cooking":
        return "cooking", "cooking"
    elif len(parts) >= 1 and parts[0] == "projects":
        return "projects", "projects"
    elif len(parts) >= 1 and parts[0] == "ideation":
        return "ideation", "ideation"
    else:
        return "general", "system"

def process_file(filepath: Path):
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return
        
    data, body = get_frontmatter(content)
    if data is None:
        data = {}
        
    stage, tag = get_stage_and_tag(filepath)
    category = data.get("category", "system")
    
    # Reconstruct dictionary to enforce strict order
    new_data = {
        "stage": stage,
        "category": category,
        "tag": tag
    }
    
    # Add other keys
    for k, v in data.items():
        if k not in ["stage", "category", "tag"]:
            new_data[k] = v
            
    # Serialize back to frontmatter
    yaml_str = yaml.dump(new_data, sort_keys=False, allow_unicode=True, default_flow_style=False)
    new_content = f"---\n{yaml_str}---\n{body}"
    
    filepath.write_text(new_content, encoding="utf-8")
    print(f"Updated: {filepath}")

def main():
    if not WIKI_DIR.exists():
        print("wiki/ directory not found.")
        return
        
    for filepath in WIKI_DIR.rglob("*.md"):
        if "restaurants" in filepath.parts:
            continue
        process_file(filepath)

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run the script to migrate all files**
Run: `python scripts/add_tag_property.py`
Expected output: Script outputs `Updated: ...` for all markdown files.

- [ ] **Step 3: Run validation tests to verify frontmatter changes**
Run: `pytest tests/test_wiki_structure.py -k test_frontmatter_rules -v`
Expected output: PASS

- [ ] **Step 4: Commit migration changes**
Run:
```bash
git add scripts/add_tag_property.py wiki/
git commit -m "feat: automate and standardize frontmatter with stage, category, and tag order"
```

---

### Task 4: Create root-level DESIGN.md File

**Files:**
- Create: `DESIGN.md`

- [ ] **Step 1: Write DESIGN.md standards file**
Write the page-to-page relative linking and MOC hub rules to the project root.

Write code to `DESIGN.md`:
```markdown
# Knowledge OS: Design & Linking Standards

This document establishes the structural and connection standards for the curiosity-lab vault. It ensures the vault serves as a highly connected, easily navigable digital garden.

## 1. Frontmatter Structure
All wiki pages must begin with standard frontmatter in the following strict order:
1. **stage**: Inferred by parent folder (research, ideation, projects, cooking, general).
2. **category**: High-level subject domain (cooking, career, music, system, etc.).
3. **tag**: String property matching the folder/category name for filtering.

Example:
```yaml
---
stage: research
category: cooking
tag: cooking
country: France
---
```

## 2. Horizontal (Intra-Stage) Connections: MOC Hubs
* Peer-to-peer pages within the same stage (e.g., two research pages) should link to each other horizontally to form context-specific threads.
* Each major category must maintain a **Map of Content (MOC)** index page (e.g., `wiki/research/cooking/index.md`) that serves as a central hub linking to all category pages.

## 3. Vertical (Cross-Stage) Connections: Hybrid Pipeline
To support the **Research ➔ Ideation ➔ Projects** workflow:
* **Research notes** link forward to relevant ideation boards or project specs.
* **Ideation notes** link back to originating research notes, and forward to promoted projects.
* **Project specs** must have a `## 🔗 Connections` section linking back to BOTH parent ideation boards and relevant research notes.

## 4. Link Formatting Rules
* **Relative Paths:** Always use relative links (e.g., `[[../research/cooking/france]]`) instead of naked filenames to guarantee link portability in Obsidian, VS Code, GitHub, and Python scripts.
* **Annotated Links:** Under the `## 🔗 Connections` section of a file, every link must include a brief, one-sentence description explaining *why* it is connected.
  * *Example:* `- [[../research/cooking/france]] — provides the technical foundation for the braising methods used here.`
```

- [ ] **Step 2: Run all tests to verify 100% compliance**
Run: `pytest tests/test_wiki_structure.py -v`
Expected output: ALL TESTS PASS.

- [ ] **Step 3: Commit the design standards**
Run:
```bash
git add DESIGN.md
git commit -m "docs: establish root-level DESIGN.md linking standards"
```
