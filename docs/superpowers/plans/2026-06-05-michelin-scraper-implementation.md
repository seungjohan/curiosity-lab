# Michelin Global Full-Detail Scraper Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a robust, sequential Python scraper to extract full details for ~19,300 Michelin Guide restaurants into a CSV matching a specific format.

**Architecture:** A two-phase approach: 1) URL discovery via pagination, 2) Detail extraction with checkpointing/incremental saving.

**Tech Stack:** Python, `requests`, `BeautifulSoup4`, `pandas`.

---

### Task 1: Environment and Project Structure

**Files:**
- Create: `scripts/michelin_global_scraper.py`
- Create: `scripts/requirements.txt`

- [ ] **Step 1: Create requirements file**
```text
requests
beautifulsoup4
pandas
```

- [ ] **Step 2: Initialize scraper script with boilerplate and constants**
Include User-Agent, Base URLs, and the Column headers matching `michelin_wine_list.csv`.

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os
import json

BASE_URL = "https://guide.michelin.com"
LIST_URL = f"{BASE_URL}/en/restaurants/page/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
COLUMNS = [
    "Name", "Address", "Location", "Price", "Cuisine", 
    "Longitude", "Latitude", "PhoneNumber", "Url", 
    "WebsiteUrl", "Award", "GreenStar", "FacilitiesAndServices", "Description"
]
OUTPUT_CSV = "raw/michelin_global_restaurants.csv"
URL_LOG = "raw/michelin_urls.json"
```

- [ ] **Step 3: Commit**
```bash
git add scripts/requirements.txt scripts/michelin_global_scraper.py
git commit -m "chore: initialize michelin scraper environment"
```

---

### Task 2: Phase 1 - URL Discovery

**Files:**
- Modify: `scripts/michelin_global_scraper.py`

- [ ] **Step 1: Implement pagination crawler**
Add a function `discover_urls(max_pages=403)` that scrapes the restaurant links from each page and saves them to `raw/michelin_urls.json`.

```python
def discover_urls(max_pages=403):
    urls = []
    if os.path.exists(URL_LOG):
        with open(URL_LOG, 'r') as f:
            urls = json.load(f)
        print(f"Loaded {len(urls)} existing URLs.")
    
    start_page = (len(urls) // 20) + 1 # Rough estimate if we stopped early
    
    for page in range(1, max_pages + 1):
        print(f"Scraping page {page}...")
        response = requests.get(f"{LIST_URL}{page}", headers=HEADERS)
        if response.status_code != 200:
            print(f"Failed to load page {page}")
            continue
        
        soup = BeautifulSoup(response.content, "html.parser")
        cards = soup.select("div.card__menu")
        for card in cards:
            link = card.select_one("a")["href"]
            full_url = f"{BASE_URL}{link}"
            if full_url not in urls:
                urls.append(full_url)
        
        # Save every page to be safe
        with open(URL_LOG, 'w') as f:
            json.dump(urls, f)
            
        time.sleep(random.uniform(1, 2))
    return urls
```

- [ ] **Step 2: Test URL discovery (Dry run)**
Run: `python3 scripts/michelin_global_scraper.py` (modified to just call `discover_urls(max_pages=1)`)
Expected: `raw/michelin_urls.json` contains ~20-40 URLs.

- [ ] **Step 3: Commit**
```bash
git commit -am "feat: implement URL discovery phase"
```

---

### Task 3: Phase 2 - Detail Extraction Parser

**Files:**
- Modify: `scripts/michelin_global_scraper.py`

- [ ] **Step 1: Implement the detail parser**
Create `parse_detail(url)` that returns a dictionary matching the schema.

```python
def parse_detail(url):
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200: return None
    
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Example selectors (need verification during implementation)
    name = soup.select_one("h1.restaurant-details__name").text.strip()
    address = soup.select_one("li.restaurant-details__address").text.strip()
    
    # Award logic
    award = "Selected"
    if soup.select_one("img[src*='1star']"): award = "1 Star"
    elif soup.select_one("img[src*='2star']"): award = "2 Stars"
    elif soup.select_one("img[src*='3star']"): award = "3 Stars"
    elif soup.select_one("img[src*='bib-gourmand']"): award = "Bib Gourmand"
    
    # Price & Cuisine
    price_cuisine = soup.select_one("li.restaurant-details__price-cuisine").text.strip().split("·")
    price = price_cuisine[0].strip()
    cuisine = price_cuisine[1].strip() if len(price_cuisine) > 1 else ""
    
    # Description
    description = soup.select_one("div.restaurant-details__description--content").text.strip()
    
    # Coordinates (often in google maps link or json-ld)
    # Facilities, Phone, Website...
    
    return {
        "Name": name, "Address": address, "Url": url, 
        "Award": award, "Price": price, "Cuisine": cuisine,
        "Description": description, 
        # ... rest of fields
    }
```

- [ ] **Step 2: Commit**
```bash
git commit -am "feat: add detail page parser"
```

---

### Task 4: Checkpointing and Main Loop

**Files:**
- Modify: `scripts/michelin_global_scraper.py`

- [ ] **Step 1: Implement the main execution loop**
Load URLs, check `raw/michelin_global_restaurants.csv` for progress, and append results.

```python
def main():
    urls = discover_urls()
    
    if not os.path.exists(OUTPUT_CSV):
        pd.DataFrame(columns=COLUMNS).to_csv(OUTPUT_CSV, index=False)
    
    existing_df = pd.read_csv(OUTPUT_CSV)
    processed_urls = set(existing_df['Url'].tolist())
    
    batch = []
    for url in urls:
        if url in processed_urls: continue
        
        print(f"Scraping details for: {url}")
        data = parse_detail(url)
        if data:
            batch.append(data)
            processed_urls.add(url)
        
        if len(batch) >= 10:
            pd.DataFrame(batch).to_csv(OUTPUT_CSV, mode='a', header=False, index=False)
            batch = []
            print("Checkpoint saved.")
        
        time.sleep(random.uniform(0.5, 1.5))
    
    if batch:
        pd.DataFrame(batch).to_csv(OUTPUT_CSV, mode='a', header=False, index=False)
```

- [ ] **Step 2: Final Commit**
```bash
git commit -am "feat: complete scraper with checkpointing"
```
