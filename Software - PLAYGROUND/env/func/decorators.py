from functools import lru_cache

# Config
from env.config import config

def cached(func):
    __doc__ = func.__doc__

    @lru_cache(maxsize=config.max_lru_cache)
    def wrapper(*args, **kwargs): return func(*args, **kwargs)
    return wrapper
