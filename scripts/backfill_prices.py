import pandas as pd
import os
import re

MICHELIN_CSV = "raw/michelin_scraped_full.csv"

def map_michelin_label_to_tier(label):
    if not isinstance(label, str): return 0
    label = label.lower()
    
    # Michelin specific labels
    if "on a budget" in label: return 1
    if "moderate spend" in label: return 2
    if "special occasion" in label: return 3
    if "spare no expense" in label: return 4
    
    # Currency symbols fallback
    if "$$$$" in label or "€€€€" in label: return 4
    if "$$$" in label or "€€€" in label: return 3
    if "$$" in label or "€€" in label: return 2
    if "$" in label or "€" in label: return 1
    
    # Range fallback (e.g. "€30 - €60")
    nums = re.findall(r'\d+', label.replace(',', ''))
    if nums:
        val = int(nums[0])
        # Crude conversion for EUR/USD/GBP to KRW-like scale
        if val < 30: return 1
        if val < 80: return 2
        if val < 150: return 3
        return 4
        
    return 0

def backfill_michelin():
    if not os.path.exists(MICHELIN_CSV):
        print(f"{MICHELIN_CSV} not found.")
        return

    df = pd.read_csv(MICHELIN_CSV)
    print(f"Loaded {len(df)} restaurants from Michelin.")
    
    # Apply mapping
    df['Price_Tier'] = df['Price'].apply(map_michelin_label_to_tier)
    
    # Save back
    df.to_csv(MICHELIN_CSV, index=False)
    print(f"Updated {MICHELIN_CSV} with Price_Tier column.")
    print(df['Price_Tier'].value_counts())

if __name__ == "__main__":
    backfill_michelin()
