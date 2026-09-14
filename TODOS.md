# TODOS

Deferred work, with the reason it was deferred and the condition that should
un-defer it. A vague intention is a lie — if something is worth doing later,
the trigger is written down here.

Source: CEO plan review, 2026-07-28
(`~/.gstack/projects/seungjohan-curiosity-lab/ceo-plans/2026-07-27-connection-proposer.md`)

---

## E5 — Generic node abstraction ("the math is one math")

**The bet.** `graphrag-connection-engine.md:83` argues the vault connects
notes, The Connection connects people, and the same math runs both. If true,
the proposer should operate on an abstract `Node` with an embedding and a
category, not on markdown files.

**Deferred because** there is exactly one node type today. Abstracting over a
single case invents an interface with no second implementation to check it
against, and it always turns out wrong when the second case arrives.

**Un-defer when** a non-note domain actually exists — a real list of people,
companies, or tracks that you want ranked by surprise. At that point the
refactor is small: `build_pairs` and `score_tier` are already free of markdown
assumptions; only card loading and report rendering touch files.

---

## E6 — Vertical-axis proposer

**The idea.** Propose *pipeline* links (`Source ←`, `Feeds →`), not just
horizontal concept links.

**Deferred because** surprise scoring is symmetric — `cos(a,b) == cos(b,a)` —
so it can say two notes belong together but never which one feeds the other.
Direction needs a genuinely different signal: stage ordering, timestamps,
citation direction, or an LLM judgement per pair.

**Un-defer when** you want it enough to accept a slower, LLM-per-pair pass.
`LINKING.md:18` is deliberate — vertical links encode your judgement about
what feeds what — so this may be correct to leave hand-written forever.

---

## Blocked on an external dependency

**LLM mechanism cards.** `scripts/build_cards.py` works, but the Gemini key in
`.env` has `generate_content_free_tier_requests, limit: 0` — zero generation
quota. Embeddings on the same key work fine, so the proposer runs today on
offline cards built from your hand-written "Why this matters" lines.

Un-block by either:
- enabling billing on the Google Cloud project behind `GEMINI_API_KEY`, then
  `python scripts/build_cards.py`; or
- adding `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` to `.env` and adding that
  provider branch to `gemini_card()` in `build_cards.py`.

Expected gain: 58 of 89 offline abstractions still contain a domain word, which
muddies the mechanism signal and is why several current proposals pair a
cooking note with a career note largely because *you already wrote the bridge
into the Why line*. LLM cards read the whole note body and strip the domain,
so the tension pass (report section 3) also stays empty until this is fixed —
offline cards leave `polarity` blank.

---

## Agent context loading

Source: token-discipline audit, 2026-08-12 (triggered by a viral "10 things
senior AI engineers stopped wasting tokens on" post).

**Finding 1 — `AGENTS.md` does not auto-load into Claude Code.** Verified in a
live session: the loaded context was `~/.claude/CLAUDE.md` (global) plus
`memory/MEMORY.md`. There is no project-root `CLAUDE.md`, and the 10.8KB vault
manual was absent. Every session therefore rediscovers the frontmatter rules,
the lifecycle states, the connect-pass protocol, and the logging mandate — or
silently skips them.

**Fix, pending a decision:** either a `CLAUDE.md` at the project root, or a
symlink to `AGENTS.md`. Symlink = one file, can't drift. Separate file = room
for Claude-specific instructions that Gemini and Cursor don't see. Undecided.

**Finding 2 — `skills/linking-system/SKILL.md:38-53` duplicates
`LINKING.md:58-105`** (the two-axis diagram and the quality bar, near-verbatim).
`LINKING.md:4` explicitly forbids this: "do not duplicate these rules
elsewhere." Replace the SKILL.md copy with a pointer.

Note the `AGENTS.md` → `LINKING.md` relationship is *not* duplication —
`AGENTS.md:111` summarises and points at the canonical file. That's correct as
built.

**Finding 3 — the logging mandate is the real per-session token cost.**
`AGENTS.md:130-135` requires every prompt and change to land in `wiki/log.md`,
now 44KB (~11k tokens). An agent appending to the top table will often read the
whole file first.

**Deferred because** the rule earns its keep — it is what makes history
traceable across Claude, Gemini and Cursor, and no cost pressure is being felt
today. **Un-defer when** sessions start hitting usage limits, or the log passes
~100KB. The fix is cheap when needed: split by year into `wiki/log/2026.md`
with a Dataview roll-up, or instruct agents to read only the top N lines.

### What the audit rejected, so it isn't re-litigated

Of the post's 10 points, 6 do not apply here and 3 are wrong:

- **"Streaming responses kill your prompt cache"** — false. Streaming is
  transport; caching is server-side prefix reuse. Unrelated mechanisms.
- **The Andrej Karpathy quote ("90% of your AI coding bill…")** — no locatable
  source. Treat as invented attribution.
- **Model-routing / cheaper-default-model points** — assume a per-token API
  bill. On a Claude subscription the constraint is usage limits, not dollars.
- **"Auto-context loading 50 files", "80,000-token prompts"** — this vault is
  265 markdown files and 784KB of `wiki/`. The 485MB on disk is `.git` (191M),
  `raw/` (116M), `venv` and `.smart-env` — none of which costs a token.

The one point that *did* apply is #7 (write knowledge down once instead of
re-deriving it per session) — and it applied in reverse: the knowledge is
already written, it just wasn't loading. See Finding 1.

---

## Smaller items

- `scripts/lint_wiki.py` still hardcodes `WIKI_DIR`, the Key Takeaway string
  and the Connections heading. Everything else now reads `linking.config.json`.
  Not urgent; it is the last unported script.
- `tests/test_bluer_parser.py` needs `bs4`, which is not installed, so a bare
  `pytest tests/` aborts at collection. Either `pip install beautifulsoup4`
  into `venv/` or delete the test if the Bluer scraper is retired.
- `multi-signal-fusion` holds 28% of all concept assignments and spans
  cooking/product/system. By `LINKING.md:102`'s own bar that is "too vague".
  Consider splitting it into two narrower atoms.
- `bridging-structural-holes` and `ai-as-enabler-not-replacer` are each
  confined to one category, so neither is doing cross-domain work yet.
