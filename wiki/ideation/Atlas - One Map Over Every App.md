---
stage: ideation
category: product
concepts: [bridging-structural-holes, multi-signal-fusion]
lifecycle: building
---

> [!IMPORTANT] Key Takeaway
> **Why this matters:** My work is split across Obsidian, Notion, Figma, GitHub, Linear, Vercel and GA4, and nothing shows it as one picture. Every tool stores its own pieces; none of them shows how the pieces connect.
> **How to use it:** Build **Atlas**: one visual canvas whose nodes *point at* live files in other apps instead of importing them. The same nodes can be laid out as a mind map, brainstorm, workflow, process, or a 0→1 product journey.
> **Informs:** The software build (deep dive in a separate project folder). It may share an engine with [[Meeting Line - Before, During, After]] and [[../projects/prd/Constellate_prd|Constellate]].

# Atlas: One Map Over Every App

## Problem Statement: The Pieces Live Everywhere, the Picture Lives Nowhere
Building something from 0 to 1 means planning in Obsidian or Notion, designing in Figma, building through Linear with Cursor or AI agents, deploying on Vercel, and checking GA4. Brainstorms and mind maps are just as scattered. Three things go wrong:

1. **No whole view.** I can't see where a project is, or how its parts connect, without opening five apps.
2. **Finding is slow.** "Where was that file?" costs time every day.
3. **The why is lost.** Why a decision was made sits in one app, and what came of it sits in another.

## Core Product Thesis: The Map Is a View, Not a Home
- **Point, don't import.** Each node is a live link to the real thing (an Obsidian note, a Notion page, a Figma frame, a repo, a deploy). Click it and the original opens. Nothing is copied, so the map never goes stale and never becomes another silo.
- **One map, many shapes.** Mind map, brainstorm, workflow, process and timeline are *layouts* of the same nodes, not separate documents.
- **Visual like Make or n8n,** but for thinking and building, not only for automations.
- **First use case: 0→1 product development.** One map per project, from spark → research → spec → build → deploy → analytics. Brainstorms and mind maps live inside its early stages.

## 💭 Reflection: Visualizing Is the Core
It's not bad to picture my idea the way Make or n8n do. But I don't only want a workflow; visualizing can mean many things: a mind map, a brainstorming map, a workflow, a process, my whole software or product development from 0 to 1. The core part is the visualizing, and combining everything into one map. When I make a map, I want it to open the specific file easily, wherever it lives, in Obsidian, Notion or something else. Like People Chain, it combines apps, but here the focus is the one map.

## 📡 Landscape (from memory, not yet scanned)
*(Unverified. Re-check before building.)*

| Layer | Who's there | What they miss |
|:--|:--|:--|
| Canvas + embeds | Heptabase, Kosmik, Milanote, Muse, Scrintal, Obsidian Canvas, tldraw | Mostly import or copy content; tied to one app's data |
| All-in-one workspaces | Notion, Tana, Capacities, Coda | You have to move in; become another silo |
| Node-graph automation | Make, n8n, Zapier Canvas | Map automations, not thinking or projects |
| Whiteboards | Miro, FigJam | Links are static pictures, not live files |

**Where the gap looks real:** a canvas that sits *on top of* every app with live links, plus switchable layouts of the same nodes.

## Core User Flow (v1 sketch)
1. Create a map for a project (e.g. Trip Guide).
2. Add nodes by pasting a link or picking a file: an Obsidian note, Notion page, Figma file, GitHub repo, URL.
3. Connect the nodes; label each edge (feeds, blocks, became).
4. Switch the layout: mind map ↔ workflow ↔ timeline.
5. Click any node to open the original in its own app.

## Challenges
- **Integration upkeep.** Every app's API differs; some (Apple Notes, KakaoTalk) barely have one. Start with links plus local files (Obsidian).
- **"For everything" is too wide.** Lead with 0→1 product development; let the other uses follow.
- **Crowded category.** It needs a sharp answer to "why not Heptabase or Obsidian Canvas?"

## Open Questions
- ~~**Is Atlas the visual layer of Constellate, or its own product?**~~ Decided 2026-10-24: its own product (Atlas PRD D1).
- ~~**Separate app, PeopleChain feature, or Atlas for the product-development workflow?**~~ Decided 2026-10-24: inside Atlas (PRD D12).
- **Same engine as Meeting Line?** Both gather a scattered trail into one view, one for people and one for projects.
- **Who is it for first?** Me (vault + my build tools), solo builders, or small teams?
- **Should Atlas suggest links you didn't draw?** That's the Kind-2 connection idea from [[../research/system/two-kinds-of-connection]].

## 🔗 Connections

### ⬆ Pipeline
- Back ← [[sparks|✨ Spark List]]: grew from the `Product development controller` spark (2026-10-23), renamed Atlas (2026-10-24).
- Feeds → software build: `~/Cursor/atlas` (Tauri desktop app, v0.3; PRD in `prd/PRD.md`). Product development lives there as its first strong use case (PRD D12, 2026-10-24), not in a separate app or in PeopleChain.
- Sibling → [[Meeting Line - Before, During, After]]: the same "scattered trail into one view" engine, pointed at people.
- Related → [[../projects/prd/Constellate_prd|Constellate]]: possible overlap; decide whether Atlas is its visual layer.
- Hub → [[../index|Master Index]]

<!-- AUTO-CONCEPTS:START -->
### 🔀 Concepts (auto-generated — do not edit)
- **bridging-structural-holes** → [[Connecting the Dots]] (system), [[../projects/prd/Constellate_prd]] (product), [[../research/system/AI-Industry-Map-2026]] (system), [[../research/system/connecting_the_dot]] (system), [[../research/system/graph-theory-foundations]] (system), [[../research/system/graphrag-connection-engine]] (system), [[../research/system/linking-algorithms-survey]] (system), [[../research/system/two-kinds-of-connection]] (system)
- **multi-signal-fusion** → [[Advance Planner]] (system), [[Been There]] (system), [[Chronicle - Personal Topic Timeline]] (product), [[Company Fit Finder - Where to Work]] (system), [[Connecting the Dots]] (system), [[Meeting Line - Before, During, After]] (product), [[Taste Detector]] (system), [[Triathlon Photo Finder]] (system), [[Wine Value Advisor]] (system), [[../projects/Michelin Filter]] (system), [[../projects/Trip Guide - Shareable Restaurant Map]] (travel), [[../projects/prd/Chronicle_prd]] (product), [[../research/cooking/selected-restaurants]] (cooking), [[../research/system/connecting_the_dot]] (system), [[../research/system/graph-theory-foundations]] (system), [[../research/system/graphrag-connection-engine]] (system), [[../research/system/linking-algorithms-survey]] (system)
<!-- AUTO-CONCEPTS:END -->

---
- **Subject**: [[Startup & Side Projects]]
- **Source**: User idea (2026-10-23, renamed and broadened 2026-10-24)
