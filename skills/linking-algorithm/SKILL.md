---
name: linking-algorithm
description: The owner's linking algorithm for unexpected connections (의외의 연결성) — every resource gets a thinking flow (what moves it, what it moves), two resources link where their flows meet, and the kind of meeting is the reason shown. Also the two-axis note linking and surprise proposer for markdown vaults. Use when designing, tuning or explaining linking for a project; when adapting it to a new kind of resource (web archive, study notes, a day journal…); or when installing or running the vault proposer.
---

# Linking Algorithm

One question runs through every project that uses this skill:

> How do I find a valuable, *unexpected* connection between two things I saved or studied,
> instead of waiting to remember both at once?

Similarity can't answer it. Nike and Nintendo share no words and no embedding neighbourhood;
they meet only through a **third thing**, free time, which one draws people out into and the
other keeps them in from. So the algorithm doesn't compare resources with each other. It writes
down what each resource touches and finds where two of them touch the same thing.

The skill has two parts:

| | What it is | Where it runs |
|---|---|---|
| **Part 1: the algorithm** | Thinking flows and where they meet: the reasoning, the kinds, the scoring, and how to adapt it to a project's own resources. **`core/flowlink.py`** is the latest version in one stdlib file, held to Constellate's own output, with a time layer | Constellate (`algorithm/pipeline/`, and the app's `src/lib/flows.ts`), Dendrite and Dayweb (each runs a copy of `core/flowlink.py`) |
| **Part 2: the vault toolkit** | Two-axis note linking plus the surprise proposer, as portable scripts | curiosity-lab, installable with `install.py` |

Read [references/thinking-flows.md](references/thinking-flows.md) for the full algorithm and
what was measured, and [references/adapting.md](references/adapting.md) before bringing it into
a new project.

---

## Part 1: the algorithm

### Two kinds of connection

| | Kind 1: analogy | Kind 2: hidden shared variable ⭐ |
|---|---|---|
| The link is | the same mechanism | wired to the same third thing |
| Found by | going **up** (abstract until they meet) | going **sideways** (what each touches) |
| Similarity finds it? | sometimes | **never** |

Kind 2 is the one wanted most, and its sharpest form is **the minus**: one thing quietly works
against the other (Nintendo lowers outdoor activity, which Nike needs).

### A thinking flow per resource

```
up        what moves it            {"interest-rates": -1}   it suffers when rates rise
down      what it moves            {"prices": +1}            it pushes prices up
chain     cause → effect steps     [["prices", "youth-emigration", +1]]   up to 3 out
entities  who and what it is about ["Nintendo", "Switch 2"]
```

Variables are **quantities that rise and fall in daily life** (time at home, outdoor activity,
prices, sleep). Abstract nodes (trust, risk, skill) join the unrelated. A variable can be
**limited**: a budget someone spends (free time, attention, money).

### Where two flows meet, and how

Walk each flow up to 3 steps, signs multiplying along the path. Two flows meet wherever they
reach the same variable. *How* they reach it is the kind, and the kind is the reason shown:

| Kind | Shape | Reads as | Justifies a link alone |
|---|---|---|---|
| influence | A reaches X, X moves B | A **feeds** / **works against** B | yes |
| rivals | both drive a *limited* X down | they compete for it | yes |
| opposite pull | both drive X, opposite ways | one undoes the other | yes |
| opposite stakes | X moves both directly, opposite ways | one wins when the other loses | yes |
| co-drivers, shared exposure, distant stakes | same direction, or stakes inferred far down a chain | an ally / a shared topic | **no**, weight only |

`score = kind weight × rarity(X) × 0.7^(hops − 1)`. A variable reached by more than a tenth of
all flows (floor 20) is a **hub**, background rather than a reason ("AI" on every saved page).
A link is shown only when one meeting could justify it on its own.

### Making it trustworthy: the GraphRAG steps

1. **Write both sides.** Without `up`, 5,170 meetings were allies and only 108 influence.
2. **Merge names** (entity resolution). Flows meet only on the very same name: synonyms are renamed,
   is-a steps join narrow to broad, and an edge two flows wrote independently becomes shared.
3. **Check every "because"** before it is shown. 1,707 read, 301 dropped, and the drops traced back to
   weak labels, which were fixed at the source.
4. **Summarise groups** (label propagation, edges weighted by shared neighbours).
5. **Answer whole-archive questions** by map-reduce over those summaries.
6. **Write the flow at capture**, reusing the existing vocabulary.

Then a **QA pass**: a stronger model rechecks what the first one wrote, reports, and fixes only
what the owner approves, after a snapshot.

### Rules learned the hard way

- **An example is one case, not the rule.** Never tune to the example that started it.
- **Direction must be written down.** "Threatened by health" read backwards made gluten
  intolerance an enemy of healthy eating.
- **A remedy lowers its problem; it is not moved by it.**
- **"Both depend on X" is a shared topic, not a mechanism.** Only a direction makes Kind 2.
- **The weakest labels make the worst becauses.** Fixing labels did more than any rule.
- **A verdict is only stable if the ranking is.** Break ties by name: Python randomises set order.
- **The owner's own links are the test** (golden pairs), never pairs the algorithm proposed.
- **Save dates are not the world.** Use publication dates for trends.

### The core, and time

`core/flowlink.py` is Part 1 as code: canonical names, shared and consensus edges, signed reach,
rarity and hubs, meeting kinds, verdicts, groups, bridges, storylines, bursts. `test_flowlink.py`
checks it against Constellate's pipeline on 1,188 meetings, so a project running it runs *the*
algorithm, not a look-alike. Copy `core/flowlink.py`, `flowlink_parity.json` and `test_flowlink.py`
into the project's `scripts/`; the project writes only an adapter that turns its resources into
flows.

The core adds a **time layer** Constellate didn't need (it reads dates only for trends): a flow
may carry `when` (a day, a year, `1600s`, `44 BC`), and then a cause must come before its effect
(otherwise the meeting is *hindsight*: weight, never a reason), and `years_apart` lets each
project weigh distance in time its own way. Where a project is indexed by date, this is where it
differs most.

### Adapting it to a project

**Keep the project's main idea.** The algorithm improves how a project links; it never changes
what the project is for or who writes what. Write the main idea down first and check every
adaptation against it.

The algorithm is the same everywhere; what changes is **who may write a flow**, **what
"distant" means**, and **what has to stay private**. Ask these five questions first:

1. **What is one resource?** A web page, a study note, a day of activity, a moment.
2. **Who may write its flow?** An LLM (public pages), an agent on request (notes in the owner's
   words), or only the owner (private text).
3. **What is distance?** The value is in links across it: topics in Constellate, subjects in
   Dendrite, time in Dayweb. Links that don't cross it count half.
4. **What already links things?** Don't re-propose it: an existing bond, a topic page.
5. **What is the test set?** The owner's own links.

| | Constellate | Dendrite | Dayweb |
|---|---|---|---|
| Resource | saved web page, video, post | study note | day of activity; moments in it |
| Flow written by | Gemini at capture, Claude on request | the bond pass, as `causes` / `enables` / `competes_for` | the owner only: topic labels and `←` `~` `≠` |
| The minus | works against, rivals | `competes_for` | `≠` tension, and signs multiplied |
| Distance | market flow (topic) | subject, and historical time (one moment ≤ 50 years) | time (near days left out; same date last month/year ×1.5) |
| Time rule | dates only for trends | a cause before its effect; common cause and complement are reasons inside one historical moment; studied long ago ×1.25 | "may feed" runs forward and lands within 30 days |
| Already linked | Related panel | 🔗 Bonds | topic pages |
| Test set | golden pairs | bonds `found by: me` | the owner's `~` / `≠` pairs |
| Output | the Related panel, named kinds | ranked bond leads, never written | *Same things* lines and `topics/_leads.md`, never a moment |
| Left out | — | an LLM writing flows, signs on everything, summaries | any LLM on text, summaries (interpretation is myself-lab's) |

---

## Part 2: the vault toolkit

A portable knowledge-linking toolkit for any folder of markdown notes. Stdlib Python only, no
pip installs. It does three jobs, and the distinction matters:

| | |
|---|---|
| **Renderer**: `build_connections.py` | Draws the links you already declared in `concepts:` frontmatter. Deterministic, idempotent, offline. |
| **Structure**: `graph_analysis.py` | Analyzes the graph those links form: connected components, orphan notes, shortest path between any two notes (BFS/DFS/DSU). Exact, O(V+E), offline. |
| **Proposer**: `propose_connections.py` | Argues for links you *never* declared, by comparing mechanisms across domains. |

A fourth script, `lint_wiki.py`, is the health check: config-driven structural lint
(frontmatter order, required sections, concept-node markers).

### The proposer's idea

Ranking note pairs by similarity finds notes about the same topic: links you already know about.
So every pair gets two scores and the ranking is their difference:

```
surprise = mechanism_similarity − topic_similarity
```

High mechanism, low topic = two clusters that share a pattern but no vocabulary (Burt's
structural hole). The two similarities come from different embedding models, so each is
converted to a percentile rank inside its own tier before subtracting. This is Kind 1 done well.
It cannot see Kind 2, which is why Part 1 exists.

### The two axes

```
   VERTICAL: the pipeline (hand-written; your judgement)
   Reference ─▶ Research ─▶ Idea ─▶ Project

   HORIZONTAL: concepts (auto-generated; never drifts)
   page ─▶ [[concept]] ◀─ page
```

A **concept atom** is a mechanism, never a noun-topic. The quality bar, for both parts:

> "This connects because **[specific mechanism]**, not just because they share a topic."

### Files

Everything vault-specific lives in `linking.config.json`. The scripts contain no hardcoded paths,
headings, or folder names.

| File | Role |
|---|---|
| `scripts/wiki_lib.py` | Config loader, frontmatter parser, path classification, privacy check. Everything imports this. |
| `scripts/lint_wiki.py` | The health check. |
| `scripts/build_connections.py` | The renderer. Writes between `AUTO-` markers only. |
| `scripts/graph_analysis.py` | The structural analyzer. |
| `scripts/build_cards.py` | Extracts a mechanism card per note (LLM, or offline from hand-written takeaway lines). |
| `scripts/propose_connections.py` | The proposer. Scores, ranks, writes the report. |
| `linking.config.json` | All the vault-specific settings. |
| `tests/test_wiki_structure.py` | Structural tests driven by the config. |

### Install into another project

```bash
python skills/linking-algorithm/install.py /path/to/other-project
```

Copies the config-driven scripts plus a config template, nothing vault-specific. Then edit
`linking.config.json` in the target, at minimum `wiki_dir`, `private_paths` and
`required_sections`. `python install.py --list` prints the exact manifest.

The thinking-flow part is not installed by this script: its shape depends on the resource, so
each project carries its own adaptation (see [references/adapting.md](references/adapting.md)).

### Running it

```bash
python scripts/lint_wiki.py                    # 0. health check
python scripts/build_connections.py            # 1. render the links you declared
python scripts/build_connections.py --check    #    CI: exit 1 if stale
python scripts/graph_analysis.py               # 2. components, orphans, degree hubs
python scripts/graph_analysis.py --path A B    #    shortest link-chain between two notes
python scripts/build_cards.py --offline        # 3. mechanism cards (no API)
python scripts/propose_connections.py --explain  # 4. propose
```

Read `wiki/_proposals.md`, judge each pair in one breath, and record the verdict in
`wiki/_proposal-decisions.md`. Judged pairs are never proposed again.

### Privacy

`private_paths` lists folders that must never reach an LLM or a hosted API. The guarantee is
structural: `build_cards.py` iterates a public-only list and re-asserts `is_private()` at the
point of transmission; private notes are still scorable with local vectors; `is_private()` fails
closed. The same rule decides Part 1's "who may write a flow".

### Model safety

Vectors from two different embedding models must never be compared. Every vector cache is
tagged with its model id, a changed model triggers a full rebuild, and each tier is single-model.

### Tuning

| Symptom | Knob |
|---|---|
| Nothing above the floor | lower `proposer.mechanism_floor` |
| One note dominates the list | lower `proposer.max_appearances_per_note` |
| Reference tables crowding results | add to `proposer.exclude_globs` |
| Proposals feel obvious | your abstractions still carry domain nouns: switch off `--offline` |

### Known limits

- Offline cards reuse your own prose, which still names its domain.
- The proposer is symmetric, so it cannot suggest *direction*. Part 1's flows can.
