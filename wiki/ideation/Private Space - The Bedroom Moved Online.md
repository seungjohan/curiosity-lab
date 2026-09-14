---
stage: ideation
category: music
concepts: [interpretation-over-artifact, abundance-flips-value]
lifecycle: spark
---

> [!IMPORTANT] Key Takeaway
> **Why this matters:** Private space used to be architectural — your house, your bedroom, the door you closed. It isn't anymore. The playlist, the prompt history, the home screen, the Obsidian vault, the camera roll, the subscription list: each is curated for an audience of one, and each reveals more than any profile does. **A profile is what you perform; a private space is what you actually are.** Nobody has built the product for that.
> **How to use it:** Treat a curated digital collection as a **room** — something you furnish privately and grant access to — rather than a feed you perform into. Room #1 is the playlist, because it's the only candidate with a clean API, an existing social ritual, and near-zero privacy risk.
> **Informs:** A music-first social product that never touches a second of audio, and a general pattern for turning any private collection into a visitable space.

# Private Space — The Bedroom Moved Online

*(Working title. The thesis is the asset, not the name.)*

## The Thesis

Your house or your bedroom is not the only private place anymore. As online life expanded, private spaces moved online with it — and we never named them or built for them.

Candidates, all of them mine already:

| Space | What it reveals |
| :--- | :--- |
| **Playlist** | Mood, era, taste, who you were at 2am |
| **AI prompts / chat history** | How you actually think, what you're insecure about |
| **Phone home screen** | Priorities, discipline, what you reach for |
| **Obsidian vault** | The shape of your curiosity |
| **Camera roll** | Where you were and what you looked at twice |
| **YouTube subscriptions** | What you're quietly becoming |

The common structure: **each is curated with real care, by you, for nobody.** No audience, no algorithm reward, no performance. That absence of audience is exactly what makes them honest — and what makes showing one to someone an act of trust rather than an act of marketing.

The social primitive that falls out: **not posting, but letting someone in.**

## The Payload — A Playlist Carries a Mood, Not a Track List

Instagram and VSCO are the right reference, but the thing being delivered has to be **a mood, a feeling, or a message** — not a catalogue of songs.

This is the sharpest version of [[../concepts/interpretation-over-artifact|interpretation over artifact]] in the whole vault. Forty tracks is the artifact. *"3am, second week after the move, couldn't sleep"* is the interpretation, and it's the thing worth receiving. Anyone can send a Spotify link; nobody can send that.

It also tells me what the day-one tool is. VSCO's presets don't add information to a photo, they set its **register** — and that's the craft act people opened the app for, long before anyone followed them. The music equivalent isn't editing audio. It's whatever lets me take a set of tracks and pitch them at a feeling: the title, the color, the cover, the sequence, the one line of context, the time of night it belongs to.

**The corollary is a hard product constraint: a playlist without a mood attached should not be postable.** The mood is the post. The tracks are the evidence.

## Why This Unlocks the Music-Social Problem

[[../research/music/music-social-media|My own research]] lists three reasons an "Instagram for music" is hard. The private-space frame kills two of them and dissolves the third.

| Stated killer | What the room frame does to it |
| :--- | :--- |
| **Music is auditory and temporal; feeds are visual and static** | Gone. You aren't rendering sound, you're rendering a *curation*. A room holds still. |
| **Licensing is a massive hurdle** | Gone, if you never host or stream a single second. Metadata plus deep links out to Spotify/Apple Music only — the Last.fm and stats.fm posture. |
| **Balancing consumption tools against creation tools** | Dissolved. Nobody creates audio here. They curate, which they already do for free. |

This is the first framing I've had that answers my own objections instead of arguing with them.

It's also a clean instance of [[../concepts/interpretation-over-artifact|interpretation over artifact]]: a playlist under this thesis isn't forty tracks, it's a room — and the tracks are just the furniture.

## 💭 Reflection: The Constraint I Spent, and What It Bought

I came in from a different direction entirely. I'd been looking at [발자취](https://apps.apple.com/kr/app/id6792431474) — a solo-built Korean walking app that fills in every 동 you've set foot in on a national dot map. Free, no account, no subscription, **no server at all**. One person shipped it and runs it at zero cost.

