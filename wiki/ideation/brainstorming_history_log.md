---
stage: ideation
category: system
tag: ideation
created: 2026-05-14
industry: N/A
status: active
topic:
- Activity
- History
- Wiki
type: log
---

> [!IMPORTANT] Key Takeaway
> **Why this matters:** Tracking the evolution of ideas and system changes provides a historical record of the decision-making process.
> **How to use it:** Review this log to understand the context of previous architectural or ideation shifts.
> **Informs:** Future system refinements and documentation organization.

# Operation Log

Append-only record of wiki operations (Ingest, Query, Health Check).

## [2026-06-15] Workspace Integration & Alignment
- Discussed merging brainstorming and research repositories.
- Resolved global GStack location strategy.
- Deleted redundant python virtual environments in research.
- Appended Q&A logs at the bottom of the file.

## [2026-06-03] Personal Blog & Portfolio Documentation Organization
- Organized documentation into separate files: [[PRD]], [[Design]], and [[Blog Portfolio - Figma Prompts.json]].
- Updated [[Personal Blog & Portfolio]] to act as the central hub.
- Integrated links into the [[index]].

## [2026-06-02] Personal Blog & Portfolio Initiation
- Created [[Personal Blog & Portfolio]] wiki page.
- Organized references from MJ Kang, Unan Palms, Alessandra Krick, and Sehyun Jeon.
- Integrated [[Personal Blog & Portfolio]] into [[index]] under Active Ideas.
- Started brainstorming session using Visual Companion.

## [2026-05-28] Favorite Foods & Michelin Data
- Created [[Favorite Foods]] wiki page with a "General Foodie" schema (Course, Component, Style, Vibe).
- Added first entry for [[Fideuá]] (Spain).
- Ingested **3,413** Michelin-awarded restaurants with the "Interesting wine list" award into `raw/michelin_wine_list.csv`.
- Integrated Culinary & Dining category into [[index]].
- Linked [[Favorite Foods]] with [[Michelin Filter]].

## [2026-05-15] Idea Stream Initialization
- Created [[Idea Stream]] as a dedicated space for capturing raw thoughts and evolving ideas.
- Initial entry: "Return to Fundamentals" (Farming, Food, Clothing, Shelter) in the AI age.
- Integrated [[Idea Stream]] into [[index]].

## [2026-05-15] Inspiration Sources Setup
- Created [[Inspiration Sources]] to document primary media and organizational influences (BizCafe, EO Global, Y Combinator).
- Integrated [[Inspiration Sources]] into the [[index]] under Media & Consumption.

## [2026-05-15] AI in Education Research
- Performed research on the side effects of AI in education for teenagers.
- Identified key trends: "The Generative AI Paradox," cognitive offloading, erosion of teacher-student bonds, and technostress.
- Created [[AI in Education - Side Effects]] with detailed findings and references.
- Updated [[research]] and [[index]] to include the new topic.
- Wiki Health Check: Identified broken link [[AI & Agentic Workflows]] and created stub. Identified other broken links in [[index]] for future remediation.

## [2026-05-14] Michelin Filter Refinement
- Refined [[Michelin Filter]] strategy to include Tier 2 (Michelin "Interesting Wine List") and Tier 3 (Local Community) filters.
- Added a comprehensive list of global and local restaurant associations for 14 countries (France, Spain, Italy, Japan, etc.) to [[Michelin Filter]].
- Updated [[ideation]] hub with the refined one-liner.

- Updated `GEMINI.md` to include `wiki/interests.md` as a core structural element.
- Created [[interests]] to track deep-dive subjects like Music Composition and AI.
- Linked [[interests]] in the central [[index]].

## [2026-05-14] Batch Data Ingestion
- Processed 50+ files from `raw/obsidian/`.
- Created specific subject pages for Startups: [[The Connection]], [[Triathlon Photo Finder]], [[Michelin Filter]], [[Webeing]], [[Market Analysis]], [[Startup Insights]].
- Created specific subject pages for Personal Reflections: [[Self-Reflection]], [[Relationship Lessons]], [[Career & Startup Mindset]], [[Dreams & Hobbies]], [[Social Interactions]].
- Updated [[index]] and [[brainstorming]] with the new structure.

