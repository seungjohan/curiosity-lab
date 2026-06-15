---
category: system
---

> [!IMPORTANT] Key Takeaway
> **Why this matters:** Standardized procedures for culinary voyages ensure efficient data gathering and a balanced mix of "Elite" and "Reasonable" dining experiences.
> **How to use it:** Follow the Voyage Briefing Process and Pre-Trip Checklist before any international or local trip.
> **Informs:** [[index|Voyage OS: Travel Hub]]

# 📋 Voyage Guidelines & Checklist

This document defines the standard procedures for planning any culinary voyage.

## 🚀 The Voyage Briefing Process

Whenever you plan a new trip, follow this automated briefing process to get immediate recommendations from your entire restaurant database.

### How to trigger a briefing:
1.  **Ask me:** *"Give me a voyage briefing for [Location]"* (e.g., "Seoul", "London", "Tokyo").
2.  **What I do:** I run the unified search script (`scripts/voyage_briefing.py`) across all your guides (Michelin, Blue Ribbon, World's 50 Best, Steak 101, Guia Repsol).
3.  **What you get:** A structured report with:
    *   **Elite Targets:** Must-go 3-star or Top 50 restaurants.
    *   **Local Finds:** Curated recommendations from all sources.
    *   **Booking Actions:** A list of establishments needing immediate reservation.
    *   **Budget Overview:** A summary of the price tiers available.

---
## 🍷 Reasonable Restaurant with Winelist

For the traveler who prioritizes the drinking experience alongside value-driven dining. This section identifies establishments that offer exceptional wine selections while maintaining a "Reasonable" (Tier 2-3) price point.

### Key Resource:
- **[[michelin_wine_list.csv|Michelin Wine List Database]]**: A curated list of establishments recognized by Michelin for their superior wine programs.

### Strategy:
1.  **Cross-Reference:** When a briefing gives you a "Reasonable Version" list, check them against the wine list database.
2.  **Look for recognized lists:** Favor restaurants that have won specialized awards for their cellar quality but haven't reached "Elite" price tiers yet.

---
## 🌟 The Voyage Checklist (Pre-Trip)

Before departing on any trip, perform these checks:

1.  **[ ] Data Refresh:** Re-run scrapers for the target region (Blue Ribbon, Michelin, etc.) to get the latest awards and booking info.
2.  **[ ] The 3-Star/3-Ribbon Hunt:** Identify the "Must-Go" elite restaurants in the destination.
3.  **[ ] Advance Booking Check:** Filter by "Booking Required" and secure reservations at least 2-4 weeks in advance.
4.  **[ ] Proximity Analysis:** Use the `Coordinates` field to group restaurants by neighborhood to minimize travel time.
5.  **[ ] Budget Balancing:** Ensure a mix of Tier 1-4 restaurants to balance the trip's "burn rate."

## 💰 Universal Price Tier Mapping

All restaurant data is normalized to this 1-4 scale for easy cross-guide comparison.

| Tier | Michelin Label | Est. Cost (KRW) | Travel Vibe |
| :--- | :--- | :--- | :--- |
| **1 ($)** | On a budget | < 30,000 | Casual / Quick lunch |
| **2 ($$)** | A moderate spend | 30,000 - 80,000 | Regular dinner / Local find |
| **3 ($$$)** | Special occasion | 80,000 - 200,000 | Date night / Birthday |
| **4 ($$$$)** | Spare no expense | > 200,000 | Once-in-a-lifetime voyage |

---
## 🔗 Connections
- [[index|Voyage OS: Travel Hub]]
