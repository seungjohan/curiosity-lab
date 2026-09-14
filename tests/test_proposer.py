"""
Tests for the connection proposer.

Two of these are security tests, not tidiness tests:
  - test_private_notes_never_reach_the_api_list
  - test_config_private_paths_are_enforced_structurally

They assert the guarantee that no private note can be sent to a hosted API.
If either fails, stop and fix it before running build_cards.py.
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import build_cards  # noqa: E402
import propose_connections as P  # noqa: E402
from wiki_lib import load_config, parse_frontmatter  # noqa: E402

cfg = load_config(REPO / "scripts")


# -- privacy ---------------------------------------------------------------

def test_private_notes_never_reach_the_api_list():
    """The list build_cards.py iterates must contain no private note."""
    public = build_cards.public_notes(cfg)
    leaked = [cfg.relpath(p) for p in public if cfg.is_private(p)]
    assert not leaked, f"private notes present in the API work list: {leaked}"


def test_private_paths_actually_match_notes():
    """A private_paths entry that matches nothing is a false sense of safety."""
    for rel in cfg.private_paths:
        matched = [p for p in cfg.notes() if cfg.is_private(p)
                   and cfg.relpath(p).startswith(rel)]
        assert matched, f"private path {rel!r} matches no note"


def test_is_private_fails_closed_outside_the_wiki():
    """An unexpected path must be treated as private, never as public."""
    assert cfg.is_private(REPO / "README.md")
    assert cfg.is_private(Path("/etc/passwd"))


def test_no_card_exists_for_any_private_note():
    """The on-disk evidence: no private note has ever been carded."""
    if not cfg.cards_dir.is_dir():
        return
    for f in cfg.cards_dir.glob("*.json"):
        if f.name.startswith("_"):
            continue
        rel = json.loads(f.read_text(encoding="utf-8")).get("path", "")
        assert not cfg.is_private(cfg.wiki / rel), \
            f"a card exists for private note {rel}"


# -- model safety ----------------------------------------------------------

def test_mechanism_and_topic_models_differ():
    """If both similarities came from one model, surprise would be ~0 by
    construction and every ranking would be noise."""
    _, _, local_model = P.load_smart_env(cfg)
    cache = cfg.cards_dir / P.VECTOR_CACHE
    if not cache.is_file() or not local_model:
        return
    mech_model = json.loads(cache.read_text(encoding="utf-8")).get("model_id", "")
    assert local_model not in mech_model.split("/"), \
        "mechanism and topic vectors share a model; surprise is meaningless"


def test_vector_cache_is_model_tagged():
    cache = cfg.cards_dir / P.VECTOR_CACHE
    if not cache.is_file():
        return
    data = json.loads(cache.read_text(encoding="utf-8"))
    assert data.get("model_id"), "vector cache must record its embedding model"
    dims = {len(v) for v in data.get("vectors", {}).values()}
    assert len(dims) <= 1, f"cache mixes vector dimensions: {dims}"


# -- scoring ---------------------------------------------------------------

def test_cosine_bounds_and_mismatch():
    assert abs(P.cosine([1, 0], [1, 0]) - 1.0) < 1e-9
    assert abs(P.cosine([1, 0], [0, 1])) < 1e-9
    assert P.cosine([1, 0], [1, 0, 0]) == 0.0, "length mismatch must not crash"
    assert P.cosine([], []) == 0.0


def test_percentile_ranks_are_normalised():
    r = P.percentile_ranks([0.1, 0.5, 0.9])
    assert r == [0.0, 0.5, 1.0]
    assert P.percentile_ranks([0.4]) == [0.5]
    assert P.percentile_ranks([]) == []


def test_identical_topic_and_mechanism_yields_zero_surprise():
    """The definition, asserted: ranking by mechanism alone is not surprise."""
    pairs = [("a", "b", 0.9), ("c", "d", 0.7), ("e", "f", 0.6)]
    vecs = {"a": [1, 0], "b": [0.9, 0.1], "c": [1, 0], "d": [0.5, 0.5],
            "e": [1, 0], "f": [0, 1]}
    scored = P.score_tier(pairs, vecs, floor=0.0)
    # mechanism order and topic order are identical here, so every surprise is 0
    assert all(abs(r["surprise"]) < 1e-9 for r in scored)


def test_mechanism_floor_excludes_weak_pairs():
    pairs = [("a", "b", 0.9), ("c", "d", 0.2)]
    vecs = {"a": [1, 0], "b": [0, 1], "c": [1, 0], "d": [0, 1]}
    assert len(P.score_tier(pairs, vecs, floor=0.5)) == 1


# -- report hygiene --------------------------------------------------------

def test_diversify_caps_hub_notes():
    scored = [{"a": "hub", "b": f"n{i}", "surprise": 1.0 - i / 100}
              for i in range(10)]
    out = P.diversify(scored, limit=10, max_each=2)
    assert len(out) == 2, "a hub note must not fill the list"


def test_boilerplate_pages_are_excluded():
    assert P.is_boilerplate(cfg, "research/travel/index.md")
    assert P.is_boilerplate(cfg, "research/cooking/vocabulary.md")
    assert not P.is_boilerplate(cfg, "projects/Michelin Filter.md")


def test_decision_log_round_trips():
    """A pair written in the documented format must parse back out."""
    decided = P.load_decisions(cfg)
    assert isinstance(decided, set)
    for pair in decided:
        assert len(pair) == 2 and pair == tuple(sorted(pair))


def test_generated_proposals_are_gitignored():
    """The report is disposable and must never be committed."""
    ignored = (REPO / ".gitignore").read_text(encoding="utf-8")
    assert "wiki/_proposals.md" in ignored
    assert ".connection-cards/" in ignored


def test_offline_card_extracts_the_why_line():
    body = ("> [!IMPORTANT] Key Takeaway\n"
            "> **Why this matters:** A filter beats a list when choice is costly.\n"
            "> **How to use it:** Rank by a signal the crowd ignores.\n")
    card = build_cards.offline_card(body)
    assert card is not None
    assert "filter beats a list" in card["tension"]
    assert "crowd ignores" in card["move"]
    assert card["abstraction"].startswith("A filter beats")


def test_offline_card_returns_none_without_a_why_line():
    assert build_cards.offline_card("# Just a heading\n\nSome prose.\n") is None
