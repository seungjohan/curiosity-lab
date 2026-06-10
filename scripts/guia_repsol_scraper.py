import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

URL = "https://www.guiarepsol.com/es/comer/soles-repsol/ediciones-de-soles-guia-repsol/"
OUTPUT_CSV = "raw/guia_repsol_full.csv"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def scrape_guia_repsol():
    print(f"Fetching {URL}...")
    try:
        response = requests.get(URL, headers=HEADERS)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    restaurants = []

    # Find the containers for each Soles category
    # Based on research, categories are under <span class="title-block-result">X Soles 2026</span>
    sections = soup.find_all('span', class_='title-block-result')
    
    if not sections:
        print("No sections found with class 'title-block-result'. Trying fallback...")
        # Fallback: some pages might use different tags or classes
        sections = soup.find_all(lambda tag: tag.name in ['span', 'h2', 'h3'] and ('Soles 2026' in tag.get_text() or '1 Sol 2026' in tag.get_text()))

    for section in sections:
        title = section.get_text(strip=True)
        if "2026" not in title:
            continue
            
        award = ""
        if "3 Soles" in title:
            award = "3 Soles"
        elif "2 Soles" in title:
            award = "2 Soles"
        elif "1 Sol" in title:
            award = "1 Sol"
        else:
            continue
            
        print(f"Processing category: {award}")
        
        # Collect all <ul> tags until the next title-block-result or end of sections
        curr = section.find_next()
        while curr:
            if curr.name == 'span' and 'title-block-result' in curr.get('class', []):
                break
            
            if curr.name == 'ul' and 'galardonados' in curr.get('class', []):
                items = curr.find_all('li')
                for item in items:
                    name_span = item.find('span', class_='name')
                    loc_span = item.find('span', class_='localidad')
                    
                    if name_span and loc_span:
                        name = name_span.get_text(strip=True)
                        city = loc_span.get_text(strip=True)
                        province = item.get('data-provincia', '')
                        
                        location = f"{city}, {province}, Spain" if province else f"{city}, Spain"
                        
                        # Avoid duplicates
                        if not any(r['Name'] == name and r['Location'] == location for r in restaurants):
                            restaurants.append({
                                "Name": name,
                                "Location": location,
                                "Award": award,
                                "Description": "",
                                "Website": ""
                            })
            curr = curr.find_next()

    if not restaurants:
        print("No restaurants found. Check if the selectors are correct.")
        return

    df = pd.DataFrame(restaurants)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Successfully saved {len(df)} restaurants to {OUTPUT_CSV}")

if __name__ == "__main__":
    if not os.path.exists("raw"):
        os.makedirs("raw")
    scrape_guia_repsol()
