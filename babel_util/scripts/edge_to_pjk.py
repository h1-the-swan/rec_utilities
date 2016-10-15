from util.PajekFactory import PajekFactory
from util.misc import open_file

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Creates Pajek (.net) files from an edge/link file")
    parser.add_argument('outfile')
    parser.add_argument('--delimiter', '-d', help="Field delimiter", default='\t')
    parser.add_argument('--temp-dir', help="Directory to store temporary files in", default=None)
    parser.add_argument('infile', nargs='+')
    arguments = parser.parse_args()

    pjk = PajekFactory(temp_dir=arguments.temp_dir)

    for filename in arguments.infile:
        with open_file(filename) as f:
            for line in f:
                v_from, v_to = line.split(arguments.delimiter)
                pjk.add_edge(v_from, v_to)

    with open_file(arguments.outfile, 'w') as f:
        pjk.write(f)