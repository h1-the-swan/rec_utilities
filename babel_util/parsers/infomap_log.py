from datetime import datetime

DT_FORMAT = "%Y-%m-%d %H:%M:%S"

class InfomapLog(object):
    def __init__(self, stream):
        self._stream = stream
        self._lines = None
        self._num_levels = None

    def _get_line(self, string):
        l = filter(lambda s: s.count(string), self._lines)
        assert len(l) == 1
        return l[0]

    def _get_brackets(self, string, delim=',', dtype=None):
        """For any line containing string and some [stuff], return [stuff]"""
        l = self._get_line(string)
        contents = l[l.index('[')+1:l.index(']')].split(delim)
        assert len(contents) == self.num_levels()
        if dtype:
            return map(dtype, contents)
        return contents

    def _get_stat(self, string):
        """For any line containing string that ends ([sum|average]: 12345), get the sum/average."""
        return self._get_line(string).split(": ")[2].strip()[:-1]

    def parse(self):
        if not self._lines:
            self._lines = self._stream.readlines()

        return {"filename": self.filename(),
                "runtime": self.runtime(),
                "dangling_nodes": self.dangling_nodes(),
                "nodes": self.nodes(),
                "links": self.links(),
                "self_links": self.self_links(),
                "num_levels": self.num_levels(),
                "num_modules": self.num_modules(),
                "num_leaves": self.num_leaves(),
                "average_child_degree": self.average_child(),
                "module_codelength": self.module_codelength(),
                "leaf_node_codelength": self.leaf_node_codelength(),
                "total_codelength": self.total_codelength(),
                "per_level_num_modules": self.per_level_modules(),
                "per_level_num_leaf_nodes": self.per_level_leaf_nodes(),
                "per_level_avg_child_degree": self.per_level_avg_child_degree(),
                "per_level_module_codelength": self.per_level_codelength_modules(),
                "per_level_leaf_codelength": self.per_level_codelength_leaf_nodes(),
                "per_level_total_codelength": self.per_level_codelength_total(),
                }

    def filename(self):
        return self._get_line("Input network:").split(":")[1].split('/')[-1].strip()

    def runtime(self):
        s = self._get_line("starts at [").split('[')[1].strip()[:-1]
        e = self._get_line("ends at [").split('[')[1].strip()[:-1]
        s = datetime.strptime(s, DT_FORMAT)
        e = datetime.strptime(e, DT_FORMAT)
        return (e - s).total_seconds()

    def dangling_nodes(self):
        return int(self._get_line("dangling nodes").split(" ")[2])

    def nodes(self):
        return int(self._get_line("==>").split(" ")[2])

    def links(self):
        return int(self._get_line("==>").split(" ")[5])

    def self_links(self):
        return int(self._get_line("self-links.").split(" ")[3])

    def num_levels(self):
        if self._num_levels is None:
            self._num_levels = int(self._get_line("Best end modular solution in").split(" ")[5])
        return self._num_levels

    def num_modules(self):
        return int(self._get_stat("number of modules"))

    def num_leaves(self):
        return int(self._get_stat("number of leaf nodes"))

    def average_child(self):
        return float(self._get_stat("average child degree"))

    def module_codelength(self):
        return float(self._get_stat("codelength for modules"))

    def leaf_node_codelength(self):
        return float(self._get_stat("codelength for leaf nodes"))

    def total_codelength(self):
        return float(self._get_stat("codelength total"))

    def per_level_modules(self):
        return self._get_brackets("Per level number of modules", dtype=int)

    def per_level_leaf_nodes(self):
        return self._get_brackets("Per level number of leaf nodes", dtype=int)

    def per_level_avg_child_degree(self):
        return self._get_brackets("Per level average child degree", dtype=float)

    def per_level_codelength_modules(self):
        return self._get_brackets("Per level codelength for modules", dtype=float)

    def per_level_codelength_leaf_nodes(self):
        return self._get_brackets("Per level codelength for leaf nodes", dtype=float)

    def per_level_codelength_total(self):
        return self._get_brackets("Per level codelength total", dtype=float)

