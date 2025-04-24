from typing import Iterator

# Types
from env.types.typing import ITER

def iterate_with_offset(list: list[ITER], offset: int = 0) -> Iterator[ITER]:
    """
    Iterate over a list with an offset.
    
    :param list: The list to iterate over.
    :param offset: The offset to start from.
    """
    n: int = len(list)
    for i in range(n): yield list[(i + offset) % n]
