import json
import os
import time
from playwright.sync_api import sync_playwright

SEARCH_URL = "https://www.bluer.co.kr/search?tabMode=single&searchWord=&ribbonType=&region=&zone=&menu=&price=&feature=&orderBy=popular"
OUTPUT_FILE = "raw/bluer_urls.json"
BASE_URL = "https://www.bluer.co.kr"

def discover_urls():
    with sync_playwright() as p:
        # Launch browser with specific options to be more robust
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        page.set_default_timeout(60000)
        
        print(f"Navigating to {SEARCH_URL}...")
        try:
            page.goto(SEARCH_URL, wait_until="networkidle", timeout=60000)
        except Exception as e:
            print(f"Initial navigation warning: {e}. Attempting to proceed...")
            
        # Wait for the restaurant list items to be present
        try:
            page.wait_for_selector("[data-href^='/restaurants/']", timeout=15000)
        except Exception as e:
            print(f"Selector timeout: {e}. Page content might be different or taking too long.")
            # Print page title and some content for debugging if it fails
            print(f"Page title: {page.title()}")
            browser.close()
            return

        last_count = 0
        scroll_count = 0
        max_scrolls = 10 # Set to 10 for a solid "dry run"
        
        while scroll_count < max_scrolls:
            # Scroll to bottom
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2) # Wait for content to load
            
            # Count current restaurant links
            current_count = page.locator("[data-href^='/restaurants/']").count()
            print(f"Scroll {scroll_count + 1}: Found {current_count} items...")
            
            if current_count == last_count:
                # Try scrolling a bit more or waiting
                page.evaluate("window.scrollBy(0, -200)") # Scroll up slightly
                time.sleep(1)
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(3)
                if page.locator("[data-href^='/restaurants/']").count() == last_count:
                    print("No more items loading.")
                    break
            
            last_count = current_count
            scroll_count += 1

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
        
        if urls:
            os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                json.dump(urls, f, ensure_ascii=False, indent=4)
            print(f"Saved {len(urls)} URLs to {OUTPUT_FILE}")
        else:
            print("No URLs found. Output file not created.")
            
        browser.close()

if __name__ == "__main__":
    discover_urls()
