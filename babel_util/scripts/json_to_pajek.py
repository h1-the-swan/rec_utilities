#!/usr/bin/env python3
from util.misc import open_file, Benchmark
from util.PajekFactory import PajekFactory
import ujson


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Creates Pajek (.net) files from JSON")
    parser.add_argument('outfile')
    parser.add_argument('--temp-dir', help="Directory to store temporary files in", default=None)
    parser.add_argument('--subject', '-s', help="For WoS, subject must include this.")
    parser.add_argument('infile', nargs='+')
    arguments = parser.parse_args()

    b = Benchmark()
    pjk = PajekFactory(temp_dir=arguments.temp_dir)

    for filename in arguments.infile:
        with open_file(filename) as f:
            for line in f:
                entry = ujson.loads(line)
                b.increment()

                if arguments.subject and arguments.subject not in entry["subject"]:
                    continue

                for citation in entry["citations"]:
                    pjk.add_edge(entry["id"], citation)

    b.print_freq()
    with open_file(arguments.outfile, "w") as f:
        pjk.write(f)
