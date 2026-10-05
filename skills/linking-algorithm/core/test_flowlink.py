"""Tests for flowlink.py. Run from the folder holding it: python3 -m unittest test_flowlink

flowlink_parity.json was written by Constellate's own pipeline (algorithm/pipeline/
thinking.py through export_app.best_meetings) over 48 made-up flows: the core
must meet them exactly as that pipeline does, every kind, score and sentence.
"""

import json
import unittest
from collections import Counter
from pathlib import Path

import flowlink as fl

PARITY = json.loads((Path(__file__).parent / "flowlink_parity.json").read_text())


class SameAsConstellate(unittest.TestCase):
    def test_every_resource_meets_every_other_the_same_way(self):
        web = fl.Web(PARITY["flows"], PARITY["canon"], PARITY["limited"], PARITY["broad"], PARITY["drops"])
        for a, expected in PARITY["best"].items():
            got = {b: {"kind": m.kind, "variable": m.variable, "sign": m.sign, "score": round(m.score, 6),
                       "sentence": m.sentence} for b, m in web.best(a).items()}
            self.assertEqual(got, expected, a)


def flow(**kw):
    return {"up": {}, "down": {}, "chain": [], "entities": [], **kw}


class Time(unittest.TestCase):
    def test_reads_dates_the_way_notes_write_them(self):
        self.assertEqual(fl.when("1600s"), fl.When(1600, 1700))
        self.assertEqual(fl.when("1960s"), fl.When(1960, 1970))
        self.assertEqual(fl.when("17th century"), fl.When(1600, 1700))
        self.assertEqual(fl.when("44 BC"), fl.When(-44, -43))
        self.assertEqual(fl.when("5th century BC"), fl.When(-500, -400))
        self.assertEqual(fl.when("1600-1650"), fl.When(1600, 1651))
        self.assertEqual(fl.when(1665), fl.When(1665, 1666))
        self.assertAlmostEqual(fl.when("2026-01-01").start, 2026.0)
        self.assertIsNone(fl.when("Ancient Rome"))
        self.assertIsNone(fl.when("2026-02-30"))

    def test_a_cause_comes_before_its_effect(self):
        lens = flow(down={"the-infinitely-small": 1})
        cells = flow(up={"the-infinitely-small": 1})
        early, late = fl.When(1590, 1610), fl.When(1665, 1666)
        web = fl.Web({"lens": lens, "cells": cells}, when={"lens": early, "cells": late})
        self.assertEqual(web.best("lens")["cells"].kind, "influence")
        backwards = fl.Web({"lens": lens, "cells": cells}, when={"lens": late, "cells": early})
        m = backwards.best("lens")["cells"]
        self.assertEqual(m.kind, "hindsight")
        self.assertFalse(fl.can_justify(m))
        self.assertTrue(m.sentence.startswith("in hindsight: "))

    def test_unknown_or_overlapping_dates_change_nothing(self):
        lens, cells = flow(down={"x": 1}), flow(up={"x": 1})
        same = fl.Web({"a": lens, "b": cells}, when={"a": fl.When(1600, 1700), "b": fl.When(1650, 1660)})
        self.assertEqual(same.best("a")["b"].kind, "influence")
        none = fl.Web({"a": lens, "b": cells}, when={"a": fl.When(1700, 1701)})
        self.assertEqual(none.best("a")["b"].kind, "influence")

    def test_years_apart(self):
        self.assertEqual(fl.years_apart(fl.When(1600, 1700), fl.When(1650, 1660)), 0)
        self.assertEqual(fl.years_apart(fl.When(-44, -43), fl.When(1600, 1700)), 1643)
        self.assertIsNone(fl.years_apart(None, fl.When(1, 2)))


class Collection(unittest.TestCase):
    def test_storyline_moves_forward_and_keeps_its_weakest_link_strong(self):
        order = ["a", "b", "c", "d"]
        w = {("a", "b"): 0.9, ("b", "c"): 0.8, ("a", "c"): 0.2, ("c", "d"): 0.7, ("b", "d"): 0.1}
        self.assertEqual(fl.storyline(order, w, steps=4), (["a", "b", "c", "d"], 0.7))
        self.assertEqual(fl.storyline(order, {("b", "a"): 1.0}, steps=3), ([], 0.0))

    def test_groups_do_not_flood_across_one_bridge(self):
        g = {"a": {"b", "c"}, "b": {"a", "c"}, "c": {"a", "b", "d"}, "d": {"c", "e", "f"}, "e": {"d", "f"}, "f": {"d", "e"}}
        lab = fl.communities(g)
        self.assertEqual(lab["a"], lab["b"])
        self.assertEqual(lab["e"], lab["f"])
        self.assertNotEqual(lab["a"], lab["e"])

    def test_bridge_needs_a_foothold_in_two_groups(self):
        left = {f"l{i}" for i in range(4)}
        right = {f"r{i}" for i in range(4)}
        g = {v: (left - {v}) for v in left} | {v: (right - {v}) for v in right}
        g["x"] = {"l0", "l1", "r0", "r1"}
        for v in ("l0", "l1", "r0", "r1"):
            g[v] = g[v] | {"x"}
        self.assertEqual([v for v, *_ in fl.bridges(g)], ["x"])

    def test_a_burst(self):
        months = fl.month_range("2026-01", "2026-12")
        totals = Counter({m: 10 for m in months})
        seen = {"travel": ["2026-05"] * 8 + ["2026-01", "2026-09"]}
        self.assertEqual([(t, months[a], months[b]) for t, a, b, _ in fl.bursts(seen, months, totals)],
                         [("travel", "2026-05", "2026-05")])


if __name__ == "__main__":
    unittest.main()
