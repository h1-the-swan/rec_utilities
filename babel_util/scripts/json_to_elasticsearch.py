#!/usr/bin/env python3
from storage.elasticsearch import Metadata
from util.misc import open_file
import ujson
from functools import partial

ES_USER = "ES_USERNAME"
ES_PASSWORD = "ES_PASSWORD"
ES_HOST = "ES_HOST"


def add_publisher(pub, e):
    e["publisher"] = pub
    return e


def filter_dict(valid_keys, e):
    return {k: e[k] for k in e if k in valid_keys}

if __name__ == "__main__":
    import argparse
    import os
    import logging
    parser = argparse.ArgumentParser(description="Load JSON to Elasticsearch")
    parser.add_argument('infile', nargs='+')
    parser.add_argument('--dryrun', '-d', help="Don't actually modify the metadata database, but parse all files.", action="store_true")
    parser.add_argument('--keys', '-k', help="Comma separated list of keys to include. Include all by default.")
    parser.add_argument('--username',
                        help="Elasticsearch username. If not provided read from environment variable " + ES_USER,
                        default=os.environ.get(ES_USER))
    parser.add_argument('--password',
                        help="Elasticsearch password. If not provided read from environment variable " + ES_PASSWORD,
                        default=os.environ.get(ES_PASSWORD))
    parser.add_argument('--host',
                        help="Elasticsearch host. If not provided read from environment variable " + ES_HOST,
                        default=os.environ.get(ES_HOST))
    parser.add_argument('--publisher', #TODO: One day, change this to dataset
                        help="Publisher name to inject into each JSON document")

    args = parser.parse_args()

    if not args.username or not args.password:
        logging.warning("No username or password provided")

    pub_up = None
    if args.publisher:
        pub_up = partial(add_publisher, args.publisher)

    key_filter = None
    if args.keys:
        keys = set((args.keys.split(",")))
        if not keys <= Metadata.fields:
            raise ValueError("Trying to include an unknown field: % " % keys - Metadata.fields)
        key_filter = partial(filter_dict, keys)

    p = Metadata(args.host, args.username, args.password)
    for filename in args.infile:
        with open_file(filename) as f:
            itr = map(ujson.loads, f)

            if pub_up:
                itr = map(pub_up, itr)

            if key_filter:
                itr = map(key_filter, itr)

            if args.dryrun:
                for e in itr:
                    print(e)
            else:
                print(p.insert_bulk(itr))
