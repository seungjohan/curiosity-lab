import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os

BASE_URL = "https://www.theworlds50best.com"
LIST_URLS = [
    f"{BASE_URL}/list/1-50",
    f"{BASE_URL}/list/51-100"
]
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
OUTPUT_CSV = "raw/worlds_50_best_full.csv"

def extract_list():
    restaurants = []
    
    for list_url in LIST_URLS:
        print(f"Fetching list from {list_url}...")
        try:
            response = requests.get(list_url, headers=HEADERS)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            
            # The page contains grids: 1-50 and 51-100
            grids = soup.find_all("div", class_="list-grid")
            
            for grid in grids:
                items = grid.find_all("div", class_="list-item")
                print(f"Found {len(items)} items in grid.")
                
                for item in items:
                    try:
                        rank_text = item.find("p", class_="rank").text.strip()
                        rank = int(rank_text)
                        
                        name_el = item.find("h2")
                        if not name_el:
                            continue
                        name = name_el.text.strip()
                        
                        # Location is usually in the first <p> in item-bottom
                        bottom_div = item.find("div", class_="item-bottom")
                        location = ""
                        if bottom_div:
                            loc_p = bottom_div.find("p")
                            if loc_p:
                                location = loc_p.text.strip()
                        
                        # Detail link
                        link_el = item.find("a", href=True)
                        detail_url = ""
                        if link_el:
                            href = link_el["href"]
                            if href.startswith("/"):
                                detail_url = BASE_URL + href
                            elif href.startswith("http"):
                                detail_url = href
                        
                        # Use a dict to avoid duplicates if same restaurant appears on multiple pages/grids
                        restaurant_data = {
                            "Rank": rank,
                            "Name": name,
                            "Location": location,
                            "DetailUrl": detail_url
                        }
                        
                        # Check if already added
                        if not any(r["Rank"] == rank for r in restaurants):
                            restaurants.append(restaurant_data)
                            
                    except Exception as e:
                        print(f"Error parsing item: {e}")
        except Exception as e:
            print(f"Error fetching {list_url}: {e}")
                
    return restaurants

def parse_detail(url):
    if not url: return "", ""
    print(f"  Parsing detail: {url}")
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Website selector
        website = ""
        website_tag = soup.select_one("a[aria-label*='website']")
        if website_tag:
            website = website_tag["href"]
        else:
            # Fallback for website
            for a in soup.find_all("a", href=True):
                if "website" in a.text.lower() or (a.get("aria-label") and "website" in a["aria-label"].lower()):
                    website = a["href"]
                    break
        
        # Description selector: div.content.profile contains the main text
        description = ""
        profile_div = soup.select_one("div.content.profile")
        if profile_div:
            # Get all paragraphs within the profile div that have text
            # We skip the first few (rank, city, chef) and last (address)
            paras = [p.text.strip() for p in profile_div.find_all("p") if p.text.strip()]
            
            # Filter: descriptive paragraphs usually have a decent length
            desc_paras = [p for p in paras if len(p) > 50 and not p.startswith("http")]
            
            # Join the first few meaningful paragraphs
            description = " ".join(desc_paras[:3])
        
        return website, description
    except Exception as e:
        print(f"  Error parsing {url}: {e}")
        return "", ""

def main():
    if not os.path.exists("raw"):
        os.makedirs("raw")
        
    restaurants = extract_list()
    if restaurants:
        print(f"Found {len(restaurants)} restaurants. Fetching details...")
        for r in restaurants:
            website, description = parse_detail(r["DetailUrl"])
            r["Website"] = website
            r["Description"] = description
            # Polite scraping
            time.sleep(random.uniform(1, 2))
            
        df = pd.DataFrame(restaurants)
        # Sort by rank just in case
        df = df.sort_values("Rank")
        df.to_csv(OUTPUT_CSV, index=False)
        print(f"Successfully saved {len(df)} restaurants to {OUTPUT_CSV}")
    else:
        print("No restaurants found.")

if __name__ == "__main__":
    main()
