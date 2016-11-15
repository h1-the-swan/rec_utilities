#!/usr/bin/env python3
from parsers.wos import WOSStream
from util.PajekFactory import PajekFactory
from util.misc import open_file, Benchmark

if __name__ == "__main__":
    import argparse
    import sys
    parser = argparse.ArgumentParser(description="Creates Pajek (.net) files from WOS XML")
    parser.add_argument('infile')
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    arguments = parser.parse_args()

    with open_file(arguments.infile) as f:
        p = WOSStream(f)
        
        for entry in p.parse():
            for citation in entry["citations"]:
                arguments.infile.write("%s\t%s\n" % (entry["id"], citation))
