# Guia Repsol 2026 Scraper Update Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Scrape the full list of 2026 Guia Repsol awardees (808 restaurants) and update the `raw/guia_repsol_full.csv` file.

**Architecture:** Rewrite `scripts/guia_repsol_scraper.py` to use `requests` and `BeautifulSoup` to parse the official Guia Repsol editions page. The script will iterate through the 3, 2, and 1 Soles sections and extract restaurant details.

**Tech Stack:** Python, requests, BeautifulSoup4, pandas.

---

### Task 1: Update Scraper Script

**Files:**
- Modify: `scripts/guia_repsol_scraper.py`

- [ ] **Step 1: Rewrite the scraper to fetch and parse the HTML**

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

URL = "https://www.guiarepsol.com/es/comer/soles-repsol/ediciones-de-soles-guia-repsol/"
OUTPUT_CSV = "raw/guia_repsol_full.csv"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def scrape_guia_repsol():
    print(f"Fetching {URL}...")
    response = requests.get(URL, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to fetch page: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    restaurants = []

    # Find the containers for each Soles category
    # Based on research, categories are under <span class="title-block-result">X Soles 2026</span>
    sections = soup.find_all('span', class_='title-block-result')
    
    for section in sections:
        title = section.get_text(strip=True)
        if "2026" not in title:
            continue
            
        award = ""
        if "3 Soles" in title:
            award = "3 Soles"
        elif "2 Soles" in title:
            award = "2 Soles"
        elif "1 Sol" in title:
            award = "1 Sol"
        else:
            continue
            
        print(f"Processing category: {award}")
        
        # The list follows the title block
        # Usually in a <ul> with class 'galardonados row'
        ul = section.find_next('ul', class_='galardonados')
        if not ul:
            continue
            
        items = ul.find_all('li')
        for item in items:
            name_span = item.find('span', class_='name')
            loc_span = item.find('span', class_='localidad')
            
            if name_span and loc_span:
                name = name_span.get_text(strip=True)
                city = loc_span.get_text(strip=True)
                province = item.get('data-provincia', '')
                
                location = f"{city}, {province}, Spain" if province else f"{city}, Spain"
                
                restaurants.append({
                    "Name": name,
                    "Location": location,
                    "Award": award,
                    "Description": "", # Summary page doesn't have descriptions
                    "Website": ""
                })

    df = pd.DataFrame(restaurants)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Successfully saved {len(df)} restaurants to {OUTPUT_CSV}")

if __name__ == "__main__":
    if not os.path.exists("raw"):
        os.makedirs("raw")
    scrape_guia_repsol()
```

- [ ] **Step 2: Run the scraper**

Run: `python3 scripts/guia_repsol_scraper.py`
Expected: Output showing "Successfully saved ~808 restaurants to raw/guia_repsol_full.csv"

- [ ] **Step 3: Verify the CSV content**

Run: `head -n 20 raw/guia_repsol_full.csv`
Expected: Verify headers and the first few 3 Soles restaurants (e.g., ABaC, A Tafona, etc.)

- [ ] **Step 4: Commit the changes**

```bash
git add scripts/guia_repsol_scraper.py raw/guia_repsol_full.csv
git commit -m "feat: update Guia Repsol scraper and data for 2026"
```
