import csv
import os
import re

WIKI_DIR = "wiki/cooking/restaurants"
WORLDS_50_CSV = "raw/worlds_50_best_full.csv"
MICHELIN_CSV = "raw/michelin_scraped_full.csv"
STEAK_101_CSV = "raw/steak_101_full.csv"
REPSOL_CSV = "raw/guia_repsol_full.csv"
SELECTED_RESTAURANTS_MD = "wiki/cooking/selected-restaurants.md"

def slugify(name):
    s = name.lower()
    # Remove accents/special chars for basic slug
    s = re.sub(r"[^a-z0-9]", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")

selected_list = []

print("Ingesting World's 50 Best...")
with open(WORLDS_50_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        if i >= 50: break
        award = f"World's 50 Best #{row['Rank']}"
        selected_list.append({"Name": row['Name'], "Location": row['Location'], "Award": award, "Source": "World's 50 Best"})

print("Ingesting Michelin 3 Stars...")
with open(MICHELIN_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['Award'] == "3 Stars":
            award = "3 Michelin Stars"
            selected_list.append({"Name": row['Name'], "Location": row['Location'], "Award": award, "Source": "Michelin"})

print("Ingesting Steak 101...")
if os.path.exists(STEAK_101_CSV):
    with open(STEAK_101_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i >= 50: break
            award = f"Steak 101 #{row['Rank']}"
            selected_list.append({"Name": row['Name'], "Location": row['Location'], "Award": award, "Source": "Steak 101"})

print("Ingesting Guia Repsol...")
if os.path.exists(REPSOL_CSV):
    with open(REPSOL_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            selected_list.append({"Name": row['Name'], "Location": row['Location'], "Award": row['Award'], "Source": "Guia Repsol"})

print("Generating Selected Restaurants master list...")
with open(SELECTED_RESTAURANTS_MD, 'w', encoding='utf-8') as f:
    f.write("""---
category: cooking
---

> [!IMPORTANT] Key Takeaway
> **Why this matters:** This consolidated list allows for cross-guide comparison and strategy development for 'reasonable fine dining'.
> **How to use it:** Use this as a reference for selecting restaurants that meet multiple validation criteria.
> **Informs:** [[wiki/projects/Michelin Filter.md|Michelin Filter Project]]

# 🍴 Selected Restaurants

Consolidated list of high-tier restaurants from global guides.

""")
    f.write("| Name | Location | Award | Source |\n")
    f.write("| :--- | :--- | :--- | :--- |\n")
    for r in selected_list:
        f.write(f"| {r['Name']} | {r['Location']} | {r['Award']} | {r['Source']} |\n")
    
    f.write("\n## 🔗 Connections\n")
    f.write("- [[wiki/cooking/index.md|Culinary Master Index]]\n")
    f.write("- [[wiki/projects/Michelin Filter.md|Michelin Filter Project]]\n")

print(f"Done! Ingested {len(selected_list)} restaurants total.")


print(f"Done! Ingested {len(selected_list)} restaurants total.")