What I said I wanted from it was the economics: no backend, no second party, no cold start, works for user #1 on day one. My board is full of ideas that fail all four — [[Been There]] needs advisor verification and crisis escalation before it does anything; [[The Connection]] and [[Company Fit Finder - Where to Work]] need a matching pool to exist first. I'm tired of designing things that require a crowd before they require anything else.

Then I drifted. Travel, maybe? Music? And I landed on *music social media — VSCO but for music* — which is the precise opposite of the constraint I'd just chosen. A social network is the one shape that needs a server, needs accounts, needs moderation, and is worth nothing to its first user. I was told as much, and I picked it anyway.

I don't think the drift was noise. I think it was the idea arriving before I had words for it.

Because what I actually meant wasn't *a feed for music*. It was this: **we have private spaces online now, and nobody treats them as spaces.** The playlist, the prompt log, the home screen, the vault, the album, the subscription list. Those are rooms. I curate every one of them carefully and show them to almost no one, and when I do show someone, it means something.

So I spent the solo-economics constraint, and this is what it bought — a thesis that's bigger than the app that started it. That trade only pays off if the thing I build is genuinely about *access and intimacy* and not just another gallery with softer fonts. **A public feed of private spaces is a contradiction. It's a profile with better lighting.** If I can't answer what governs the door, I've spent the constraint for nothing.

The other thing worth admitting: 발자취's real invention was never the economics. It was the **complete finite board** — every 행정동 in Korea, sitting there waiting to be filled in. That's what makes it compulsive instead of merely pleasant. I didn't pick that property, and I should stay honest that I haven't replaced it with anything yet.

## Scope — Six Rooms Is a Platform

I named six private spaces. That's six integrations, six privacy postures, six rendering problems — a platform, built before its first room works. Decomposed:

**Room #1 is the playlist — decided.** The only candidate with a clean public API, an already-legible social ritual (*"send me your playlist"*), the lowest privacy risk of the six, and the domain I keep returning to anyway. Everything else becomes room type #2 once #1 is real.

Ranked for later, with the honest objection to each:

| Room | Why it's interesting | Why not first |
| :--- | :--- | :--- |
| **YouTube subscriptions** | Public API, deeply revealing, nobody has touched it | Second-most legible; strongest candidate for room #2 |
| **AI prompts** | Newest private space in existence; genuinely unclaimed | No API, and the privacy exposure is severe — people would be horrified |
| **Home screen** | Existing tour genre, instantly readable | It's just a screenshot; no depth, nothing to explore |
| **Camera roll** | Maximum intimacy | Instagram already is this, and the sensitivity is extreme |
| **Obsidian vault** | Closest to me personally | Audience of approximately nobody |

## The Open Question — What Governs the Door

**Unresolved. This is where the idea lives or dies**, since "private" has to be a mechanic and not a decoration.

| Mechanic | How it works | Trade |
| :--- | :--- | :--- |
| **Mutual exchange** | You can't enter someone's room unless you've opened yours to them | *I'll show you mine if you show me yours* — the childhood ritual the thesis evokes. Reciprocity becomes structural, lurking dies, and wanting in requires having a room, which is a viral loop for free |
| **Invitation only** | You hand out keys one person at a time | Most honest to the thesis, zero discovery, growth entirely word-of-mouth |
| **Open rooms** | Anyone wanders in | Simplest, closest to how VSCO actually behaves — but then it's a profile, and privacy is just styling |
| **Timed opening** | Room is visitable for a window, then shuts | Scarcity manufactures the occasion to look |

## 🧩 Four Mechanics (added by me, 2026-08-21)

### 1. Render the playlist as a physical music object
A turntable. Or a cassette, a CD case, a MiniDisc, a crate of vinyl. **This is the day-one tool** — the thing I was missing when I asked what makes the app worth opening with zero followers.

It does three jobs at once:
- **The craft act.** Choosing *cassette* over *vinyl* sets the register the way a VSCO preset does. No information added, everything about tone changed.
- **The mood carrier.** It is how *"3am, second week after the move"* becomes visible instead of merely stated.
- **The export.** A rendered object screenshots well, which is how it reaches Instagram — the 발자취 trick of letting a graph you don't own do the distribution.

Precedent exists: **MD Vinyl** (MD Studio) sits at ~2,500 ratings and was still shipping in July 2026, purely on rendering music as a physical object. So the willingness is real; the open question is whether it is durable or a novelty spike.

