---
stage: ideation
category: system
concepts: [multi-signal-fusion, high-signal-filter]
lifecycle: researching
---

> [!IMPORTANT] Key Takeaway
> **Why this matters:** Most diners have no way to judge whether a restaurant's wine price is fair — restaurants won't share their lists, but public retail data can approximate a fair-price baseline.
> **How to use it:** Use Michelin's "Interesting Wine List" tier as the first-pass restaurant filter, then layer a public-data price estimator on top to judge and recommend specific wines.
> **Informs:** An extension of [[../projects/Michelin Filter|Michelin Filter]] — same problem (finding real value in fine dining), applied to the wine list specifically.

# Wine Value Advisor

## Overview
People rarely know what a "good" wine price is — is this bottle a fair markup, or a rip-off? Restaurants won't share their actual lists or margins, but the *inputs* that drive wine pricing (vintage year, grape variety, region, weather/catastrophe events, trade policy, country of origin) are publicly observable, and public retail/marketplace prices for the same or comparable bottles exist. This idea approximates a fair-price baseline from public data and uses it two ways.

## Two-Part Approach

### 1. Restaurant filter — reuse Michelin's "Interesting Wine List" tier
Michelin already does the hard curation work: its "Interesting Wine List" award identifies restaurants known for offering wine at *reasonable* prices. This is exactly [[../projects/Michelin Filter|Michelin Filter]]'s existing Tier 2 filter — this idea doesn't need to re-solve restaurant selection, just consume it as the first-pass filter before layering on wine-specific analysis.

### 2. Wine price/quality estimator — new
Since exact restaurant lists aren't available, estimate a fair price for a given wine from public signals:
- **Vintage year** — quality and price vary hugely year to year.
- **Grape variety & region** — baseline price/quality expectations.
- **Weather/catastrophe in that vintage** — frost, drought, or disease years shift both quality and scarcity.
- **Policy & country** — tariffs, import duty, and currency shifts move retail price independent of the wine itself.
- **Public retail/marketplace data** — big-box wine retailers, online wine shops, and public sale listings as the price-comparison baseline.

**User flow:** scan or enter a restaurant's wine list (name + listed price) → compare against the estimated fair-price index → flag good value vs. markup → optionally personalize the recommendation using a user taste profile entered in advance.

## Challenges
- **No ground truth**: restaurants won't share sourcing cost or margin — this is always a proxy estimate, never exact.
- **Price volatility drivers are numerous and noisy**: vintage quality, weather, tariffs, and currency all move independently; the estimate is only as good as how well these are fused.
- **Menu parsing**: real wine lists are inconsistently formatted and often multilingual — turning a photo/scan into structured (name, vintage, price) data is its own problem.
- **Restaurant markup varies legitimately** (service, ambiance, storage) — a "high" price isn't always unfair; the tool should flag, not accuse.

## 📊 Data Sources

### Restaurant filter (Part 1) — ready
- [[../../raw/michelin_wine_list.csv|Michelin "Interesting Wine List" (3,490 restaurants)]] — the full scraped dataset backing Part 1's restaurant filter. Source: [guide.michelin.com/.../interesting_wine_list](https://guide.michelin.com/us/en/restaurants/interesting_wine_list). Refreshed 2026-07-15 (was 3,413 on 2026-06-15; +133 newly awarded, −56 delisted).
  - **Columns:** Name, Address, Location, Price (€–€€€€, local currency), Cuisine, Longitude, Latitude, PhoneNumber, Url, WebsiteUrl, Award, GreenStar, FacilitiesAndServices, Description.
  - **Award mix:** 131 × 3-Star · 379 × 2-Star · 1,197 × 1-Star · 232 × Bib Gourmand · 1,551 × Selected. All 3,490 carry the "Interesting wine list" facility.
  - Same source family as [[../research/cooking/selected-restaurants|Selected Restaurants]].
  - *Refresh method:* headless browser (gstack `/browse`, to pass Michelin's bot protection); prior snapshot kept at `raw/michelin_wine_list.backup-2026-06-15.csv`.

### Wine estimator (Part 2) — not yet gathered
- Public wine retail/marketplace price data (e.g. Wine-Searcher, Vivino, big-box retailers) to build the fair-price baseline. *(To source.)*

## 📚 References
- [YouTube — wine pricing/value (video)](https://www.youtube.com/watch?v=hxxMY1mVpKA) — reference for how wine value/pricing is judged.
- [Wine Spectator](https://www.winespectator.com/) — wine ratings/scores and the Restaurant Wine List Awards (Award of Excellence, Best of Award of Excellence, Grand Award). Doubles as a possible restaurant-filter signal (Part 1) alongside Michelin's "Interesting Wine List" and a wine-quality reference for the estimator (Part 2).

## 🔗 Connections

### ⬆ Pipeline
- Back ← [[../projects/Michelin Filter]] — this idea extends Michelin Filter's Tier 2 "Interesting Wine List" strategy into wine-specific pricing analysis
- Related → [[../research/cooking/selected-restaurants]] — global/local guide sources already used for restaurant-side filtering
- Back ← [[ideation]] — tracked on the active ideation board

<!-- AUTO-CONCEPTS:START -->
### 🔀 Concepts (auto-generated — do not edit)
- **multi-signal-fusion** → [[Advance Planner]] (system), [[Been There]] (system), [[Chronicle - Personal Topic Timeline]] (product), [[Company Fit Finder - Where to Work]] (system), [[Taste Detector]] (system), [[The Connection]] (system), [[Triathlon Photo Finder]] (system), [[../projects/Michelin Filter]] (system), [[../projects/Trip Guide - Shareable Restaurant Map]] (travel), [[../projects/prd/Chronicle_prd]] (product), [[../research/cooking/selected-restaurants]] (cooking), [[../research/system/connecting_the_dot]] (system), [[../research/system/graph-theory-foundations]] (system), [[../research/system/graphrag-connection-engine]] (system)
- **high-signal-filter** → [[Company Fit Finder - Where to Work]] (system), [[../projects/Michelin Filter]] (system), [[../projects/Trip Guide - Shareable Restaurant Map]] (travel), [[../projects/prd/Constellate_prd]] (product), [[../research/cooking/selected-restaurants]] (cooking), [[../research/music/music-social-media]] (music)
<!-- AUTO-CONCEPTS:END -->
