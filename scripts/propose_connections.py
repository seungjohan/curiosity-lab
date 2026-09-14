#!/usr/bin/env python3
"""
propose_connections.py — proposes connections you have not made yet.

build_connections.py is a RENDERER: it draws links you already declared.
This is a PROPOSER: it reads the whole vault and argues for pairs you never
tagged.

THE CORE IDEA — surprise, not similarity
----------------------------------------
Ranking pairs by raw note similarity finds notes about the same topic. Those
are the links you already know about; it is a misfiling detector, not an idea
generator. So every pair gets two scores:

    mechanism_similarity   how alike are the underlying mechanisms
    topic_similarity       how alike is the subject matter

    surprise = mechanism_similarity - topic_similarity

A pair that shares a mechanism while sharing no subject matter is exactly
Burt's structural hole: two clusters that never talk. That is where an idea
comes from. Same-topic pairs score near zero and fall away on their own.

The two similarities come from different embedding models with different
cosine distributions, so subtracting raw cosines would be meaningless. Each is
converted to a percentile rank within its own tier first — then the
subtraction compares like with like.

TIERS (decisions 2 and 4) — never mix embedding models inside one comparison
---------------------------------------------------------------------------
  Tier 1  public <-> public   mechanism = card abstraction vectors (hosted)
  Tier 2  any pair touching   mechanism = Smart Connections local block
          a private note      vectors — a private note never leaves the disk

Both tiers take topic similarity from the same local whole-note vectors, so
every pair is scorable and no pair is scored across two models.

Usage:
    python scripts/propose_connections.py            # write wiki/_proposals.md
    python scripts/propose_connections.py --dry-run  # print, write nothing
    python scripts/propose_connections.py --top 40
    python scripts/propose_connections.py --explain  # show score components

Stdlib only.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
import urllib.error
import urllib.request
from fnmatch import fnmatch
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from wiki_lib import (  # noqa: E402
    content_hash, die, load_config, load_env_key, parse_frontmatter,
)

AJSON_LINE = re.compile(r'^"(?P<key>(?:[^"\\]|\\.)*)":\s*(?P<val>\{.*?\}),?\s*$')
VECTOR_CACHE = "_mechanism_vectors.json"


# --------------------------------------------------------------------------
# T4 — Smart Connections .ajson store
# --------------------------------------------------------------------------

def load_smart_env(cfg) -> tuple[dict, dict, str]:
    """Parse the Smart Connections store.

    The store is APPEND-ONLY: the same key is written many times as the plugin
    re-embeds, and earlier copies routinely have no vector at all. Last write
    wins — reading the first match silently yields empty vectors.

    Returns (whole_note_vecs, key_takeaway_vecs, model_id).
    """
    sources: dict[str, dict] = {}
    blocks: dict[str, dict] = {}
    if not cfg.smart_env_dir.is_dir():
        return {}, {}, ""
    for f in sorted(cfg.smart_env_dir.glob("*.ajson")):
        for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line or not line.startswith('"'):
                continue
            m = AJSON_LINE.match(line)
            if not m:
                continue
            key = m.group("key")
            try:
                val = json.loads(m.group("val"))
            except json.JSONDecodeError:
                continue
            if key.startswith("smart_sources:"):
                sources[key[len("smart_sources:"):]] = val   # last write wins
            elif key.startswith("smart_blocks:"):
                blocks[key[len("smart_blocks:"):]] = val

    # Smart Connections indexes from the Obsidian vault root, so its keys carry
    # the wiki/ prefix. Everything else here works in wiki-relative paths.
    prefix = cfg.data.get("wiki_dir", "wiki").strip("/") + "/"

    def to_rel(key: str) -> str | None:
        return key[len(prefix):] if key.startswith(prefix) else None

    model_id = ""
    note_vecs: dict[str, list[float]] = {}
    for path, rec in sources.items():
        rel = to_rel(path)
        if rel is None:
            continue
        emb = (rec or {}).get("embeddings") or {}
        for mid, e in emb.items():
            if e and e.get("vec"):
                note_vecs[rel] = e["vec"]
                model_id = model_id or mid
                break

    # The bare-'#' block is the text before the first heading — the Key
    # Takeaway callout. It is the closest thing to a hand-written mechanism
    # statement that never leaves the machine.
    takeaway_vecs: dict[str, list[float]] = {}
    for key, rec in blocks.items():
        if not key.endswith("#"):
            continue
        rel = to_rel(key[:-1])
        if rel is None:
            continue
        emb = (rec or {}).get("embeddings") or {}
        for _mid, e in emb.items():
            if e and e.get("vec"):
                takeaway_vecs[rel] = e["vec"]
                break
    return note_vecs, takeaway_vecs, model_id


# --------------------------------------------------------------------------
# T5 — pluggable embedder, model-id tagged
# --------------------------------------------------------------------------

def embed_texts(texts: list[str], cfg, api_key: str) -> tuple[list[list[float]], str]:
    """Embed a batch. Returns (vectors, model_id).

    Swap provider here; everything downstream only reads the model_id tag.
    """
    provider = cfg.embedding.get("provider", "gemini")
    model = cfg.embedding.get("model", "gemini-embedding-001")
    dims = int(cfg.embedding.get("dimensions", 768))
    if provider != "gemini":
        die(f"embedding provider {provider!r} not implemented")

    out: list[list[float]] = []
    url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
           f"{model}:batchEmbedContents")
    for i in range(0, len(texts), 90):
        chunk = texts[i:i + 90]
        payload = {"requests": [
            {"model": f"models/{model}",
             "content": {"parts": [{"text": t or " "}]},
             "outputDimensionality": dims}
            for t in chunk]}
        req = urllib.request.Request(
            url, data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json",
                     "x-goog-api-key": api_key})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                data = json.load(r)
        except urllib.error.HTTPError as e:
            die(f"embedding failed ({e.code}): {e.read().decode()[:300]}")
        out.extend(e["values"] for e in data["embeddings"])
    return out, f"{provider}/{model}/{dims}"


def load_or_build_mech_vectors(cfg, cards: dict, refresh: bool) -> tuple[dict, str]:
    """Mechanism vectors for card abstractions, cached by text hash."""
    cache_file = cfg.cards_dir / VECTOR_CACHE
    cache = {}
    if cache_file.is_file() and not refresh:
        try:
            cache = json.loads(cache_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            cache = {}

    model_id = cache.get("model_id", "")
    vecs: dict[str, list[float]] = cache.get("vectors", {})
    hashes: dict[str, str] = cache.get("hashes", {})

    need = [p for p, c in cards.items()
            if hashes.get(p) != content_hash(c["card"]["abstraction"])]
    if need:
        key_env = cfg.embedding.get("api_key_env", "GEMINI_API_KEY")
        api_key = load_env_key(key_env, cfg.repo)
        if not api_key:
            die(f"{key_env} not found; cannot embed mechanism abstractions")
        print(f"  embedding {len(need)} abstraction(s)…")
        new_vecs, new_model = embed_texts(
            [cards[p]["card"]["abstraction"] for p in need], cfg, api_key)
        if model_id and new_model != model_id:
            # Decision 2A: a silent model swap would corrupt every score.
            print(f"  ! embedding model changed ({model_id} -> {new_model}); "
                  f"rebuilding all vectors", file=sys.stderr)
            vecs, hashes = {}, {}
            need = list(cards)
            new_vecs, new_model = embed_texts(
                [cards[p]["card"]["abstraction"] for p in need], cfg, api_key)
        model_id = new_model
        for p, v in zip(need, new_vecs):
            vecs[p] = v
            hashes[p] = content_hash(cards[p]["card"]["abstraction"])
        cache_file.write_text(json.dumps(
            {"model_id": model_id, "vectors": vecs, "hashes": hashes}),
            encoding="utf-8")
    return {p: vecs[p] for p in cards if p in vecs}, model_id


# --------------------------------------------------------------------------
# scoring
# --------------------------------------------------------------------------

def cosine(a: list[float], b: list[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0


def percentile_ranks(values: list[float]) -> list[float]:
    """Map values to [0,1] by rank. Makes two different model spaces
    comparable, which raw cosines are not."""
    n = len(values)
    if n < 2:
        return [0.5] * n
    order = sorted(range(n), key=lambda i: values[i])
    ranks = [0.0] * n
    for pos, i in enumerate(order):
        ranks[i] = pos / (n - 1)
    return ranks


def load_cards(cfg) -> dict:
    cards = {}
    if not cfg.cards_dir.is_dir():
        return cards
    for f in cfg.cards_dir.glob("*.json"):
        if f.name.startswith("_"):
            continue
        try:
            rec = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if rec.get("card", {}).get("abstraction"):
            cards[rec["path"]] = rec
    return cards


def load_decisions(cfg) -> set[tuple[str, str]]:
    """E3 — pairs already accepted or rejected are never proposed again."""
    seen: set[tuple[str, str]] = set()
    if not cfg.decisions_file.is_file():
        return seen
    for line in cfg.decisions_file.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\s*-\s*\[[x ]\]\s*`([^`]+)`\s*<->\s*`([^`]+)`", line)
        if m:
            seen.add(tuple(sorted((m.group(1), m.group(2)))))
    return seen


# --------------------------------------------------------------------------
# T6 — tier routing
# --------------------------------------------------------------------------

def is_boilerplate(cfg, rel: str) -> bool:
    """Index pages, vocabulary lists and reference tables carry no
    transferable mechanism (LINKING.md §5), so they only add noise here."""
    return any(fnmatch(rel, g) or fnmatch("/" + rel, "*/" + g.lstrip("*/"))
               for g in cfg.exclude_globs)


def diversify(scored, limit, max_each):
    """Stop one hub note from filling the whole list."""
    seen: dict[str, int] = {}
    out = []
    for r in scored:
        if seen.get(r["a"], 0) >= max_each or seen.get(r["b"], 0) >= max_each:
            continue
        seen[r["a"]] = seen.get(r["a"], 0) + 1
        seen[r["b"]] = seen.get(r["b"], 0) + 1
        out.append(r)
        if len(out) >= limit:
            break
    return out

def build_pairs(cfg, cards, mech_vecs, note_vecs, takeaway_vecs, fm_by_path):
    """Every scorable pair, assigned to exactly one tier.

    Tier 1 mechanism vectors are hosted-model vectors of LLM/Why abstractions.
    Tier 2 mechanism vectors are local Key-Takeaway block vectors, used for any
    pair touching a private note. A private path never appears in `cards`, so
    it can never reach tier 1 or the hosted embedder.
    """
    all_notes = cfg.notes(include_concepts=False)
    scorable = []
    for p in all_notes:
        rel = cfg.relpath(p)
        if is_boilerplate(cfg, rel):
            continue
        priv = cfg.is_private(p)
        has_mech = (not priv and rel in mech_vecs) or (priv and rel in takeaway_vecs)
        if not has_mech or rel not in note_vecs:
            continue
        scorable.append((p, rel, priv))

    tier1, tier2 = [], []
    for i in range(len(scorable)):
        for j in range(i + 1, len(scorable)):
            (_, ra, priva), (_, rb, privb) = scorable[i], scorable[j]
            fa, fb = fm_by_path.get(ra, {}), fm_by_path.get(rb, {})
            # A connection inside one category is rarely a surprise.
            if fa.get("category") and fa.get("category") == fb.get("category"):
                continue
            # Already linked on a shared atom — you know about this one.
            if set(fa.get("concepts", [])) & set(fb.get("concepts", [])):
                continue
            if priva or privb:
                mech = cosine(takeaway_vecs.get(ra, mech_vecs.get(ra, [])),
                              takeaway_vecs.get(rb, mech_vecs.get(rb, [])))
                if ra in takeaway_vecs and rb in takeaway_vecs:
                    tier2.append((ra, rb, mech))
            else:
                tier1.append((ra, rb, cosine(mech_vecs[ra], mech_vecs[rb])))
    return tier1, tier2


# --------------------------------------------------------------------------
# T8 — surprise scoring
# --------------------------------------------------------------------------

def score_tier(pairs, note_vecs, floor):
    """surprise = rank(mechanism_sim) - rank(topic_sim), within this tier."""
    if not pairs:
        return []
    kept = [(a, b, m) for a, b, m in pairs if m >= floor]
    if not kept:
        return []
    topics = [cosine(note_vecs[a], note_vecs[b]) for a, b, _ in kept]
    mechs = [m for _, _, m in kept]
    mr, tr = percentile_ranks(mechs), percentile_ranks(topics)
    out = []
    for i, (a, b, m) in enumerate(kept):
        out.append({"a": a, "b": b, "mech": m, "topic": topics[i],
                    "mech_rank": mr[i], "topic_rank": tr[i],
                    "surprise": mr[i] - tr[i]})
    out.sort(key=lambda r: -r["surprise"])
    return out


# --------------------------------------------------------------------------
# E1 — candidate new atoms
# --------------------------------------------------------------------------

def cluster_atoms(scored, cards, min_size=3, k=3):
    """Notes that keep co-occurring in surprising pairs but share no atom.

    Connected components are the obvious approach and the wrong one: on a
    dense similarity graph every threshold percolates into a single blob that
    names nothing. So the graph is MUTUAL top-k — an edge survives only if
    each note is among the other's k most surprising partners. That is a much
    stronger claim than "similar enough", and it cannot percolate.

    A surviving group spanning three or more categories is a mechanism your
    concept vocabulary has no name for yet.
    """
    best: dict[str, list[str]] = {}
    for r in scored:
        best.setdefault(r["a"], [])
        best.setdefault(r["b"], [])
        if len(best[r["a"]]) < k:
            best[r["a"]].append(r["b"])
        if len(best[r["b"]]) < k:
            best[r["b"]].append(r["a"])

    mutual: dict[str, set[str]] = {}
    for a, partners in best.items():
        for b in partners:
            if a in best.get(b, []):
                mutual.setdefault(a, set()).add(b)
                mutual.setdefault(b, set()).add(a)

    seen: set[str] = set()
    out = []
    for node in sorted(mutual, key=lambda n: -len(mutual[n])):
        if node in seen:
            continue
        members = {node} | mutual[node]
        # one hop, so a group stays a neighbourhood rather than a component
        if len(members) < min_size:
            continue
        seen |= members
        cats = {cards[m]["category"] for m in members if m in cards}
        if len(cats) < 3:
            continue
        untagged = [m for m in members if not cards.get(m, {}).get("concepts")]
        out.append({"members": sorted(members), "categories": sorted(cats),
                    "untagged": untagged})
    out.sort(key=lambda g: -len(g["members"]))
    return out


# --------------------------------------------------------------------------
# E2 — tension pass
# --------------------------------------------------------------------------

def find_tensions(scored, cards, axis_by_note):
    """Same mechanism, opposite polarity — a TRIZ contradiction in your vault."""
    out = []
    for r in scored:
        if r["mech_rank"] < 0.6:
            continue
        pa = (cards.get(r["a"], {}).get("card", {}).get("polarity") or "").lower()
        pb = (cards.get(r["b"], {}).get("card", {}).get("polarity") or "").lower()
        if not pa or not pb or pa == pb:
            continue
        la, ra_ = (pa.split("-vs-") + [""])[:2]
        lb, rb_ = (pb.split("-vs-") + [""])[:2]
        # Opposed if one note's positive pole is the other's negative pole.
        if (la and la == rb_) or (lb and lb == ra_):
            out.append({**r, "polarity_a": pa, "polarity_b": pb})
    return out


# --------------------------------------------------------------------------
# E4 — atom health
# --------------------------------------------------------------------------

def atom_health(cfg, fm_by_path):
    """LINKING.md's own quality bar, applied to the atom vocabulary."""
    counts: dict[str, list[str]] = {}
    cats: dict[str, set] = {}
    for rel, fm in fm_by_path.items():
        for c in fm.get("concepts", []):
            counts.setdefault(c, []).append(rel)
            cats.setdefault(c, set()).add(fm.get("category", "?"))
    total = sum(len(v) for v in counts.values()) or 1
    rows = []
    for atom, notes in sorted(counts.items(), key=lambda kv: -len(kv[1])):
        share = len(notes) / total
        flags = []
        if share > 0.25:
            flags.append(f"**{share:.0%} of all tags** — likely too vague")
        if len(notes) == 1:
            flags.append("only one instance — a candidate, not a link yet")
        if len(cats[atom]) == 1:
            flags.append(f"confined to *{list(cats[atom])[0]}* — not yet crossing")
        rows.append((atom, len(notes), sorted(cats[atom]), flags))
    orphans = [p.stem for p in cfg.concepts_dir.glob("*.md")
               if p.stem != "index" and p.stem not in counts]
    return rows, orphans


