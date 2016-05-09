#!/usr/bin/env python3
from util.misc import open_file, Benchmark
from util.PajekFactory import PajekFactory
import ujson


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Creates Pajek (.net) files from JSON")
    parser.add_argument('outfile')
    parser.add_argument('--temp-dir', help="Directory to store temporary files in", default=None)
    parser.add_argument('--subject', '-s', help="For WoS, subject must include this. Can be a comma seperated list.")
    parser.add_argument('--wos-only', help="For WoS, exclude any citations or ids that contain a dot (.)", action="store_true")
    parser.add_argument('infile', nargs='+')
    arguments = parser.parse_args()

    b = Benchmark()
    pjk = PajekFactory(temp_dir=arguments.temp_dir)

    subjects = None
    if arguments.subject:
        subjects = set(arguments.subject.split(","))

    for filename in arguments.infile:
        with open_file(filename) as f:
            for line in f:
                entry = ujson.loads(line)
                b.increment()

                if arguments.wos_only and '.' in entry["id"]:
                    continue

                if subjects:
                    if "subject" not in entry:
                        continue

                    if not subjects.intersection(entry["subject"]):
                        continue

                for citation in entry["citations"]:
                    if arguments.wos_only and '.' in citation:
                        continue

                    pjk.add_edge(entry["id"], citation)

    b.print_freq()
    with open_file(arguments.outfile, "w") as f:
        pjk.write(f)
