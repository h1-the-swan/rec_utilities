#!/usr/bin/env python3
import unittest
from parsers.infomap_log import InfomapLog

L1 = "infomap.log"
PARSED = {'per_level_num_modules': [9861, 4862, 47536, 121373, 46736, 4454, 184, 6, 0], 'num_leaves': 1146432, 'leaf_node_codelength': 4.043955986, 'links': 2360025, 'module_codelength': 5.224179254, 'self_links': 37, 'per_level_module_codelength': [0.068050433, 0.997671699, 2.285006274, 1.675351952, 0.188030483, 0.009791429, 0.000267017, 9.968e-06, 0.0], 'per_level_avg_child_degree': [9861.0, 5.45168, 12.0002, 9.1543, 5.24276, 3.678, 3.44701, 3.97283, 2.0], 'total_codelength': 9.26813524, 'filename': 'acoustics.net', 'average_child_degree': 76.9053, 'per_level_leaf_codelength': [0.0, 0.034513916, 0.013425651, 1.742221128, 1.928613294, 0.302656274, 0.021481528, 0.001026542, 1.7652e-05], 'per_level_total_codelength': [0.068050433, 1.032185615, 2.298431925, 3.41757308, 2.116643777, 0.312447703, 0.021748545, 0.00103651, 1.7652e-05], 'dangling_nodes': 978796, 'per_level_num_leaf_nodes': [0, 48897, 10809, 313786, 589593, 167441, 15169, 725, 12], 'nodes': 1146432, 'runtime': 141.0, 'num_levels': 9, 'num_modules': 235012}

class TestInfomapLog(unittest.TestCase):
    def setUp(self):
        self._stream = open(L1, "r")
        self._parser = InfomapLog(self._stream)
        self._parser.parse()

    def tearDown(self):
        self._stream.close()

    def test_filename(self):
        self.assertEqual(PARSED['filename'], self._parser.filename())

    def test_runtime(self):
        self.assertEqual(PARSED['runtime'], self._parser.runtime())

    def test_dangling(self):
        self.assertEqual(PARSED['dangling_nodes'], self._parser.dangling_nodes())

    def test_nodes(self):
        self.assertEqual(PARSED['nodes'], self._parser.nodes())

    def test_links(self):
        self.assertEqual(PARSED['links'], self._parser.links())

    def test_self_links(self):
        self.assertEqual(PARSED['self_links'], self._parser.self_links())

    def test_num_levels(self):
        self.assertEqual(PARSED['num_levels'], self._parser.num_levels())

    def test_num_modules(self):
        self.assertEqual(PARSED['num_modules'], self._parser.num_modules())

    def test_num_leaves(self):
        self.assertEqual(PARSED['num_leaves'], self._parser.num_leaves())

    def test_avg_child(self):
        self.assertEqual(PARSED['average_child_degree'], self._parser.average_child())

    def test_module_codelength(self):
        self.assertEqual(PARSED['module_codelength'], self._parser.module_codelength())

    def test_leaf_node_codelength(self):
        self.assertEqual(PARSED['leaf_node_codelength'], self._parser.leaf_node_codelength())

    def test_total_codelength(self):
        self.assertEqual(PARSED['total_codelength'], self._parser.total_codelength())

    def test_per_level_modules(self):
        self.assertListEqual(PARSED['per_level_num_modules'],
                             self._parser.per_level_modules())

    def test_per_level_leaf_nodes(self):
        self.assertListEqual(PARSED['per_level_num_leaf_nodes'],
                             self._parser.per_level_leaf_nodes())

    def test_per_level_avg_child_degree(self):
        self.assertListEqual(PARSED['per_level_avg_child_degree'],
                             self._parser.per_level_avg_child_degree())

    def test_per_level_module_codelength(self):
        self.assertListEqual(PARSED['per_level_module_codelength'],
                             self._parser.per_level_codelength_modules())

    def test_per_level_leaf_codelength(self):
        self.assertListEqual(PARSED['per_level_leaf_codelength'],
                             self._parser.per_level_codelength_leaf_nodes())

    def test_per_level_total_codelength(self):
        self.assertListEqual(PARSED['per_level_total_codelength'],
                             self._parser.per_level_codelength_total())

    def test_parse(self):
        self.assertDictContainsSubset(PARSED, self._parser.parse())

if __name__ == '__main__':
    unittest.main()
