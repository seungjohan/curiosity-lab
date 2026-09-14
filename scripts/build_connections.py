#!/usr/bin/env python3
"""
build_connections.py — horizontal-axis link generator.

Reads the `concepts:` frontmatter of every managed page, then:
  1. Writes each page's "### 🔀 Concepts" block (between AUTO-CONCEPTS markers),
     listing sibling pages that share a concept, grouped by concept and
     annotated with each sibling's category.
  2. Writes each concept node's "Instanced by" list (between AUTO-INSTANCES
     markers).

The vertical axis (hand-written "### ⬆ Pipeline" links) is never touched.
Only content between the AUTO markers is managed. Idempotent — safe to rerun.

Usage:
    python scripts/build_connections.py           # write changes
    python scripts/build_connections.py --check   # report only, exit 1 if stale

Paths and markers come from linking.config.json. Stdlib only.
See LINKING.md for the standard this implements.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from wiki_lib import (  # noqa: E402
    load_config, parse_frontmatter, rel_link, replace_block, write_or_check,
)


def build(check: bool) -> int:
    cfg = load_config()
    concepts_start, concepts_end = cfg.concepts_markers
    instances_start, instances_end = cfg.instances_markers

    pages = {p: parse_frontmatter(p.read_text(encoding="utf-8")) for p in cfg.notes()}

    # concept -> pages that instance it (concept nodes themselves excluded)
    concept_pages: dict[str, list[Path]] = {}
    for path, fm in pages.items():
        if cfg.is_concept_node(path):
            continue
        for c in fm.get("concepts", []):
            concept_pages.setdefault(c, []).append(path)

    known_concepts = {p.stem for p in cfg.concepts_dir.glob("*.md") if p.stem != "index"}
    stale: list[str] = []

    for c in concept_pages:
        if c not in known_concepts:
            print(f"  ! concept '{c}' has no node in {cfg.concepts_dir.name}/",
                  file=sys.stderr)

    # 1. per-page concept blocks
    for path, fm in pages.items():
        if cfg.is_concept_node(path):
            continue
        my_concepts = fm.get("concepts", [])
        if not my_concepts:
            continue
        lines = ["### 🔀 Concepts (auto-generated — do not edit)"]
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
        new_text = replace_block(path.read_text(encoding="utf-8"),
                                 concepts_start, concepts_end, "\n".join(lines))
        stale += write_or_check(path, new_text, check, cfg.repo)

    # 2. concept-node instance lists
    for node in sorted(cfg.concepts_dir.glob("*.md")):
        if node.stem == "index":
            continue
        instances = concept_pages.get(node.stem, [])
        if instances:
            lines = ["## Instanced by (auto-generated)"]
            for p in sorted(instances):
                lines.append(f"- {rel_link(node, p)} ({pages[p].get('category', '?')})")
            body = "\n".join(lines)
        else:
            body = "## Instanced by (auto-generated)\n- *(no pages tagged yet)*"
        new_text = replace_block(node.read_text(encoding="utf-8"),
                                 instances_start, instances_end, body)
        stale += write_or_check(node, new_text, check, cfg.repo)

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


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="report stale files without writing; exit 1 if any")
    args = ap.parse_args()
    sys.exit(build(check=args.check))
