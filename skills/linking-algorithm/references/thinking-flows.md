# Thinking flows: the algorithm in full

The reference implementation is Constellate's `algorithm/pipeline/` (branch `algorithm`), tested
on a snapshot of a 993-resource archive of saved pages, videos and posts. Its running record is
`LINKING-ALGORITHM.md` §6–§9 in that repo; backlog rows N273–N308 hold every request behind it.

## How it got here

| Step | Idea | Why it changed |
|---|---|---|
| Keyword overlap | link what shares tags and keywords | finds the same topic only; generic words (`music`) linked everything |
| Surprise proposer | mechanism similarity − topic similarity | Kind 1 done well; still blind to Kind 2 |
| Causal card | `{consumes, depends_on, produces, competes_with, threatened_by}` per item | direction was implicit and got read backwards |
| Signed arrows (N293) | what a thing pushes or needs, up or down | made **the minus** visible: one quietly works against the other |
| Thinking flows (N303) | a small signed graph per resource, meetings named by kind | "an example is one case, not the rule": general, not tuned to Nike/Nintendo |
| GraphRAG steps (N307) | both sides, merged names, checked becauses, summaries, questions, capture | each fixed a measured failure (below) |

## The flow

```json
{
  "up":       {"time-at-home": -1},
  "down":     {"outdoor-activity": 1, "running-shoe-demand": 1},
  "chain":    [["outdoor-activity", "running-shoe-demand", 1]],
  "entities": ["Nike"]
}
```

Writing rules, each learned from a failure:

- **Reuse before you coin.** Two flows meet only on the very same name; 806 variables for 993
  flows meant `eating-out` and `pizzeria-demand` never met. The writer is shown the existing
  vocabulary (at capture: the 150 most used).
- **Quantities, not themes.** Variables rise and fall: outdoor activity, prices, sleep.
- **Direction is explicit.** Every arrow carries +1 or −1.
- **A remedy lowers its problem.** An anti-anxiety video *lowers* anxiety; written as "moved up
  by anxiety" it made two anti-anxiety videos work against each other.
- **Up and down never share a variable.** If both, keep it on `down`.
- **Small.** At most 3 per side, 3 chain steps, 6 entities.
- **`limited`** marks a budget someone spends (free time, attention, money): what turns "both
  lower it" into rivalry.

## Reach

From `down`, walk forward along the flow's own chain plus the **shared edges**; from `up`, walk
backward. Up to `MAX_HOPS = 3`; the sign is the product along the path.

Shared edges, walked by every flow:
- `is_a` steps (narrow → broad, +1): `pizzeria-demand` is a kind of `eating-out`.
- a short `world` list of general cause and effect.
- **consensus**: an edge written by `CONSENSUS = 2` or more separate flows. Two independent
  readings agreeing is better evidence than either alone.

Synonyms are renamed first (`same`, `entities` in `canon.json`).

## Meetings

For flows A and B, every variable both reach is a meeting. Its kind:

| Kind | A | B | Weight | Alone? | Sentence |
|---|---|---|---|---|---|
| influence | reaches X | is moved by X | 1.0 | yes | A → more X → less Y → works against B |
| rivals | lowers limited X | lowers limited X | 0.9 | yes | they compete for X |
| opposite-pull | raises X | lowers X | 0.8 | yes | one undoes the other |
| opposite-stakes | gains when X rises | loses when X rises, both direct | 0.8 | yes | one wins when the other loses |
| co-drivers | raises X | raises X | 0.5 | no | allies |
| shared-exposure | moved by X | moved by X, same way | 0.4 | no | a shared topic |
| distant-stakes | opposite stakes found down a chain | | 0.4 | no | measured as noise: 3,936 pairs |

```
meeting score = weight × idf(X) × 0.7^(hops − 1)
idf(X)        = ln((N + 1) / (df + 1)) + 1
```

A variable reached by more than 10% of flows (floor 20) is a **hub**, skipped as a reason.
Meetings sort by (−score, variable, kind); ties broken by name everywhere, because Python
randomises set order and verdicts keyed to a ranking otherwise churn between runs.

## In the linker

Flows are one source of evidence among several; Constellate's linker sums them all:

| Evidence | Weight |
|---|---|
| summary similarity | 1.0 × cosine, floor 0.12 |
| shared hashtag | 0.035 × rarity |
| shared keyword | 0.03 × rarity; a superset word (on > 5% of the archive) counts ¼ |
| same creator | 0.05 × rarity (the source, e.g. YouTube, is too broad to use) |
| a focused note of the owner's citing both | 0.5 |
| a Notion page holding both | 0.3 |
| thinking-flow meeting | 0.04 × meeting score |
| shared entity | 0.06 × rarity |

A link is shown when **one** piece could justify it alone, or the specific evidence together
reaches **0.2** (two rare keywords, say). Then × the owner's own lift (favourite +0.3, Later +0.1,
sticker +0.1 each, up to three); top 6. Allies add weight but are never the reason shown.

Every link names its kind: your tag · same entity · same topic · same creator · your note ·
keywords together · pulls against · feeds · works against.

## Checked becauses

`verify.py` lists every meeting behind a shown link not yet judged; a model reads each with both
resources' titles and summaries and records `held` or `dropped`, keyed
`"a|b|variable|kind"` (a, b sorted). Dropped meetings are filtered before scoring.

1,707 read, 301 dropped. The drops clustered on a few weak labels: "tech hiring" on every career
post, "gear spending" on every tutorial, "AI coding works against learning X". Fixing 299 labels
at the source did more than any rule.

## Graph layer

- **Groups**: label propagation over the panels, each edge weighted 1 + shared neighbours (plain
  propagation flooded across a single edge).
- **Summaries**: per group of 4+, name · what · drivers · what is changing. Stored, and matched to
  today's groups by Jaccard ≥ 0.5, so a stale summary shows as stale.
- **Suggested flows**: groups mostly unfiled, named by their summary.
- **Bridges**: resources with a foothold of 2 links in each of 2 groups (betweenness alone ranked
  vague shorts first).
- **Bursts**: Kleinberg's two-state model, S = 3 (his 2 is for thousands of items a month),
  γ = 1, dated by **publication**: 971 of 993 were saved in one import month.
- **Storylines**: Shahaf & Guestrin's max-min chain: the weakest link in a chain is maximised.

## Whole-archive questions

`ask.py` ranks group summaries against the question by TF-IDF, then a model maps over the top
groups (with their resources) and reduces to one answer that cites groups.

## At capture

The app asks its model for the flow alongside the rest of the enrichment, listing the archive's
existing variables so new resources reuse names. Stored as JSON on the item. The guard enforces
the writing rules (at most 3 per side, up ∩ down removed from up).

## QA pass

A stronger model rechecks what the capture model wrote against the page and the capture rule:
it reports, then applies only fixes the owner approves, after a snapshot, never to fields the
owner edited, never over a value that changed since the check, and logs each fix.

## Measured on the archive

| | |
|---|---|
| Links resting on generic keys | 25% → 0% |
| Links on superset words only | 35% → 0% |
| Influence meetings once flows had an up side | 108 → thousands |
| Minus pairs reaching a panel | 85 (34 across topics) |
| Becauses read / dropped | 1,707 / 301 |
| Owner's rule (Tame Impala) | 0 violations |
| Golden pairs (proposed, not the owner's) | 5 / 6 |
