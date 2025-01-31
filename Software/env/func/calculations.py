from functools import lru_cache

# Classes
from env.func.Classes import Coordinate

# Cache up to 50 different circles
@lru_cache(maxsize=50)
def calc_circle_coordinates(radius: float) -> list[Coordinate]:
        # The calculations will be added as soon as @Mr.Hühnchen is done
        raise NotImplementedError("This function is not implemented yet!")
