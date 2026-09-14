#!/usr/bin/env python3
"""
build_cards.py — per-note mechanism cards.

For each PUBLIC note, an LLM extracts the transferable mechanism underneath
the topic: the tension it wrestles with, the move that resolves it, and an
`abstraction` written with every domain noun stripped out.

That abstraction is the whole point. Embedding "a curator reduces an
overwhelming set to a few candidates using a signal the crowd ignores"
puts a restaurant note next to a music note. Embedding the note itself
puts it next to other restaurant notes. Relational similarity generates
ideas; topical similarity doesn't.

PRIVACY (decision 10A): notes under `private_paths` are never read here.
The filter is structural — the loop iterates over the public list, so no
code path exists that could send a private note to the API.

Cached by content hash in `.connection-cards/` (gitignored), so a rerun
costs nothing for unchanged notes.

Two sources, same output shape:

  --offline   Build cards from the hand-written "Why this matters" / "How to
              use it" lines already in each note. No API, no cost, works now.
              Weaker: your own prose still carries its domain nouns, so the
              mechanism signal is muddier.
  (default)   Ask an LLM to strip the domain and name the mechanism. Better
              signal, needs a generation-capable API key.

The proposer prefers LLM cards and falls back to offline ones per note, so
you can upgrade a slice at a time.

Usage:
    python scripts/build_cards.py --offline       # no API; start here
    python scripts/build_cards.py                 # LLM cards for public notes
    python scripts/build_cards.py --limit 10      # cheap trial run
    python scripts/build_cards.py --force         # ignore cache, re-extract
    python scripts/build_cards.py --stats         # cache status, no API calls

Stdlib only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from wiki_lib import (  # noqa: E402
    content_hash, die, load_config, load_env_key, parse_frontmatter,
    strip_frontmatter,
)

CARD_SCHEMA = {
    "type": "object",
    "properties": {
        "tension": {"type": "string"},
        "actors": {"type": "array", "items": {"type": "string"}},
        "move": {"type": "string"},
        "constraint": {"type": "string"},
        "abstraction": {"type": "string"},
        "polarity": {"type": "string"},
        "confidence": {"type": "number"},
    },
    "required": ["tension", "actors", "move", "constraint",
                 "abstraction", "polarity", "confidence"],
}

PROMPT = """\
You are extracting the transferable MECHANISM from one note in a personal \
knowledge vault. You are not summarising it.

A mechanism is the pattern the note is an *instance of* — the thing that could \
recur in a completely unrelated domain. The topic is scaffolding; throw it away.

Return JSON with these fields:

- "tension": the contradiction the note wrestles with, as two things in \
conflict. One sentence. If the note names no tension, describe the friction it \
implicitly works around.
- "actors": 2-5 GENERIC roles, e.g. "an overwhelmed chooser", "a noisy signal", \
"a gatekeeper". Never domain nouns.
- "move": the specific action or strategy that resolves the tension. One \
sentence, active voice.
- "constraint": what must hold for the move to work, or what breaks it.
- "abstraction": 1-2 sentences stating the mechanism with EVERY domain noun \
removed. This is the most important field. Forbidden: any word naming the \
note's subject matter or any proper noun. Replace them with generic roles. \
A reader must NOT be able to guess whether this note is about cooking, music, \
careers, software, or anything else. Write it so it could headline a paper in \
any field.
- "polarity": the axis of the tension as "X-vs-Y" in generic terms \
(e.g. "abundance-vs-scarcity", "speed-vs-depth"). Use "" if the note has no \
real polarity.
- "confidence": 0.0-1.0. How clearly does this note express a transferable \
mechanism at all? A raw reference table or a list of facts should score below \
0.3. Be honest — low scores are useful.

Note title: {title}

---
{body}
---

