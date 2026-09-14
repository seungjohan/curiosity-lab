"""Filter raw/extracts/*.csv down to locally-rooted, reachable restaurants.

Rules:
  - drop every 3 Stars and 2 Stars row
  - drop 1 Star and Selected rows whose cooking is not Spanish/Catalan
    (Barcelona) or Portuguese (Lisbon, Porto)
  - keep every Bib Gourmand
  - keep every non-Michelin row (Guia Repsol picks, World's 101 Best Steak)

Cuisine calls come from reading each Michelin description, not from the
Cuisine label alone - the label never says "Spanish" or "Catalan".
Originals are preserved under raw/extracts/unfiltered/.
"""

import csv
import os
import shutil

EXTRACTS = "raw/extracts"
BACKUP = os.path.join(EXTRACTS, "unfiltered")
CITIES = ["Barcelona", "Lisbon", "Porto"]

DROP_TIERS = {"3 Stars", "2 Stars"}

# name -> why it is not local cooking
NOT_LOCAL = {
    # Barcelona, 1 Star
    "Caelis": "French - chef Romain Fornell",
    "COME by Paco Méndez": "Mexican",
    "Dos Palillos": "Asian/Japanese tapas fusion",
    "Fishølogy": "Italian chefs, Nordic-Greek concept",
    "Kamikaze": "Asian/Chinese fusion",
    "Koy Shunka": "Japanese",
    "MAE Barcelona": "pan-Latin syncretism (Costa Rica/Colombia/Spain)",
    "Slow & Low": "World Cuisine - Mexican, Thai, Argentine",
    "Suto": "Japanese",
    # Barcelona, Selected
    "Ají": "Nikkei - Japanese/Peruvian",
    "Albé": "Lebanese touches, Mexican executive chef",
    "Contraban": "classical French cuisine",
    "Fronda Pasaje": "Argentine chef, plant-based",
    "Jiribilla": "Mexican",
    "Maymanta": "Peruvian",
    "âme": "French Contemporary",
    # Lisbon, 1 Star
    "EPUR": "French - chef Vincent Farges",
    "Grenache": "French Contemporary",
    "Kabuki Lisboa": "Japanese",
    "Kanazawa": "Japanese",
    "YŌSO": "Japanese",
    # Lisbon, Selected
    "Downunder by Justin Jennings": "Australian Contemporary",
    "Eleven": "German chef, Mediterranean-inspired",
    "Omakase Wa": "Japanese",
    "Oven": "Nepali",
    "Salta": "Asian/Central American fusion",
    # Porto, 1 Star
    "Le Monument": "French - chef Julien Montbabut",
    # Porto, Selected
    "Cafeína": "International/French",
    "Izakaya Japanese Cuisine": "Japanese",
    "Kaigi": "Japanese",
    "Tokkotai": "Japanese",
}

CUISINE_FILTERED = {"1 Star", "Selected"}


def keep(row):
    award = row["Michelin_Award"]
    if award in DROP_TIERS:
        return False, f"{award} - too formal"
    if award in CUISINE_FILTERED and row["Name"] in NOT_LOCAL:
        return False, NOT_LOCAL[row["Name"]]
    return True, ""


def main():
    os.makedirs(BACKUP, exist_ok=True)
    dropped = []
    combined = []
    for city in CITIES:
        name = city.lower() + ".csv"
        src = os.path.join(EXTRACTS, name)
        if not os.path.exists(os.path.join(BACKUP, name)):
            shutil.copy2(src, os.path.join(BACKUP, name))
        with open(os.path.join(BACKUP, name), newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            fields = reader.fieldnames
            rows = list(reader)
        kept = []
        for r in rows:
            ok, why = keep(r)
            (kept if ok else dropped).append(r if ok else (city, r["Name"], r["Michelin_Award"], why))
        with open(src, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=fields)
            w.writeheader()
            w.writerows(kept)
        combined.extend(kept)
        print(f"{src}: {len(rows)} -> {len(kept)}")
    all_src = os.path.join(EXTRACTS, "all-cities.csv")
    if not os.path.exists(os.path.join(BACKUP, "all-cities.csv")):
        shutil.copy2(all_src, os.path.join(BACKUP, "all-cities.csv"))
    with open(all_src, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(combined)
    print(f"{all_src}: {len(combined)} total\n")
    print(f"dropped {len(dropped)}:")
    for city, n, award, why in dropped:
        print(f"  {city:10} {n[:30]:32} {award or '-':13} {why}")


if __name__ == "__main__":
    main()
