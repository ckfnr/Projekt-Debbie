from functools import lru_cache

# Classes
from env.func.Classes import Coordinate

@lru_cache(maxsize=50)
def calc_circle_coordinates(step_width: float, coordinate_count: int) -> list[Coordinate]:
    """Calculates the coordinates of a circle with a specified step width and coordinate count."""
    raise NotImplementedError("This function is not implemented yet!")

@lru_cache(maxsize=50)
def calc_ll_t_servo_angles(coordinate: Coordinate) -> tuple[int, int]:
    """Calculates the lower_leg and thigh servo angles."""
    raise NotImplementedError("This function is not implemented yet!")
