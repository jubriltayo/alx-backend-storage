#!/usr/bin/env python3
""" Python function that returns all students sorted by average score """


def top_students(mongo_collection):
    """ Returns all students sorted by average score """
    query = [
        {"$unwind": "$topics"},
        {"$group": {
            "_id": "$_id",
            "name": {"$first": "$name"},
            "averageScore": {"$avg": "$topics.score"}
        }},
        {"$sort": {"averageScore": -1}}
    ]
    return list(mongo_collection.aggregate(query))
