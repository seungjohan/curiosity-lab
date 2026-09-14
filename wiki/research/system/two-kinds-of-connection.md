---
stage: research
category: system
tag: system
concepts: [bridging-structural-holes]
about: A live brainstorm — the realization that "unexpected connection" splits into two fundamentally different kinds (shared abstract shape vs. shared hidden variable), and that the connection engine so far only finds the first.
type: deep-dive
status: open
---

> [!IMPORTANT] Key Takeaway
> **Why this matters:** The connections that actually excite me (Nike vs Nintendo, Covid → travel/dining) are **not** the kind the engine finds. The engine finds *analogy* (same shape, different domain). Those examples are a different animal: two things wired to the same **hidden variable**. Chasing better analogy was chasing the wrong half.
> **How to use it:** This is a **living note**, not a finished design — captured mid-brainstorm on 2026-08-06 so the thinking (and the open questions) aren't lost. Pick up from "Open questions" below.
> **Informs:** [[connecting_the_dot|Connecting the Dots]], and whether the [[graphrag-connection-engine|proposer]] needs a *second* engine.

# Two Kinds of Connection

The seed was the book framing **"Nike's real competitor is Nintendo."** On the surface, zero relation. But: the more people play Nintendo, the less they go outside, the less their shoes wear out, the fewer Nike they buy. And after Covid, one event flattened travel, dining-out, and gyms all at once. I want *this* kind of unexpected link — and it forced a realization about what the vault's engine can and can't do.

## The split

Everything the vault's engine does finds connection by **similarity** — "these two are the same shape underneath" (Gentner's structure-mapping, embeddings, the abstraction ladder). But Nike/Nintendo aren't the same shape. They're connected by something else:

> They're both secretly wired to **one hidden variable: free time.** Nintendo *consumes* it; Nike *depends on* it being spent outdoors. Not alike — **competing for the same invisible resource.** More of one starves the other.

Covid is its cousin: one hidden *cause* (everyone stays home) fanning out to many effects at once — one shared upstream node, many downstream victims.

| | **Kind 1 — Analogy** (what the engine finds) | **Kind 2 — Hidden shared variable** (Nike·Nintendo) |
| :--- | :--- | :--- |
| The link is | same abstract *shape* | wired to the same *third thing* |
| The two things are | alike underneath | often totally unalike, even opposite |
| You find it by | going **up** — abstract until they meet | going **sideways** — into what each one touches |
| Example | Michelin filter ≈ music discovery | Nike ⇄ Nintendo (both hang on free time) |
| Sub-types | — | substitutes (compete for a resource), complements (rise together), common-cause (one event, many effects) |

## Worked examples (the seeds — keep collecting these)

These are the concrete cases that sparked the whole idea. Each is a Kind-2 link: two unlike things colliding on a hidden node. Append new ones as they come up — examples are the fuel for understanding this.

**1. Nike ⇄ Nintendo** — *"Nike's real competitor is Nintendo"* (book framing).
- Surface: a shoe company and a game company. No relation.
- Hidden variable: **free time.** Nintendo *consumes* it (indoors); Nike *depends on* it being spent outdoors, where shoes wear out and get re-bought.
- Relationship: **substitutes** — they compete for the same finite resource. More Nintendo → less outdoor time → shoes last longer → fewer Nike sales.
- Sign of the collision: opposite (one consumes the resource, the other needs it spent a certain way).

**2. Covid-19 → travel · dining-out · gyms · cinemas** — one shock, many victims.
- Surface: unrelated industries.
- Hidden variable: a shared **upstream cause** — "everyone stays home."
- Relationship: **common-cause fan-out** — one event moves all of them at once, in the same direction.
- Why it's creative: it predicts *co-movement* you'd never guess by comparing the industries to each other. They're linked only through their shared root.

**3. (Complement, for contrast) Grills ⇄ charcoal / razors ⇄ blades** — same hidden variable, *same* sign.
- Hidden variable: the shared activity (grilling, shaving).
- Relationship: **complements** — one's rise *lifts* the other. The opposite sign from substitutes.