### 2. Playlists belong to people
The unit is **a person's shelf**, not a floating playlist. You browse *someone*, and their rooms sit together as a body of taste. This is what makes it a room rather than a feed, and it is precisely what Spotify does worst — a Spotify playlist is an orphan object with a tiny avatar next to it.

### 3 + 4. Discovery by track overlap — **the strongest idea in this note**

> Lots of intersection means high probability that the *other* songs are my taste.

Mechanically this is set intersection over track IDs. No ML, no training data, no model. Two playlists share 14 songs; the other 30 in mine become a ranked recommendation for you, **and the person behind them comes attached**.

What it solves, all at once:

| Problem | How overlap answers it |
| :--- | :--- |
| *Why would I enter a stranger's room?* | You are not browsing randomly. You are routed by measured overlap. |
| *Whose taste do I trust?* | **Overlap is the credential.** Not fame, not follower count — arithmetic. This is what dissolves the artist-supply problem for good. |
| *What is the finite board?* | **This is it.** "Unheard songs from rooms that overlap with you" is a backlog that refills forever, and overlap % is a number that visibly grows. I flagged earlier that I had no replacement for 발자취's complete index. This is the replacement. |
| *What is the day-one experience?* | Connect Spotify, and immediately see who you overlap with. Value before you make anything. |

**The reframe that matters.** Spotify already runs this algorithm — Discover Weekly leans heavily on collaborative filtering over playlist co-occurrence *(flagged for verification)*. So I am not proposing a better algorithm than Spotify's. I am proposing **the same algorithm with the human left in.**

Discover Weekly hands you a song stripped of provenance. You never learn who loved it, what else sat beside it, or what room it came from. That anonymity is not a technical necessity — it is a product choice, and it is the one I would invert. **Attribution is the product.**

That also settles a tension from earlier in this session. I had written off "the perfect playlist for my mood" as algorithm territory I should not enter. Wrong framing. The move is not to out-recommend Spotify — it is to refuse to hide the person.

### ⚠️ Two things that will break this if I ignore them

1. **Overlap on hits is noise.** If scoring is raw intersection count, everyone overlaps on the same 200 global hits and the signal collapses. It must be **weighted by inverse popularity** — one shared obscure track should outrank twenty shared chart songs. That is the difference between a real taste signal and a popularity contest, and it is a v1 requirement, not an optimisation.
2. **Overlap has a brutal cold start.** With ten users there are no meaningful intersections; this is collaborative filtering's oldest problem. **The fix is to seed the corpus with public playlists before launching** — thousands of them, pulled via API, including the fan-made rebuilds of Frank Ocean's list sitting in that Instagram comment section. That makes overlap work on day one *and* stocks the shelves with artist rooms at the same time. Feasibility depends on current Spotify API terms — under verification.

## 📡 Landscape (verified 2026-08-21)

*(Method: iTunes Search API — 14 queries × US + 8 × KR storefronts, 280 unique apps — plus a YouTube channel search. Rating counts are a **traction proxy, not downloads**; relevance-ordered and not exhaustive. **No apps were trialled**, and every claim below is store metadata, not hands-on. Search engines were CAPTCHA-blocked, so no press or funding data was gathered.)*

**My assumption going in — "there's no specific service, people just use YouTube or Spotify" — is false.** A dozen exist. But the real finding is better than the one I assumed: **the category is a graveyard with one survivor, and the survivor won by demanding no curation at all.**

### The dominators — they own the playlist itself

