---
name: linking-system
description: Two-axis note linking plus a connection proposer for markdown knowledge bases. Renders concept links you declared, then proposes cross-domain pairs you never made, ranked by surprise (shared mechanism minus shared topic). Use when setting this system up in a new vault or repo, or when tuning/running the proposer.
---

# Linking System

A portable knowledge-linking system for any folder of markdown notes. Stdlib
Python only — no pip installs.

It does three jobs, and the distinction matters:

| | |
|---|---|
| **Renderer** — `build_connections.py` | Draws the links you already declared in `concepts:` frontmatter. Deterministic, idempotent, offline. |
| **Structure** — `graph_analysis.py` | Analyzes the graph those links form: connected components, orphan notes, shortest path between any two notes (BFS/DFS/DSU). Exact, O(V+E), offline. |
| **Proposer** — `propose_connections.py` | Argues for links you *never* declared, by comparing mechanisms across domains. |

A fourth script, `lint_wiki.py`, is the health check: config-driven structural
lint (frontmatter order, required sections, concept-node markers).

## The idea worth keeping

Ranking note pairs by similarity finds notes about the same topic. Those are
the links you already know about — it is a misfiling detector, not an idea
generator.

So every pair gets two scores and the ranking is their difference:

```
surprise = mechanism_similarity − topic_similarity
```

High mechanism, low topic = two clusters in your vault that share a pattern but
no vocabulary. That is Burt's structural hole, and it is where ideas come from.
Same-topic pairs score near zero and sink on their own.

The two similarities come from different embedding models, so raw cosines are
not comparable. Each is converted to a percentile rank inside its own tier
before subtracting.

## The two axes

```
   VERTICAL — the pipeline (hand-written; your judgement)
   Reference ─▶ Research ─▶ Idea ─▶ Project

   HORIZONTAL — concepts (auto-generated; never drifts)
   page ─▶ [[concept]] ◀─ page
```

A **concept atom** is a mechanism, never a noun-topic. The quality bar:

> "This connects because **[specific mechanism]**, not just because they share a topic."

"Both are about product strategy" → too vague, skip.
"Both reduce an overwhelming set to the few that matter via a distinctive key" → an atom.

## Files

Everything vault-specific lives in `linking.config.json`. The scripts contain
no hardcoded paths, headings, or folder names.

| File | Role |
|---|---|
| `scripts/wiki_lib.py` | Config loader, frontmatter parser, path classification, privacy check. Everything imports this. |
| `scripts/lint_wiki.py` | The health check. Config-driven structural lint (frontmatter order, required sections, markers). |
| `scripts/build_connections.py` | The renderer. Writes between `AUTO-` markers only. |
| `scripts/graph_analysis.py` | The structural analyzer. BFS/DFS/DSU components, orphans, shortest paths, degree hubs. |
| `scripts/build_cards.py` | Extracts a mechanism card per note (LLM, or offline from hand-written takeaway lines). |
| `scripts/propose_connections.py` | The proposer. Scores, ranks, writes the report. |
| `linking.config.json` | All the vault-specific settings. |
| `tests/test_wiki_structure.py` | Structural tests driven by the config. |

## Install into another project

```bash
python skills/linking-system/install.py /path/to/other-project
```

That copies the config-driven scripts plus a config template, and copies
nothing vault-specific. Then edit `linking.config.json` in the target — at
minimum `wiki_dir`, `private_paths`, and `required_sections`.
`python install.py --list` prints the exact manifest and what is left behind.

## Running it

```bash
# 0. health check (structural lint)
python scripts/lint_wiki.py

# 1. render the links you declared
python scripts/build_connections.py
python scripts/build_connections.py --check    # CI: exit 1 if stale

# 2. inspect the structure you built
python scripts/graph_analysis.py               # components, orphans, degree hubs
python scripts/graph_analysis.py --verify      # prove BFS = DFS = DSU
python scripts/graph_analysis.py --path A B     # shortest link-chain between two notes

# 3. build mechanism cards
python scripts/build_cards.py --offline        # no API, uses your own prose
python scripts/build_cards.py                  # better: LLM strips the domain

# 4. propose
python scripts/propose_connections.py --explain
```

Read `wiki/_proposals.md`, judge each pair in one breath, and record the verdict
in `wiki/_proposal-decisions.md`. Judged pairs are never proposed again.

## Privacy

`private_paths` in the config lists folders that must never reach an LLM or a
hosted API. The guarantee is structural, not a flag:

- `build_cards.py` iterates a public-only list, so no private note has a code
  path to the API. It re-asserts `is_private()` at the point of transmission.
- Private notes are still *scorable* — they use local Smart Connections block
  vectors, which never leave the disk. Nothing is excluded from the results,
  only from the network.
- `Config.is_private()` fails closed: a path outside the note root counts as
  private.

## Model safety

Vectors from two different embedding models must never be compared — the
scores look plausible and are meaningless. Every vector cache is tagged with
its model id, a changed model triggers a full rebuild, and each tier is
internally single-model.

## Tuning

| Symptom | Knob |
|---|---|
| Nothing above the floor | lower `proposer.mechanism_floor` |
| One note dominates the list | lower `proposer.max_appearances_per_note` |
| Reference tables crowding results | add to `proposer.exclude_globs` |
| Proposals feel obvious | your abstractions still carry domain nouns — switch off `--offline` |

## Known limits

- Offline cards reuse your own prose, which still names its domain. `build_cards.py`
  reports how many abstractions leaked a domain word — treat a high count as a
  signal that the mechanism signal is muddy.
- The proposer is symmetric, so it cannot suggest *direction*. Vertical
  (pipeline) links stay hand-written on purpose.
