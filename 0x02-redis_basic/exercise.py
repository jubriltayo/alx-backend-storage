#!/usr/bin/env python3
""" This module defines Cache class """
import redis
import uuid
from typing import Union, Callable, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ count the number of calls made to a method in the Cache class """
    @wraps(method)
    def caller(self, *args, **kwargs) -> Any:
        """ calls the given method and increments its counter """
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return caller


def call_history(method: Callable) -> Callable:
    """ calls the details/logs of a method in the Cache class """
    @wraps(method)
    def caller(self, *args, **kwargs) -> Any:
        """ retrieves input and output and returns the method's output """
        input_key = "{}:inputs".format(method.__qualname__)
        output_key = "{}:outputs".format(method.__qualname__)

        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(input_key, str(args))

        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(output_key, output)
        return output
    return caller


def replay(fn: Callable) -> None:
    """ display the history of calls of a Cache class method """
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    fn_name = fn.__qualname__
    input_key = "{}:inputs".format(fn_name)
    output_key = "{}:outputs".format(fn_name)
    fn_call_count = 0
    if redis_store.exists(fn_name) != 0:
        fn_call_count = int(redis_store.get(fn_name))
    print("{} was called {} times:".format(fn_name, fn_call_count))
    fn_inputs = redis_store.lrange(input_key, 0, -1)
    fn_outputs = redis_store.lrange(output_key, 0, -1)
    for fn_input, fn_output in zip(fn_inputs, fn_outputs):
        print("{}(*{}) -> {}".format(fn_name, fn_input.decode("utf-8"),
                                     fn_output))


class Cache():
    """ creates the class Cache """
    def __init__(self):
        """ Initializes an instance of Cache class """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
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
