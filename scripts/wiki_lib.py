#!/usr/bin/env python3
"""
wiki_lib.py — shared helpers for the linking system.

Everything vault-specific lives in linking.config.json, never in code. Copy
this file plus the scripts that import it into another project, drop a config
next to it, and the system works there unchanged.

Stdlib only. No PyYAML, no requests.

See LINKING.md for the standard this implements.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from pathlib import Path

CONFIG_NAME = "linking.config.json"

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


# --------------------------------------------------------------------------
# config
# --------------------------------------------------------------------------

def find_config(start: Path | None = None) -> Path:
    """Walk up from `start` (default: this file) looking for linking.config.json."""
    here = (start or Path(__file__)).resolve()
    for parent in [here, *here.parents]:
        candidate = parent / CONFIG_NAME if parent.is_dir() else parent.parent / CONFIG_NAME
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(
        f"{CONFIG_NAME} not found above {here}. "
        "Copy the template from skills/linking-system/ and edit it."
    )


class Config:
    """Loaded linking.config.json plus the derived absolute paths."""

    def __init__(self, path: Path):
        self.path = path
        self.repo = path.parent
        self.data = json.loads(path.read_text(encoding="utf-8"))

        self.wiki = self.repo / self.data.get("wiki_dir", "wiki")
        self.concepts_dir = self.repo / self.data.get("concepts_dir", "wiki/concepts")

        self.private_paths: list[str] = self.data.get("private_paths", [])
        self.exclude_paths: list[str] = self.data.get("exclude_paths", [])
        self.frontmatter_required: list[str] = self.data.get(
            "frontmatter_required", ["stage", "category"])
        self.tag_overrides: dict = self.data.get("tag_overrides", {})
        self.tag_map: dict = self.data.get("tag_map", {})
        self.tag_default: str = self.data.get("tag_default", "system")
        self.required_sections: dict = self.data.get("required_sections", {})

        markers = self.data.get("markers", {})
        self.concepts_markers = tuple(markers.get(
            "concepts", ["<!-- AUTO-CONCEPTS:START -->", "<!-- AUTO-CONCEPTS:END -->"]))
        self.instances_markers = tuple(markers.get(
            "instances", ["<!-- AUTO-INSTANCES:START -->", "<!-- AUTO-INSTANCES:END -->"]))

        p = self.data.get("proposer", {})
        self.smart_env_dir = self.repo / p.get("smart_env_dir", ".smart-env/multi")
        self.cards_dir = self.repo / p.get("cards_dir", ".connection-cards")
        self.proposals_file = self.repo / p.get("proposals_file", "wiki/_proposals.md")
        self.decisions_file = self.repo / p.get("decisions_file", "wiki/_proposal-decisions.md")
        self.mechanism_floor = float(p.get("mechanism_floor", 0.55))
        self.top_n = int(p.get("top_n", 25))
        self.exclude_globs: list[str] = p.get("exclude_globs", [])
        self.max_appearances = int(p.get("max_appearances_per_note", 2))
        self.llm = p.get("llm", {})
        self.embedding = p.get("embedding", {})

    # -- path classification -------------------------------------------------

    def relpath(self, path: Path) -> str:
        """Path relative to the wiki root, posix-style. '' if outside the wiki."""
        try:
            return path.resolve().relative_to(self.wiki.resolve()).as_posix()
        except ValueError:
            return ""

    def is_private(self, path: Path) -> bool:
        """True if this note may NEVER be sent to an LLM or hosted API.

        Structural guarantee (decision 10A): every outbound code path calls
        this. A path outside the wiki entirely is treated as private — fail
        closed, so an unexpected path can never leak.
        """
        rel = self.relpath(path)
        if not rel:
            return True
        return any(rel == p or rel.startswith(p.rstrip("/") + "/")
                   for p in self.private_paths)

    def is_excluded(self, path: Path) -> bool:
        """Generated or bookkeeping files the linker and linter should ignore."""
        rel = self.relpath(path)
        if not rel:
            return True
        return any(rel == p or rel.startswith(p.rstrip("/") + "/")
                   for p in self.exclude_paths)

    def is_concept_node(self, path: Path) -> bool:
        return self.concepts_dir.resolve() in path.resolve().parents

    def notes(self, include_concepts: bool = True) -> list[Path]:
        """Every managed note, sorted. Excluded paths are dropped."""
        out = [p for p in self.wiki.rglob("*.md") if not self.is_excluded(p)]
        if not include_concepts:
            out = [p for p in out if not self.is_concept_node(p)]
        return sorted(out)

    def expected_tag(self, path: Path) -> str:
        """Tag implied by folder, per tag_map. '<prefix>/*' captures one segment.

        `tag` is a semantic filter label, not a strict folder mirror; notes
        that deliberately differ are listed in tag_overrides.
        """
        rel = self.relpath(path)
        if rel in self.tag_overrides:
            return self.tag_overrides[rel]
        parts = Path(rel).parts
        if not parts:
            return self.tag_default
        for pattern, value in self.tag_map.items():
            pat = Path(pattern).parts
            if len(pat) > len(parts):
                continue
            if all(pp == "*" or pp == ap for pp, ap in zip(pat, parts)):
                if value == "$1":
                    idx = pat.index("*")
                    return parts[idx]
                return value
        return self.tag_default


_CONFIG: Config | None = None


def load_config(start: Path | None = None) -> Config:
    global _CONFIG
    if _CONFIG is None:
        _CONFIG = Config(find_config(start))
    return _CONFIG


# --------------------------------------------------------------------------
# markdown
# --------------------------------------------------------------------------

def parse_frontmatter(text: str) -> dict:
    """Minimal frontmatter reader. Supports `key: value` and inline
    `concepts: [a, b, c]` lists — the only structure this system needs.

    Preserves key order, so callers can assert on frontmatter_order.
    """
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
            end = val.find("]")
            inner = val[1:end] if end != -1 else val[1:]
            fm[key] = [x.strip() for x in inner.split(",") if x.strip()]
        else:
            if " #" in val:
                val = val.split(" #", 1)[0].strip()
            fm[key] = val
    return fm


def strip_frontmatter(text: str) -> str:
    m = FRONTMATTER_RE.match(text)
    return text[m.end():] if m else text


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
    return text.rstrip() + "\n\n" + block + "\n"


def write_or_check(path: Path, new_text: str, check: bool, repo: Path) -> list[str]:
    """Write unless `check`; either way report the path if it would change."""
    current = path.read_text(encoding="utf-8")
    if current == new_text:
        return []
    if not check:
        path.write_text(new_text, encoding="utf-8")
    return [str(path.relative_to(repo))]


def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


# --------------------------------------------------------------------------
# secrets
# --------------------------------------------------------------------------

_ENV_LINE = re.compile(r"\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)")


def load_env_key(name: str, repo: Path) -> str | None:
    """Read a key from the process env, falling back to an untracked .env.

    Never logs or returns the value anywhere but to the caller.
    """
    if os.environ.get(name):
        return os.environ[name]
    env_file = repo / ".env"
    if not env_file.is_file():
        return None
    for line in env_file.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("#"):
            continue
        m = _ENV_LINE.match(line)
        if m and m.group(1) == name:
            return m.group(2).strip().strip('"').strip("'")
    return None


def die(msg: str) -> None:
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)
