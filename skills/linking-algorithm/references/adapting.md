# Adapting the algorithm to a project

The algorithm (thinking-flows.md) is one idea: write down what each resource touches, link two
where they touch the same thing, and name how. Every project that adopts it has to answer five
questions first, because the answers change the code more than any weight does.

## First: keep the main idea

Before any of this, write down what the project is *for* and who writes what, and hold every
change against it. The algorithm improves how a project links; it is never the point of the
project. Dendrite stays a study log that bonds different subjects in my words; Dayweb stays a
vault of my moments that records structure and never interprets.

## Run the core, adapt the flows

Since N311 every project runs the same core, `core/flowlink.py` (tested against Constellate's
output), and writes only an adapter: what a flow is made of, who may write it, and how time
weighs. A re-implementation drifts from the algorithm the moment the algorithm improves.

## The five questions

1. **What is one resource?** The unit that gets a flow. Not always the obvious one: in a day
   journal the day is the container and the *moment* is the unit.
2. **Who may write its flow?**
   - Public text: an LLM may write it, at capture or in a batch.
   - The owner's own words: an agent may fill structured fields **on request**, the owner corrects.
   - Private text: **only the owner**. The flow is whatever the owner already marks: labels,
     links, markers. No text leaves the machine.
3. **What is distance?** The value of a link is crossing something: topics, subjects, time.
   A link that doesn't cross it is the one the owner would have found anyway. **Count it half;
   don't drop it.**
4. **What already links things?** A bond, a topic page, a panel. Don't propose it again; count
   it instead.
5. **What is the test set?** The owner's own links: bonds they found, echoes they wrote, golden
   pairs. Never pairs the algorithm proposed (that's circular).

Then two rules hold everywhere:

- **Propose, don't write**, wherever the owner's words live.
- **Rarity, not counts.** A name on a tenth of everything (floor 20) is background.

## Worked example 1: Constellate (saved web pages)

| Question | Answer |
|---|---|
| Resource | a saved page, video or post (public) |
| Flow written by | Gemini at capture; Claude for batches asked for in a session |
| Distance | market flow (tech, economy, world…); dates only for trends inside one |
| Already linked | the owner's tags, notes and Notion pages: evidence, not proposals |
| Test set | `golden.json`: the owner's rules plus pairs they confirm |

Everything in thinking-flows.md applies. Signs matter here: markets are where "one works
against the other" is common.

## Worked example 2: Dendrite (study notes)

| Question | Answer |
|---|---|
| Resource | a study note, one subject, in the owner's words ("organize, don't add") |
| Flow written by | the bond pass, filling three link fields, on request |
| Distance | **subject**: French ⇄ biology is the value; a lead inside one subject counts half |
| Already linked | 🔗 Bonds (each "connects because ___", `found by: me` or `bond pass`) |
| Test set | bonds `found by: me` |

The note already answered half the shadow question (era, people, place, threads). What it
lacked was direction, so three fields were added:

```yaml
causes: ["[[the infinitely small]]"]   # what made this happen   (up)
enables: ["[[germ theory]]"]           # what this made possible (down)
competes_for: ["[[free time]]"]        # what it fought others for (the minus)
```

**Adapt the structure, not just add a script.** Each Kind 2 sub-type got its own field, so the
vault itself can say how two notes meet:

- the note footer has typed columns: ⬅ led here via · ➡ led on via · 🌱 same cause · ⚔ both
  fought for · also shares (Dataview, always on);
- the third thing gets a **node page** (a template) that lists notes by their role toward it:
  what it caused, what made it possible, who fought over it. The bridge made visible;
- every bond names its kind, so who finds which kind of connection can be counted;
- the index gains *One cause, many subjects* and *Fought over across subjects*.

The script (`bond_leads.py`) ranks for a bond pass: kinds weighted, rare nodes first, a lead inside
one subject at half, era/people/place weight only, plus storylines, spellings to merge and open
questions a note may touch.

Code: `dendrite/scripts/bond_leads.py`, 14 tests; templates `dendrite.md`, `node.md`. It prints; it never writes a note.

## Worked example 3: Dayweb (days and moments)

| Question | Answer |
|---|---|
| Resource | a day of activity (notes created, diary entries, commits) and, inside it, moments |
| Flow written by | **only the owner**: topic labels (tags, folders, journals, repos) and `←` `~` `≠` |
| Distance | **time**: the verb is *remind*; a link inside one week counts half |
| Already linked | topic pages (every day of one subject), so a shared topic halves a day link and never makes one alone |
| Test set | the owner's `~` / `≠` day pairs: PRD §7 waits on this before any semantic tier |

**The third thing is time itself.** Every subject draws on the same limited budget of days, so
the meeting kinds are read from how topics move through months (monthly share of active days):

- **trades off with**: one takes more of my days when the other takes less (the minus on a
  calendar). Only steady habits are compared (6+ shared months, each on in a quarter of them):
  without that, 191 pairs, mostly topics that merely happened apart; with it, 62;
- **rises with** · **began after** (the week before its first day) · **busiest** (Kleinberg) ·
  **gone quiet**: on each topic page, typed;
- **in the flow** on each day note: a topic's first day, its return after 30+ days, its busiest
  stretch (549 of 882 days);
- day-to-day links: words decide; the same week, or a topic both share, counts half (280 of
  1,458 re-ranked; inside a week 438 → 247);
- moments: echo +1, tension −1, two moments tied to one third take the product (Heider's
  balance) to propose `~` or `≠`; 3+ echoes become a line to name; the owner's own echoes are
  the test.

The vault's LINKING.md was rewritten as its own (it had been the study vault's copy).