The three sub-types of Kind 2, seen across these: **substitute** (compete for a resource, opposite sign), **complement** (enable each other, same sign), **common-cause** (one upstream node, many effects).

*(Next: add your own as you notice them — a stream 😤 blame is often a Kind-2 collision in disguise: "X ruined Y" usually means X and Y share a hidden variable.)*

## Why the current engine can't find Kind 2

This is the important part. `propose_connections.py` scores `surprise = mechanism − topic`, and every input is a **similarity** measure. Nike and Nintendo are *not* similar — embeddings place them far apart, and the abstraction ladder never makes them meet, because there is no shared shape to meet at. **The engine is structurally blind to Kind 2.** We've been perfecting the half that finds analogies while the connections that thrill me are mostly the other half.

## A way to find Kind 2 — the "shadow" method (idea, unbuilt)

You don't compare the two things. You give each thing a **shadow** — not *"what is this an example of?"* (that's Kind 1) but:

> *what does it consume, depend on, produce, compete with, threaten?*

- **Nike's shadow:** `depends on → free time spent outdoors, physical activity`
- **Nintendo's shadow:** `consumes → free time, indoor attention`

They never look alike — but their shadows **collide on "free time," with opposite signs.** That collision *is* the connection. Substitutes collide on a resource with opposite signs; complements with the same sign; Covid-style links collide on a shared *cause*.

Sketch of a second engine: give each note a small **causal card** — `{consumes, depends_on, produces, competes_with, threatened_by}` — then hunt for notes whose cards name the same hidden node. This is a sibling to the mechanism-abstraction card, not a replacement. It's a **directed/resource graph** problem, not a similarity problem.

## How this reframes the principles

- **Burt (structural holes)** — still applies, but the "hole" is now a *shared hidden node* two distant things both touch, not a shared mechanism.
- **TRIZ** — strongly applies: "resources" and "contradiction" are core TRIZ ideas, and Nike/Nintendo is a resource-competition insight.
- **Gentner / embeddings** — this is exactly their **limit**. Both are similarity-based; both miss things that are coupled but not alike.
- **Graph theory** — Kind 2 lives on a *causal* graph with intermediate nodes; finding a link = two nodes with a short path through a shared hidden node.

## Candidate concept atom (not yet created)

`coupled-through-a-hidden-variable` — two unlike things linked because they both touch the same latent resource/cause (substitute, complement, or common-cause). Relational ✓. Only one instance so far (this note), so per [[../../../LINKING.md|LINKING §4]] it's a **candidate, not an atom yet.** Promote it once a second page instances it.

## Open questions (resume here)

1. **Is Kind 2 really the target?** Confirmed strongly by the Nike/Nintendo + Covid examples — but is *all* the creativity I want Kind 2, or a mix of both kinds?
2. **Which hidden variables matter most?** The whole second engine hinges on which latent nodes it watches. Nike/Nintendo was **time**. Candidates: *attention, money, trust, physical presence, status, energy, risk.* Which of these hide the most surprising collisions for the things I care about? ← *left off here.*
3. **One engine or two?** Does Kind 2 become a second mode of `propose_connections.py`, or its own tool? (Different graph, different card.)
4. **Do the paused three gates still apply?** The leak-check was for Kind 1 abstractions; Kind 2 cards need their own quality bar.

## 🔗 Connections

### ⬆ Pipeline
- Back ← [[connecting_the_dot|Connecting the Dots]] — the parent; this note argues its "abstraction ladder" only covers Kind 1
- Pairs with → [[graphrag-connection-engine|GraphRAG & the Connection Engine]] — the similarity engine that is blind to Kind 2
- Hub → [[../../index|Master Index]]

<!-- AUTO-CONCEPTS:START -->
### 🔀 Concepts (auto-generated — do not edit)
- **bridging-structural-holes** → [[../../ideation/The Connection]] (system), [[../../projects/prd/Constellate_prd]] (product), [[AI-Industry-Map-2026]] (system), [[connecting_the_dot]] (system), [[graph-theory-foundations]] (system), [[graphrag-connection-engine]] (system)
<!-- AUTO-CONCEPTS:END -->
