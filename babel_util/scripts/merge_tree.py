from util.misc import open_file
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Merge tree files")
    parser.add_argument('outfile')
    parser.add_argument('infiles', nargs='+')

    args = parser.parse_args()

    with open_file(args.outfile, 'w') as outf:
        for i, filename in enumerate(args.infiles, start=1):
            with open_file(filename) as inf:
                l = inf.readline()
                if l[0] == "#":
                    continue
                 outf.write("%d:%s\n" % (i, l))
