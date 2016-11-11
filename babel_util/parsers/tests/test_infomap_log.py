#!/usr/bin/env python3
import unittest
from parsers.infomap_log import InfomapLog

L1 = "infomap.log"


class TestInfomapLog(unittest.TestCase):
    def setUp(self):
        self._stream = open(L1, "r")
        self._parser = InfomapLog(self._stream)
        self._parser.parse()

    def tearDown(self):
        self._stream.close()

    def test_filename(self):
        self.assertEqual("acoustics.net", self._parser.filename())

    def test_runtime(self):
        self.assertEqual(141.0, self._parser.runtime())

    def test_dangling(self):
        self.assertEqual(978796, self._parser.dangling_nodes())

    def test_nodes(self):
        self.assertEqual(1146432, self._parser.nodes())

    def test_links(self):
        self.assertEqual(2360025, self._parser.links())

    def test_self_links(self):
        self.assertEqual(37, self._parser.self_links())

    def test_num_levels(self):
        self.assertEqual(9, self._parser.num_levels())

    def test_num_modules(self):
        self.assertEqual(235012, self._parser.num_modules())

    def test_num_leaves(self):
        self.assertEqual(1146432, self._parser.num_leaves())

    def test_avg_child(self):
        self.assertEqual(76.9053, self._parser.average_child())

    def test_module_codelength(self):
        self.assertEqual(5.224179254, self._parser.module_codelength())

    def test_leaf_node_codelength(self):
        self.assertEqual(4.043955986, self._parser.leaf_node_codelength())

    def test_total_codelength(self):
        self.assertEqual(9.268135240, self._parser.total_codelength())

    def test_parse(self):
        print self._parser.parse()

if __name__ == '__main__':
    unittest.main()
