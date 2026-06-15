import time
from playwright.sync_api import sync_playwright

SEARCH_URL = "https://www.bluer.co.kr/search?tabMode=single&searchWord=&ribbonType=&region=&zone=&menu=&price=&feature=&orderBy=popular"

def check_buttons():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(SEARCH_URL)
        page.wait_for_timeout(5000)
        
        print("Checking buttons:")
        btns = page.query_selector_all("button, a.btn, div.btn")
        for btn in btns:
            try:
                text = btn.inner_text().strip()
                if text:
                    print(f"  Button: [{text}]")
            except:
                pass
                
        # Check if there's a specific "show results" button that needs clicking
        # In the web_fetch, it said "식당 0 개 보기"
        # Let's see if we can find it.
        target_btn = page.query_selector("button:has-text('식당')")
        if target_btn:
            print(f"Found target button: {target_btn.inner_text()}")
            target_btn.click()
            page.wait_for_timeout(3000)
            items = page.query_selector_all("[data-href^='/restaurants/']")
            print(f"Items after clicking target button: {len(items)}")

        browser.close()

if __name__ == "__main__":
    check_buttons()
