#!/usr/bin/env python3
""" This module defines Cache class """
import redis
import uuid
from typing import Union, Callable


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

    def get(self, key: str, fn: Callable = None
            ) -> Union[str, bytes, int, float]:
        """ retrieve values from Redis data storage"""
        data = self._redis.get(key)
        if fn is not None:
            return fn(data)
        else:
            return data

    def get_str(self, key: str) -> str:
        """ method to convert data to string """
        return self.get(key, fn=lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """ method to convert data to integer """
        return self.get(key, fn=lambda x: int(x))
