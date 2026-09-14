"""Add Website and Maps_Url links to raw/extracts/*.csv.

Website comes from three places, in priority order:
  1. what the CSV already had (Michelin wine-list scrape)
  2. the "Visit Website" link scraped off each Michelin restaurant page
  3. a hand-checked file for rows with no Michelin page (Repsol/steak-list only)

Maps_Url is built deterministically from the address, so every row gets one.
"""

import csv
import os
import sys
import urllib.parse

EXTRACTS = "raw/extracts"
CITIES = ["Barcelona", "Lisbon", "Porto"]
NEW_COLS = ["Maps_Url"]
COUNTRY = {"Barcelona": "Spain", "Lisbon": "Portugal", "Porto": "Portugal"}


def load_tsv(path):
    out = {}
    if not os.path.exists(path):
        return out
    with open(path, newline="", encoding="utf-8") as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 3 and parts[2].strip():
                out[(parts[0], parts[1])] = parts[2].strip()
    return out


def maps_url(row):
    """Google Maps search link - address when we have one, else name + city."""
    q = row["Address"].strip() or f"{row['Name']}, {row['City']}, {COUNTRY[row['City']]}"
    if row["Address"].strip():
        q = f"{row['Name']}, {q}"
    return "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(q)


def main(scraped_path, manual_path):
    scraped = load_tsv(scraped_path)
    manual = load_tsv(manual_path)
    print(f"scraped sites: {len(scraped)} | manual sites: {len(manual)}")

    all_rows, stats = [], {"kept": 0, "scraped": 0, "manual": 0, "none": 0}
    for city in CITIES:
        path = os.path.join(EXTRACTS, city.lower() + ".csv")
        with open(path, newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            fields = [f for f in reader.fieldnames if f not in NEW_COLS]
            rows = list(reader)

        for r in rows:
            key = (r["City"], r["Name"])
            if r["Website"].strip():
                stats["kept"] += 1
            elif key in scraped:
                r["Website"] = scraped[key]
                stats["scraped"] += 1
            elif key in manual:
                r["Website"] = manual[key]
                stats["manual"] += 1
            else:
                stats["none"] += 1
            r["Maps_Url"] = maps_url(r)

        out_fields = fields + NEW_COLS
        with open(path, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=out_fields)
            w.writeheader()
            w.writerows(rows)
        all_rows.extend(rows)
        print(f"{path}: {len(rows)} rows")

    path = os.path.join(EXTRACTS, "all-cities.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=out_fields)
        w.writeheader()
        w.writerows(all_rows)
    print(f"{path}: {len(all_rows)} rows\n")

    print("website source:", stats)
    missing = [r for r in all_rows if not r["Website"].strip()]
    print(f"\nstill missing a website: {len(missing)}")
    for r in missing:
        print(f"  {r['City']:10} {r['Name']}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
