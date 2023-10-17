#!/usr/bin/env python3
"""Python function that lists all documents in a collection"""


def list_all(mongo_collection):
    """ lists all documents in a collection """
    documents = []
    for doc in mongo_collection.find():
        documents.append(doc)
    return documents
