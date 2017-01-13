#!/usr/bin/env python3
import leveldb
import msgpack
import csv
from util.misc import Benchmark, open_file

REQUIRED_KEYS = {'title', 'paper_id', 'date'}

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Creates a LevelDB of TSV metadata in infile")
    parser.add_argument('infile')
    parser.add_argument('leveldb_path')
    parser.add_argument('--benchmark-freq', default=100000, type=int)
    parser.add_argument('--delimiter', '-d', default='\t')
    args = parser.parse_args()

    db = leveldb.LevelDB(args.db_path,
                         write_buffer_size=100 << 20,  # 100MB
                         block_cache_size=400 << 20)  # 400MB

    with open_file(args.infile) as ifs:
        b = Benchmark(args.benchmark_freq)
        reader = csv.DictReader(ifs, delimiter=args.delimiter)
        for row in reader:
            if not REQUIRED_KEYS.issubset(row.keys()):
                print(row)
                raise KeyError("Not all required keys present")
            db.Put(row["paper_id"].encode(), msgpack.packb(row))
            b.increment()

    b.print_freq()
    print(db.GetStats())