Return only the JSON object."""

# Words that would leak the domain back into the abstraction.
STOPWORDS = {
    "the", "a", "an", "of", "and", "or", "to", "in", "is", "are", "that",
    "this", "it", "its", "for", "on", "with", "as", "by", "be", "not",
    "when", "from", "at", "into", "than", "then", "but", "can", "has",
}


def gemini_card(title: str, body: str, cfg, api_key: str) -> dict:
    model = cfg.llm.get("model", "gemini-2.5-flash")
    url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
           f"{model}:generateContent")
    payload = {
        "contents": [{"parts": [{"text": PROMPT.format(title=title, body=body)}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": CARD_SCHEMA,
            "temperature": 0.4,
        },
    }
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "x-goog-api-key": api_key})
    last_err = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                data = json.load(r)
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(text)
        except (urllib.error.HTTPError, urllib.error.URLError,
                KeyError, json.JSONDecodeError) as e:
            last_err = e
            if isinstance(e, urllib.error.HTTPError) and e.code in (400, 403):
                raise
            import time
            time.sleep(2 ** attempt)
    raise RuntimeError(f"card extraction failed after retries: {last_err}")


WHY_RE = re.compile(r"\*\*Why this matters:\*\*\s*(.+)")
HOW_RE = re.compile(r"\*\*How to use it:\*\*\s*(.+)")
INFORMS_RE = re.compile(r"\*\*Informs:\*\*\s*(.+)")


def _clean(s: str) -> str:
    """Strip callout markers, wikilink brackets and bold from a takeaway line."""
    s = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", s)
    s = re.sub(r"\[\[([^\]]+)\]\]", r"\1", s)
    s = s.replace("**", "").strip().lstrip("> ").strip()
    return s


def offline_card(body: str) -> dict | None:
    """Card built from the note's own hand-written takeaway lines.

    Not an LLM substitute — it is the decision-1 baseline. The author already
    wrote one sentence on why each note matters; nothing was reading it.
    """
    why = WHY_RE.search(body)
    how = HOW_RE.search(body)
    if not why:
        return None
    why_t, how_t = _clean(why.group(1)), _clean(how.group(1)) if how else ""
    informs = INFORMS_RE.search(body)
    return {
        "tension": why_t,
        "actors": [],
        "move": how_t,
        "constraint": _clean(informs.group(1)) if informs else "",
        "abstraction": (why_t + " " + how_t).strip(),
        "polarity": "",
        "confidence": 0.5,
    }


def leak_check(card: dict, title: str, category: str) -> list[str]:
    """Domain words that survived into the abstraction — quality signal."""
    abstraction = card.get("abstraction", "").lower()
    candidates = {w.lower() for w in re.findall(r"[A-Za-z]{4,}", title)}
    candidates.add(category.lower())
    return sorted(w for w in candidates
                  if w not in STOPWORDS and w in abstraction)


def cache_path(cfg, path: Path) -> Path:
    safe = cfg.relpath(path).replace("/", "__").replace(" ", "_")
    return cfg.cards_dir / f"{safe}.json"


def public_notes(cfg) -> list[Path]:
    """The ONLY list the LLM ever sees. Privacy is enforced here, once."""
    return [p for p in cfg.notes(include_concepts=False) if not cfg.is_private(p)]


def build(limit: int | None, force: bool, stats_only: bool,
          workers: int, offline: bool) -> int:
    cfg = load_config()
    cfg.cards_dir.mkdir(parents=True, exist_ok=True)

    source = "offline" if offline else "llm"
    model = "why-line" if offline else cfg.llm.get("model", "gemini-2.0-flash")

    notes = public_notes(cfg)
    private_count = sum(1 for p in cfg.notes(include_concepts=False)
                        if cfg.is_private(p))

    todo = []
    cached = 0
    for path in notes:
        text = path.read_text(encoding="utf-8")
        h = content_hash(text)
        cp = cache_path(cfg, path)
        if cp.is_file() and not force:
            try:
                rec = json.loads(cp.read_text(encoding="utf-8"))
                # An existing LLM card is never downgraded by an offline run.
                if rec.get("hash") == h and (
                        rec.get("source") == source
                        or (offline and rec.get("source") == "llm")):
                    cached += 1
                    continue
            except json.JSONDecodeError:
                pass
        todo.append((path, text, h))

    print(f"{len(notes)} public notes, {private_count} private (never sent).")
    print(f"{cached} cached and current, {len(todo)} need extraction "
          f"(source: {source}).")
    if stats_only:
        return 0
    if limit:
        todo = todo[:limit]
        print(f"--limit {limit}: extracting {len(todo)}.")
    if not todo:
        print("Nothing to do.")
        return 0

    api_key = None
    if not offline:
        key_env = cfg.llm.get("api_key_env", "GEMINI_API_KEY")
        api_key = load_env_key(key_env, cfg.repo)
        if not api_key:
            die(f"{key_env} not found in environment or .env")

    failures: list[str] = []
    leaks: list[str] = []
    skipped: list[str] = []

    def work(item):
        path, text, h = item
        # Belt-and-braces: re-assert privacy at the point of transmission.
        if cfg.is_private(path):
            raise AssertionError(f"private note reached the API path: {path}")
        fm = parse_frontmatter(text)
        body = strip_frontmatter(text).strip()[:12000]
        title = path.stem
        if offline:
            card = offline_card(body)
            if card is None:
                skipped.append(cfg.relpath(path))
                return
        else:
            try:
                card = gemini_card(title, body, cfg, api_key)
            except Exception as e:
                failures.append(f"{cfg.relpath(path)}: {type(e).__name__} {e}")
                return
        leaked = leak_check(card, title, fm.get("category", ""))
        if leaked:
            leaks.append(f"{cfg.relpath(path)}: {', '.join(leaked)}")
        record = {
            "path": cfg.relpath(path),
            "hash": h,
            "source": source,
            "model": model,
            "category": fm.get("category", ""),
            "stage": fm.get("stage", ""),
            "concepts": fm.get("concepts", []),
            "leaked_domain_words": leaked,
            "card": card,
        }
        cache_path(cfg, path).write_text(
            json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")

    with ThreadPoolExecutor(max_workers=1 if offline else workers) as ex:
        list(ex.map(work, todo))

    made = len(todo) - len(failures) - len(skipped)
    print(f"\nExtracted {made} card(s) via {model}.")
    if skipped:
        print(f"{len(skipped)} note(s) have no '**Why this matters:**' line "
              f"and were skipped:")
        for line in skipped[:10]:
            print(f"  - {line}")
    if leaks:
        print(f"{len(leaks)} abstraction(s) still contain a domain word "
              f"(weaker mechanism signal).")
    if failures:
        print(f"\n{len(failures)} failure(s):", file=sys.stderr)
        for line in failures[:10]:
            print(f"  ✗ {line}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--offline", action="store_true",
                    help="build cards from hand-written Why lines; no API")
    ap.add_argument("--limit", type=int, help="extract at most N notes")
    ap.add_argument("--force", action="store_true", help="ignore cache")
    ap.add_argument("--stats", action="store_true", help="report cache only")
    ap.add_argument("--workers", type=int, default=6)
    a = ap.parse_args()
    sys.exit(build(a.limit, a.force, a.stats, a.workers, a.offline))
