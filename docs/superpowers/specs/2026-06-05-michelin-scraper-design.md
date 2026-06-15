---
category: system
status: approved
date: 2026-06-05
---

# Design Spec: Michelin Global Full-Detail Scraper

## 1. Overview
A Python-based scraper to extract full details for all restaurants listed in the global Michelin Guide. The goal is to produce a single, comprehensive CSV file for analysis and integration into the Knowledge OS.

## 2. Success Criteria
- [ ] Successfully scrapes ~19,300 restaurants globally.
- [ ] Extracts name, award, price, cuisine, location, contact info, and description.
- [ ] Implements a checkpointing system to resume from interruptions.
- [ ] Adheres to rate-limiting to minimize risk of blocking.
- [ ] Outputs to `raw/michelin_global_restaurants.csv`.

## 3. Data Schema
The output CSV will contain the following columns, matching the user's `michelin_wine_list.csv` sample:

| Column | Description |
| :--- | :--- |
| `Name` | Restaurant name |
| `Address` | Full street address |
| `Location` | City, Country string |
| `Price` | Price category (e.g., €€€€) |
| `Cuisine` | Cuisine type(s) |
| `Longitude` | Geographic longitude |
| `Latitude` | Geographic latitude |
| `PhoneNumber` | Contact phone number |
| `Url` | Michelin Guide page URL |
| `WebsiteUrl` | Restaurant website URL |
| `Award` | Michelin Award (e.g., "3 Stars", "Bib Gourmand") |
| `GreenStar` | Boolean (0 or 1) indicating Green Star status |
| `FacilitiesAndServices` | Comma-separated list of amenities |
| `Description` | Michelin's editorial summary |

## 4. Technical Strategy

### Phase 1: URL Discovery
- Iterate through pagination: `https://guide.michelin.com/en/restaurants/page/[1-403]`.
- Extract unique restaurant detail URLs from each list page.
- Store discovered URLs in a temporary `raw/michelin_urls.txt` or a JSON file to track progress.

### Phase 2: Detail Scraping
- Load URLs from Phase 1.
- Visit each URL sequentially.
- Parse detail pages for the full schema.
- **Checkpointing:** Check existing `michelin_global_restaurants.csv` to skip already scraped URLs. Append new results every 10 successful scrapes.

### Anti-Blocking & Reliability
- **User-Agent:** Use a modern browser User-Agent string.
- **Rate Limiting:** Random delay between 0.5s and 1.5s per request.
- **Retries:** 3 retries for transient network errors (404, 500, timeouts).
- **Extraction:** Target specific HTML classes and data attributes identified during research.

## 5. Infrastructure
- **Language:** Python 3.x
- **Libraries:** `requests`, `BeautifulSoup4`, `pandas` (for CSV handling).
- **Location:** `scripts/michelin_global_scraper.py`
- **Output:** `raw/michelin_global_restaurants.csv`
