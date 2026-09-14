---
stage: ideation
category: system
concepts: [multi-signal-fusion, high-signal-filter, interpretation-over-artifact, abundance-flips-value]
lifecycle: spark
aliases: [Company Compass]
---

> [!IMPORTANT] Key Takeaway
> **Why this matters:** Finding companies is easy — LinkedIn and Glassdoor list them all. The hard, unsolved part is *understanding* a company well enough to judge whether it fits **you**, and then knowing how to *approach* it. As startups stop being "the risky choice," the scarce skill becomes selecting the right one wisely.
> **How to use it:** Fuse a company's scattered public footprint (funding, team, reviews, growth, culture signals) into a confident read, match it against who the user is, and surface the few high-fit companies with a way in — not a list of 10,000.
> **Informs:** The user's own career search (the [[../research/career/Finding-Dream-Services|career]] research folder is this idea done by hand). Sibling engine to [[Taste Detector]].

# Company Compass / Company Fit Finder - Where to Work

## Overview
A service that helps you **get to know a company deeply and judge whether it fits you** — then how to approach it. Not another job board or ratings aggregator: a *fit engine* that reads a company's real character from the footprint it has already left in the world and holds it up against the user's own profile.

The wedge is the gap everyone feels: you can *find* thousands of companies in seconds, but you can't *know* them — and you certainly can't tell which one is right for the specific person you are.

## The Pain (why LinkedIn / Glassdoor aren't enough)
- **Discovery is solved; understanding isn't.** Listings tell you a company exists and its headcount. They don't tell you what it's actually like, where it's going, or whether it matches your values, stage-of-life, and risk appetite.
- **Reviews are noisy and biased.** Glassdoor/Blind skew toward the disgruntled and the recruited-by-HR-to-post-nice. A single rating hides more than it reveals.
- **Approaching them is hard.** Even once you've picked a good target, cold outreach is brutal. Knowing *how to get in* (warm paths, framing, timing) is a separate unsolved problem.
- **The stakes moved.** See the thesis below — choosing where to work is a higher-leverage, more selectable decision than it used to be, but people still make it on vibes and a careers page.

## Market Thesis — startups are no longer "the risky choice"
- Markets expand fast; the time to gather **1B users** keeps shrinking. The old "startup = gamble, big co = safe" framing is outdated.
- **Choosing to work at a startup is already the brave, high-ability move** — the barrier now isn't courage, it's *judgment*: which startup, at which stage, for which kind of person.
- So the scarce, valuable skill becomes **selecting a company with a broad, wise, insightful perspective** — not just reading a pitch deck. ([[abundance-flips-value]]: when the option becomes abundant and normalized, the *judgment to choose well* becomes the premium.)
- That judgment is exactly what a good service can systematize and give to people who don't have a decade of pattern-matching yet.

