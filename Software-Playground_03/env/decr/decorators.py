from functools import lru_cache, wraps
from typing import Callable, TypeVar, Any, get_type_hints, Type, Optional

F = TypeVar("F", bound=Callable[..., Optional[Any]])

# Config
from env.config import config

def cached(func):
    __doc__ = func.__doc__  # Show the doc of the given function

    @lru_cache(maxsize=config.max_lru_cache)
    def wrapper(*args, **kwargs): return func(*args, **kwargs)
    return wrapper

def validate_types(func: F) -> F:
    """Decorator to enforce type checking on function arguments."""
    __doc__ = func.__doc__  # Show the doc of the given function
    hints = get_type_hints(func)
    
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        bound_arguments = func.__code__.co_varnames[:func.__code__.co_argcount]
        arguments = dict(zip(bound_arguments, args))
        arguments.update(kwargs)
        
        for arg_name, arg_value in arguments.items():
            if arg_name in hints and not isinstance(arg_value, hints[arg_name]):
                raise TypeError(
                    f"Argument '{arg_name}' must be {hints[arg_name]}, got {type(arg_value)} instead."
                )
        
        return func(*args, **kwargs)
    
    return wrapper  # type: ignore


def validate_types_class(cls: Type[Any]) -> Type[Any]:
    """Decorator to enforce type checking on all methods of a class."""
    __doc__ = cls.__doc__  # Show the doc of the given class
    
    for attr_name, attr_value in cls.__dict__.items():
        if callable(attr_value):  # Check if it's a method/function
            setattr(cls, attr_name, validate_types(attr_value))
    return cls
