from playwright.sync_api import sync_playwright
import time

def fetch_page(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        page.goto(url)
        time.sleep(5)  # Wait for content to load
        content = page.content()
        browser.close()
        return content

if __name__ == "__main__":
    url = "https://www.bluer.co.kr/restaurants/42661"
    html = fetch_page(url)
    with open("sample_bluer_full_2.html", "w") as f:
        f.write(html)
    print(f"Fetched {url} and saved to sample_bluer_full_2.html")
