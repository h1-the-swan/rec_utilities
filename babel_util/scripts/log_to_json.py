import json
from parsers.infomap_log import InfomapLog

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Creates JSON file from Infomap Logs")
    parser.add_argument('outfile')
    parser.add_argument('infiles', nargs='+')

    args = parser.parse_args()

    logs = []
    for filename in args.infiles:
        with open(filename) as f:
            parser = InfomapLog(f)
            logs.append(parser.parse())

    with open(args.outfile, 'w') as f:
        json.dump(logs, f)
