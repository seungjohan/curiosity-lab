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
            
            # Find all potential restaurant items. 
            # 1-50 are in 'div.list-item', 51-100 are also in 'div.list-item' but in a different grid.
            items = soup.find_all("div", class_="list-item")
            print(f"Found {len(items)} potential items.")
            
            for item in items:
                try:
                    # Skip if it's not a restaurant (e.g. ad or info block)
                    rank_el = item.select_one(".rank")
                    if not rank_el:
                        continue
                    
                    rank = int(rank_el.text.strip())
                    
                    name_el = item.find("h2") or item.find("h3")
                    if not name_el:
                        continue
                    name = name_el.text.strip()
                    
                    location = ""
                    loc_el = item.select_one(".location") or item.select_one(".item-bottom p")
                    if loc_el:
                        location = loc_el.text.strip()
                    
                    # Detail link: it might wrap the whole item or be a button/link inside
                    link_el = item.find("a", href=True) or item.parent.find("a", href=True)
                    detail_url = ""
                    if link_el:
                        href = link_el["href"]
                        if href.startswith("/"):
                            detail_url = BASE_URL + href
                        elif href.startswith("http"):
                            detail_url = href
                    
                    # Store if we haven't seen this rank yet
                    if not any(r["Rank"] == rank for r in restaurants):
                        restaurants.append({
                            "Rank": rank,
                            "Name": name,
                            "Location": location,
                            "DetailUrl": detail_url
                        })
                            
                except Exception as e:
                    # Silently skip items that don't have rank (often ads or placeholders)
                    pass
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
