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

# Sniff

*Formerly **Advance Planner** (renamed 2026-11-03). Named after the truffle dog that finds the hidden, seasonal thing for you. The project folder and README live in `~/Cursor/sniff`.*

## Overview
**Sniff** is the root project: a taste-driven recommendation and notification engine. You save information about yourself — interests, tastes, history — and a location (where you are now, or where you'll be), and it surfaces *what you can do there*, alerting you early enough to act. The point is that it does the remembering and timing so you don't have to keep checking.

The same engine specializes into **sub-projects** by context:
- **Travel Planner** — traveling to a different city or country; plan the trip ahead around what's happening and what fits your taste.
- **Business-Trip Planner** — for people who travel frequently for work: they land in a new city on a fixed schedule but have no time to research it. The service reads the trip dates (from calendar/itinerary) and pre-surfaces what fits their taste in the free windows around meetings — a good dinner near the hotel, a run route, a concert the evening they're free — so downtime abroad turns into something worth doing without any planning effort.
- **Dating Planner** — planning a date somewhere; the right spot or event at the right time.
- ...and other contexts the same taste-plus-location model can serve.

## Core Loop — type a place, get everything
**The default behavior of the Travel Planner.** The interest profile is saved once and always on; the user never re-states it. They type only a location (optionally dates), and the engine searches **every interest in the profile** for that place and returns **all the options** — spots, experiences, one-day classes, events, food.

1. **Profile (saved, always on)** — cooking class, sports, music, busking, networking, parties, startup/IT, food, …
2. **Input** — just a place: "Naples", or "Italy, 10 days, early October".
3. **Search per interest × place × date** — one search lane per interest, run automatically.
4. **Output** — every option grouped by interest; the user picks, and picks feed the itinerary and the [[#Journey Optimizer — save places, get the route|Journey Optimizer]].

| Interest | What it finds for the place |
| --- | --- |
| **Signature food** | The dish the place is known for (vongole pasta in Naples) and where it's done best |
| **Seasonal food** | What's in season *that month* (white truffle in Alba, October) |
| **Cooking class** | One-day class for that local dish |
| **Music / busking** | Live venues, busking spots, festivals on the dates |
| **Sports** | Matches on the dates, pickup games, local sports culture |
| **Startup / IT / networking** | Meetups, tech events, coworking hubs |
| **Party** | Nightlife areas, events that week |

**Regional source swap — China uses Dianping.** Search lanes don't use one global source: in mainland China, locals pick restaurants on **Dianping (大众点评)**, not Google Maps (poorly usable there) or Western review sites. For a China place, the food lanes (signature food, seasonal food, nightlife) read Dianping signals instead — see [[#Dianping (大众点评) — the China restaurant source|Dianping]] below.

**Data has three freshness tiers:** signature dishes are stable (collect once, store per place); seasonal food is a fixed month calendar (store once); events, matches and meetups change weekly (search live for each request).

## Journey Optimizer — save places, get the route
**Sub-project of the Travel Planner.** Save interests, places, restaurants and experiences in any order (several restaurants in Barcelona, Madrid and Valencia, a farm stay in Andalusia, something in Porto). It researches each one and plans the **most efficient journey**:

1. **Cluster** — group pins into city/region bases.
2. **Order** — find the shortest loop between bases; avoid backtracking.
3. **Mode per leg** — compare train / flight / car on real door-to-door time and cost (rural pins, like an Andalusian farm, may need a car; plan where to drop it).
4. **Nights per base** — sized by how many things are saved there (4 restaurants ≥ 2 dinners).
5. **Day routes** — group by neighborhood inside each city.
6. **Pin cost** — show what each pin costs the trip ("Porto: +1 flight, +1.5 days, for 1 item — drop it or add more?"). The trade-offs only the user can judge are the real product.

**Dates: both modes.** Fixed dates → fit the best subset into the window. Open dates → say how many days the whole list needs. Same engine, set by the user's planning style.

**Suggestions: open, as much as possible.** Beyond the saved list, freely suggest everything that fits taste along the route ("you're passing Valencia anyway — paella class, Albufera sunset"), marked as suggestions so saved pins stay distinct.

**Ties back to timing:** the route fixes the dates, the dates trigger the booking-window alerts.

**Build: files, not an app.** For personal use: one dump file per trip (`wiki/travel/{trip}.md`), an agent "plan pass" writes the `## Plan` section, optional map via the [[../../scripts/trip_guide/food-map.html|food-map]] pattern. Add a database (Dataview frontmatter first) only when filtering across trips becomes a real need; a scheduled agent can cover alerts later.

## Dianping (大众点评) — the China restaurant source
In China, **Dianping** (run by Meituan) is the default way people choose where to eat — the equivalent of Google Maps reviews elsewhere. A planner that ignores it will recommend from sources locals don't use. What the engine should take from it:

- **Ratings + review volume** — star score, per-person price (人均), and review count; high score with a large review count is the trust signal, a high score on few reviews is not.
- **Ranked lists** — the **Must-Eat List (必吃榜)** and the **Black Pearl Guide (黑珍珠)** are published through Dianping/Meituan; see [[../research/cooking/selected-restaurants#15. 黑珍珠餐厅指南 (Black Pearl Restaurant Guide, 흑진주 가이드)|Black Pearl in the restaurant DB]]. Use them as the "known-good" layer, the way Michelin is used elsewhere.
- **Local dish tags** — Dianping's category and dish-recommendation tags feed the *signature food* lane (the dish a city is known for and where locals say it's best).
- **Queue / reservation info** — many popular places run queues or booking via the app; surfacing this feeds the timing alerts.
- **Chinese-language search** — queries must run in Chinese (place and dish names in 汉字); an English-only search misses most of it.

**Caveats:** there is no open public API, the app is Chinese-language and tied to a local phone number / Meituan account, and scraping is restricted — so in the files-first build this starts as a **manual input** (user pastes the Dianping page or screenshot into the trip dump file and the plan pass reads it), not an automated lane. Also remember Dianping's parent Meituan publishes the Black Pearl list, so the judge and the marketplace share an owner (noted in the restaurant DB).

**Profile Enrichment fit:** a Dianping *saved/collected list* (收藏) is the China equivalent of Google Maps saved places below.

## How It Works
1. **Save your profile** — tastes, interests, past experiences, constraints. You can type these in, or **import them from services you already use** (see below).
2. **Set a location + time horizon** — current location, or a future destination and dates.
3. **Get recommendations + notifications** — matched to your profile and surfaced *when it matters* (book now, tickets just opened, this falls inside your trip window), so nothing time-sensitive slips by unwatched.

## Profile Enrichment via Connected Services
Rather than making the user fill out a long taste questionnaire, let them **connect existing accounts** and pull their real preferences automatically — richer and more honest than self-reported input:
- **Spotify** — favorite artists, genres, and top tracks → drives concert/orchestra/busking/live-music-bar recommendations (e.g. "an artist you play a lot is touring near you next month").
- **Instagram / photo library** — places, food, and activities you already gravitate to.
- **Google Maps / reviews & saved places** — restaurants and spots you've liked or bookmarked.
- **Dianping (大众点评) — for China** — collected restaurants and past reviews, since Google Maps is unreliable there (see [[#Dianping (大众点评) — the China restaurant source|Dianping]]).
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
- **Regional platforms**: the best source differs by country (Dianping in China); each region needs its own source, language and access route, and some (Dianping) have no open API.
- **Integration & privacy**: pulling taste from Spotify/Instagram/Maps/Strava/Calendar means OAuth scopes, per-service API limits, and careful consent + data-handling — users must trust what's imported and how it's used.

## 🔗 Connections

### ⬆ Pipeline
- Back ← [[ideation]] — tracked on the active ideation board
- Back ← [[../projects/Michelin Filter]] — its three-tier filter is the known-good layer for the food lanes, and its My Maps export was a hand-built Travel-Planner result
- Related → [[Wine Value Advisor - Fair Price Check for Restaurant Wine Lists|Wine Value Advisor]] — a lane for wine drinkers: judges whether the wine list at a restaurant this surfaces is fairly priced
- Related → [[Taste Detector - Taste Profile from Digital Footprints|Taste Detector]] — could auto-build the taste profile this service acts on
- Related → [[../research/cooking/selected-restaurants]] — restaurant-hotspot data this could reuse
- Hub → [[../index|Master Index]]

<!-- AUTO-CONCEPTS:START -->
### 🔀 Concepts (auto-generated — do not edit)
- **multi-signal-fusion** → [[Atlas - One Map Over Every App]] (product), [[Been There - Peer Help from Someone Who Lived It]] (system), [[Chronicle - Personal Topic Timeline]] (product), [[Company Fit Finder - Where to Work]] (system), [[Connecting the Dots - Non-Obvious Links Between Notes and People]] (system), [[Ieum - One Line per Person, Before and After Every Meeting]] (product), [[Taste Detector - Taste Profile from Digital Footprints]] (system), [[Triathlon Photo Finder - Find Race Photos by Bib, Face and Gear]] (system), [[Wine Value Advisor - Fair Price Check for Restaurant Wine Lists]] (system), [[../projects/Michelin Filter]] (system), [[../projects/Trip Guide - Shareable Restaurant Map]] (travel), [[../projects/prd/Chronicle_prd]] (product), [[../research/cooking/selected-restaurants]] (cooking), [[../research/system/connecting_the_dot]] (system), [[../research/system/graph-theory-foundations]] (system), [[../research/system/graphrag-connection-engine]] (system), [[../research/system/linking-algorithms-survey]] (system)
- **needle-in-haystack-retrieval** → [[Insight Capture - Your Interpretation Over the Source File]] (product), [[Triathlon Photo Finder - Find Race Photos by Bib, Face and Gear]] (system), [[../projects/Trip Guide - Shareable Restaurant Map]] (travel), [[../research/system/graphrag-connection-engine]] (system)
<!-- AUTO-CONCEPTS:END -->
