#!/usr/bin/env python
from util.misc import open_file, Benchmark
from parsers.ai2 import AI2
import ujson

if __name__ == "__main__":
    import argparse
    import sys
    parser = argparse.ArgumentParser(description="Converts AI2 input to standard JSON output")
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    args = parser.parse_args()

    p = AI2()
    for paper in p.parse(args.infile):
        args.outfile.write(ujson.dumps(paper))
        args.outfile.write('\n')
