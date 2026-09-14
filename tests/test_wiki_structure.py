"""
Structural tests for the vault.

Rules come from linking.config.json, not from hardcoded strings, so this file
is portable: point the config at another vault and these tests still apply.

Stdlib only — no PyYAML. Frontmatter is parsed by scripts/wiki_lib.py, the
same parser the generators use, so tests and generators can never disagree.
"""
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from wiki_lib import load_config, parse_frontmatter  # noqa: E402

cfg = load_config(REPO / "scripts")


def test_wiki_exists():
    assert cfg.wiki.is_dir(), f"wiki directory must exist at {cfg.wiki}"
    assert cfg.notes(), "wiki must contain at least one managed note"


def test_required_frontmatter_keys_come_first():
    """Every managed note opens with the required keys, in order.

    `tag` is deliberately NOT required: it is a semantic filter label that
    only 85 of 119 notes carry. Requiring it was the old rule and the vault
    moved on; `concepts` and `axis` legitimately take third position.
    """
    problems = []
    for path in cfg.notes():
        fm = parse_frontmatter(path.read_text(encoding="utf-8"))
        rel = cfg.relpath(path)
        if not fm:
            problems.append(f"{rel}: no YAML frontmatter")
            continue
        head = list(fm.keys())[:len(cfg.frontmatter_required)]
        if head != cfg.frontmatter_required:
            problems.append(
                f"{rel}: must start with {cfg.frontmatter_required}, got {head}")
    assert not problems, "frontmatter problems:\n  " + "\n  ".join(problems)


def test_tag_matches_folder_or_declared_override():
    """When present, `tag` mirrors the folder unless config declares otherwise."""
    problems = []
    for path in cfg.notes(include_concepts=False):
        fm = parse_frontmatter(path.read_text(encoding="utf-8"))
        if "tag" not in fm:
            continue
        expected = cfg.expected_tag(path)
        if fm["tag"] != expected:
            problems.append(
                f"{cfg.relpath(path)}: tag={fm['tag']!r}, expected {expected!r} "
                "(add to tag_overrides in linking.config.json if intentional)")
    assert not problems, "tag problems:\n  " + "\n  ".join(problems)


def test_declared_tag_overrides_still_exist():
    """An override for a note that has been moved or renamed is dead config."""
    missing = [rel for rel in cfg.tag_overrides if not (cfg.wiki / rel).is_file()]
    assert not missing, f"tag_overrides point at missing notes: {missing}"


def test_private_paths_exist_and_are_nonempty():
    """The privacy allowlist must name real directories.

    A typo here would silently make a private folder public to the LLM pass,
    so this is a security test, not a tidiness one.
    """
    for rel in cfg.private_paths:
        d = cfg.wiki / rel
        assert d.is_dir(), f"private_paths names {rel!r}, which is not a directory"
        assert list(d.rglob("*.md")), f"private path {rel!r} contains no notes"


def test_every_referenced_concept_has_a_node():
    """A `concepts:` value with no node in wiki/concepts/ is a broken link."""
    known = {p.stem for p in cfg.concepts_dir.glob("*.md") if p.stem != "index"}
    referenced = set()
    for path in cfg.notes(include_concepts=False):
        fm = parse_frontmatter(path.read_text(encoding="utf-8"))
        referenced.update(fm.get("concepts", []))
    assert not (referenced - known), f"concepts with no node: {sorted(referenced - known)}"


def test_concept_nodes_are_instanced_or_declared_candidates():
    """Every concept node carries the auto-instances block the builder fills."""
    start, end = cfg.instances_markers
    for node in cfg.concepts_dir.glob("*.md"):
        if node.stem == "index":
            continue
        text = node.read_text(encoding="utf-8")
        assert start in text and end in text, (
            f"{node.name} is missing the AUTO-INSTANCES markers; "
            "run python scripts/build_connections.py")


def test_generated_links_are_up_to_date():
    """`build_connections.py --check` must be clean — no uncommitted drift."""
    result = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "build_connections.py"), "--check"],
        capture_output=True, text=True, cwd=REPO)
    assert result.returncode == 0, (
        "generated links are stale; run python scripts/build_connections.py\n"
        + result.stdout + result.stderr)


def test_linking_standard_is_documented():
    """LINKING.md is the canonical standard; DESIGN.md was folded into it."""
    linking = REPO / "LINKING.md"
    assert linking.is_file(), "LINKING.md must exist — it is the canonical standard"
    content = linking.read_text(encoding="utf-8")
    for heading in ("Frontmatter", "Vertical axis", "Horizontal axis", "Quality bar"):
        assert heading in content, f"LINKING.md must document '{heading}'"
