import csv
import os
import re

WIKI_DIR = "wiki/cooking/restaurants"
WORLDS_50_CSV = "raw/worlds_50_best_full.csv"
MICHELIN_CSV = "raw/michelin_scraped_full.csv"
STEAK_101_CSV = "raw/steak_101_full.csv"
REPSOL_CSV = "raw/guia_repsol_full.csv"
SELECTED_RESTAURANTS_MD = "wiki/cooking/selected-restaurants.md"

os.makedirs(WIKI_DIR, exist_ok=True)

def slugify(name):
    s = name.lower()
    # Remove accents/special chars for basic slug
    s = re.sub(r"[^a-z0-9]", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")

def create_page(name, location, award, description, website, source_tag):
    filename = f"{slugify(name)}.md"
    filepath = os.path.join(WIKI_DIR, filename)
    
    # Extract country if possible from location
    country = "Unknown"
    if "," in location:
        parts = [p.strip() for p in location.split(",")]
        country = parts[-1]
        # Common cleanup
        if country.lower() == "usa": country = "USA"
        if country.lower() == "uk": country = "UK"
        if country.lower() == "south korea": country = "Korea"

    content = f"""---
category: cooking
type: Restaurant
country: {country}
tags: [cooking, restaurant, {source_tag}]
award: "{award}"
location: "{location}"
website: "{website}"
---

> [!IMPORTANT] Key Takeaway
> **Why this matters:** {name} is a global culinary leader with a {award} rating.
> **How to use it:** Study their unique approach to {source_tag} excellence and innovation.
> **Informs:** Culinary product thinking and sensory design.

# {name}

{description}

## 🔗 Connections
- [[wiki/cooking/index.md|Culinary Master Index]]
"""
    # Link to country page if it exists
    country_file = f"wiki/cooking/{country.lower()}.md"
    if os.path.exists(country_file):
        content += f"- [[wiki/cooking/{country.lower()}.md|{country} Cuisine]]\n"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

selected_list = []

print("Ingesting World's 50 Best...")
with open(WORLDS_50_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        if i >= 50: break
        award = f"World's 50 Best #{row['Rank']}"
        create_page(
            name=row['Name'],
            location=row['Location'],
            award=award,
            description=row['Description'],
            website=row['Website'],
            source_tag="Worlds50Best"
        )
        selected_list.append({"Name": row['Name'], "Location": row['Location'], "Award": award, "Source": "World's 50 Best"})

print("Ingesting Michelin 3 Stars...")
with open(MICHELIN_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['Award'] == "3 Stars":
            award = "3 Michelin Stars"
            create_page(
                name=row['Name'],
                location=row['Location'],
                award=award,
                description=row['Description'],
                website=row['WebsiteUrl'],
                source_tag="Michelin3Stars"
            )
            selected_list.append({"Name": row['Name'], "Location": row['Location'], "Award": award, "Source": "Michelin"})

print("Ingesting Steak 101...")
if os.path.exists(STEAK_101_CSV):
    with open(STEAK_101_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i >= 50: break
            award = f"Steak 101 #{row['Rank']}"
            create_page(
                name=row['Name'],
                location=row['Location'],
                award=award,
                description=f"{row['Name']} is ranked #{row['Rank']} in the World's 101 Best Steak Restaurants.",
                website="",
                source_tag="Steak101"
            )
            selected_list.append({"Name": row['Name'], "Location": row['Location'], "Award": award, "Source": "Steak 101"})

print("Ingesting Guia Repsol...")
if os.path.exists(REPSOL_CSV):
    with open(REPSOL_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            create_page(
                name=row['Name'],
                location=row['Location'],
                award=row['Award'],
                description=row['Description'],
                website=row['Website'],
                source_tag="GuiaRepsol"
            )
            selected_list.append({"Name": row['Name'], "Location": row['Location'], "Award": row['Award'], "Source": "Guia Repsol"})

print("Generating Selected Restaurants master list...")
with open(SELECTED_RESTAURANTS_MD, 'w', encoding='utf-8') as f:
    f.write("---\ncategory: cooking\n---\n\n# 🍴 Selected Restaurants\n\nConsolidated list of high-tier restaurants from global guides.\n\n")
    f.write("| Name | Location | Award | Source |\n")
    f.write("| :--- | :--- | :--- | :--- |\n")
    for r in selected_list:
        f.write(f"| [[wiki/cooking/restaurants/{slugify(r['Name'])}.md|{r['Name']}]] | {r['Location']} | {r['Award']} | {r['Source']} |\n")

print(f"Done! Ingested {len(selected_list)} restaurants total.")
