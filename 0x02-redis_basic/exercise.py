#!/usr/bin/env python3
""" This module defines Cache class """
import redis
import uuid
from typing import Union


class Cache():
    """ creates the class Cache """
    def __init__(self):
        """ Initializes an instance of Cache class """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ method to create and store random key """
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)
        return random_key
