import time
from playwright.sync_api import sync_playwright

SEARCH_URL = "https://www.bluer.co.kr/search?tabMode=single&searchWord=&ribbonType=&region=&zone=&menu=&price=&feature=&orderBy=popular"

def inspect():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
        page = context.new_page()
        print(f"Navigating to {SEARCH_URL}...")
        page.goto(SEARCH_URL, wait_until="networkidle")
        time.sleep(10)  # Wait longer
        
        links = page.query_selector_all("a")
        print(f"Found {len(links)} links.")
        for link in links:
            href = link.get_attribute("href")
            if href and ("view" in href or "article" in href):
                print(f"  MATCH: {href}")
                
        # Count elements with data-href starting with /restaurants/
        items = page.query_selector_all("[data-href^='/restaurants/']")
        print(f"Found {len(items)} elements with data-href starting with '/restaurants/'")
        for item in items[:10]:
            print(f"  Data-href: {item.get_attribute('data-href')}")
            
        # Try to scroll and see if more appear
        if items:
            print("Scrolling...")
            for _ in range(3):
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(2)
            
            items_after = page.query_selector_all("[data-href^='/restaurants/']")
            print(f"Found {len(items_after)} elements after scrolling.")
            
        browser.close()

if __name__ == "__main__":
    inspect()
