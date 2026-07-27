---
stage: ideation
category: system
concepts: [multi-signal-fusion, needle-in-haystack-retrieval]
lifecycle: researching
---

> [!IMPORTANT] Key Takeaway
> **Why this matters:** The best experiences — bookings, event tickets, seasonal happenings — have a narrow timing window, and non-planners miss them simply from not tracking things far enough ahead. Constant manual checking is the tax nobody wants to pay.
> **How to use it:** Save who you are — taste, interests, history — plus your current or future location, and the service recommends what to do and *notifies* you at the right moment, no consistent checking required.
> **Informs:** Travel, dating, and lifestyle-experience product exploration under one root platform.

# Advance Planner

## Overview
**Advance Planner** is the root project: a taste-driven recommendation and notification engine. You save information about yourself — interests, tastes, history — and a location (where you are now, or where you'll be), and it surfaces *what you can do there*, alerting you early enough to act. The point is that it does the remembering and timing so you don't have to keep checking.

The same engine specializes into **sub-projects** by context:
- **Travel Planner** — traveling to a different city or country; plan the trip ahead around what's happening and what fits your taste.
- **Business-Trip Planner** — for people who travel frequently for work: they land in a new city on a fixed schedule but have no time to research it. The service reads the trip dates (from calendar/itinerary) and pre-surfaces what fits their taste in the free windows around meetings — a good dinner near the hotel, a run route, a concert the evening they're free — so downtime abroad turns into something worth doing without any planning effort.
- **Dating Planner** — planning a date somewhere; the right spot or event at the right time.
- ...and other contexts the same taste-plus-location model can serve.

## How It Works
1. **Save your profile** — tastes, interests, past experiences, constraints. You can type these in, or **import them from services you already use** (see below).
2. **Set a location + time horizon** — current location, or a future destination and dates.
3. **Get recommendations + notifications** — matched to your profile and surfaced *when it matters* (book now, tickets just opened, this falls inside your trip window), so nothing time-sensitive slips by unwatched.

## Profile Enrichment via Connected Services
Rather than making the user fill out a long taste questionnaire, let them **connect existing accounts** and pull their real preferences automatically — richer and more honest than self-reported input:
- **Spotify** — favorite artists, genres, and top tracks → drives concert/orchestra/busking/live-music-bar recommendations (e.g. "an artist you play a lot is touring near you next month").
- **Instagram / photo library** — places, food, and activities you already gravitate to.
- **Google Maps / reviews & saved places** — restaurants and spots you've liked or bookmarked.
- **Strava / fitness apps** — running, cycling, swimming activity → sports and route recommendations.
- **Calendar** — free windows and travel dates, so timing alerts land when you can actually act.

The more sources connected, the sharper and more *relational* the recommendations, with far less manual setup. (Trade-off: each integration means API access, OAuth scopes, and privacy/consent handling — see Challenges.)

## Worked Example (my own taste)
My interests: **cooking, music, making local friends, swimming, cycling, camping, walking around town, networking parties, sports.** From that profile plus a location, the service would recommend:

| Interest | What it surfaces |
| --- | --- |
| **Cooking** | Nice restaurants, local cooking classes, open house parties (e.g. via Airbnb Experiences), food markets |
| **Music** | Concerts, musicals, orchestra dates, famous busking spots, music-instrument shops, bars with live-music events |
| **Swimming** | Famous swimming beaches and spots |
| **Sports / cycling** | Pickup soccer with locals, groups to join, cycling routes and clubs |
| **Camping / walking** | Good camping sites, scenic town-walk routes |
| **Networking** | Networking parties and meetups nearby |
| **Alcohol / nightlife** | Pub crawls, bar-hopping routes, craft-beer and cocktail spots, brewery/distillery tours, tasting events |

Each recommendation is **relational**: it's not a flat "top 10" list but a suggestion tied to *who you are* and *where/when you are* — and delivered as a timely notification rather than something you have to go hunting for.

## Who This Is For
People who aren't natural planners and would otherwise forget or under-organize time-sensitive opportunities — the service does the remembering and timing. Especially useful when you land somewhere new (travel) or want to do more of what you love where you already live.

A strong fit is **frequent business travelers**: they cycle through unfamiliar cities on tight, fixed schedules with real gaps between meetings, but no bandwidth to research each place. Because their trip dates and locations are already structured (calendar, flights, hotels), the engine has clean inputs and can quietly fill the free windows with taste-matched things to do — high value, near-zero effort from the user.

## Challenges
- **Event data coverage**: aggregating reliable, current calendars (festivals, concerts, meetups, classes) across many regions and languages.
- **Reservation & signup windows aren't public**: restaurant booking-open dates, class signups, and pickup-game groups are rarely exposed via clean APIs.
- **Modeling "taste" usefully**: turning saved interests and history into genuinely specific, relational recommendations, not generic top-10 lists.
- **Local/social discovery**: finding "play soccer with locals" or "open house party" opportunities means tapping community sources, not just formal event listings.
- **Long-horizon forecasting**: far-future plans (a trip 6+ months out) may need to act on calendars that aren't published yet.
- **Integration & privacy**: pulling taste from Spotify/Instagram/Maps/Strava/Calendar means OAuth scopes, per-service API limits, and careful consent + data-handling — users must trust what's imported and how it's used.

## 🔗 Connections

### ⬆ Pipeline
- Back ← [[ideation]] — tracked on the active ideation board
- Related → [[Taste Detector]] — could auto-build the taste profile this service acts on
- Related → [[../research/cooking/selected-restaurants]] — restaurant-hotspot data this could reuse
- Hub → [[../index|Master Index]]

<!-- AUTO-CONCEPTS:START -->
### 🔀 Concepts (auto-generated — do not edit)
- **multi-signal-fusion** → [[Been There]] (system), [[Chronicle - Personal Topic Timeline]] (product), [[Company Fit Finder - Where to Work]] (system), [[Taste Detector]] (system), [[The Connection]] (system), [[Triathlon Photo Finder]] (system), [[Wine Value Advisor]] (system), [[../projects/Michelin Filter]] (system), [[../projects/prd/Chronicle_prd]] (product), [[../research/cooking/selected-restaurants]] (cooking), [[../research/system/connecting_the_dot]] (system), [[../research/system/graphrag-connection-engine]] (system)
- **needle-in-haystack-retrieval** → [[Triathlon Photo Finder]] (system), [[Unified-Media-Insight-Capture-Tool]] (product), [[../research/system/graphrag-connection-engine]] (system)
<!-- AUTO-CONCEPTS:END -->
