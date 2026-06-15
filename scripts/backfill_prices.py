import pandas as pd
import os
import re

MICHELIN_CSV = "raw/michelin_scraped_full.csv"

def map_michelin_label_to_tier(label):
    if not isinstance(label, str): return 0
    label = label.lower()
    
    if "on a budget" in label: return 1
    if "moderate spend" in label: return 2
    if "special occasion" in label: return 3
    if "spare no expense" in label: return 4
    
    if "$$$$" in label or "€€€€" in label: return 4
    if "$$$" in label or "€€€" in label: return 3
    if "$$" in label or "€€" in label: return 2
    if "$" in label or "€" in label: return 1
    
    nums = re.findall(r'\d+', label.replace(',', ''))
    if nums:
        val = int(nums[0])
        if val < 30: return 1
        if val < 80: return 2
        if val < 150: return 3
        return 4
    return 0

def backfill_michelin():
    if os.path.exists(MICHELIN_CSV):
        df = pd.read_csv(MICHELIN_CSV)
        df['Price_Tier'] = df['Price'].apply(map_michelin_label_to_tier)
        df.to_csv(MICHELIN_CSV, index=False)
        print(f"Updated {MICHELIN_CSV} with Price_Tier.")

def backfill_other_guides():
    # World's 50 Best
    w50_csv = "raw/worlds_50_best_full.csv"
    if os.path.exists(w50_csv):
        df = pd.read_csv(w50_csv)
        df['Price_Tier'] = 4
        df.to_csv(w50_csv, index=False)
        print(f"Updated {w50_csv} with Price_Tier 4.")

    # Steak 101
    steak_csv = "raw/steak_101_full.csv"
    if os.path.exists(steak_csv):
        df = pd.read_csv(steak_csv)
        df['Price_Tier'] = df.apply(lambda x: 4 if (isinstance(x.get('Rank'), (int, float)) and x['Rank'] <= 20) else 3, axis=1)
        df.to_csv(steak_csv, index=False)
        print(f"Updated {steak_csv} with estimated Price_Tiers.")

    # Guia Repsol
    repsol_csv = "raw/guia_repsol_full.csv"
    if os.path.exists(repsol_csv):
        df = pd.read_csv(repsol_csv)
        def map_repsol(award):
            if not isinstance(award, str): return 2
            if "3 Soles" in award: return 4
            if "2 Soles" in award: return 3
            return 2
        df['Price_Tier'] = df['Award'].apply(map_repsol)
        df.to_csv(repsol_csv, index=False)
        print(f"Updated {repsol_csv} with Price_Tiers based on Soles.")

if __name__ == "__main__":
    backfill_michelin()
    backfill_other_guides()
