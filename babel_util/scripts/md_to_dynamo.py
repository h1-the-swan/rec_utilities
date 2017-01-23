from storage.dynamo import Metadata, DATASETS
import logging
import csv
from util.misc import Benchmark, open_file
import boto3

REQUIRED_KEYS = {'title', 'paper_id', 'date'}

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Creates or updates a DynmoDB table with TSV metadata.")
    parser.add_argument('dataset', help="Dataset", choices=DATASETS)
    parser.add_argument('metadata')
    parser.add_argument('--benchmark-freq', default=100000, type=int)
    parser.add_argument('--delimiter', '-d', default='\t')
    parser.add_argument("--region", help="Region to connect to", default="us-east-1")
    parser.add_argument("--include", help="Comma separated list of additional field to include")
    parser.add_argument("-c", "--create", help="create table in database", action="store_true")
    parser.add_argument("-f", "--flush", help="flush database.", action="store_true")
    parser.add_argument("-n", "--dryrun", help="Process data, but don't insert into DB", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    table_name = args.dataset + "_md"

    if args.region == "localhost":
        client = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    else:
        client = boto3.resource('dynamodb')

    include_fields = set(REQUIRED_KEYS)

    if args.include:
        include_fields.add(map(str.strip, args.include.split(",")))

    t = Metadata(client, table_name)

    if args.flush:
        logging.info("Deleting table: " + t.table_name)
        if not args.dryrun:
            t.delete()

    if args.create:
        logging.info("Creating table: " + t.table_name)
        if not args.dryrun:
            t.create(write=2000)

    b = Benchmark(args.benchmark_freq)
    with open_file(args.metadata) as ifs:
        with t.get_batch_put_context() as batch:
            reader = csv.DictReader(ifs, delimiter=args.delimiter)
            for row in reader:
                new_row = {k:v for k,v in row.items() if k in include_fields}
                if not REQUIRED_KEYS.issubset(new_row.keys()):
                    print(row)
                    raise KeyError("Not all required keys present")
                if not args.dryrun:
                    batch.put_item(Item=new_row)
                b.increment()

    if not args.dryrun:
        t.update_throughput()

    b.print_freq()
