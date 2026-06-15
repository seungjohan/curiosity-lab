import json
import os
import time
import random
import re
import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

# Configuration
URL_LOG = "raw/bluer_urls.json"
OUTPUT_CSV = "raw/blue_ribbon_full.csv"
CHECKPOINT_INTERVAL = 10

COLUMNS = [
    "Name", "Ribbons", "Address", "Region", "Cuisine", 
    "Phone", "Price_Range", "Price_Tier", "Booking_Info", 
    "Opening_Hours", "Coordinates", "Description", "Source_Url"
]

class BlueRibbonParser:
    @staticmethod
    def map_price_to_tier(price_str):
        if not price_str: return 0
        nums = re.findall(r'[\d,]+', price_str)
        if not nums: return 0
        try:
            val = int(nums[0].replace(',', ''))
            if val < 30000: return 1
            elif val < 80000: return 2
            elif val < 200000: return 3
            else: return 4
        except: return 0

    @staticmethod
    def parse_ribbons(soup):
        # The ribbons are usually in a div.header-inner or similar
        # Looking for ribbon images
        ribbon_img = soup.select_one('img[src*="ribbon"]')
        if ribbon_img:
            src = ribbon_img.get('src', '')
            match = re.search(r'ribbon(\d)', src)
            if match: return int(match.group(1))
        
        # Check for text in ribbon container
        ribbon_box = soup.select_one('.ribbon-box, .ribbon')
        if ribbon_box:
            txt = ribbon_box.get_text()
            if '3' in txt: return 3
            if '2' in txt: return 2
            if '1' in txt: return 1
        return 0

    @staticmethod
    def parse_page(html, url):
        soup = BeautifulSoup(html, 'html.parser')
        data = {k: "" for k in COLUMNS}
        data["Source_Url"] = url
        
        # New selectors based on live site analysis
        name_tag = soup.select_one('h1.restaurant_title, div.header-inner h1, .restaurant-name')
        if not name_tag:
            # Try to get from page title as fallback
            title_tag = soup.select_one('title')
            if title_tag:
                data["Name"] = title_tag.get_text().split('|')[0].strip()
        else:
            data["Name"] = name_tag.get_text(strip=True)

        data["Ribbons"] = BlueRibbonParser.parse_ribbons(soup)
        
        # Info items (Address, Phone, etc.)
        info_items = soup.select('div.info-inner li, ul.info-list li')
        for li in info_items:
            label_tag = li.select_one('strong, span.label')
            if not label_tag: continue
            
            label = label_tag.get_text(strip=True)
            value = li.get_text(strip=True).replace(label, '').strip()
            
            if "주소" in label or "위치" in label:
                data["Address"] = value
                if value:
                    data["Region"] = value.split()[0].replace("서울특별시", "서울").replace("경기도", "경기")
            elif "전화" in label:
                data["Phone"] = value
            elif "메뉴" in label or "가격" in label:
                data["Price_Range"] = value
                data["Price_Tier"] = BlueRibbonParser.map_price_to_tier(value)
            elif "영업" in label or "시간" in label:
                data["Opening_Hours"] = value
            elif "예약" in label:
                data["Booking_Info"] = value

        # Description
        desc_tag = soup.select_one('div.review-content, .pick-text, .description')
        if desc_tag:
            data["Description"] = desc_tag.get_text(strip=True)
            
        return data

def main():
    if not os.path.exists(URL_LOG): return
    with open(URL_LOG, 'r') as f: urls = json.load(f)

    if not os.path.exists(OUTPUT_CSV):
        pd.DataFrame(columns=COLUMNS).to_csv(OUTPUT_CSV, index=False)
        processed_urls = set()
    else:
        existing_df = pd.read_csv(OUTPUT_CSV)
        processed_urls = set(existing_df['Source_Url'].dropna().tolist())

    remaining_urls = [u for u in urls if u not in processed_urls]
    if not remaining_urls: return

    batch = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        page = context.new_page()

        for i, url in enumerate(remaining_urls):
            print(f"Scraping {i+1}/{len(remaining_urls)}: {url}")
            try:
                page.goto(url, wait_until="networkidle", timeout=30000)
                time.sleep(2) # Extra wait for dynamic data
                data = BlueRibbonParser.parse_page(page.content(), url)
                if data["Name"]: # Only add if we got a name
                    batch.append(data)
                
                if len(batch) >= CHECKPOINT_INTERVAL:
                    pd.DataFrame(batch).to_csv(OUTPUT_CSV, mode='a', header=False, index=False)
                    batch = []
                    print("Checkpoint saved.")
            except Exception as e:
                print(f"Error: {e}")
            
            time.sleep(random.uniform(2, 4))
            
        if batch:
            pd.DataFrame(batch).to_csv(OUTPUT_CSV, mode='a', header=False, index=False)
        browser.close()

if __name__ == "__main__":
    main()
