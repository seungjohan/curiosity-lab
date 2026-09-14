---
stage: projects
category: travel
tag: projects
created: 2026-09-02
industry: Food Tech
status: active
topic:
- Travel
- Dining
- Data
type: build
concepts: [high-signal-filter, multi-signal-fusion, needle-in-haystack-retrieval]
lifecycle: building
---

> [!IMPORTANT] Key Takeaway
> **Why this matters:** The restaurant database was only ever readable by me. This is the first attempt to hand it to **someone else** — and the handoff constraint (a friend, on a phone, possibly without data) is what forced every design decision, killing Google My Maps outright.
> **How to use it:** Read the Rejected Approaches section before building any other shareable artifact from vault data — the same three failure modes (no deep-link, no offline, no import) will recur.
> **Informs:** The delivery layer for [[Michelin Filter|Michelin Filter]]; any future "give my research to a person" output.

# Trip Guide — Shareable Restaurant Map

A single self-contained HTML file holding **283 restaurants across Barcelona, Lisbon and Porto**, merged from three independent sources, searchable by dish, and sortable by distance from a typed-in location. Built to hand to a friend travelling there — not to read myself.

## The Constraint That Shaped Everything

The recipient is **a friend, not me**: no CSV literacy, on a phone, possibly roaming without data, and unwilling to install anything. Every rejected approach below failed on one of those four.

## Data Sources (three layers)

| Layer | Count | Origin | Completeness |
| :--- | ---: | :--- | :--- |
| 내가 가본 곳 | 45 | Google Maps saved-places export (658 rows → filtered to 3 cities) | Full — address, rating, price, note, 3 dishes |
| 미슐랭 · 레스폴 | 81 | `raw/extracts/all-cities-full.csv` | Full — incl. review-derived dishes for all 81 |
| 현지 가이드 | 157 | `raw/extracts/bcbm-lisboa-porto.csv` (Boa Cama Boa Mesa) | Partial — 44/157 dishes, 23/157 characteristics |

Zero overlap between the three. The Portuguese local guide and Michelin disagree about Portugal almost entirely — the same finding recorded on 2026-09-01 in [[../research/cooking/selected-restaurants|Selected Restaurants]].

### The city filter was derived, not given
The Google export has **no city or coordinate column** — only names and URLs. Cities were recovered from the Google feature IDs embedded in each URL (`1s0x{hex}:0x{hex}`): the first hex is a geographic quadtree cell, so nearby places share long prefixes. Clustering those prefixes separated Barcelona (`0x12a4a2`) from Lisbon (`0xd1933`) from Porto (`0xd2464`) — and caught near-misses that would have sent him to the wrong town (the saved Gelados Santini and 100 Montaditos pins are the **Cascais** branches; Pez Globo is in Mataró, 30km out).

## Rejected Approaches

Recording these because each one looked correct until it was tested.

**Google Maps saved lists — impossible.** Export-only. There is no import path at all; places must be saved one at a time. Dead on arrival for 283 rows.

**Google My Maps — built it, then abandoned it.** CSV import works and the map renders, but the pin popup shows **only the columns present in the CSV**, so the first import produced pins with a name and nothing else. Enriching the CSV (address, rating, price, hours) fixed the popup. What could not be fixed: **a My Maps pin is a coordinate, not a Google business listing**, so there is no path from the pin to the restaurant's actual profile — no photos, no reviews, no hours, no directions. A URL column renders as a clickable link in the desktop popup, but inside the Google Maps app the popup is truncated and the link may not fire. The whole point was "friend taps a name and sees the restaurant," and My Maps structurally cannot do that.

**Netlify Drop — rejected on retention.** Unclaimed anonymous deploys don't survive a trip. Sources disagree on the window (Vercel's docs say ~1 hour; Netlify's support forum says 24h; Netlify's own 2026 post describes suspend-then-delete after a week for the 14M unclaimed backlog) — but none of them is "the length of a holiday." A claimed free account is permanent; a file has no expiry at all, which is why the file won.

## What Shipped

A single HTML file, ~300KB, no build step, no server, no dependencies beyond a webfont that degrades gracefully.

- **Four tabs** — 내가 가본 곳 / 미슐랭·레스폴 / 현지 가이드 / 내 주변, then city chips and free-text search within each.
- **Name = Google Maps deep link.** Uses the official Maps URL API (`/maps/search/?api=1&query={name}&query_place_id={pid}`). The legacy `/maps/place/?q=place_id:` form was tried first and **did not open reliably** — the fix was passing both the name and the place ID, so place ID wins and name-search is the fallback.
- **내 주변 — typed location, not GPS.** Browser geolocation is blocked on `file://`, which kills it for an emailed file. Instead a **528-entry gazetteer is embedded in the page**: 119 hand-written landmarks (with KR/ES/PT/EN aliases), all 283 restaurant names, and ~180 street names auto-derived from the address column by averaging the coordinates of every restaurant on that street. Typing "시아두", "sagrada", "Ramiro" or a pasted `38.71, -9.14` all resolve offline; anything else falls back to a Nominatim lookup bounded to the Iberian viewbox.
- **Synonym search index.** Hidden per-card keyword expansion covering Korean spelling variants, the original-language term, and English (빠에야/파에야/paella/arroz; 뿔뽀/pulpo/polvo/octopus; 크로케타/크로켓/고로케/croquete).

