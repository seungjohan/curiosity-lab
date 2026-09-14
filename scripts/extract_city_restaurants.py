"""Extract restaurant rows for given cities out of the raw/ guide scrapes.

Merges Michelin (full + wine-list subset), Guia Repsol, World's 50 Best and
World's 101 Best Steak into one row per restaurant, keyed on normalised name.

Usage:  python3 scripts/extract_city_restaurants.py Barcelona Lisbon Porto
Writes: raw/extracts/<city>.csv  and  raw/extracts/all-cities.csv
"""

import csv
import os
import re
import sys
import unicodedata

RAW = "raw"
OUT_DIR = os.path.join(RAW, "extracts")

MICHELIN_FULL = os.path.join(RAW, "michelin_scraped_full.csv")
MICHELIN_WINE = os.path.join(RAW, "michelin_wine_list.csv")
REPSOL = os.path.join(RAW, "guia_repsol_full.csv")
WORLDS_50 = os.path.join(RAW, "worlds_50_best_full.csv")
STEAK_101 = os.path.join(RAW, "steak_101_full.csv")

FIELDS = [
    "City", "Name", "Michelin_Award", "Green_Star", "Repsol_Award",
    "Worlds_50_Best_Rank", "Steak_101_Rank", "Notable_Wine_List",
    "Cuisine", "Price", "Price_Tier", "Address", "Phone",
    "Latitude", "Longitude", "Michelin_Url", "Website", "Sources", "Description",
]


def norm(name):
    """Fold accents and punctuation so 'Cañeta' and 'Caneta' collapse."""
    s = unicodedata.normalize("NFKD", name or "")
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]", "", s)


def michelin_city(address):
    """Michelin addresses end '<street>, <City>, <postcode>, <Country>'."""
    parts = [p.strip() for p in (address or "").split(",")]
    return parts[-3] if len(parts) >= 3 else ""


def blank():
    return {f: "" for f in FIELDS}


def collect(cities):
    wanted = {norm(c): c for c in cities}
    out = {}  # (city, norm_name) -> row

    def slot(city, name):
        key = (city, norm(name))
        if key not in out:
            row = blank()
            row["City"], row["Name"] = city, name
            out[key] = row
        return out[key]

    def tag(row, source):
        seen = [s for s in row["Sources"].split("; ") if s]
        if source not in seen:
            seen.append(source)
        row["Sources"] = "; ".join(seen)

    # 1. Michelin full scrape - richest record, but carries no coordinates.
    with open(MICHELIN_FULL, newline="", encoding="utf-8", errors="replace") as fh:
        for r in csv.DictReader(fh):
            city = wanted.get(norm(michelin_city(r.get("Address"))))
            if not city:
                continue
            row = slot(city, (r.get("Name") or "").strip())
            row.update({
                "Michelin_Award": (r.get("Award") or "").strip(),
                "Green_Star": "yes" if (r.get("GreenStar") or "").strip() not in ("", "0", "False") else "",
                "Cuisine": (r.get("Cuisine") or "").strip(),
                "Price": (r.get("Price") or "").strip(),
                "Price_Tier": (r.get("Price_Tier") or "").strip(),
                "Address": (r.get("Address") or "").strip(),
                "Phone": (r.get("PhoneNumber") or "").strip(),
                "Michelin_Url": (r.get("Url") or "").strip(),
                "Website": (r.get("WebsiteUrl") or "").strip(),
                "Description": " ".join((r.get("Description") or "").split()),
            })
            tag(row, "Michelin")

    # 2. Wine-list subset - same schema plus usable lat/lon.
    with open(MICHELIN_WINE, newline="", encoding="utf-8", errors="replace") as fh:
        for r in csv.DictReader(fh):
            city = wanted.get(norm(michelin_city(r.get("Address"))))
            if not city:
                continue
            row = slot(city, (r.get("Name") or "").strip())
            row["Notable_Wine_List"] = "yes"
            row["Latitude"] = (r.get("Latitude") or "").strip()
            row["Longitude"] = (r.get("Longitude") or "").strip()
            for src, dst in (("Award", "Michelin_Award"), ("Cuisine", "Cuisine"),
                             ("Price", "Price"), ("Address", "Address"),
                             ("PhoneNumber", "Phone"), ("Url", "Michelin_Url"),
                             ("WebsiteUrl", "Website")):
                if not row[dst]:
                    row[dst] = (r.get(src) or "").strip()
            if not row["Description"]:
                row["Description"] = " ".join((r.get("Description") or "").split())
            tag(row, "Michelin wine list")

    # 3. Guia Repsol - Spain only, location reads '<City>, <Province>, Spain'.
    with open(REPSOL, newline="", encoding="utf-8", errors="replace") as fh:
        for r in csv.DictReader(fh):
            parts = [p.strip() for p in (r.get("Location") or "").split(",")]
            city = wanted.get(norm(parts[0])) if parts else None
            if not city:
                continue
            row = slot(city, (r.get("Name") or "").strip())
            row["Repsol_Award"] = (r.get("Award") or "").strip()
            if not row["Price_Tier"]:
                row["Price_Tier"] = (r.get("Price_Tier") or "").strip()
            if not row["Website"]:
                row["Website"] = (r.get("Website") or "").strip()
            if not row["Description"]:
                row["Description"] = " ".join((r.get("Description") or "").split())
            tag(row, "Guia Repsol")

    # 4. World's 50 Best - bare city name in Location.
    with open(WORLDS_50, newline="", encoding="utf-8", errors="replace") as fh:
        for r in csv.DictReader(fh):
            city = wanted.get(norm((r.get("Location") or "").split(",")[0]))
            if not city:
                continue
            row = slot(city, (r.get("Name") or "").strip())
            row["Worlds_50_Best_Rank"] = (r.get("Rank") or "").strip()
            if not row["Website"]:
                row["Website"] = (r.get("Website") or "").strip()
            if not row["Description"]:
                row["Description"] = " ".join((r.get("Description") or "").split())
            tag(row, "World's 50 Best")

    # 5. World's 101 Best Steak.
    with open(STEAK_101, newline="", encoding="utf-8", errors="replace") as fh:
        for r in csv.DictReader(fh):
            city = wanted.get(norm((r.get("Location") or "").split(",")[0]))
            if not city:
                continue
            row = slot(city, (r.get("Name") or "").strip())
            row["Steak_101_Rank"] = (r.get("Rank") or "").strip()
            if not row["Price_Tier"]:
                row["Price_Tier"] = (r.get("Price_Tier") or "").strip()
            tag(row, "World's 101 Best Steak")

    return out


AWARD_ORDER = {"3 Stars": 0, "2 Stars": 1, "1 Star": 2, "Bib Gourmand": 3, "Selected": 4, "": 5}


def sort_key(row):
    return (AWARD_ORDER.get(row["Michelin_Award"], 5), row["Name"].lower())


def main(cities):
    os.makedirs(OUT_DIR, exist_ok=True)
    rows = collect(cities)
    combined = []
    for city in cities:
        city_rows = sorted((r for (c, _), r in rows.items() if c == city), key=sort_key)
        path = os.path.join(OUT_DIR, city.lower().replace(" ", "-") + ".csv")
        with open(path, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=FIELDS)
            w.writeheader()
            w.writerows(city_rows)
        combined.extend(city_rows)
        print(f"{path}: {len(city_rows)} restaurants")
    path = os.path.join(OUT_DIR, "all-cities.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(combined)
    print(f"{path}: {len(combined)} restaurants")


if __name__ == "__main__":
    main(sys.argv[1:] or ["Barcelona", "Lisbon", "Porto"])
