from functools import lru_cache
from typing import Any, get_type_hints

# Config
from env.config import config

def cached(func):
    """Decorator to cache some data to prevent recomputing."""
    __doc__ = func.__doc__  # Show the doc of the given function

    @lru_cache(maxsize=config.max_lru_cache)
    def wrapper(*args, **kwargs): return func(*args, **kwargs)
    return wrapper

def validate_types(func):
    """Decorator to enforce type checking on function arguments."""
    __doc__ = func.__doc__  # Show the doc of the given function
    hints = get_type_hints(func)

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        bound_arguments = func.__code__.co_varnames[:func.__code__.co_argcount]
        arguments = dict(zip(bound_arguments, args))
        arguments.update(kwargs)
        
        for arg_name, arg_value in arguments.items():
            if arg_name in hints and not isinstance(arg_value, hints[arg_name]):
                raise TypeError(f"Argument '{arg_name}' must be {hints[arg_name]}, got {type(arg_value)} instead.")
        
        return func(*args, **kwargs)
    
    return wrapper
