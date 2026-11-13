---
stage: ideation
category: product
concepts: [interpretation-over-artifact, multi-signal-fusion]
lifecycle: spark
---

> [!IMPORTANT] Key Takeaway
> **Why this matters:** Meeting tools treat each meeting as a separate event. A real relationship is a **line**: a cold email, a first call, a coffee, a client meeting. The context for meeting 3 is spread across Gmail, notes, research tabs and memory, so every "before" starts from scratch and every "after" fades.
> **How to use it:** Give each person or client one visual line that runs from first contact to the latest follow-up, with three phases on every meeting point: **before** (research, history), **during** (notes, live summary), **after** (my takeaways, highlights, follow-ups). Online and offline.
> **Informs:** A meeting-to-meeting memory layer; possibly the same "gather the trail into one line" engine as the product development controller spark.

# Ieum

*Formerly **Peoplechain** (renamed 2026-11-09), and before that **Meeting Line: Before, During, After**. The build lives in `~/Cursor/ieum`.*

## Problem Statement: Every Meeting Starts from Zero
Cold mail and online meetings bring a steady stream of new people, and offline meetings with clients and my own team keep coming too. Three things go wrong:

1. **Before is a rebuild.** To prepare I dig through the cold email thread, old notes, LinkedIn, company pages and whatever background I scraped last time. It's scattered, so I prepare less than I should.
2. **During is split attention.** Following the conversation and writing notes compete for the same focus, especially offline, where there's no Zoom audio to lean on.
3. **After evaporates.** What I *learned* and *felt* is freshest right after the meeting ends. If it isn't saved in that moment, it's gone. A transcript doesn't save it, because a transcript records what was said, not what I took away.

## Core Product Thesis: The Line Is the Product
- **One line per person or client.** First message → every conversation → every note I wrote → research and scraped background → each meeting → follow-ups, in order, on one screen.
- **Each meeting has three phases.**
  - **Before:** a brief built automatically from everything already on the line.
  - **During:** quick notes, plus an optional transcript from whatever recorder is in use.
  - **After:** a 2-minute prompt right after the meeting: what did I learn, what's the one follow-up, how did it feel. Then highlights and a summary.
- **Continuity beats capture.** Granola, Otter and Plaud compete hard on *during*. The gap is that meeting 3 automatically opens with the cold email and meetings 1 and 2 already lined up.

## 💭 Reflection: Granola Saves the Meeting, Not My Memory
Granola is good at saving a meeting. What I actually want to keep is different: my memory and my insight right after it ends, and the thread that links this meeting to the cold email that started it and the next one I'll have. That's why I want to build it myself. The value isn't in transcribing better; it's in the line staying mine and staying connected, from the first message to the last follow-up, whether the meeting was on Zoom or across a table.

## 📡 Landscape (scanned 2026-10-23)
*(Web scan, not product trials. Most sources are vendor or affiliate pages.)*

