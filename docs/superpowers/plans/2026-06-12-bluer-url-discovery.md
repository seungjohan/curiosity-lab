# Blue Ribbon URL Discovery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Discover restaurant URLs from Blue Ribbon Survey's search page and save them to `raw/bluer_urls.json`.

**Architecture:** Use Playwright to navigate to the search page, scroll to the bottom repeatedly to trigger infinite scroll/lazy loading, and then extract URLs matching the pattern `[data-href^='/restaurants/']`.

**Tech Stack:** Python, Playwright, scraper_venv.

---

### Task 1: Initialize Discovery Script

**Files:**
- Create: `scripts/bluer_discovery.py`

- [ ] **Step 1: Write the discovery script with scrolling logic**

```python
import json
import os
import time
from playwright.sync_api import sync_playwright

SEARCH_URL = "https://www.bluer.co.kr/search"
OUTPUT_FILE = "raw/bluer_urls.json"
BASE_URL = "https://www.bluer.co.kr"

def discover_urls():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print(f"Navigating to {SEARCH_URL}...")
        page.goto(SEARCH_URL)
        
        # Wait for the restaurant list to load
        page.wait_for_selector("[data-href^='/restaurants/']")
        
        last_count = 0
        scroll_count = 0
        max_scrolls = 100 # Adjust as needed for "dry run" or full discovery
        
        while scroll_count < max_scrolls:
            # Scroll to bottom
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2) # Wait for content to load
            
            # Count current restaurant links
            current_count = page.locator("[data-href^='/restaurants/']").count()
            print(f"Scroll {scroll_count + 1}: Found {current_count} items...")
            
            if current_count == last_count:
                # Try one more time or break
                time.sleep(3)
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                if page.locator("[data-href^='/restaurants/']").count() == last_count:
                    print("No more items loading.")
                    break
            
            last_count = current_count
            scroll_count += 1
            
            # For a dry run/testing, we might want to stop early
            if scroll_count >= 5: # Limit for dry run
                 break

        # Extract URLs
        elements = page.locator("[data-href^='/restaurants/']").all()
        urls = []
        for el in elements:
            href = el.get_attribute("data-href")
            if href:
                full_url = f"{BASE_URL}{href}"
                if full_url not in urls:
                    urls.append(full_url)
        
        print(f"Extraction complete. Total unique URLs found: {len(urls)}")
        
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(urls, f, ensure_ascii=False, indent=4)
        
        print(f"Saved to {OUTPUT_FILE}")
        browser.close()

if __name__ == "__main__":
    discover_urls()
```

- [ ] **Step 2: Run the script (Dry Run)**

Run: `scraper_venv/bin/python scripts/bluer_discovery.py`
Expected: Script runs, scrolls a few times, and creates `raw/bluer_urls.json`.

- [ ] **Step 3: Verify the output file**

Run: `ls -lh raw/bluer_urls.json`
Expected: File exists and has content.

- [ ] **Step 4: Commit the changes**

```bash
git add scripts/bluer_discovery.py raw/bluer_urls.json
git commit -m "feat(scraper): add Blue Ribbon URL discovery script and initial URLs"
```
