#!/usr/bin/env python
import itertools
from operator import attrgetter, itemgetter


class ClusterRecommendation(object):
    __slots__ = ("cluster_id", "papers")

    def __init__(self, cluster_id, papers):
        self.cluster_id = cluster_id
        self.papers = [(p.pid, p.score) for p in papers]

    def __str__(self):
        return "%s %s" % (self.cluster_id, len(self.papers))

    def __repr__(self):
        return "<ClusterRecommendation %s>" % self.cluster_id

    def get_papers(self):
        """Only return a tuple of papers"""
        return tuple(zip(*self.papers))[0]

def get_parent(cluster_id):
    parent = ":".join(cluster_id.split(":")[:-1])
    if parent == "":
        return None
    return parent

def get_subtree(cluster_id):
    subtree = ":".join(cluster_id.split(":")[1:])
    if subtree == "":
        return None
    return subtree

def make_leaf_rec(stream, rec_limit=10):
    leaf_stream = itertools.groupby(stream, lambda e: e.local)
    for (cluster_id, stream) in leaf_stream:
        papers = [e for e in stream]
        papers = sorted(papers, key=attrgetter('score'), reverse=True)
        yield ClusterRecommendation(cluster_id, papers[:rec_limit])

def parse_tree(stream, rec_limit=10):
    mstream = make_leaf_rec(stream, rec_limit)
    child_stream = itertools.groupby(mstream, lambda e: get_parent(e.cluster_id))
    for (parent_cluster_id, recs) in child_stream:
        child_recs = [r for r in recs]
        papers = itertools.chain.from_iterable(map(attrgetter('papers'), child_recs))
        parent_papers = tuple(zip(*sorted(papers, key=itemgetter(1), reverse=True)))[0]
        yield (parent_cluster_id, parent_papers[:rec_limit], child_recs)
