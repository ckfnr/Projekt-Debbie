from typing import get_type_hints

def validate_types(func):
    __doc__ = func.__doc__  # Show the doc of the given function
    hints = get_type_hints(func)

    def wrapper(*args, **kwargs):
        bound_arguments = func.__code__.co_varnames[:func.__code__.co_argcount]
        arguments = dict(zip(bound_arguments, args))
        arguments.update(kwargs)
        
        for arg_name, arg_value in arguments.items():
            if arg_name in hints and not isinstance(arg_value, hints[arg_name]):
                raise TypeError(
                    f"Argument '{arg_name}' must be {hints[arg_name]}, got {type(arg_value)} instead."
                )
        
        return func(*args, **kwargs)
    
    return wrapper

# Example usage:
@validate_types
def add(x: int, y: int) -> int:
    return x + y

print(add(3, 5))  # Works fine
print(add(3, "5"))  # Raises TypeError

def validate_types_class(cls):
    __doc__ = cls.__doc__  # Show the doc of the given class
    for attr_name, attr_value in cls.__dict__.items():
        if callable(attr_value):  # Check if it's a method/function
            setattr(cls, attr_name, validate_types(attr_value))
    return cls
