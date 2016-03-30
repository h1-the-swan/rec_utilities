#!/usr/bin/env python3

if __name__ == "__main__":
    import argparse
    from util.AutoID import AutoID
    from util.misc import open_file
    import pickle
    parser = argparse.ArgumentParser(description="Remap strings to ids")
    parser.add_argument('infile')
    parser.add_argument('outfile')
    parser.add_argument('pickle', help="Store AutoID pickle")
    parser.add_argument('--start', type=int, default=1, help="Value to start with")
    parser.add_argument('--delimiter', default=' ', help="ID delimiter", type=str)
    arguments = parser.parse_args()

    aid = AutoID(arguments.start)
    with open_file(arguments.outfile, "w") as o:
        with open_file(arguments.infile) as f:
            for line in f:
                o.write(arguments.delimiter.join(list(map(str, map(aid.__getitem__, map(str.strip, line.split(arguments.delimiter)))))))
                o.write('\n')

    with open(arguments.pickle, "wb") as p:
        pickle.dump(aid, p, pickle.HIGHEST_PROTOCOL)



