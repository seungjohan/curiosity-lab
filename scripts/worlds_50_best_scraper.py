import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os

BASE_URL = "https://www.theworlds50best.com"
LIST_URL = f"{BASE_URL}/list/1-50"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
OUTPUT_CSV = "raw/worlds_50_best_full.csv"

def extract_list():
    print(f"Fetching list from {LIST_URL}...")
    response = requests.get(LIST_URL, headers=HEADERS)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    
    restaurants = []
    
    # The page contains multiple grids: 1-50 and 51-100
    grids = soup.find_all("div", class_="list-grid")
    
    for grid in grids:
        list_type = grid.get("data-list")
        if list_type not in ["1-50", "51-100"]:
            continue
            
        items = grid.find_all("div", class_="list-item")
        print(f"Found {len(items)} items in {list_type} grid.")
        
        for item in items:
            try:
                rank_text = item.find("p", class_="rank").text.strip()
                rank = int(rank_text)
                
                name_el = item.find("h2")
                name = name_el.text.strip()
                
                # Location is usually in the first <p> in item-bottom
                bottom_div = item.find("div", class_="item-bottom")
                location = ""
                if bottom_div:
                    loc_p = bottom_div.find("p")
                    if loc_p:
                        location = loc_p.text.strip()
                
                # Detail link - only present for some (usually top 50)
                link_el = item.find("a", href=True)
                # Note: multiple <a> tags might exist (image and name). 
                # We want the one that leads to the restaurant page.
                detail_url = ""
                if link_el:
                    href = link_el["href"]
                    if href.startswith("/"):
                        detail_url = BASE_URL + href
                    elif href.startswith("http"):
                        detail_url = href
                
                restaurants.append({
                    "Rank": rank,
                    "Name": name,
                    "Location": location,
                    "Detail URL": detail_url
                })
            except Exception as e:
                print(f"Error parsing item: {e}")
                
    return restaurants

def main():
    if not os.path.exists("raw"):
        os.makedirs("raw")
        
    restaurants = extract_list()
    if restaurants:
        df = pd.DataFrame(restaurants)
        # Sort by rank just in case
        df = df.sort_values("Rank")
        df.to_csv(OUTPUT_CSV, index=False)
        print(f"Successfully saved {len(df)} restaurants to {OUTPUT_CSV}")
    else:
        print("No restaurants found.")

if __name__ == "__main__":
    main()
