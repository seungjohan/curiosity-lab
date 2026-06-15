# World's 50 Best Restaurants Scraper Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Python scraper to extract Rank, Name, Location, Website, and Description for the World's 50 Best Restaurants into a CSV.

**Architecture:** A two-stage sequential scraper: 1) Scrape the main list page for basic info and detail URLs, 2) Visit each detail URL for the website and editorial summary.

**Tech Stack:** Python, `requests`, `BeautifulSoup4`, `pandas`.

---

### Task 1: Script Initialization and List Extraction

**Files:**
- Create: `scripts/worlds_50_best_scraper.py`

- [ ] **Step 1: Initialize script with constants and main list parser**
Implement the `extract_list()` function to get the 1-100 list data.

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os

BASE_URL = "https://www.theworlds50best.com"
LIST_URL = f"{BASE_URL}/list/1-50"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
OUTPUT_CSV = "raw/worlds_50_best_full.csv"

def extract_list():
    response = requests.get(LIST_URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    
    restaurants = []
    # Selectors based on the site structure (Rank, Name, Location, Detail Link)
    items = soup.select("div.item") # Placeholder, need to verify
    for item in items:
        rank = item.select_one(".rank").text.strip()
        name = item.select_one("h2").text.strip()
        location = item.select_one(".location").text.strip()
        detail_link = item.select_one("a")["href"]
        restaurants.append({
            "Rank": rank,
            "Name": name,
            "Location": location,
            "DetailUrl": f"{BASE_URL}{detail_link}" if detail_link.startswith("/") else detail_link
        })
    return restaurants
```

- [ ] **Step 2: Commit**
```bash
git add scripts/worlds_50_best_scraper.py
git commit -m "chore: initialize worlds 50 best scraper and list parser"
```

---

### Task 2: Detail Parser and Main Loop

**Files:**
- Modify: `scripts/worlds_50_best_scraper.py`

- [ ] **Step 1: Implement detail parser and execution loop**
Add `parse_detail(url)` and the `main()` function.

```python
def parse_detail(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        
        website = soup.select_one("a[aria-label*='website']")["href"] # Verify selector
        description = soup.select_one(".description").text.strip() # Verify selector
        
        return website, description
    except Exception as e:
        print(f"Error parsing {url}: {e}")
        return "", ""

def main():
    print("Fetching the list...")
    restaurants = extract_list()
    
    full_data = []
    for i, res in enumerate(restaurants):
        print(f"[{i+1}/{len(restaurants)}] Parsing {res['Name']}...")
        website, description = parse_detail(res["DetailUrl"])
        res["Website"] = website
        res["Description"] = description
        full_data.append(res)
        time.sleep(random.uniform(1, 2))
        
    df = pd.DataFrame(full_data)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Done! Saved to {OUTPUT_CSV}")
```

- [ ] **Step 2: Commit**
```bash
git commit -am "feat: implement detail parsing and main loop for 50 best scraper"
```
