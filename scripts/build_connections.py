#!/usr/bin/env python3
"""
build_connections.py — horizontal-axis link generator for curiosity-lab.

Reads the `concepts:` frontmatter of every page under wiki/, then:
  1. Writes each page's "### 🔀 Concepts" block (between AUTO-CONCEPTS markers),
     listing sibling pages that share a concept, grouped by concept and
     annotated with each sibling's category.
  2. Writes each concept node's "Instanced by" list (between AUTO-INSTANCES
     markers) in wiki/concepts/.

The vertical axis (hand-written "### ⬆ Pipeline" links) is never touched.
Only content between the AUTO markers is managed. Idempotent — safe to rerun.

Usage:
    python scripts/build_connections.py          # write changes
    python scripts/build_connections.py --check   # report only, exit 1 if stale

No third-party dependencies (stdlib only).
See LINKING.md for the standard this implements.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
WIKI = REPO / "wiki"
CONCEPTS_DIR = WIKI / "concepts"

CONCEPTS_START = "<!-- AUTO-CONCEPTS:START -->"
CONCEPTS_END = "<!-- AUTO-CONCEPTS:END -->"
INSTANCES_START = "<!-- AUTO-INSTANCES:START -->"
INSTANCES_END = "<!-- AUTO-INSTANCES:END -->"

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def parse_frontmatter(text: str) -> dict:
    """Minimal frontmatter reader. Supports `key: value` and inline
    `concepts: [a, b, c]` lists — the only structure this script needs."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    fm: dict = {}
    for line in m.group(1).splitlines():
        if ":" not in line or line.startswith(" "):
            continue
        key, _, val = line.partition(":")
        key, val = key.strip(), val.strip()
        if val.startswith("["):
            # inline flow list; parse only within brackets, ignore trailing # comment
            end = val.find("]")
            inner = val[1:end] if end != -1 else val[1:]
            fm[key] = [x.strip() for x in inner.split(",") if x.strip()]
        else:
            # scalar; strip trailing YAML comment
            if " #" in val:
                val = val.split(" #", 1)[0].strip()
            fm[key] = val
    return fm


def rel_link(src: Path, dst: Path) -> str:
    """Obsidian relative wikilink from src file to dst file, no .md."""
    rel = os.path.relpath(dst.with_suffix(""), src.parent)
    return f"[[{rel}]]"


def replace_block(text: str, start: str, end: str, body: str) -> str:
    """Replace content between start/end markers. If markers are absent,
    append a fresh block. Returns updated text."""
    block = f"{start}\n{body}\n{end}"
    if start in text and end in text:
        pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
        return pattern.sub(lambda _: block, text, count=1)
    # append before trailing whitespace
    return text.rstrip() + "\n\n" + block + "\n"


def load_pages() -> dict[Path, dict]:
    pages = {}
    for path in WIKI.rglob("*.md"):
        fm = parse_frontmatter(path.read_text(encoding="utf-8"))
        pages[path] = fm
    return pages


def build(check: bool) -> int:
    pages = load_pages()

    # concept -> list of page paths that instance it (excluding concept nodes)
    concept_pages: dict[str, list[Path]] = {}
    for path, fm in pages.items():
        if CONCEPTS_DIR in path.parents:
            continue
        for c in fm.get("concepts", []):
            concept_pages.setdefault(c, []).append(path)

    known_concepts = {p.stem for p in CONCEPTS_DIR.glob("*.md") if p.stem != "index"}
    stale: list[str] = []

    # warn on concepts referenced but with no node
    for c in concept_pages:
        if c not in known_concepts:
            print(f"  ! concept '{c}' has no node in wiki/concepts/", file=sys.stderr)

    # 1. per-page concept blocks
    for path, fm in pages.items():
        if CONCEPTS_DIR in path.parents:
            continue
        my_concepts = fm.get("concepts", [])
        if not my_concepts:
            continue
        lines: list[str] = ["### 🔀 Concepts (auto-generated — do not edit)"]
        any_sibling = False
        for c in my_concepts:
            siblings = [p for p in concept_pages.get(c, []) if p != path]
            if not siblings:
                continue
            any_sibling = True
            refs = ", ".join(
                f"{rel_link(path, s)} ({pages[s].get('category', '?')})"
                for s in sorted(siblings)
            )
            lines.append(f"- **{c}** → {refs}")
        if not any_sibling:
            lines.append("- *(no cross-links yet — concept has only one instance)*")
        body = "\n".join(lines)
        new_text = replace_block(path.read_text(encoding="utf-8"),
                                 CONCEPTS_START, CONCEPTS_END, body)
        stale += write_or_check(path, new_text, check)

    # 2. concept-node instance lists
    for node in CONCEPTS_DIR.glob("*.md"):
        if node.stem == "index":
            continue
        instances = concept_pages.get(node.stem, [])
        if instances:
            lines = ["## Instanced by (auto-generated)"]
            for p in sorted(instances):
                cat = pages[p].get("category", "?")
                lines.append(f"- {rel_link(node, p)} ({cat})")
            body = "\n".join(lines)
        else:
            body = "## Instanced by (auto-generated)\n- *(no pages tagged yet)*"
        new_text = replace_block(node.read_text(encoding="utf-8"),
                                 INSTANCES_START, INSTANCES_END, body)
        stale += write_or_check(node, new_text, check)

    if check:
        if stale:
            print(f"STALE: {len(stale)} file(s) need regeneration:", file=sys.stderr)
            for s in stale:
                print(f"  - {s}", file=sys.stderr)
            return 1
        print("Connections up to date.")
        return 0

    print(f"Wrote concept links across {len(concept_pages)} concept(s), "
          f"{sum(len(v) for v in concept_pages.values())} tag(s).")
    return 0


def write_or_check(path: Path, new_text: str, check: bool) -> list[str]:
    current = path.read_text(encoding="utf-8")
    if current == new_text:
        return []
    if check:
        return [str(path.relative_to(REPO))]
    path.write_text(new_text, encoding="utf-8")
    return [str(path.relative_to(REPO))]


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="report stale files without writing; exit 1 if any")
    args = ap.parse_args()
    sys.exit(build(check=args.check))