## [2026-05-14] Schema Update
- Updated `GEMINI.md` to include "Evolution & Instruction Updates" protocol.
- Clarified `raw/` directory purpose as the source for inspirations and research data.

## [2026-05-14] Initialization
- Created project structure: `raw/`, `wiki/`.
- Initialized `GEMINI.md` with management rules.
- Created `wiki/index.md`, `wiki/Log.md`, and `wiki/brainstorming.md`.
- Bootstrapped wiki with [[llm-wiki-pattern]].

## 📜 Workspace Consolidation Discussion Logs

### Prompts & Decisions (June 15, 2026)

**Q1: Should I put GStack in each project? Can't I just put those globally so that I don't need to add those files in each project?**
- **Decision:** Yes, GStack should be global.
- **Details:** The GStack framework files (cloned in `/brainstorming/gstack`) are redundant in individual repositories. GStack's active skills live in the global configuration directory (`~/.claude/` or `~/.gemini/`). We can delete the local cloned folder once files are merged.

**Q2: Deleting Virtual Environments**
- **Decision:** Redundant python virtual environments are deleted.
- **Details:** Deleted `scraper_venv`, `test_venv`, `temp_venv`, and `venv` from `/Users/seungjohan/Obsidian/research/`, immediately freeing up **530 MB** of disk space.

**Q3: How do GStack and GBrain mention their thinking flow for ideation?**
- **Details:**
  1. **Startup Mode (YC Office Hours):** Uses six forcing questions asked one at a time (Demand Reality, Status Quo, Desperate Specificity, Narrowest Wedge, Observation & Surprise, Future-Fit) to validate user demand and build a specific target audience.
  2. **Builder Mode (Generative Design Partner):** Focuses on delight, shareability, and self-solving (generative brainstorming for hackathons/side projects).
  3. **Landscape Awareness (Search Before Building):** Uses three-layer synthesis to analyze conventional wisdom and uncover "Eureka Moments" (Layer 1: General knowledge, Layer 2: Current search discourse, Layer 3: Why it's wrong).

**Q4: What were the deleted virtual environments for, and do I need them right now?**
- **Decision:** Not needed currently.
- **Details:** The virtual environments (`scraper_venv`, `test_venv`, `temp_venv`, `venv`) contained the Python runtimes and libraries (like `requests`, `beautifulsoup4`) required by your Michelin and 50 Best restaurant scraper scripts. Since you aren't active scraping today, they are safe to delete. When we resume scripting, we will instantiate a single, consolidated `venv` at the root, saving several hundred MBs.

**Q5: How can I adjust GStack/GBrain's thinking flow into my own, or operate without them?**
**Q5: How can you adjust GStack/GBrain's thinking flow into my own, or operate without them?**
- **Details:**
  - **With GStack:** Use the `/office-hours` command in Cursor when starting a new idea. It will guide you through the forcing questions and output a clean, formatted design spec.
  - **Without GStack:** Manually write a "Pre-flight Spec" in your `wiki/projects/` directory using a simple three-question markdown template (Pain Point, Target Human, 1-Day Wedge) to validate thoughts before coding.

**Q6: Should we run GStack inside each project, and what are the structures of both projects to map them together?**
- **Decision:** GStack will be used globally and on-demand, not cloned locally in each folder.
- **Details:** Detailed mapping of the current side-by-side structure of `Obsidian/research` and `Cursor/brainstorming` was created to visualize how files (e.g., flat brainstorming notes vs. category-based research notes, raw inputs, and python scripts) will consolidate under a single separate vault.

**Q7: How can we make the directories align with the thinking flow, and what is the simple explanation of this workflow?**
- **Decision:** Align folders directly with the thinking steps: `Research (wiki/{category}/) ➔ Ideation (wiki/ideation/) ➔ Specs (wiki/projects/) ➔ Execution (scripts/) ➔ Log & Learnings (wiki/log.md)`.
- **Details:**
  1. **Simplifying the flow (ELI10):** Explained how the flow prevents coding without validation by inserting a short "Stop and Think" gate (creating a spec in `/wiki/projects/` with 3 forcing questions) before writing code in `/scripts/`.
  2. **Ideation graduation status:** Proposed keeping `wiki/ideation/ideation.md` as a central dashboard with statuses (`Researching` ➔ `Validated` ➔ `Coding`) and links to connect everything.

## 🔗 Connections
- [[../index|Master Index]]
