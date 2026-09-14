#!/usr/bin/env python3
"""
install.py — copy the linking system into another project.

Copies only the portable files: the config-driven scripts, a config template,
and the structural tests. Nothing vault-specific comes along — no concept
nodes, no notes, no tag maps.

Usage:
    python skills/linking-system/install.py /path/to/other-project
    python skills/linking-system/install.py /path/to/other-project --force
    python skills/linking-system/install.py --list
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent
REPO = SKILL_DIR.parent.parent

# (source relative to repo root, destination relative to target root)
PORTABLE = [
    ("scripts/wiki_lib.py", "scripts/wiki_lib.py"),                    # shared: config, parsing, privacy
    ("scripts/lint_wiki.py", "scripts/lint_wiki.py"),                 # health: config-driven structural linter
    ("scripts/build_connections.py", "scripts/build_connections.py"), # renderer: declared concept links
    ("scripts/graph_analysis.py", "scripts/graph_analysis.py"),       # structural: BFS/DFS/DSU, orphans, paths
    ("scripts/build_cards.py", "scripts/build_cards.py"),             # proposer: per-note mechanism cards
    ("scripts/propose_connections.py", "scripts/propose_connections.py"), # proposer: undeclared pairs by surprise
    ("tests/test_wiki_structure.py", "tests/test_wiki_structure.py"), # config-driven structural tests
    ("setup.cfg", "setup.cfg"),
]

TEMPLATE = ("skills/linking-system/linking.config.template.json",
            "linking.config.json")

GITIGNORE_LINES = [
    "# Connection proposer (generated)",
    ".connection-cards/",
    "wiki/_proposals.md",
]

NOT_PORTABLE = """\
Deliberately NOT copied — these encode this vault's judgement, not the system:
  wiki/concepts/*.md        your concept vocabulary; grow a new one
  LINKING.md                the standard, worth rewriting in your own words
  linking.config.json       you get the template instead
  tests/test_proposer.py    privacy/model tests coupled to this vault's config
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("target", nargs="?", help="destination project root")
    ap.add_argument("--force", action="store_true", help="overwrite existing files")
    ap.add_argument("--list", action="store_true", help="show the manifest and exit")
    a = ap.parse_args()

    if a.list or not a.target:
        print("Portable files:")
        for src, dst in PORTABLE + [TEMPLATE]:
            print(f"  {src:<45} -> {dst}")
        print()
        print(NOT_PORTABLE)
        return 0 if a.list else 1

    target = Path(a.target).expanduser().resolve()
    if not target.is_dir():
        print(f"error: {target} is not a directory", file=sys.stderr)
        return 1
    if target == REPO:
        print("error: target is the source repo", file=sys.stderr)
        return 1

    written, skipped = [], []
    for src_rel, dst_rel in PORTABLE + [TEMPLATE]:
        src = REPO / src_rel
        if not src.is_file():
            print(f"  ! missing source {src_rel}", file=sys.stderr)
            continue
        dst = target / dst_rel
        if dst.exists() and not a.force:
            skipped.append(dst_rel)
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        written.append(dst_rel)

    gi = target / ".gitignore"
    existing = gi.read_text(encoding="utf-8") if gi.is_file() else ""
    missing = [ln for ln in GITIGNORE_LINES if ln not in existing]
    if missing:
        with gi.open("a", encoding="utf-8") as f:
            f.write("\n" + "\n".join(missing) + "\n")
        written.append(".gitignore (appended)")

    for path in written:
        print(f"  + {path}")
    for path in skipped:
        print(f"  = {path} (exists; --force to overwrite)")

    print(f"\nInstalled into {target}")
    print("\nNext:")
    print("  1. Edit linking.config.json — wiki_dir, private_paths, "
          "required_sections, tag_map")
    print("  2. python scripts/lint_wiki.py                 # structural health")
    print("  3. python scripts/build_connections.py --check # renderer (CI)")
    print("  4. python scripts/graph_analysis.py            # structure: components, orphans, hubs")
    print("  5. python scripts/build_cards.py --offline     # mechanism cards")
    print("  6. python scripts/propose_connections.py --explain  # surprising pairs")
    print()
    print(NOT_PORTABLE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