## The Bigger Bet — an alternative to LinkedIn
"There's no real competitor to LinkedIn" is almost a VC truism — and it's *true*, because LinkedIn's moat isn't features, it's the **professional social graph + being the system-of-record for professional identity** (1B+ profiles, everyone's résumé, network lock-in). Frontal clones die against that.
- **Don't attack the graph — flank it.** LinkedIn is a *directory + rolodex*: it lists and connects, but it has **no opinion**. It never tells you *which* company is right for *you*, or why. That judgment layer is exactly what it structurally under-serves.
- **The wedge as an entry point:** if "where should I work, and why" starts *here* instead of in LinkedIn's search box, this becomes an alternative front door to the same decision — a beachhead in LinkedIn's territory, taken from the side.
- **Honest read:** "alternative to LinkedIn" is the *ambition*, not the v1. The realistic path is owning the fit/selection layer LinkedIn ignores, earning trust there, then expanding — not out-listing the listing king on day one.

## Signals to Read (the company's footprint)
Each is weak alone; fused, they resolve a confident picture ([[multi-signal-fusion]]):
- **Funding & investors** — round history, who's on the cap table, runway implications, investor quality/thesis.
- **Founders & team** — backgrounds, prior exits/failures, tenure, who's leaving (LinkedIn departures are a signal).
- **Reviews, de-biased** — Glassdoor / Blind / levels.fyi read *as a distribution*, weighted against known bias, not a single star count.
- **Growth & momentum** — hiring velocity, product ship cadence, press, traffic/app-rank trends.
- **Culture signals** — eng blog, GitHub activity, how they write job posts, how founders talk publicly, values-in-practice vs values-on-the-wall.
- **Trajectory** — is this a rocket, a plateau, or a slow bleed? Stage-appropriate for *this* person?

## Data Backbone (sourcing & scraping)
The engine is only as good as its data — the hard, unglamorous core.
- **Primary sources:** LinkedIn (team, tenure, headcount trend, departures), Glassdoor / Blind (reviews, comp, sentiment), Indeed (job postings → hiring velocity), plus Crunchbase (funding), levels.fyi (comp), news/press.
- **Scraping is the obvious path *and* the dangerous one.** LinkedIn is famously litigious about it (the multi-year *hiQ Labs v. LinkedIn* fight) and blocks aggressively; Glassdoor/Indeed restrict it in ToS. So scraping = real legal exposure + a brittle anti-bot cat-and-mouse.
- **The hybrid that survives:** lean on official APIs where they exist, **user-authorized data** (the user connects/exports their *own* LinkedIn — sidesteps ToS, the same OAuth/export move [[Taste Detector]] landed on against the data walls), licensed data vendors, and fully-public/press data. Treat mass scraping as the *fragile* part of the plan, not the foundation.

## Fit Matching (the differentiator)
Knowing the company is half of it. The other half is **matching it to who the user is** — the same fusion move as [[Taste Detector]], pointed at companies instead of people:
- Read the *person's* profile (values, risk tolerance, career stage, working style, what they want next).
- Read the *company's* character from the signals above.
- Score **fit**, not just quality — a great company can be a bad fit, and a scrappy one can be perfect for a specific person.
- Explain the *why* — interpretation over raw data ([[interpretation-over-artifact]]): the value is the judgment "this fits you because…", not the underlying LinkedIn page.

## Standardizing the Company (the scoring core)
Without a **standard that turns a company into comparable numbers, "fit" collapses into subjective suggestion** — a vibe the user can't trust or compare. The core IP is a *company scoring standard*: a fixed schema of dimensions, each scored on a normalized scale, so any two companies become comparable and fit becomes **computed**, not asserted. (Same instinct as [[../projects/Michelin Filter|Michelin Filter]] and [[high-signal-filter]] — a trusted standard that separates signal from noise.)
- **Numericalize what's genuinely numeric:** funding stage / runway, growth & hiring velocity, tenure & attrition, review-score *distributions*, comp percentiles.
- **Structure the soft stuff into rubrics, not fake numbers:** culture, mission, working style scored on *anchored* scales (defined 1–5 descriptions) so scoring is repeatable — not free-text vibes, but also not pretending culture is a precise float.
- **Fit = the two vectors compared:** person-profile · company-profile across the standard's dimensions → a transparent score with visible components ("strong on autonomy & growth, weak on stability"). This is also the honest answer to the *"defining fit"* problem below.
- **Guard against false precision:** the standard's credibility is the *breakdown*, not a single black-box number. Over-quantifying culture produces confident nonsense — show the factors and how each scored, always.

## The Approach Layer
Selection isn't the finish line — *getting in* is. A wiser version of [[Return to Basics|referral]]-style warm-path thinking (cf. parked **Flexible Lit**):
- Surface warm connections and realistic paths in.
- Suggest framing/positioning for *this* company and *this* person.
- Timing — when a company is hiring vs. quietly freezing.

## 🧭 Directions Being Explored
- **The standard is the moat.** Anyone can scrape; the defensible asset is the *scoring standard* + the earned trust that it's *right* — the opinionated layer LinkedIn and Glassdoor never built.
- **Fit over ranking.** Don't rebuild Glassdoor's leaderboard; own the personal fit judgment nobody sells.
- **De-biased review synthesis** as a credible, defensible sub-product on its own.
- **The user's own [[../research/career/Finding-Dream-Services|career/ folder]] is the proof + seed:** 80+ hand-built company deep-dives, regional AI maps, visa/application notes. That's this idea run manually — real pain, real prior art, a starter dataset and a taste function.
- **Sibling to [[Taste Detector]]:** same multi-signal-fusion engine; if built, they could share infrastructure (footprint → profile → match).

## Challenges
- **Data reliability**: reviews are biased and gameable; funding data is stale/private for early startups; de-biasing is the hard technical core.
- **Data access & legality**: the richest sources (LinkedIn especially) fight scraping hard — legal exposure (*hiQ Labs v. LinkedIn*) plus brittle anti-bot. Durable access likely means user-authorized exports/APIs, not mass scraping.
- **False precision in scoring**: numericalizing qualitative traits (culture, fit) risks confident-but-wrong scores; the standard must stay transparent and component-wise, or it becomes astrology with a dashboard.
- **Defining "fit"**: quantifying person↔company match meaningfully (echoes [[The Connection]]'s synergy-quantification problem).
- **Private-company opacity**: the most interesting early startups leave the thinnest public footprint — cold-start on the *company* side.
- **Moat vs. incumbents**: LinkedIn, Glassdoor, Crunchbase, levels.fyi all own pieces; the defensible slice is *personal fit + approach*, not raw data.
- **Trust**: a fit verdict people act on (a job is a big decision) has to earn deep trust and explain itself.
- **Cold start on the person side**: a thin user profile yields a weak match — same footprint problem as [[Taste Detector]].

## 🔗 Connections

### ⬆ Pipeline
- Back ← [[ideation]] — tracked on the active ideation board
- Related → [[Taste Detector]] — same signal-fusion engine, pointed at companies instead of people
- Related → [[The Connection]] — person↔entity fit/synergy scoring
- Related → [[../projects/Michelin Filter|Michelin Filter]] — sibling "trusted standard" play: score/curate quality on a defined standard
- Seed ← [[../research/career/Finding-Dream-Services|Finding Dream Services]] — the career research that surfaced this
- Hub → [[../index|Master Index]]

<!-- AUTO-CONCEPTS:START -->
### 🔀 Concepts (auto-generated — do not edit)
- **multi-signal-fusion** → [[Advance Planner]] (system), [[Been There]] (system), [[Chronicle - Personal Topic Timeline]] (product), [[Taste Detector]] (system), [[The Connection]] (system), [[Triathlon Photo Finder]] (system), [[Wine Value Advisor]] (system), [[../projects/Michelin Filter]] (system), [[../projects/Trip Guide - Shareable Restaurant Map]] (travel), [[../projects/prd/Chronicle_prd]] (product), [[../research/cooking/selected-restaurants]] (cooking), [[../research/system/connecting_the_dot]] (system), [[../research/system/graph-theory-foundations]] (system), [[../research/system/graphrag-connection-engine]] (system)
- **high-signal-filter** → [[Wine Value Advisor]] (system), [[../projects/Michelin Filter]] (system), [[../projects/Trip Guide - Shareable Restaurant Map]] (travel), [[../projects/prd/Constellate_prd]] (product), [[../research/cooking/selected-restaurants]] (cooking), [[../research/music/music-social-media]] (music)
- **interpretation-over-artifact** → [[Chronicle - Personal Topic Timeline]] (product), [[Finding What You Like - Rekindling Passion & Curiosity]] (system), [[Keep in Touch - Relationship Chronicle]] (system), [[Private Space - The Bedroom Moved Online]] (music), [[The Connection]] (system), [[Unified-Media-Insight-Capture-Tool]] (product), [[../projects/prd/Chronicle_prd]] (product), [[../projects/prd/Constellate_prd]] (product), [[../research/career/Creative-Tech-Trends]] (career), [[../research/vibecoding/karpathy-llm-wiki]] (vibecoding)
- **abundance-flips-value** → [[Private Space - The Bedroom Moved Online]] (music), [[Return to Basics]] (system), [[Unified-Media-Insight-Capture-Tool]] (product), [[../projects/Michelin Filter]] (system), [[../research/cooking/coq-au-vin]] (cooking), [[../research/cooking/soupe-a-loignon]] (cooking)
<!-- AUTO-CONCEPTS:END -->
