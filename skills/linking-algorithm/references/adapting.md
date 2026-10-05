# Adapting the algorithm to a project

The algorithm (thinking-flows.md) is one idea: write down what each resource touches, link two
where they touch the same thing, and name how. Every project that adopts it has to answer five
questions first, because the answers change the code more than any weight does.

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

Kinds: led to (A enables what causes B) · common cause · competition · same mechanism (Kind 1
concept) · shared thread · complement. Era, people and place add weight only: "both about Europe"
fails the quality bar. Context-only leads need two shared names and are flagged.

Extra outputs fitted to the vault's habits: storylines (notes chained by enables → causes across
subjects), names in 3+ subjects ("secretly one story"), spellings to merge (`[[17th century]]` ⇄
`[[1600s]]`), open questions a note may touch.

Left out, on purpose: an LLM writing fields (notes are the owner's words), signs on everything
(one minus covers it), group summaries (not until there are many notes).

Code: `dendrite/scripts/bond_leads.py`, 13 tests, mutation-checked. It prints; it never writes.

## Worked example 3: Dayweb (days and moments)

| Question | Answer |
|---|---|
| Resource | a day of activity (notes created, diary entries, commits) and, inside it, moments |
| Flow written by | **only the owner**: topic labels (tags, folders, journals, repos) and `←` `~` `≠` |
| Distance | **time**: the verb is *remind*; a link inside one week counts half |
| Already linked | topic pages (every day of one subject), so a shared topic halves a day link and never makes one alone |
| Test set | the owner's `~` / `≠` day pairs: PRD §7 waits on this before any semantic tier |

The day links come from shared words (unchanged gate) and are re-ranked by the two halvings. On
882 days the same 1,458 links stayed, re-ranked: 280 changed, links inside one week 438 → 247,
links between days no topic joins 485 → 670.

Moments carry signs the owner writes: echo +1, tension −1. Two moments tied to one third take the
product (Heider's balance), proposing `~` or `≠`. A split vote proposes nothing. Three or more
moments joined by echoes become a line to name (the owner names threads).

Over time (no text needed): **gone quiet** (on a topic in the last 90 days, none in the last 14),
**bursts** (Kleinberg over active days per month), **where a topic came from** (what else was
active in the week before it began, the flow's up side read from dates).

Left out, on purpose: any LLM on text (myself-lab and Day One are private), summaries
(interpretation is myself-lab's job).

Code: `dayweb/scripts/day_links.py` (+ `analyze_days.py` uses its ranking), 13 tests,
mutation-checked. Output: `topics/_leads.md`, gitignored; counts only on screen.

## Checklist for a new project

- [ ] Answer the five questions in the project's own agent file.
- [ ] Decide the flow fields from what the resource already carries; add only what is missing
      (usually direction).
- [ ] Name every kind with a sentence a person can check.
- [ ] Rarity weighting and a hub cut; deterministic ties.
- [ ] Count-half for links that don't cross the project's distance.
- [ ] Output is a proposal the owner accepts, unless the owner said otherwise.
- [ ] Tests on a made-up fixture, mutation-checked; real data checked by counts if it is private.
- [ ] Measure against the owner's own links before tuning anything.
