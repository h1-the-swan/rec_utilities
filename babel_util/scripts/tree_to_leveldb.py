#!/usr/bin/env python3
import leveldb
from recommenders.ef2 import parse_tree
from parsers.tree import TreeFile
import msgpack
from util.misc import Benchmark, open_file

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Creates recommendations and stores in an LevelDB from a tree file (.tree)")
    parser.add_argument('infile')
    parser.add_argument('db_path')
    parser.add_argument("--wos-only", help="Only include papers in the WOS collection", action="store_true")
    parser.add_argument('--benchmark-freq', default=10000, type=int)
    parser.add_argument('-l', '--limit', type=int, help="Max number of recommendations to generate per-paper", default=10)
    args = parser.parse_args()

    db = leveldb.LevelDB(args.db_path,
                         write_buffer_size=100 << 20,  # 100MB
                         block_cache_size=400 << 20)  # 400MB

    with open_file(args.infile) as ifs:
        b = Benchmark(args.benchmark_freq)
        # Remove any non-wos entries
        if args.wos_only:
            tf = filter(lambda r: r.pid.startswith("WOS:") and '.' not in r.pid, TreeFile(ifs))
        else:
            tf = TreeFile(ifs)

        writer = db

        for parent_cid, parent_papers, leaf_recs in parse_tree(tf, args.limit):
            for l in leaf_recs:
                for paper in l.get_papers():
                    # Register each paper's cluster_id
                    writer.Put(("paper|" + paper).encode(), l.cluster_id.encode())
                    b.increment()
                # Register recommendations for each leaf cluster
                writer.Put(("cluster|" + l.cluster_id).encode(), msgpack.packb(l.get_papers()))
                b.increment()
            # Now register the parent (expert) recommendations
            # TODO: A hacky method to stop us from registering singleton-parents
            if ':' in parent_cid:
                writer.Put(("cluster|" + parent_cid).encode(), msgpack.packb(parent_papers))
            b.increment()

        b.print_freq()

        print(db.GetStats())