# --------------------------------------------------------------------------
# T7 — report
# --------------------------------------------------------------------------

def fmt_pair(cfg, r, cards, fm_by_path, explain):
    """One proposal. Both sides get their mechanism shown, because the whole
    judgement is 'is this really the same mechanism?' — one side can't answer it."""
    out = []
    a, b = r["a"], r["b"]

    def cat(rel):
        return (fm_by_path.get(rel, {}).get("category")
                or cards.get(rel, {}).get("category") or "?")

    def link(rel):
        return f"[[{Path(rel).with_suffix('').as_posix()}|{Path(rel).stem}]]"

    head = f"- {link(a)} *({cat(a)})*  ↔  {link(b)} *({cat(b)})*"
    if explain:
        head += (f"\n  - `surprise {r['surprise']:+.2f}` "
                 f"= mech {r['mech_rank']:.2f} − topic {r['topic_rank']:.2f}  "
                 f"(raw cos: mech {r['mech']:.3f}, topic {r['topic']:.3f})")
    else:
        head += f"  — `surprise {r['surprise']:+.2f}`"
    out.append(head)
    for rel, label in ((a, "A"), (b, "B")):
        abst = cards.get(rel, {}).get("card", {}).get("abstraction", "")
        if abst:
            out.append(f"  - **{label}.** {' '.join(abst.split())[:200].strip()}")
        else:
            out.append(f"  - **{label}.** *(private — matched on local vectors, "
                       f"no card generated)*")
    return "\n".join(out)


