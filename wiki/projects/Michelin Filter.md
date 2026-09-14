---
stage: projects
category: system
tag: projects
created: 2026-05-14
industry: Food Tech
status: active
topic:
- Food
- Data
- Dining
type: research
concepts: [high-signal-filter, multi-signal-fusion, abundance-flips-value]
lifecycle: building
---

> [!IMPORTANT] Key Takeaway
> **Why this matters:** A specialized filtering strategy to find high-quality, authentic, and "reasonable" fine dining by cross-referencing global accolades with local community validation.
> **How to use it:** Apply the three-tier strategy (Global ➔ Specialized ➔ Local) when scouting for new culinary research targets.
> **Informs:** Culinary product thinking and travel intelligence.

# Michelin Filter

## Overview
A curated, data-driven list of fine dining restaurants filtered from premium sources to identify "reasonable" and high-quality culinary experiences. This project aims to bridge the gap between international prestige and local authenticity.

## The "Reasonable Fine Dining" Strategy
1. **Tier 1: Global Validation**: Filter by prestigious global associations (Michelin, World's 50 Best).
2. **Tier 2: Specialized Curation**: Focus on the **"Interesting Wine List"** category within the Michelin Guide to find restaurants with exceptional beverage programs that may be overlooked by those focusing only on stars.
3. **Tier 3: Local Verification**: Cross-reference with authoritative local community ratings to ensure the restaurant is respected by those who live there and offers genuine value.

### Tier 3 sources, by judging mechanism (2026-09-01)
Tier 3 was the thin tier — it named "local community ratings" without saying which. Mapped for Iberia, sorted by *how* they judge, because that is what makes them independent of each other:

| Source | Country | Who judges | Why it is a distinct signal |
| :--- | :--- | :--- | :--- |
| [[../../raw/guides/macarfi_spain.csv\|Guía Macarfi]] | ES | ~2,000 unpaid local *embajadores* | The structural twin of Blue Ribbon Survey — a distributed panel of committed local diners, not inspectors |
| [[../../raw/boa_cama_boa_mesa_all_editions.csv\|Boa Cama Boa Mesa]] | PT | Staff journalists touring the whole country | The only PT source with a **hotel axis** alongside restaurants |
| [[../../raw/guides/mesa_marcada_mesa_diaria.csv\|Prémios Mesa Marcada — Mesa Diária]] | PT | 309-person peer jury | Portugal's dedicated **moderate-price** award |
| [[../../raw/guides/michelin_bib_gourmand_es_pt.csv\|Michelin Bib Gourmand]] | ES + PT | Same inspectors, hard price cap | The **only** tier with an enforced ceiling (€40/3 courses in Spain) |
| Guía Repsol **Soletes** | ES + PT | Repsol staff | The everyday/affordable tier — ⚠️ **not yet captured**, app-only |

## Tier 4: Price (added 2026-09-01)
The project's whole premise is the word *"reasonable"*, but nothing in Tiers 1–3 measures spend. **Michelin publishes only a €€€€ band and never a number**, so a per-person figure had to be researched per restaurant. Three findings change how the filter should work:

1. **Bib Gourmand is the only tier that actually tracks price.** Across the 81-restaurant working set: Bib mean **€45**; Michelin Selected, Repsol 1 Sol and Repsol 2 Soles all cluster at **€70–72**. That gap is Michelin's own €40 cap showing up in the data.
2. **Award tiers are not price tiers.** Boa Cama Boa Mesa's *Garfo de Prata* spans **€30 → €185**; Michelin *Selected* spans **€32 → €160**. Neither can be used as a value filter.
3. **The real value mechanism is the `menú del día` / `menu executivo`**, not any award. The Yeatman (2★, Garfo de Platina) serves a **~€40 set lunch against a €290 tasting**; dop €20 vs €75; OMA €16 vs €70; Oníric €26 vs €80. **A lunch-price column would out-perform every award tier as a value filter.**

⚠️ **Price basis is not uniform.** Roughly half the figures are a *tasting-menu* price (the most expensive way to eat somewhere) and half a *two-course à-la-carte average* (a modest order). The `Price_Basis` column marks which. All figures are **per person, food only, drinks excluded**; wine pairings run €30–50 on top and can near-double the bill.

## Data Scope
- **Fields**: Name, Address, Location, Price, Cuisine, Coordinates, Phone, URL, Website, Awards (Michelin Stars, Green Star, Wine List Award), Local Ratings (e.g., Ribbons, Soles, Points), Facilities.
- **Added 2026-09-01**: `Avg_Price_EUR`, `Price_Basis`, `Price_Detail` (the actual menu structure, e.g. *"Herrén lunch €26; Oníric €48; Somni €80"*), `Price_Source`, `Maps_Url`.

## Gotchas found while building (do not re-learn these)
- **`michelin_scraped_full.csv` stores Iberian `Location` as a postcode**, not a city. City must be parsed from `Address` (`<street>, <City>, <postcode>, <country>`).
- **That scrape's `WebsiteUrl` is empty for all 12,730 rows** and `Latitude`/`Longitude` for all of them — but the live Michelin pages *do* carry a "Visit Website" link, and `michelin_wine_list.csv` has coordinates for all 3,490 of its rows.
- **Michelin's `Cuisine` field never says "Spanish" or "Catalan"** (only 2 rows in the Iberian set say "Portuguese"). Filtering for local cuisine by label deletes everything; it has to be read out of the description.
- **Guía Repsol names differ from Michelin names** for the same restaurant (`Estimar` / `Estimar - Rafa Zafra`, `Eldelmar` / `Eldelmar - Hermanos Torres`). Dedupe needs accent-folding *plus* prefix stripping.

## ⚠️ Finding that challenges the method (2026-09-04)
Measured across all captured guides (Michelin ★, Bib, Repsol Soles, Macarfi, Boa Cama Boa Mesa, Mesa Diária, World's 50 Best):

**83.4% of restaurants appear in exactly one guide.** Only 3.7% appear in three or more. So "cross-reference the guides", the strategy above, has very little to work with — and where it *does* work, the overlaps are between guides measuring the same thing (Michelin ★ ∩ Repsol Soles = **75%** of the smaller set; both are Spanish fine-dining establishment guides).

Worse, consensus and price move together. Across the 81-restaurant priced set:

| Listed in | n | Median price |
| :--- | ---: | ---: |
| 1 guide | 64 | **€55** |
| 2 guides | 14 | €79 *(+44%)* |
| 3 guides | 3 | €90 *(+64%)* |

**Cross-referencing is a price-raising operator, not a value-finding one.** Each additional guide that agrees adds roughly 40% to the bill. The method as written selects *against* the project's own stated goal of "reasonable".

Two controls confirm it is consensus specifically, not prestige generally:
- **Michelin absence does not make things cheap** — restaurants *not* in Michelin run slightly dearer (median €64 vs €60). It is agreement that costs, not stars.
- **Bib Gourmand (median €45) vs all other Michelin tiers (€70)** — the one tier with an enforced cap is the one tier that behaves.

**Open question this raises:** consensus is a *confidence* signal, not a *value* signal. A filter can maximise one or the other, not both. Which is this project for?


## 📁 Data Assets
Every file this project reads or produces, with what it is for. **`-full.csv` variants keep the full provenance columns; the short files are the app-facing views** — do not treat the short one as authoritative.

### Working sets — Barcelona · Lisboa · Porto
| File | Rows | What it holds |
| :--- | ---: | :--- |
| [[../../raw/extracts/all-cities-full.csv\|all-cities-full.csv]] | 81 | **Authoritative.** 21 columns — awards, cuisine, address, phone, `Avg_Price_EUR`, `Price_Detail`, `Price_Source`, `Maps_Url` |
| [[../../raw/extracts/all-cities.csv\|all-cities.csv]] | 81 | App-facing view of the same 81 |
| [[../../raw/extracts/barcelona.csv\|barcelona.csv]] · [[../../raw/extracts/lisbon.csv\|lisbon.csv]] · [[../../raw/extracts/porto.csv\|porto.csv]] | 56 · 14 · 11 | Per-city splits, same schema — one file per My Maps layer |
| [[../../raw/extracts/google-my-maps.csv\|google-my-maps.csv]] | 81 | Import-ready for mymaps.google.com (position by `Address`, title by `Name`, group by `Tier`) |
| [[../../raw/extracts/removed-1star.csv\|removed-1star.csv]] | 24 | The Michelin ★ removed in two passes, prices and links intact — restore from here, not from `unfiltered/` |
| `raw/extracts/unfiltered/` · `with-all-links/` | — | Pre-filter and pre-link-collapse snapshots |

### Boa Cama Boa Mesa
| File | Rows | What it holds |
| :--- | ---: | :--- |
| [[../../raw/boa_cama_boa_mesa_all_editions.csv\|all_editions.csv]] | 2,399 | **832 unique restaurants, 12 editions (2014-2025).** ⚠️ `Listing_Type` matters: 2016-19 rows are the *full guide* (~500-570/yr), all other years are *award winners only* (26-86/yr) |
| [[../../raw/boa_cama_boa_mesa_2026.csv\|2026.csv]] | 63 | The 2026 award layer — 39 restaurants + 22 hotels + 2 special awards |
| [[../../raw/extracts/bcbm-lisboa-porto-full.csv\|bcbm-lisboa-porto-full.csv]] | 165 | **Authoritative.** Keeps `Editions`, `Years`, `Listing_Type`, `Price_Basis`, `Price_Detail` |
| [[../../raw/extracts/bcbm-lisboa-porto.csv\|bcbm-lisboa-porto.csv]] | 165 | App-facing view (Google-enriched columns, no provenance) |
| [[../../raw/extracts/boa-cama-my-maps.csv\|boa-cama-my-maps.csv]] | 39 | The 2026 award restaurants, addressed and priced |

### Value-tier guides — one file per guide
| File | Rows | What it holds |
| :--- | ---: | :--- |
| [[../../raw/guides/michelin_bib_gourmand_es_pt.csv\|michelin_bib_gourmand_es_pt.csv]] | 223 | 197 ES + 26 PT. **The only tier with an enforced price cap** (€40/3 courses) |
| [[../../raw/guides/macarfi_spain.csv\|macarfi_spain.csv]] | 1,964 | 16 provinces. Names + provinces only — **no prices or addresses yet** |
| [[../../raw/guides/mesa_marcada_mesa_diaria.csv\|mesa_marcada_mesa_diaria.csv]] | 11 | Mesa Diária winners 2019-2025 + 2025 nominees |
| [[../../raw/melhor_pastel_de_nata.csv\|melhor_pastel_de_nata.csv]] | 33 | Single-product competition, 2009-2025 + 2026 finalists |

### Pipeline scripts
`extract_city_restaurants.py` → `filter_local_cuisine.py` → `merge_prices.py` → `add_links.py`. Run in that order; each is re-runnable.

### Known gaps
- **Guía Repsol Soletes** — not captured. Six scrape routes failed; the list is app-only and refreshes 2-3× a year (see the BLOCKED entry in [[../log|log.md]]).
- **Guía Repsol Portugal Soles** — 41 Soles + 79 *Restaurantes Guía Repsol* (2026) are documented but not yet in a file. `guia_repsol_full.csv` is **Spain-only**, which is why every Lisboa/Porto row shows blank for Repsol.
- **133 of 165** Lisboa/Porto BCBM rows still unpriced.
- **Macarfi** has no price or address layer.


## 🔗 Connections

### ⬆ Pipeline
- Back ← [[../research/cooking/selected-restaurants|Selected Restaurants]] — research supplying the ranking signals (Michelin, 50 Best, Repsol, local guides)
- Source ← [[../../raw/extracts/all-cities.csv|raw/extracts/]] — the working set: 81 Barcelona/Lisboa/Porto restaurants with per-person price, address and map link
- Source ← [[../../raw/guides/michelin_bib_gourmand_es_pt.csv|raw/guides/]] — the value-tier layer (Bib Gourmand, Macarfi, Mesa Diária), split one file per guide
- Feeds → [[../ideation/Wine Value Advisor|Wine Value Advisor]] — this project's Tier 2 wine-list flag now travels in the extract as `Notable_Wine_List`, which is that idea's first-pass filter
- Feeds → [[../ideation/Advance Planner|Advance Planner]] — the Google My Maps export is a working Travel-Planner artefact: taste-filtered places, priced and pinned, for a specific destination
- Back ← [[../ideation/Return to Basics]] — the physical-first curation thesis this project operationalizes
- Feeds → [[Trip Guide - Shareable Restaurant Map|Trip Guide]] — the three-tier strategy rendered as a deliverable someone else can actually use on a phone
- Related → [[../research/cooking/Favorite Foods|Favorite Foods]] — personal taste profile to filter against
- Hub → [[../index|Master Index]]

<!-- AUTO-CONCEPTS:START -->
### 🔀 Concepts (auto-generated — do not edit)
- **high-signal-filter** → [[../ideation/Company Fit Finder - Where to Work]] (system), [[../ideation/Wine Value Advisor]] (system), [[Trip Guide - Shareable Restaurant Map]] (travel), [[prd/Constellate_prd]] (product), [[../research/cooking/selected-restaurants]] (cooking), [[../research/music/music-social-media]] (music)
- **multi-signal-fusion** → [[../ideation/Advance Planner]] (system), [[../ideation/Been There]] (system), [[../ideation/Chronicle - Personal Topic Timeline]] (product), [[../ideation/Company Fit Finder - Where to Work]] (system), [[../ideation/Taste Detector]] (system), [[../ideation/The Connection]] (system), [[../ideation/Triathlon Photo Finder]] (system), [[../ideation/Wine Value Advisor]] (system), [[Trip Guide - Shareable Restaurant Map]] (travel), [[prd/Chronicle_prd]] (product), [[../research/cooking/selected-restaurants]] (cooking), [[../research/system/connecting_the_dot]] (system), [[../research/system/graph-theory-foundations]] (system), [[../research/system/graphrag-connection-engine]] (system)
- **abundance-flips-value** → [[../ideation/Company Fit Finder - Where to Work]] (system), [[../ideation/Private Space - The Bedroom Moved Online]] (music), [[../ideation/Return to Basics]] (system), [[../ideation/Unified-Media-Insight-Capture-Tool]] (product), [[../research/cooking/coq-au-vin]] (cooking), [[../research/cooking/soupe-a-loignon]] (cooking)
<!-- AUTO-CONCEPTS:END -->

---
- **Subject**: [[Startup & Side Projects]]
- **Source**: `raw/obsidian/startup/idea/Listing reasonable Michelin restaurants.md`
