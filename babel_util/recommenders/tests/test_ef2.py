import unittest
from recommenders.ef2 import make_leaf_rec, parse_tree
from parsers.tree import TreeFile

EXPERT = [[18, 23, 24, 26, 27],
          [17, 15, 14, 13],
          [12, 16, 11, 10],
          [9, 20, 21, 25],
          [8, 6, 5, 4],
          [3, 7, 2, 1],
          [22, 19]]

CLASSIC = [[18, 23, 24, 26, 27, 17, 12, 15, 16, 11, 14, 13, 10],
           [9, 8, 20, 21, 25, 6, 3, 7, 5, 4, 2, 22, 1, 19]]


SINGLETONS = [
    '1:276:1:1 0 "1" 1959666',
    '1:277:1:1 0 "2" 3198129',
    '1:278:1:1 0 "3" 9248225'
]

ANSWERS = {"1:1": ("18", "23", "24", "26", "27"),
           "1:2": ("17", "15", "14", "13"),
           "1:3": ("12", "16", "11", "10"),
           "2:1": ("9", "20", "21", "25"),
           "2:2": ("8", "6", "5", "4"),
           "2:3": ("3", "7", "2", "1"),
           "2:4": ("22", "19")
           }


def make_answer(answers, current):
    r = None
    for a in answers:
        if int(current) in a:
            r = list(map(str, a.copy()))  # Make a copy and convert to strings
            r.remove(current)

    if not r:
        raise ValueError(current)

    return r[:10]


class TestEF2Rec(unittest.TestCase):
    def setUp(self):
        self.tr = TreeFile(open("./ninetriangles.tree", "r"))
        self.deep = TreeFile(open("./deepnetwork.tree", "r"))

    def test_make_leaf(self):
        for rec in make_leaf_rec(self.tr):
            self.assertTupleEqual(rec.get_papers(), ANSWERS[rec.cluster_id])

    def test_parse_tree(self):
        for rec in parse_tree(self.deep):
            print(rec)