Spotify (**41.5M** ratings global, 444K KR), YouTube Music (**460K** KR — #1 in Korea), Apple Music, and the Korean incumbents NAVER VIBE (77K), 지니 (16K), FLO (14K), 벅스 (7K). Playlists are a native feature of all of them, free, with the audio attached. Anything built here is a **companion to** these, never a replacement.

### The niche — alive vs. dead, by last ship date

| App | Ratings | Last update | Read |
| :--- | ---: | :--- | :--- |
| **Airbuds Widget** | 159,029 | 2026-08-11 | **The winner.** 4.8★, shipping. A home-screen widget — *zero curation*. More App Store ratings than Letterboxd. |
| stats.fm | 46,640 | 2026-08-12 | Claims 15M+ users. Stats, not social. |
| **Superfan** | 2,882 | **2026-08-14** | Shipped a week ago. Claims **500,000 fans**. See the warning below. |
| EQUALS | 8,694 | 2026-08-03 | Launched Nov 2024, still versioned **v0.1.238** |
| bopdrop | 3,709 | 2026-07-13 | Post-a-song-a-day feed |
| Shelf (Koodos) | 3,007 | 2026-08-07 | Cross-platform taste profile — nearest miss to the room idea |
| Echo | 2,022 | 2026-08-05 | Launched Jan 2025, album ranking |
| ~~Discz~~ | 30,689 | 2024-08-15 | **Dead with 30K ratings.** Traction is not survival. |
| ~~핀플리 (Pinply)~~ | 7,902 | 2024-12-05 | **The Korean playlist app. Already tried, already stopped.** |
| ~~8tracks~~ | 1,493 | 2022-06-17 | The original. Was enormous in 2012. |
| ~~Juicebox~~ | 370 | 2022-04-02 | Dead |
| ~~Anthems~~ | 295 | 2025-01-13 | Dead |
| Last.fm | 1,537 | 2026-07-18 | The granddaddy of music-social, now a **2.3★** app |

**Two patterns, and they disagree with each other.** Every app that asks the user to *make* something sits in the low thousands or is dead; the one that asks for nothing has 159K. But 8tracks — the biggest curation play ever — died of **licensing**, not curation fatigue: it streamed real audio. That death does not transfer to a metadata-only design. Don't let the convenient reading win by default; both readings are live.

### ⚠️ Superfan is the direct competitor

Its App Store copy is this note's thesis, nearly verbatim: *"I started Superfan because music didn't feel personal anymore. Streaming made everything available. But it made me feel distant from the artists we love and the friends I used to share music with."* Same diagnosis, same emotional target, 500K claimed users, shipping daily. **Any version of this has to answer "why not Superfan?"** — and I can't answer that until I've actually used it.

### 🇰🇷 The Korean finding — the real competitor isn't an app

Asked where people actually share playlists, the honest answer in Korea is **YouTube channels**, and they are enormous:

| Channel | Subscribers |
| :--- | ---: |
| 때껄룩 ᴛᴀᴋᴇ ᴀ ʟᴏᴏᴋ | **1.86M** |
| 리플레이 LEEPLAY | **868K** |
| 찐막 JJINMAK | 477K |
| 밤공원 | 245K |
| 릴숭어 lil mullet | 114K |

**리플레이's own channel description is this idea, already running:** *"Music that I remember at the moment I took the photo — 사진을 찍었던 순간에 생각나는 음악 몇 곡."* Photo, memory, mood, playlist. 868,000 people subscribe to it.

So the demand is **proven at a scale no app in the table above has reached** — millions of Koreans already consume playlists-as-mood. It's just delivered *broadcast, by creators, on YouTube, for free*.

That reframes the opportunity precisely: **the unbuilt thing is not the mood playlist. It's the mood playlist as something you send to one person instead of publish to a million.** 때껄룩 is one-to-many and parasocial. A room with a door is one-to-one and reciprocal. That's the gap — and it's a much narrower, more defensible claim than "no service exists."

**Next research pass:** actually install Superfan, Airbuds and Shelf; confirm the 8tracks licensing account from press rather than memory; find out why 핀플리 stopped; check whether any 플레이리스트 channel has tried to convert its audience into a product.

### 🎤 The artist-playlist question — asked three times, so it's the real pull

*"I'd be curious about my favourite singer's playlist."* Raised three separate times in one session. Checked directly:

| Tier | Who holds it | Size |
| :--- | :--- | ---: |
| **Curators / DJs / selectors** | **Mixcloud** — running since 2011, still shipping | 89,794 · 4.8★ |
| | **NTS Radio** — 70+ cities, the taste-defining one | 1,979 · 4.9★ |
| **Pop artists** | **Apple Music 1** artist-hosted radio shows; **Spotify Artist Picks** | Owned by the platforms |
| **Friend graph** | Airbuds, MUBR | 159K |

**Correction — Mixcloud and NTS are the wrong comparison. They are mix culture, not list culture.** Those two are not weak competitors for this; they are a different medium entirely, and conflating them hid the gap rather than describing it.

| | **Mix** (Mixcloud, NTS, Boiler Room, RA) | **List** (what this is about) |
| :--- | :--- | :--- |
| Form | One continuous audio file, an hour long | Discrete, named tracks |
| Transparency | Opaque — the tracklist is hidden or absent | Fully scannable; you see every title |
| Agency | Linear, radio-like; you can't pick | Skip, sample, steal one song, save it |
| Who can make one | **DJs.** Requires beatmatching and performance skill | **Anyone with taste.** No skill barrier |
| Hosting | Real audio → licensing, royalties, cost | Metadata + deep links → free |

**Frank Ocean is the proof.** He is not a DJ. He did not mix anything. He wrote down fifty songs he loves. **There is no Mixcloud for that** — which is exactly why it ended up in a 368-page print magazine, and why fans are rebuilding it by hand in an Instagram comment section a decade later.

The same applies to Korea: 때껄룩 and 리플레이 publish **lists** — visible tracklists you can read — not DJ sets. The 1.86M-subscriber phenomenon is list culture, and Mixcloud does not touch it.

So the corrected answer is: for a **non-DJ musician with taste, there is nowhere to put it.** Spotify Artist Picks is one buried pinned item. Apple Music 1 requires a radio show and a deal. Mixcloud requires you to be a DJ. That gap is narrower and more real than "no service exists," and it is not the content-acquisition fight I described a moment ago — the skill barrier is what made supply look impossible, and lists don't have one.

**But Korea already dissolved the supply problem.** 때껄룩 (1.86M) is not a famous musician. 리플레이 (868K) is not a famous musician. They are channels with a consistent, recognisable sensibility, built from nothing in a couple of years.

> **The curator does not need to be famous. They need to be consistent.** Fame is just the cheapest available proxy for *taste I trust* — and Korea proved that proxy can be manufactured from scratch.

**Evidence that the demand is real and unserved — Frank Ocean's list.** When *Blonde* dropped in 2016, Frank Ocean also released **`Boys Don't Cry`**, a 368-page magazine, and buried in it was **a list of 50 of his favourite songs** — Nina Simone, Daft Punk, The Smiths, Aphex Twin, Steve Reich, Todd Rundgren, Stevie Wonder. It ran as a designed two-page spread: the speaker set-up at Rick Rubin's Shangri-La in Malibu on one side, album art alongside the list. Not a bare tracklist — **a room, laid out**.

Genius reposted it a decade later and it took **19K likes and 96 comments in a day** ([reference below](#-references)). The part that matters most is in the comments: **fans immediately posted Spotify and YouTube playlists they had rebuilt from the list by hand**, unprompted, for free.

That is the whole argument in one artifact:

1. The curiosity is **durable** — ten years on, an artist's favourites list is still the most interesting thing about the record.
2. The presentation was **spatial and designed**, not a list. Which is the room thesis, executed in print, in 2016.
3. **No product holds it.** It lived in an out-of-print magazine and now survives as pasted links in an Instagram comment section. Fans are doing the product's job manually because the product doesn't exist.

### ⚠️ The thing I keep describing vs. the thing I keep wanting

Worth writing down plainly, because it's a contradiction at the centre of this note.

**Everything I describe wanting is *looking*, not *showing*.** My favourite singer's playlist. The perfect playlist for my mood. What's in someone else's room. Not once have I described wanting to show mine.

That matters, because the two mechanics are opposed:

- **Mutual exchange** (the reciprocity mechanic recommended earlier) *taxes* looking — you must show to see. If my real drive is curiosity, that mechanic frustrates the exact thing I came for.
- **The curator model** serves looking directly, needs no reciprocity, and is proven at 1.86M subscribers in my own market.

So the door question may have been the wrong question, or at least premature. **The prior question is whether this is a looking product or a showing product** — and I should answer it from my own behaviour rather than from what sounds better.

## Challenges

- **The tool has to work alone.** Instagram shipped filters, VSCO shipped presets, TikTok shipped an editor. Every music social app that died was a feed and nothing else. Whatever the room-building tool is, it must be worth opening with zero followers.
- **Spending the solo-economics constraint has a bill attached** — server, accounts, moderation, and a cold start. That cost is now real and unavoidable.
- **No finite board yet.** 발자취's compulsion came from a complete index waiting to be filled. This has no equivalent, and "come back to look at your own room" is a weak reason to return.
- **Intimacy doesn't scale, and that may be the feature** — but it makes every growth mechanic fight the product's own premise.
- **Streaming API dependency.** Spotify PKCE is client-side, but the terms, rate limits, and the standing risk of the platform closing the door are all outside my control.

## Open Questions

- **What governs the door?** The one blocking question — see the table above.
- **What is the day-one tool?** Narrowed by the mood framing above: it's whatever pitches a set of tracks at a feeling. But *which* controls — title, color, cover, sequence, a line of context, a time of night — and how few can I ship with and still have it feel like craft rather than a form?
- **What replaces the finite board?** Or does the intimacy mechanic carry retention on its own?
- **Is a room a snapshot or a living thing?** A playlist that keeps changing is a different object from one preserved as it was on a particular night — and "the room you had in 2024" may be the more moving artifact.
- **Does the visitor leave a trace?** A guestbook, a mark, silence. Whether visits are visible changes the entire emotional register.
- **Does this collapse back into [[Taste Detector]]?** Both turn consumption into a portrait. That one reads taste privately; this one hands it to another person. Same engine, or two products that merely rhyme?

## 📚 References

- [Instagram — Genius on Frank Ocean's *Boys Don't Cry* favourite-songs list (post, 2026-08-20)](https://www.instagram.com/p/DcR8my7HLYe/?img_index=4) — the 50-song list from the *Blonde* companion magazine, laid out as a designed two-page spread. 19K likes, 96 comments; **fans rebuilt the list as Spotify and YouTube playlists in the comments**, which is the demand evidence. Source for the artist-playlist section above.
- [App Store — 발자취 by Nyeok.Co](https://apps.apple.com/kr/app/id6792431474) — the serverless, solo-built walking app this session started from.
- [YouTube — 때껄룩 ᴛᴀᴋᴇ ᴀ ʟᴏᴏᴋ](https://www.youtube.com/@takealook.) *(1.86M subs)* — proof a playlist curator needs consistency, not fame.
- [YouTube — 리플레이 LEEPLAY](https://www.youtube.com/@leeplay.official) *(868K subs)* — *"사진을 찍었던 순간에 생각나는 음악"*: photo, memory, mood, playlist. This idea, already running as a channel.
- [Melon — 멜론 DJ](https://www.melon.com/dj/today/djtoday_list.htm) — Melon's feature for users to share their own playlists with others, like Spotify. A Korean incumbent already has list sharing built in, so sharing alone isn't the gap.
- [Spotify](https://open.spotify.com/) — my read: its algorithm tailors to a user's taste well, and making a playlist public is easy. This is the bar a companion product has to sit beside, not beat (see *"the same algorithm with the human left in"* above).

## 🔗 Connections

### ⬆ Pipeline
- Back ← [[sparks|✨ Spark List]] — promoted from the `Music-first gallery / creation SNS` spark (2026-08-09)
- Source ← [[../research/music/music-social-media|Music-Focused Social Media Research]] — the three stated killers this thesis answers
- Related → [[Taste Detector]] — the same consumption-as-portrait engine, pointed inward rather than outward
- Related → [[Unified-Media-Insight-Capture-Tool]] — both make the private reaction, not the media, the object of value
- Related → [[Keep in Touch - Relationship Chronicle]] — both bet that intimacy is the scarce thing worth building for
- Hub → [[../index|Master Index]]

---
- **Subject**: [[Startup & Side Projects]]
- **Source**: Brainstorm session 2026-08-21 (Claude Code, Opus 5), starting from [발자취](https://apps.apple.com/kr/app/id6792431474) by Nyeok.Co

<!-- AUTO-CONCEPTS:START -->
### 🔀 Concepts (auto-generated — do not edit)
- **interpretation-over-artifact** → [[Chronicle - Personal Topic Timeline]] (product), [[Company Fit Finder - Where to Work]] (system), [[Finding What You Like - Rekindling Passion & Curiosity]] (system), [[Keep in Touch - Relationship Chronicle]] (system), [[The Connection]] (system), [[Unified-Media-Insight-Capture-Tool]] (product), [[../projects/prd/Chronicle_prd]] (product), [[../projects/prd/Constellate_prd]] (product), [[../research/career/Creative-Tech-Trends]] (career), [[../research/vibecoding/karpathy-llm-wiki]] (vibecoding)
- **abundance-flips-value** → [[Company Fit Finder - Where to Work]] (system), [[Return to Basics]] (system), [[Unified-Media-Insight-Capture-Tool]] (product), [[../projects/Michelin Filter]] (system), [[../research/cooking/coq-au-vin]] (cooking), [[../research/cooking/soupe-a-loignon]] (cooking)
<!-- AUTO-CONCEPTS:END -->
