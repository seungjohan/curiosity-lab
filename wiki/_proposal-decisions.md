---
stage: general
category: system
---

> [!IMPORTANT] Key Takeaway
> **Why this matters:** A proposer that keeps re-suggesting a pair you already rejected becomes noise, and you stop reading it. This file is the memory that stops that.
> **How to use it:** Move a pair here from [[_proposals|Proposed connections]] once you have judged it. Tick the box if you accepted it. Either way it will never be proposed again.
> **Informs:** `scripts/propose_connections.py`, which reads this file on every run.

# ⚖️ Proposal decisions

One line per judged pair. The format is parsed, so keep it exactly:

```markdown
- [x] `path/a.md` <-> `path/b.md` — accepted, tagged `atom-name`
- [ ] `path/a.md` <-> `path/b.md` — rejected, only a shared vocabulary
```

Paths are wiki-relative, in backticks, separated by `<->`. Everything after the
em dash is a free note to yourself; the parser ignores it.

This file is tracked in git — unlike `_proposals.md`, your judgements are worth
keeping.

## Decisions

<!-- add lines below -->

## 🔗 Connections

### ⬆ Pipeline
- Source ← [[_proposals|Proposed connections]] — where the pairs come from
- Feeds → [[../LINKING|Linking Standard]] — accepted pairs become `concepts:` tags
