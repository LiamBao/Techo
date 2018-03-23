import functools
from functools import wraps


"""
    functools实现数据缓存:
"""
# Python2 实现数据缓存:
def memoize(function):
    memo = {}
    @wraps(function)
    def wrapper(*args):
        if args in memo:
            return memo[args]
        else:
            rv = function(*args)
            memo[args] = rv
            return rv
    return wrapper

@memoize
def fibonacci(n):
    if n < 2: return n
    return fibonacci(n - 1) + fibonacci(n - 2)

fibonacci(25)

# Python3 实现数据缓存
@functools.lru_cache
def functions(args):
    pass

## functools.lru_cache node:
def lru_cache(maxsize=128, typed=False):
    if maxsize is not None and not isinstance(maxsize, int):
        raise TypeError('Expected maxsize to be an interger or None')