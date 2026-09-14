#!/usr/bin/env python3
"""
lint_wiki.py — structural linter for the vault.

Checks the rules that LINKING.md states and linking.config.json encodes:

    1. frontmatter exists, and `frontmatter_required` keys come first, in order
    2. `required_sections.key_takeaway` is present
    3. `required_sections.connections` is present

Every string it checks against comes from the config, so pointing the config at
another vault re-points the linter with it. Stdlib only.

CONCEPT NODES ARE A DIFFERENT SCHEMA. LINKING.md section 3 defines them as
frontmatter + `# Title` + a one-line definition + the AUTO-INSTANCES markers —
deliberately short, with no Key Takeaway. Applying the standard-page rule to
them reported eight false failures; instead they must carry the instances
marker pair, which is the thing that actually matters for a concept node.

Exit code is 0 when clean and 1 when anything failed, so this can gate CI the
same way `build_connections.py --check` does.

    python scripts/lint_wiki.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from wiki_lib import load_config, parse_frontmatter  # noqa: E402


def lint_file(path: Path, cfg) -> list[str]:
    """Return a list of human-readable problems with one note."""
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as e:
        return [f"file read error: {e}"]

    errors: list[str] = []

    # 1. frontmatter, and the required keys first in declared order
    fm = parse_frontmatter(content)
    if not fm:
        errors.append("missing or malformed YAML frontmatter")
    else:
        head = list(fm.keys())[:len(cfg.frontmatter_required)]
        if head != cfg.frontmatter_required:
            errors.append(
                f"frontmatter must start with {cfg.frontmatter_required}, got {head}")

    # 2. the takeaway — or, for a concept node, the instances block instead.
    # concepts/index.md is the MOC over the atoms, not an atom itself, so it
    # is a standard page; tests/test_wiki_structure.py exempts it the same way.
    if cfg.is_concept_node(path) and path.stem != "index":
        start, end = cfg.instances_markers
        if start not in content or end not in content:
            errors.append(
                "concept node is missing the AUTO-INSTANCES markers; "
                "run python scripts/build_connections.py")
    else:
        takeaway = cfg.required_sections.get("key_takeaway")
        if takeaway and takeaway not in content:
            errors.append(f"missing '{takeaway}' block")

    # 3. connections
    connections = cfg.required_sections.get("connections")
    if connections and connections not in content:
        errors.append(f"missing '{connections}' section")

    return errors


def main() -> int:
    cfg = load_config(Path(__file__).resolve().parent)

    # cfg.notes() already drops exclude_paths (_proposals.md, agent_tasks.md,
    # log.md, _proposal-decisions.md) — bookkeeping files that were never
    # meant to satisfy the page schema.
    failures = {}
    for path in cfg.notes():
        errors = lint_file(path, cfg)
        if errors:
            failures[cfg.relpath(path)] = errors

    if not failures:
        print(f"✅ All {len(cfg.notes())} notes pass linting!")
        return 0

    print(f"Total files with errors: {len(failures)}")
    for rel, errors in sorted(failures.items()):
        print(f"❌ {rel}:")
        for error in errors:
            print(f"  - {error}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
