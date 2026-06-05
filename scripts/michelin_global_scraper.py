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

def discover_urls(max_pages=403):
    urls = []
    if os.path.exists(URL_LOG):
        with open(URL_LOG, 'r') as f:
            urls = json.load(f)
        print(f"Loaded {len(urls)} existing URLs.")
    
    for page in range(1, max_pages + 1):
        print(f"Scraping page {page}...")
        try:
            response = requests.get(f"{LIST_URL}{page}", headers=HEADERS, timeout=10)
            if response.status_code != 200:
                print(f"Failed to load page {page}: Status {response.status_code}")
                continue
            
            soup = BeautifulSoup(response.content, "html.parser")
            cards = soup.select("div.card__menu")
            count = 0
            for card in cards:
                link_tag = card.select_one("a.link")
                if link_tag and "href" in link_tag.attrs:
                    link = link_tag["href"]
                    full_url = f"{BASE_URL}{link}"
                    if full_url not in urls:
                        urls.append(full_url)
                        count += 1
            
            print(f"Found {count} new URLs on page {page}. Total: {len(urls)}")
            
            # Save every page to be safe
            os.makedirs(os.path.dirname(URL_LOG), exist_ok=True)
            with open(URL_LOG, 'w') as f:
                json.dump(urls, f, indent=4)
                
            time.sleep(random.uniform(1, 2))
        except Exception as e:
            print(f"Error on page {page}: {e}")
            
    return urls

def parse_detail(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200: return None
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Extract data using JSON-LD for robustness
        json_ld_tag = soup.find("script", type="application/ld+json")
        data_ld = {}
        if json_ld_tag:
            try:
                # The script tag might be a list of JSON-LD objects
                loaded = json.loads(json_ld_tag.string)
                if isinstance(loaded, list):
                    data_ld = loaded[0]
                else:
                    data_ld = loaded
            except: pass
            
        res = {k: "" for k in COLUMNS}
        res["Url"] = url
        res["Name"] = data_ld.get("name") or (soup.select_one("h1.data-sheet__title").text.strip() if soup.select_one("h1.data-sheet__title") else "")
        
        # Address & Location
        addr_divs = soup.select("div.data-sheet__block--text")
        if addr_divs:
            res["Address"] = addr_divs[0].get_text(separator=" ", strip=True)
            # Location is often Country, City
            parts = res["Address"].split(",")
            if len(parts) >= 2:
                res["Location"] = f"{parts[-2].strip()}, {parts[-1].strip()}"
        
        res["Cuisine"] = data_ld.get("servesCuisine")
        res["Price"] = data_ld.get("priceRange") or (soup.select_one("div.data-sheet__title-upper-info").text.split("·")[0].strip() if soup.select_one("div.data-sheet__title-upper-info") else "")
        
        # Award logic
        award_text = data_ld.get("starRating") or data_ld.get("award", {}).get("awardFor", "")
        if not award_text and soup.select_one("div.data-sheet__classification"):
            award_text = soup.select_one("div.data-sheet__classification").text
            
        if "Three Stars" in award_text or "3 Stars" in award_text: res["Award"] = "3 Stars"
        elif "Two Stars" in award_text or "2 Stars" in award_text: res["Award"] = "2 Stars"
        elif "One Star" in award_text or "1 Star" in award_text: res["Award"] = "1 Star"
        elif "Bib Gourmand" in award_text: res["Award"] = "Bib Gourmand"
        else: res["Award"] = "Selected"
        
        # Green Star and secondary details
        res["GreenStar"] = 1 if soup.select_one("img[src*='green-star']") else 0
        geo = data_ld.get("geo", {})
        res["Latitude"] = geo.get("latitude")
        res["Longitude"] = geo.get("longitude")
        res["PhoneNumber"] = data_ld.get("telephone")
        
        web_link = soup.select_one("a[aria-label*='website']") or soup.select_one("a[data-event='link-external']")
        if web_link: res["WebsiteUrl"] = web_link["href"]
        
        desc_div = soup.select_one("div.data-sheet__description")
        res["Description"] = desc_div.text.strip() if desc_div else data_ld.get("review", {}).get("description", "")
        
        facilities = [li.text.strip() for li in soup.select("div.data-sheet__facilities li")]
        res["FacilitiesAndServices"] = ", ".join(facilities) if facilities else ""
        
        return res
    except Exception as e:
        print(f"Error parsing {url}: {e}")
        return None

def main():
    print("Michelin Global Scraper Initialized")
    # Dry run with 1 page
    discover_urls(max_pages=1)

if __name__ == "__main__":
    main()