## Two Failures Worth Keeping

**The dish field wasn't in the search index.** Dishes were added, then the user searched "빠에야" and got one hit. Two separate bugs stacked: `data-q` was built from name + category + address + note + badges and **never included the dish**, and the data itself said "파에야" in some rows and "쌀 요리" in others. The instinct was to add more dishes; the actual fix was indexing the field and adding a synonym layer. *A field the search doesn't read is not data — it's decoration.*

**The `Main_Menu` column was not a menu.** The plan to fill 157 dishes assumed BCBM's `Main_Menu` held signature dishes. It holds cuisine genres ("Creative", "Contemporary") — and only for 8 rows. This is why 113 of the local-guide entries still have no dish: there is no source, and the alternative (writing plausible dishes) would have put wrong orders in a friend's hands. **Left blank on purpose.** Same call made for four restaurants whose Google listing couldn't be confidently matched (Rabo d'Pêxe, Sommelier Lisbon, Cruel, Pisca — later resolved by web search) and for Marlene, where the search returns her Time Out stall rather than the flagship.

## Open Items

- **113 local-guide dishes + 134 characteristics** — needs Google review scraping at 6 places per lookup; roughly 22 more rounds.
- **Pisca (Porto)** — the guide's address and phone match a Google listing now named *Restaurante Paco*. Probably rebranded; unverified.
- **Jardín del Alma (Barcelona)** — Google lists it as *Jardí de l'Ànima*. Same venue, different name on the sign.
- **Dessert guide layer, scoped but not built** — [O Melhor Pastel de Nata](../research/cooking/selected-restaurants.md) finalists (Lisbon, 12 venues) and the historic winners of *Mejor Croissant Artesano de Mantequilla de España* (Barcelona) would add a fourth source tab. Both are already documented as guides #12/#13.

## 📁 Data Assets
| File | Rows | What it holds |
| :--- | ---: | :--- |
| [[../../raw/extracts/restaurants-final.csv\|restaurants-final.csv]] | 238 | **The merged set the guide renders** — 45 personal saves + 81 Michelin/Repsol + 157 Boa Cama Boa Mesa, zero overlap between layers. `Avg_Price_EUR` filled for 105 |
| `scripts/trip_guide/` | — | `ko.py` (Korean rewrite), `syn.py` (search synonym layer), `README.md` |

⚠️ **`scripts/trip_guide/enrich.json` is referenced in the ENRICHED log entry but is not on disk** — the Google Places enrichment (251/283 venues, dishes for 173) currently has no saved source. Re-running Places lookups would cost API calls that have already been spent.

⚠️ **113 of the 157 local-guide rows have no signature dish.** The `Main_Menu` column in the Boa Cama Boa Mesa source holds *cuisine genre* ("Creative"), not dishes, and only for 8 rows. Left blank deliberately rather than filled with invented orders.


## 🔗 Connections

### ⬆ Pipeline
- Source ← [[../research/cooking/selected-restaurants|Selected Restaurants]] — supplies the Michelin/Repsol and Boa Cama Boa Mesa layers this guide merges
- Back ← [[Michelin Filter|Michelin Filter]] — this is that project's three-tier strategy rendered as a deliverable someone else can use
- Related → [[../research/travel/index|Travel Research]] — the logistics cluster; this guide is the on-the-ground half of the voyage briefing
- Hub → [[../index|Master Index]]

<!-- AUTO-CONCEPTS:START -->
### 🔀 Concepts (auto-generated — do not edit)
- **high-signal-filter** → [[../ideation/Company Fit Finder - Where to Work]] (system), [[../ideation/Wine Value Advisor]] (system), [[Michelin Filter]] (system), [[prd/Constellate_prd]] (product), [[../research/cooking/selected-restaurants]] (cooking), [[../research/music/music-social-media]] (music)
- **multi-signal-fusion** → [[../ideation/Advance Planner]] (system), [[../ideation/Been There]] (system), [[../ideation/Chronicle - Personal Topic Timeline]] (product), [[../ideation/Company Fit Finder - Where to Work]] (system), [[../ideation/Taste Detector]] (system), [[../ideation/The Connection]] (system), [[../ideation/Triathlon Photo Finder]] (system), [[../ideation/Wine Value Advisor]] (system), [[Michelin Filter]] (system), [[prd/Chronicle_prd]] (product), [[../research/cooking/selected-restaurants]] (cooking), [[../research/system/connecting_the_dot]] (system), [[../research/system/graph-theory-foundations]] (system), [[../research/system/graphrag-connection-engine]] (system)
- **needle-in-haystack-retrieval** → [[../ideation/Advance Planner]] (system), [[../ideation/Triathlon Photo Finder]] (system), [[../ideation/Unified-Media-Insight-Capture-Tool]] (product), [[../research/system/graphrag-connection-engine]] (system)
<!-- AUTO-CONCEPTS:END -->

---
- **Subject**: [[Startup & Side Projects]]
- **Artifacts**: `scripts/trip_guide/` (build pipeline + hand-written data), `raw/extracts/all-cities-full.csv`, `raw/extracts/bcbm-lisboa-porto.csv`
