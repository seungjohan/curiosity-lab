"""Merge researched per-restaurant prices into raw/extracts/*.csv.

Also folds two Guia Repsol rows into their Michelin twins - Repsol lists
"Estimar - Rafa Zafra" and "Eldelmar", which did not dedup against Michelin's
"Estimar" and "Eldelmar - Hermanos Torres".
"""

import csv
import os

EXTRACTS = "raw/extracts"
PRICES = os.path.join(EXTRACTS, "prices.tsv")
CITIES = ["Barcelona", "Lisbon", "Porto"]
NEW_COLS = ["Avg_Price_EUR", "Price_Detail", "Price_Source"]

# Repsol alias -> canonical Michelin name (same restaurant, same city)
ALIASES = {"Estimar - Rafa Zafra": "Estimar", "Eldelmar": "Eldelmar - Hermanos Torres"}


def load_prices():
    prices = {}
    with open(PRICES, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            prices[(r["City"], r["Name"])] = r
    return prices


def main():
    prices = load_prices()
    missing, merged = [], []
    all_rows = []
    for city in CITIES:
        path = os.path.join(EXTRACTS, city.lower() + ".csv")
        with open(path, newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            fields = [f for f in reader.fieldnames if f not in NEW_COLS]
            rows = list(reader)

        by_name = {r["Name"]: r for r in rows}
        kept = []
        for r in rows:
            target = ALIASES.get(r["Name"])
            if target and target in by_name:
                # fold this Repsol row's award into the canonical row, then drop it
                canon = by_name[target]
                if r["Repsol_Award"] and not canon["Repsol_Award"]:
                    canon["Repsol_Award"] = r["Repsol_Award"]
                srcs = [s for s in canon["Sources"].split("; ") if s]
                for s in r["Sources"].split("; "):
                    if s and s not in srcs:
                        srcs.append(s)
                canon["Sources"] = "; ".join(srcs)
                merged.append(f"{city}: '{r['Name']}' -> '{target}'")
                continue
            p = prices.get((city, r["Name"]))
            if p:
                r["Avg_Price_EUR"] = p["Avg_EUR"]
                r["Price_Detail"] = p["Price_Detail"]
                r["Price_Source"] = p["Source"]
            else:
                r["Avg_Price_EUR"] = r["Price_Detail"] = r["Price_Source"] = ""
                missing.append(f"{city}: {r['Name']}")
            kept.append(r)

        out_fields = fields + NEW_COLS
        with open(path, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=out_fields)
            w.writeheader()
            w.writerows(kept)
        all_rows.extend(kept)
        print(f"{path}: {len(kept)} rows")

    path = os.path.join(EXTRACTS, "all-cities.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=out_fields)
        w.writeheader()
        w.writerows(all_rows)
    print(f"{path}: {len(all_rows)} rows")

    print("\nmerged duplicates:")
    for m in merged:
        print("  " + m)
    print(f"\nmissing prices: {len(missing)}")
    for m in missing:
        print("  " + m)


if __name__ == "__main__":
    main()