Left out, on purpose: any LLM on text (myself-lab and Day One are private), summaries
(interpretation is myself-lab's job).

Code: `dayweb/scripts/day_links.py`, used by `analyze_days.py` and `build_topics.py`, 16 tests,
mutation-checked. Output: `topics/_leads.md`, gitignored; counts only on screen.

## The role of the date differs by project (N314)

| | Constellate | Dendrite | Dayweb |
|---|---|---|---|
| What leads | what the resource is about | **what I studied** (each log a dot) | **time** (each day a dot) |
| Role of the date | trends inside a market flow | a nudge: cause before effect, one historical moment ×1.1, studied long ago ×1.1 | the direction of the search: *grew from* walks each day back through its strongest earlier links; growth lines carry a topic forward |

## Where dates matter more (N311)

| | Dendrite | Dayweb |
|---|---|---|
| Time it knows | `year`/`era` (when the events happened), `date` (when studied) | the day itself |
| A cause before its effect | yes: backwards "led to" is hindsight | yes: "may feed" runs forward only |
| How distance in time weighs | one historical moment (≤ 50 years) makes common cause and complement reasons, ×1.25; studied 90+ days apart ×1.25 | near days (≤ 7) left out; "may feed" within 30 days; same date last month/year ×1.5 |
| Date index shown | Timeline (by `year`), Studied this week back then, storyline in historical order | On this date, In the flow, Through my labels, Often follows / followed by |

## Checklist for a new project

- [ ] Write the project's main idea first; every change is checked against it.
- [ ] Copy the core (`core/flowlink.py` and its test); write only the adapter.
- [ ] No app? Then the links must live in the pages: a regenerable block in every page and in the template, refreshed after each new page (Dendrite `bond_leads.py --write`, Dayweb `relink.py`).
- [ ] Keep a linking log in the project, so its history can be followed up there.
- [ ] Answer the five questions in the project's own agent file.
- [ ] Decide the flow fields from what the resource already carries; add only what is missing
      (usually direction).
- [ ] Put the kinds into the project's own structure (footers, hub pages, typed links), not
      only into a report. A script beside the vault is not an adaptation.
- [ ] Name every kind with a sentence a person can check.
- [ ] Rarity weighting and a hub cut; deterministic ties.
- [ ] Count-half for links that don't cross the project's distance.
- [ ] Output is a proposal the owner accepts, unless the owner said otherwise.
- [ ] Tests on a made-up fixture, mutation-checked; real data checked by counts if it is private.
- [ ] Measure against the owner's own links before tuning anything.
