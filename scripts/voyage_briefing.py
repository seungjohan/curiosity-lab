import pandas as pd
import os
import sys

# File Paths
MICHELIN_CSV = "raw/michelin_scraped_full.csv"
BLUER_CSV = "raw/blue_ribbon_full.csv"
WORLDS_50_CSV = "raw/worlds_50_best_full.csv"
STEAK_101_CSV = "raw/steak_101_full.csv"
REPSOL_CSV = "raw/guia_repsol_full.csv"

def search_restaurants(location):
    location = location.lower()
    all_matches = []

    # 1. Search Michelin
    if os.path.exists(MICHELIN_CSV):
        df = pd.read_csv(MICHELIN_CSV)
        matches = df[df['Location'].str.contains(location, case=False, na=False) | 
                    df['Address'].str.contains(location, case=False, na=False)]
        for _, row in matches.iterrows():
            all_matches.append({
                "Name": row['Name'],
                "Award": row['Award'],
                "Tier": row.get('Price_Tier', 0),
                "Source": "Michelin",
                "Info": f"Booking: {row.get('PhoneNumber', 'Contact info needed')}",
                "Booking_Req": "Check website" if row['Award'] == "3 Stars" else "Unknown"
            })

    # 2. Search Blue Ribbon
    if os.path.exists(BLUER_CSV):
        df = pd.read_csv(BLUER_CSV)
        matches = df[df['Region'].str.contains(location, case=False, na=False) | 
                    df['Address'].str.contains(location, case=False, na=False)]
        for _, row in matches.iterrows():
            all_matches.append({
                "Name": row['Name'],
                "Award": f"{row['Ribbons']} Ribbons",
                "Tier": row.get('Price_Tier', 0),
                "Source": "Blue Ribbon",
                "Info": row.get('Booking_Info', ''),
                "Booking_Req": "High" if "예약" in str(row.get('Booking_Info', '')) else "Normal"
            })

    # 3. Search Worlds 50
    if os.path.exists(WORLDS_50_CSV):
        df = pd.read_csv(WORLDS_50_CSV)
        matches = df[df['Location'].str.contains(location, case=False, na=False)]
        for _, row in matches.iterrows():
            all_matches.append({
                "Name": row['Name'],
                "Award": f"World's 50 Best #{row.get('Rank', '?')}",
                "Tier": row.get('Price_Tier', 0),
                "Source": "World's 50 Best",
                "Info": "Elite target",
                "Booking_Req": "Critical"
            })

    # 4. Search Steak 101
    if os.path.exists(STEAK_101_CSV):
        df = pd.read_csv(STEAK_101_CSV)
        matches = df[df['Location'].str.contains(location, case=False, na=False)]
        for _, row in matches.iterrows():
            all_matches.append({
                "Name": row['Name'],
                "Award": f"Steak 101 #{row.get('Rank', '?')}",
                "Tier": row.get('Price_Tier', 0),
                "Source": "Steak 101",
                "Info": "Steak expert target",
                "Booking_Req": "High"
            })

    return all_matches

def generate_briefing(location, matches):
    if not matches:
        return f"No restaurant data found for '{location}' in your current databases."

    # Categorization logic
    elite = [m for m in matches if "3" in str(m['Award']) or "50 Best" in m['Award'] or m['Tier'] == 4]
    reasonable = [m for m in matches if m['Tier'] in [2, 3] and m not in elite]
    good_to_go = [m for m in matches if m['Tier'] == 1 and m not in elite]

    briefing = f"# 🍱 Voyage Briefing: {location.capitalize()}\n\n"
    briefing += f"Found **{len(matches)}** curated restaurants in your Knowledge OS for this location.\n\n"

    briefing += "## 🏆 Elite Version (Must-Go)\n"
    briefing += "*Top-tier dining, critical bookings, and unique culinary expressions.*\n"
    if not elite:
        briefing += "- *No elite targets found. Check reasonable options below.*\n"
    for m in elite[:10]:
        briefing += f"- **{m['Name']}** ({m['Award']}) | Tier: {int(m['Tier'])} | Booking: **{m['Booking_Req']}**\n"

    briefing += "\n## 🥗 Reasonable Version (Value & Quality)\n"
    briefing += "*Excellent food at a moderate spend. The sweet spot of your voyage.*\n"
    if not reasonable:
        briefing += "- *No reasonable finds found.*\n"
    for m in reasonable[:15]:
        briefing += f"- {m['Name']} ({m['Award']}) | Tier: {int(m['Tier'])} | {m['Info']}\n"

    briefing += "\n## 🚲 Good to Go (Casual & Local)\n"
    briefing += "*High-quality casual spots, budget-friendly, and often easier to visit on short notice.*\n"
    if not good_to_go:
        briefing += "- *No casual spots found.*\n"
    for m in good_to_go[:10]:
        briefing += f"- {m['Name']} ({m['Award']}) | Tier: {int(m['Tier'])} | {m['Info']}\n"

    briefing += "\n## 📋 Voyage Checklist Actions\n"
    booking_targets = [m for m in matches if m['Booking_Req'] in ["High", "Critical"]]
    if booking_targets:
        briefing += "1. [ ] **Action Required:** Book the following establishments ASAP:\n"
        for m in booking_targets[:5]:
            briefing += f"   - {m['Name']} ({m['Source']})\n"
    
    briefing += "2. [ ] **Budget Check:** Balance your Elite/Reasonable mix.\n"
    briefing += "3. [ ] **Wine List Check:** Consult the [[wiki/travel/guidelines#reasonable-restaurant-with-winelist|Wine List Guide]] for specialized picks.\n"

    return briefing

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/voyage_briefing.py <location>")
    else:
        loc = sys.argv[1]
        results = search_restaurants(loc)
        print(generate_briefing(loc, results))
