import inspect
from types import FrameType
from functools import lru_cache, wraps
from typing import Any, get_type_hints, Callable, Optional

# Config
from env.config import config

def cached(func: Callable) -> Any:
    """Decorator to cache some data to prevent recomputing."""
    __doc__ = func.__doc__

    @lru_cache(maxsize=config.max_lru_cache)
    @wraps(func)
    def wrapper(*args, **kwargs): return func(*args, **kwargs)
    return wrapper

def validate_types(func: Callable) -> Any:
    """Decorator to enforce type checking on function arguments."""
    __doc__ = func.__doc__
    hints: dict[str, Any] = get_type_hints(func)

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        details: str = "NOT FOUND"
        # Get call frame
        ft: Optional[FrameType] = inspect.currentframe()
        if ft:
            frame: Optional[FrameType] = ft.f_back  # Get the caller's frame
            if frame:
                filename = frame.f_code.co_filename
                lineno = frame.f_lineno
                details = f"Function '{func.__name__}' called from {filename}:{lineno}"

        bound_arguments: tuple[str, ...] = func.__code__.co_varnames[:func.__code__.co_argcount]
        arguments: dict[str, Any] = dict(zip(bound_arguments, args))
        arguments.update(kwargs)

        for arg_name, arg_value in arguments.items():
            if arg_name in hints and not isinstance(arg_value, hints[arg_name]):
                raise TypeError(f"Argument '{arg_name}' must be {hints[arg_name]}, got {type(arg_value)} instead. Details: {details}")

        return func(*args, **kwargs)
    
    return wrapper
