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
        """
        Maps price range string to 1-4 tier.
        < 30k -> 1
        30k-80k -> 2
        80k-200k -> 3
        > 200k -> 4
        """
        if not price_str:
            return 0
        
        # Clean string and find numbers
        # Format usually: "₩11,500 ~ ₩16,000" or "10,000원 이하"
        nums = re.findall(r'[\d,]+', price_str)
        if not nums:
            return 0
            
        # Get the first number (usually the lower bound or the "under X" amount)
        try:
            val = int(nums[0].replace(',', ''))
            if val < 30000:
                return 1
            elif val < 80000:
                return 2
            elif val < 200000:
                return 3
            else:
                return 4
        except ValueError:
            return 0

    @staticmethod
    def parse_ribbons(soup):
        """Extract ribbon count (0-3) from soup."""
        # Ribbon images are typically like /images/common/ribbon1.png
        ribbon_img = soup.select_one('img[src*="ribbon"]')
        if ribbon_img:
            src = ribbon_img.get('src', '')
            match = re.search(r'ribbon(\d)', src)
            if match:
                return int(match.group(1))
        
        # Check for text fallback or NEW (which is essentially 0 ribbons but "selected")
        ribbon_text = soup.select_one('.ribbon-count')
        if ribbon_text:
            text = ribbon_text.get_text().strip()
            if '3' in text: return 3
            if '2' in text: return 2
            if '1' in text: return 1
            
        return 0

    @staticmethod
    def parse_page(html, url):
        soup = BeautifulSoup(html, 'html.parser')
        data = {k: "" for k in COLUMNS}
        data["Source_Url"] = url
        
        # Name
        name_tag = soup.select_one('h1.restaurant-name, .title, .restaurant_title')
        if name_tag:
            data["Name"] = name_tag.get_text().strip()
            
        # Ribbons
        data["Ribbons"] = BlueRibbonParser.parse_ribbons(soup)
        
        # Info blocks (Address, Phone, etc.)
        # These are usually in a list or div block
        info_list = soup.select('.info-list li, .restaurant-info p')
        for item in info_list:
            text = item.get_text(separator=" ", strip=True)
            if "위치" in text or "주소" in text:
                # Remove label and any leading colon/whitespace
                val = re.sub(r'^(위치|주소)\s*[:\s]*', '', text).strip()
                data["Address"] = val
                # Extract Region from address (e.g., "서울특별시 강남구" -> "서울")
                if data["Address"]:
                    parts = data["Address"].split()
                    if parts:
                        data["Region"] = parts[0].replace("서울특별시", "서울").replace("경기도", "경기")
            elif "전화" in text or "Tel" in text:
                data["Phone"] = re.sub(r'^(전화|Tel)\s*[:\s]*', '', text).strip()
            elif "메뉴" in text or "가격" in text or "₩" in text:
                data["Price_Range"] = re.sub(r'^(메뉴|가격)\s*[:\s]*', '', text).strip()
                data["Price_Tier"] = BlueRibbonParser.map_price_to_tier(data["Price_Range"])
            elif "시간" in text or "영업" in text:
                data["Opening_Hours"] = re.sub(r'^(시간|영업)\s*[:\s]*', '', text).strip()
            elif "예약" in text:
                data["Booking_Info"] = text.strip()

        # Description
        desc_tag = soup.select_one('.description, .review-content, .pick-text')
        if desc_tag:
            data["Description"] = desc_tag.get_text().strip()
            
        # Coordinates (Look for script tags or hidden inputs)
        # Often in window.__INITIAL_STATE__ or similar
        # For now, placeholder or try to extract from script
        scripts = soup.find_all('script')
        for s in scripts:
            if s.string and ('lat' in s.string.lower() or 'longitude' in s.string.lower()):
                lat_match = re.search(r'lat["\']?\s*[:=]\s*["\']?([\d\.]+)', s.string)
                lng_match = re.search(r'lng["\']?\s*[:=]\s*["\']?([\d\.]+)', s.string)
                if lat_match and lng_match:
                    data["Coordinates"] = f"{lat_match.group(1)}, {lng_match.group(1)}"
                    break
                    
        return data

def main():
    if not os.path.exists(URL_LOG):
        print(f"Error: {URL_LOG} not found. Run discovery first.")
        return

    with open(URL_LOG, 'r') as f:
        urls = json.load(f)

    # Initialize CSV
    if not os.path.exists(OUTPUT_CSV):
        pd.DataFrame(columns=COLUMNS).to_csv(OUTPUT_CSV, index=False)
        processed_urls = set()
    else:
        existing_df = pd.read_csv(OUTPUT_CSV)
        processed_urls = set(existing_df['Source_Url'].tolist())

    remaining_urls = [u for u in urls if u not in processed_urls]
    print(f"Total: {len(urls)}, Processed: {len(processed_urls)}, Remaining: {len(remaining_urls)}")

    if not remaining_urls:
        print("Everything processed.")
        return

    batch = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            for i, url in enumerate(remaining_urls):
                print(f"[{i+1}/{len(remaining_urls)}] Scraping: {url}")
                try:
                    page.goto(url, wait_until="networkidle", timeout=30000)
                    html = page.content()
                    data = BlueRibbonParser.parse_page(html, url)
                    batch.append(data)
                except Exception as e:
                    print(f"  Error scraping {url}: {e}")
                
                # Checkpoint
                if len(batch) >= CHECKPOINT_INTERVAL:
                    pd.DataFrame(batch).to_csv(OUTPUT_CSV, mode='a', header=False, index=False)
                    batch = []
                    print(f"  Checkpoint saved ({i+1}/{len(remaining_urls)})")
                
                # Random delay
                time.sleep(random.uniform(2, 5))
                
        finally:
            if batch:
                pd.DataFrame(batch).to_csv(OUTPUT_CSV, mode='a', header=False, index=False)
                print("  Final batch saved.")
            browser.close()

if __name__ == "__main__":
    main()