def write_report(cfg, ctx, explain) -> str:
    fm_by_path = ctx["fm"]
    L = []
    L.append("---")
    L.append("stage: general")
    L.append("category: system")
    L.append("---")
    L.append("")
    L.append("> [!IMPORTANT] Key Takeaway")
    L.append("> **Why this matters:** These are connections you have *not* "
             "made. Ranked by surprise — shared mechanism minus shared topic — "
             "so same-subject pairs sink and structural holes float.")
    L.append("> **How to use it:** Read a pair, decide in one breath. Accept → "
             "add a shared `concepts:` atom to both notes. Reject → it costs "
             "nothing. Log either in `_proposal-decisions.md` and it will not "
             "come back.")
    L.append("")
    L.append("# 🔮 Proposed connections")
    L.append("")
    L.append("*Generated by `scripts/propose_connections.py`. "
             "Gitignored and disposable — regenerate any time.*")
    L.append("")
    L.append("| | |")
    L.append("|---|---|")
    for k, v in ctx["funnel"].items():
        L.append(f"| {k} | {v} |")
    L.append("")

    L.append("## 1. Surprising pairs")
    L.append("")
    L.append("*Different categories, no shared atom, similar mechanism.*")
    L.append("")
    if ctx["top"]:
        for r in ctx["top"]:
            L.append(fmt_pair(cfg, r, ctx["cards"], fm_by_path, explain))
    else:
        L.append("*(nothing above the mechanism floor — lower "
                 "`proposer.mechanism_floor` in linking.config.json)*")
    L.append("")

    L.append("## 2. Candidate new atoms")
    L.append("")
    L.append("*Clusters that keep connecting across three or more categories "
             "and have no shared name yet. Name one and it becomes a concept "
             "node.*")
    L.append("")
    if ctx["clusters"]:
        for i, g in enumerate(ctx["clusters"][:6], 1):
            L.append(f"### Cluster {i} — spans {', '.join(g['categories'])}")
            for m in g["members"][:10]:
                L.append(f"- [[{Path(m).with_suffix('').as_posix()}|{Path(m).stem}]]")
            L.append("")
    else:
        L.append("*(no cluster spans three categories yet)*")
        L.append("")

    L.append("## 3. Tensions")
    L.append("")
    L.append("*Same mechanism, opposite polarity — two notes that disagree. "
             "TRIZ says an invention starts here.*")
    L.append("")
    if ctx["tensions"]:
        for r in ctx["tensions"][:10]:
            L.append(fmt_pair(cfg, r, ctx["cards"], fm_by_path, explain))
            L.append(f"  - *poles:* `{r['polarity_a']}` vs `{r['polarity_b']}`")
    else:
        L.append("*(no opposed polarities found — offline cards leave "
                 "`polarity` empty; this section fills in once LLM cards run)*")
    L.append("")

    L.append("## 4. Atom health")
    L.append("")
    rows, orphans = ctx["atoms"]
    L.append("| atom | instances | categories | flag |")
    L.append("|---|---|---|---|")
    for atom, n, cats, flags in rows:
        L.append(f"| `{atom}` | {n} | {', '.join(cats)} | "
                 f"{'; '.join(flags) if flags else '✓'} |")
    if orphans:
        L.append("")
        L.append(f"**Orphan nodes** (exist in `wiki/concepts/`, tagged nowhere): "
                 f"{', '.join('`' + o + '`' for o in orphans)}")
    L.append("")
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--top", type=int, help="pairs to report")
    ap.add_argument("--floor", type=float, help="override mechanism floor")
    ap.add_argument("--dry-run", action="store_true", help="print, write nothing")
    ap.add_argument("--explain", action="store_true", help="show score components")
    ap.add_argument("--refresh-vectors", action="store_true")
    a = ap.parse_args()

    cfg = load_config()
    top_n = a.top or cfg.top_n
    floor = a.floor if a.floor is not None else cfg.mechanism_floor

    cards = load_cards(cfg)
    if not cards:
        die("no cards found — run: python scripts/build_cards.py --offline")

    fm_by_path = {}
    for p in cfg.notes(include_concepts=False):
        fm_by_path[cfg.relpath(p)] = parse_frontmatter(p.read_text(encoding="utf-8"))

    print("Loading Smart Connections vectors…")
    note_vecs, takeaway_vecs, local_model = load_smart_env(cfg)
    print(f"  {len(note_vecs)} whole-note, {len(takeaway_vecs)} key-takeaway "
          f"({local_model or 'none'})")

    print("Loading mechanism vectors…")
    mech_vecs, mech_model = load_or_build_mech_vectors(cfg, cards, a.refresh_vectors)
    print(f"  {len(mech_vecs)} abstraction vectors ({mech_model})")

    if mech_model and local_model and mech_model.split("/")[1] == local_model:
        die("mechanism and topic vectors come from the same model; "
            "surprise would be identically zero")

    t1, t2 = build_pairs(cfg, cards, mech_vecs, note_vecs, takeaway_vecs, fm_by_path)
    s1 = score_tier(t1, note_vecs, floor)
    s2 = score_tier(t2, note_vecs, floor)
    scored = sorted(s1 + s2, key=lambda r: -r["surprise"])

    # E3: never re-propose a pair you have already judged.
    decided = load_decisions(cfg)
    before = len(scored)
    scored = [r for r in scored if tuple(sorted((r["a"], r["b"]))) not in decided]
    print(f"  {before - len(scored)} pair(s) suppressed by "
          f"{cfg.relpath(cfg.decisions_file)}")

    private_notes = [p for p in cfg.notes(include_concepts=False) if cfg.is_private(p)]
    funnel = {
        "notes considered": len(fm_by_path),
        "private (local vectors only, never sent)": len(private_notes),
        "cards available": len(cards),
        "tier 1 pairs (public↔public)": f"{len(t1)} → {len(s1)} above floor",
        "tier 2 pairs (touching a private note)": f"{len(t2)} → {len(s2)} above floor",
        "already judged (suppressed)": len(decided),
        "mechanism floor": f"{floor} (raw cosine)",
        "mechanism model": mech_model,
        "topic model": local_model or "—",
        "card source": ", ".join(sorted({c.get("source", "?") for c in cards.values()})),
    }

    ctx = {
        "funnel": funnel,
        "top": diversify(scored, top_n, cfg.max_appearances),
        "fm": fm_by_path,
        "cards": cards,
        "clusters": cluster_atoms(scored, cards),
        "tensions": find_tensions(scored, cards, {}),
        "atoms": atom_health(cfg, fm_by_path),
    }
    report = write_report(cfg, ctx, a.explain)

    print(f"\n{len(scored)} scorable pairs; top {min(top_n, len(scored))} reported.")
    if a.dry_run:
        print("\n" + report)
        return 0
    cfg.proposals_file.write_text(report, encoding="utf-8")
    print(f"Wrote {cfg.relpath(cfg.proposals_file) or cfg.proposals_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

