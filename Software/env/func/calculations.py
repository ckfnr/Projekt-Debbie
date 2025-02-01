from functools import lru_cache

# Classes
from env.func.Classes import Coordinate

#### C++ implemention ####

@lru_cache(maxsize=50)
def calc_circle_coordinates(step_width: float, coordinate_count: int) -> list[Coordinate]:
    return []
