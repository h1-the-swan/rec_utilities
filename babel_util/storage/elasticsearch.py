from elasticsearch import Elasticsearch, helpers
import logging

def make_es_entry(entry):
    """Given a dictionary representing a paper add the necessary keys for
    insertion into elasticsearch.

    Args:
        entry: Dictionary representing a paper to insert
    """

    return {"_index": "metadata",
            "_type": "paper",
            "_id": "{0}/{1}".format(entry["publisher"], entry["id"]),
            "doc": entry}

def field_guard(entry):
    """Ensure that entry only contains known keys and all required keys.

    Args:
        entry: A dictionary for a paper to insert into the metadata database

    Returns:
        entry if no unknown keys are present and all required keys are present.

    Raises:
        ValueError if unknown keys are present or required keys are missing
    """

    entry_keys = set(entry.keys())
    if not entry_keys.issubset(Metadata.fields):
        raise ValueError(str(entry_keys) + " contains unknown keys " + str(entry_keys.difference(Metadata.fields)))
    if not entry_keys.issuperset(Metadata.required_fields):
        raise ValueError("Missing required keys: " + str(entry_keys))

    return entry

class Metadata(object):
    fields = {"id", "title", "date", "publisher", "venue", "affiliations", "citations", "label", "authors", "abstract", "doi"}
    required_fields = {"id", "title", "publisher"}

    def __init__(self, hosts, username, password, index="metadata", **kwargs):
        http_auth = None
        if username and password:
            http_auth = (username, password)
        else:
            logging.warning("No username or password. Unauthenticated connection to Elasticsearch.")

        self.conn = Elasticsearch(hosts, http_auth=http_auth)
        self.index = index

    def make_id(self, publisher, paper_id):
        #TODO: Make static
        return "{0}/{1}".format(publisher, paper_id)

    def insert_bulk(self, documents):
        """Given an iterator of documents, inserts them all into the database

        Args:
            documents: An iterator of documents to insert.
            See https://elasticsearch-py.readthedocs.org/en/latest/helpers.html for info on the expected format.
        """
        iterate = map(lambda x: make_es_entry(field_guard(x)), documents)
        return helpers.bulk(self.conn, iterate)
