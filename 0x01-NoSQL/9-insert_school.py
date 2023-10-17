#!/usr/bin/env python3
"""function that inserts a new document in a collection based on kwargs """


def insert_school(mongo_collection, **kwargs):
    """function that inserts a new document in a collection using kwargs"""
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
