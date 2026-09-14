---
stage: ideation
category: system
concepts: [multi-signal-fusion]
lifecycle: spark
---

> [!IMPORTANT] Key Takeaway
> **Why this matters:** People broadcast their real taste through the digital footprints they've already left — subscriptions, the YouTube channels they follow, who they follow on Instagram, what they book and read. These signals are more honest than any survey.
> **How to use it:** Fuse those scattered signals into a confident per-person taste profile, then act on it — recommendations, matching, niche discovery.
> **Informs:** [[Advance Planner]] (the taste profile that powers its recommendations) and [[The Connection]] (taste-based matching).

# Taste Detector

## Overview
A system that **infers a person's taste and interests from the digital footprints they've already accumulated** — no long questionnaire required. Each individual signal is weak on its own, but stacked together they resolve a confident picture of who someone is and what they'd enjoy.

The exact signals differ from person to person, which is part of the point — the system reads whatever footprint each person actually has.

## Signals to Read
- **Subscriptions** — OTT/streaming, newsletters, paid memberships → what they pay attention to.
- **YouTube account** — subscribed channels + watch history. *(The strongest signal, I think — see below.)*
- **Instagram following list**, excluding friends/personal contacts → the *interest* follows (creators, brands, communities, topics), not the social graph.
- **Booking history** — restaurants, trips, events, tickets.
- **Reading list** — saved articles, Goodreads/book lists, bookmarks.
- **Music (Spotify, etc.)** — favorite artists and genres. *(Overlaps with [[Advance Planner]]'s connected-services idea.)*
- ...and other per-person sources.

## Why YouTube Especially
In the past, TV gave you only a handful of channels — everyone was funneled toward the same mainstream. Now there are effectively **infinite channels** to choose from. Big trends still exist, but the market is large enough that **you no longer have to be mainstream to survive** — a minor hobby or niche audience is a viable, even good, market on its own.

That shift makes the *mix* of channels a person subscribes to a dense, honest fingerprint of their real interests — including niche tastes they'd never volunteer in a survey. A good system can read that fingerprint and genuinely satisfy each person's specific taste, mainstream or long-tail.

## 💭 Reflection: Decentralization Demands an Embracing Attitude
A moment that crystallized this: I watched a video of women talking about their careers, and one — with **1M subscribers** — explained why she still edits her own YouTube videos instead of hiring editors. Her reasoning didn't matter to me. What struck me was that *I had never heard of her or her channel*, despite 1M subscribers.

That's the infinite-channels thesis felt firsthand. When everything is this **customized and decentralized**, no single person can follow every channel, creator, or trend anymore — there's no shared mainstream to keep up with. You are *supposed* to miss most of it.

The key implication is an attitude, not a feature: **the more decentralized taste becomes, the more important it is to understand and embrace differences rather than judge them.** We can't rank or judge someone else's taste against our own — there's no longer a common center to measure against. An embracing, non-judgmental posture toward other people's opinions and taste isn't just nice; it's the correct response to a decentralized world. (This is also the moral spine of the product: a taste mirror should *honor* niche/long-tail taste, never flatten it toward the average.)

## What We Can Do With the Taste Profile
- **Feed recommendations** → power [[Advance Planner]] and similar services with a taste profile built automatically.
- **Match people** → taste-based matching for dating, teams, or communities ([[The Connection]]).
- **Find your tribe** → surface the niche communities, events, and content that fit a minor/long-tail interest.
- **Personalized commerce & content** → serve the specific, not the average.

*(This is early — we have to dig from here — but it feels like a strong approach worth developing.)*

## 📡 Market Scan (2026)
*(First landscape pass — brainstorming, not a verdict.)*

**The neutral "taste engine" is already owned — by [Qloo](https://www.qloo.com/).** A 14-year-old, well-funded "Cultural AI": 575M+ cultural entities, trillions of behavioral signals, and it already does the cross-domain move this note imagined ("recommend a hotel from your taste in music"). It's a **privacy-first B2B API** powering Netflix, Starbucks, Michelin — and [Match Group's dating apps](https://www.globaldatinginsights.com/featured/cultural-ai-firm-qloo-partners-with-matchs-niche-apps/) (BLK, Chispa, Upward, Yuzu). It solved cold-start "with one signal" and acquired [TasteDive](https://techcrunch.com/2019/02/13/qloo-acquires-tastedive/) (the consumer "you like X → try Y" engine).

**The taste-matching thesis is validated — and being captured.** Qloo's "Currently Into" tags drove a **70% lift in likes** on Yuzu; 2026 press calls interests ["the new social currency"](https://befriend.cc/2026/03/17/top-best-dating-app-guide-for-2026-why-interests-are-the-new-social-currency/) in dating.

**Critical: the two signals assumed strongest are the two that are walled off.**
- **YouTube watch history** → [no API at all](https://issuetracker.google.com/issues/35172816); the only legal path is a user's own **Google Takeout** export. Subscriptions are available via the Data API (OAuth), but not history.
- **Instagram follows** → [killed](https://www.keyapi.ai/blog/instagram-graph-api-get-followers-list-following/). Basic Display API ended Dec 2024; Graph API doesn't expose follow lists. Scraping breaks ToS + GDPR.
- **Spotify** → feasible via OAuth (top artists/tracks), but Spotify now ships its own user-facing [Taste Profile](https://newsroom.spotify.com/2026-03-13/taste-profile-beta-announcement/).

**Where that leaves the open space:** Qloo knows taste *in the abstract* and sells it to *brands*. It does **not** ingest one specific person's real, messy footprint and hand *them* their profile. That gap — personal, private, consumer-owned — is the opening.

## 🧭 Directions Being Explored
Product story taking shape: **taste mirror as the hook → action / connection as the loop.**
- **Payoffs are a sequence, not a menu:** *self-understanding* + *cross-domain discovery* are the content (novelty-prone alone); *action* ([[Advance Planner]]) + *connection* ([[The Connection]] / find-your-people) are the loops that beat novelty death. The mirror gets people in; the loop keeps them.
- **Anti-Qloo positioning** as the whole differentiator: "Qloo knows taste; this knows *you*" — deeply personal, private, consumer-owned vs. identity-agnostic B2B.
- **Maybe detection is the wrong hard problem to own.** Data walls make auto-detection fragile; inversion — make *curating* taste effortless and spend the real effort on the **action layer**. The moat may be what you *do* with taste, not how you infer it.
- **Niche/long-tail as the wedge audience:** the mirror is most valuable to people with specific/underserved taste that mainstream recs fail — "finally, something gets me." (Direct line to this note's own infinite-channels thesis.)
- **Realistic MVP inputs given the walls:** Spotify (OAuth) + Google Takeout upload (YouTube) + link-based imports (Letterboxd, Goodreads). Instagram is effectively off the table.

## Challenges
- **Incumbent (Qloo)**: the neutral engine is a red ocean; any "general taste API" play is a thin wrapper unless it owns the *personal footprint → personal profile* angle Qloo skips.
- **Novelty death**: taste mirrors (Wrapped, Obscurify) are fun once; without an action or connection loop, retention collapses.
- **Data access**: platform APIs restrict the richest signals — YouTube watch history isn't exposed via API, and scraping Instagram follow lists runs against ToS. Legitimate access likely needs user-authorized export/OAuth (Takeout, Spotify), not scraping.
- **Separating social from taste**: distinguishing "friend/family" follows from genuine *interest* follows is non-trivial but essential.
- **Consent & privacy**: reading someone's footprint is sensitive; the value has to be worth the trust, with clear consent and data handling.
- **Inference quality**: turning raw follows/subscriptions into a usable, specific taste representation — not a generic bucket.
- **Cold start**: people with a thin digital footprint give the system little to read.

## 🔗 Connections

### ⬆ Pipeline
- Back ← [[ideation]] — tracked on the active ideation board
- Related → [[Advance Planner]] — Taste Detector builds the profile that Advance Planner acts on
- Related → [[The Connection]] — taste-based matching between people
- Hub → [[../index|Master Index]]

<!-- AUTO-CONCEPTS:START -->
### 🔀 Concepts (auto-generated — do not edit)
- **multi-signal-fusion** → [[Advance Planner]] (system), [[Been There]] (system), [[Chronicle - Personal Topic Timeline]] (product), [[Company Fit Finder - Where to Work]] (system), [[The Connection]] (system), [[Triathlon Photo Finder]] (system), [[Wine Value Advisor]] (system), [[../projects/Michelin Filter]] (system), [[../projects/Trip Guide - Shareable Restaurant Map]] (travel), [[../projects/prd/Chronicle_prd]] (product), [[../research/cooking/selected-restaurants]] (cooking), [[../research/system/connecting_the_dot]] (system), [[../research/system/graph-theory-foundations]] (system), [[../research/system/graphrag-connection-engine]] (system)
<!-- AUTO-CONCEPTS:END -->
