# Design Spec: Wiki Organization and Linking Standards

## 1. Objective
Optimize the curiosity-lab Knowledge OS structure by:
1. Deleting all 248 individual restaurant pages from the CSV ingestion to avoid vault bloat.
2. Automating frontmatter cleanup across all wiki files to enforce the mandatory property order (`stage` first, `category` second, `tag` third), adding the new `tag` property matching folder/category name.
3. Creating a root-level `DESIGN.md` file documenting the new page-to-page linking standards (MOC Hubs, Hybrid stage-to-stage vertical linking, Relative paths, and Annotated links).

---

## 2. Directory Changes & Cleanup
*   **Action:** Delete the directory `wiki/research/cooking/restaurants/` and all its `.md` files.
*   **Justification:** The master list of selected restaurants is maintained in a consolidated table in `wiki/cooking/selected-restaurants.md` and referenced directly from the raw CSV data. Deleting individual stub pages prevents visual and search bloat in Obsidian.

---

## 3. Frontmatter Automation & 'tag' Property
We will write a python script `scripts/add_tag_property.py` to recursively scan all `.md` files in `wiki/` (excluding deleted folders) and standardize their frontmatter.

### Frontmatter Schema Rules
The first three properties of every wiki file's frontmatter must be:
1.  **`stage`**: First property. Inferred from directory path:
    *   `wiki/research/` ➔ `research`
    *   `wiki/ideation/` ➔ `ideation`
    *   `wiki/projects/` ➔ `projects`
    *   `wiki/cooking/` ➔ `cooking`
    *   Others ➔ `general`
2.  **`category`**: Second property. Preserved from the existing frontmatter (defaulting to `system` for root wiki files if missing).
3.  **`tag`**: Third property (new). Derived from the directory structure to enable easy Obsidian filtering:
    *   `wiki/research/{subfolder}/` ➔ `{subfolder}` (e.g. `cooking`, `career`, `music`)
    *   `wiki/cooking/` ➔ `cooking`
    *   `wiki/projects/` ➔ `projects`
    *   `wiki/ideation/` ➔ `ideation`
    *   Root `wiki/` files ➔ `system`

*Any remaining custom properties (such as tags, country, industry, hq, etc.) will follow in alphabetical order.*

### Script Logic
*   Read each markdown file.
*   Parse current frontmatter using `pyyaml`.
*   Determine `stage`, `category`, and `tag` values.
*   Reconstruct the frontmatter dictionary to strictly force the order: `stage` ➔ `category` ➔ `tag` ➔ others.
*   Write back atomically to the file.

---

## 4. Root-Level Standards File (`DESIGN.md`)
We will create `/Users/seungjohan/Obsidian/curiosity-lab/DESIGN.md` containing:

```markdown
# Knowledge OS: Design & Linking Standards

This document establishes the structural and connection standards for the curiosity-lab vault. It ensures the vault serves as a highly connected, easily navigable digital garden.

## 1. Frontmatter Structure
All wiki pages must begin with standard frontmatter in the following strict order:
1. **stage**: Inferred by parent folder (research, ideation, projects, cooking, general).
2. **category**: High-level subject domain (cooking, career, music, system, etc.).
3. **tag**: String property matching the folder/category name for filtering.

Example:
\`\`\`yaml
---
stage: research
category: cooking
tag: cooking
country: France
---
\`\`\`

## 2. Horizontal (Intra-Stage) Connections: MOC Hubs
* Peer-to-peer pages within the same stage (e.g., two research pages) should link to each other horizontally to form context-specific threads.
* Each major category must maintain a **Map of Content (MOC)** index page (e.g., \`wiki/research/cooking/index.md\`) that serves as a central hub linking to all category pages.

## 3. Vertical (Cross-Stage) Connections: Hybrid Pipeline
To support the **Research ➔ Ideation ➔ Projects** workflow:
* **Research notes** link forward to relevant ideation boards or project specs.
* **Ideation notes** link back to originating research notes, and forward to promoted projects.
* **Project specs** must have a \`## 🔗 Connections\` section linking back to BOTH parent ideation boards and relevant research notes.

## 4. Link Formatting Rules
* **Relative Paths:** Always use relative links (e.g., \`[[../research/cooking/france]]\`) instead of naked filenames to guarantee link portability in Obsidian, VS Code, GitHub, and Python scripts.
* **Annotated Links:** Under the \`## 🔗 Connections\` section of a file, every link must include a brief, one-sentence description explaining *why* it is connected.
  * *Example:* \`- [[../research/cooking/france]] — provides the technical foundation for the braising methods used here.\`
```

---

## 5. Verification Plan
1. Check that the `wiki/research/cooking/restaurants/` folder is deleted and no untracked files remain.
2. Run the frontmatter linting script and examine `git diff` on representative files in different stages to ensure:
   * `stage` is the first property.
   * `category` is the second property.
   * `tag` is the third property with the correct value.
   * YAML is valid.
3. Check that the newly created `DESIGN.md` exists and contains the approved content.