| Layer | Who's there | What they cover | What they miss |
|:--|:--|:--|:--|
| Notetakers | Granola, Otter, Fireflies, Fathom, Zoom AI Companion, Notion AI | Transcript + summary + action items, mostly *after* ([Tana roundup](https://tana.inc/blog/best-ai-meeting-assistants-2026)) | Each meeting stands alone; no cross-meeting line |
| Offline hardware | Plaud NotePin S + Plaud Desktop (Jan 2026): one system for in-person, phone and online, no bots, records offline ([eWeek](https://www.eweek.com/news/plaud-ai-note-taking-wearable/), [Dupple review](https://dupple.com/reviews/plaud)) | Solves *during* offline | Still a recorder; no before, no relationship line |
| "Agentic" meeting tools | Tana (prep before, act during), AudioCodes (meeting prep feature) ([TechTarget](https://www.techtarget.com/enterprise-software/tip/8-AI-meeting-assistants-to-consider-in-2026?amp=1)) | Starts to cover the full loop | Organized by meeting, not by person |
| AI-native CRM | Attio (meeting prep, full interaction history), Day AI (emails/chats/meetings → CRM data) ([Day AI](https://claude.com/connectors/day-ai), [Attio](https://claude.com/connectors/attio)) | The closest to the "line": history per contact | Built for sales teams and pipelines, not for one person's memory and insight |
| Outreach | Clay (enrichment + personalized cold email) | The cold-mail start of the line | Doesn't carry through to the meeting |
| DIY | Zapier "pre-meeting brief" template (calendar attendee → CRM lookup) ([Zapier](https://zapier.com/templates/details/pre-meeting-briefs)) | Proves people want the brief | Glue, not a product |

**Where the gap looks real:**
1. **Nobody draws the line.** No source showed a cold-email → meeting → follow-up timeline as a visible, first-class view. Everyone stores the pieces; no one shows them in order.
2. **"My takeaway" vs. "what was said."** Every notetaker optimizes the transcript. The after-meeting reflection (what I learned, how it felt) isn't productized.
3. **Individual, not sales team.** Attio and Day AI have the data model, but they're framed around deals and pipelines.

## Core User Flow (v1 sketch)
1. A calendar event with an outside person (or a cold email thread) creates or extends a person's line.
2. **Before:** open the meeting point and see a brief built from the line: last contact, open follow-ups, my past takeaways, background.
3. **During:** type notes; optionally attach a transcript from Granola, Plaud or a phone recording.
4. **After:** the meeting ends → a prompt for 3 to 4 questions → saved onto the line, with highlights and follow-ups pulled out.
5. **Next time:** step 2 is already richer. The line grows itself.

## Challenges
- **Capture walls.** Gmail and Google Calendar are open; KakaoTalk and LinkedIn DMs are not. The same wall as [[Keep in Touch - Relationship Chronicle]].
- **Recording offline needs consent.** In-person recording raises etiquette and legal questions, which is one reason to lean on notes plus the after-prompt.
- **Overlap with Attio and Day AI.** "Why not just use Attio?" needs a crisp answer, probably: personal, insight-first, visual line.
- **Logging friction.** If the after-prompt feels like homework, it dies like every personal CRM.

## Open Questions
- **Is this one product with [[Keep in Touch - Relationship Chronicle]]?** Keep in Touch is the person-level thread plus cadence; this one is the meeting-level before/during/after. Likely the same line, with two zoom levels.
- **Is it one engine with the product development controller spark?** Both pull a trail scattered across tools into one ordered workflow, one for people and one for products.
- **Who is it for first?** Me with cold-mail contacts, freelancers and consultants with clients, or a small team sharing client lines?
- **Do I need a transcript at all?** If the after-prompt captures the takeaways, the v1 might need no recording.

## 🔗 Connections

### ⬆ Pipeline
- Back ← [[sparks|✨ Spark List]]: grew from the `Post-meeting memory log` spark (2026-10-23).
- Sibling → [[Keep in Touch - Relationship Chronicle]]: the same per-person thread; this one adds the meeting's before/during/after and the visual line.
- Related → [[Chronicle - Personal Topic Timeline]]: the same chronological line, pointed at topics instead of people.
- Hub → [[../index|Master Index]]

---
- **Subject**: [[Startup & Side Projects]]
- **Source**: User idea (2026-10-23), from the `Post-meeting memory log` spark

<!-- AUTO-CONCEPTS:START -->
### 🔀 Concepts (auto-generated — do not edit)
- **interpretation-over-artifact** → [[Chronicle - Personal Topic Timeline]] (product), [[Company Fit Finder - Where to Work]] (system), [[Connecting the Dots - Non-Obvious Links Between Notes and People]] (system), [[Finding What You Like - Rekindling Passion & Curiosity]] (system), [[Insight Capture - Your Interpretation Over the Source File]] (product), [[Keep in Touch - Relationship Chronicle]] (system), [[Private Space - The Bedroom Moved Online]] (music), [[Show Your Way - Instagram for Personal Methods]] (consumer), [[../projects/prd/Chronicle_prd]] (product), [[../projects/prd/Constellate_prd]] (product), [[../research/career/Creative-Tech-Trends]] (career), [[../research/vibecoding/karpathy-llm-wiki]] (vibecoding)
- **multi-signal-fusion** → [[Atlas - One Map Over Every App]] (product), [[Been There - Peer Help from Someone Who Lived It]] (system), [[Chronicle - Personal Topic Timeline]] (product), [[Company Fit Finder - Where to Work]] (system), [[Connecting the Dots - Non-Obvious Links Between Notes and People]] (system), [[Sniff - Taste-Based Travel Picks, Alerted in Advance]] (system), [[Taste Detector - Taste Profile from Digital Footprints]] (system), [[Triathlon Photo Finder - Find Race Photos by Bib, Face and Gear]] (system), [[Wine Value Advisor - Fair Price Check for Restaurant Wine Lists]] (system), [[../projects/Michelin Filter]] (system), [[../projects/Trip Guide - Shareable Restaurant Map]] (travel), [[../projects/prd/Chronicle_prd]] (product), [[../research/cooking/selected-restaurants]] (cooking), [[../research/system/connecting_the_dot]] (system), [[../research/system/graph-theory-foundations]] (system), [[../research/system/graphrag-connection-engine]] (system), [[../research/system/linking-algorithms-survey]] (system)
<!-- AUTO-CONCEPTS:END -->
