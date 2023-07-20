#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import redis
import requests
from functools import wraps
from typing import Callable

redis_store = redis.Redis()


def data_cacher(method: Callable) -> Callable:
    '''
    Decorator function to cache the output of fetched data
    and track the request count.

    Parameters:
        method (Callable): The function to be decorated.

    Returns:
        Callable: The wrapped function with caching and tracking behavior.
    '''

    @wraps(method)
    def invoker(url: str) -> str:
        '''
        Wrapper function for caching the output and tracking the request count.

        Parameters:
            url (str): The URL whose content needs to be fetched.

        Returns:
            str: The content of the URL.
        '''

        # Increment the count for this URL
        redis_store.incr(f'count:{url}')

        # Check if the URL content is already cached
        result = redis_store.get(f'result:{url}')

        if result:
            # If cached, return the cached content
            return result.decode('utf-8')

        # If not cached, fetch the content using the provided method
        result = method(url)

        # Cache the result with an expiration time of 10 seconds
        if result:
            redis_store.setex(f'result:{url}', 10, result)

        return result

    return invoker


@data_cacher
def get_page(url: str) -> str:
    '''
    Fetches the content of a URL and caches the request's
    response with an expiration time of 10 seconds,
    while also tracking the number of times the URL was accessed.

    Parameters:
        url (str): The URL whose content needs to be fetched.

    Returns:
        str: The content of the URL.
    '''

    result = requests.get(url).text
    return result
