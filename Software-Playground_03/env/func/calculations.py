from numpy import sin, cos, tan, arcsin, arccos, arctan, radians, degrees

# Config
from env.config import config

# Classes
from env.classes.Classes import Coordinate

# Decorators
from env.decr.decorators import cached

# Convert sin, cos, tan, arcsin, arccos, arctan
@cached
def _rad(num: float) -> float:  return radians(num)
@cached
def _deg(num: float) -> float:  return degrees(num)
@cached
def _sin(num: float) -> float:  return sin(_rad(num))
@cached
def _cos(num: float) -> float:  return cos(_rad(num))
# @cached
# def _tan(num: float) -> float:  return tan(_rad(num))
@cached
def _asin(num: float) -> float: return _deg(arcsin(num))
# @cached
# def _acos(num: float) -> float: return _deg(arccos(num))
# @cached
# def _atan(num: float) -> float: return _deg(arctan(num))

@cached
def calc_circle_coordinates(step_width: float, angle: float, max_points: int, point: int, circle_multiplier: float = config.number_a) -> list[Coordinate]:
    """
    Calculates the coordinates of a circle with a specified step width and coordinate count.
    
    :param centert_multiplier (float): The multiplier of how much the center of the circle will be moved down. (param 'a' in the maths-pdf)
    """
    return [calc_coordinate(step_width=step_width, angle=angle, max_points=max_points, point=point, circle_multiplier=circle_multiplier) for point in range(max_points+1)]

@cached
def calc_servo_angles(coordinate: Coordinate) -> tuple[int, int, int]:
    """Calculates the lower_leg and thigh servo angles."""
    raise NotImplementedError("This function is not implemented yet!")

@cached
def calc_coordinate(step_width: float, angle: float, max_points: int, point: int, circle_multiplier: float) -> Coordinate:
    """
    Calculates a 3D coordinate based on a step width, angle, and a given point index.

    This function determines a coordinate in a structured pattern based on mathematical 
    transformations involving trigonometric functions.

    :param step_width: The width of a step used to determine the spacing of points.
    :type step_width: float
    :param angle: The angle in degrees used for rotational calculations.
    :type angle: float
    :param max_points: The total number of points in the sequence.
    :type max_points: int
    :param point: The index of the current point (0-based).
    :type point: int
    :param circle_multiplier: A multiplier affecting the curvature of the coordinate arrangement.
                              Defaults to `config.number_a`.
    :type circle_multiplier: float
    :return: A `Coordinate` object containing the calculated (x, y, z) position.
    :rtype: Coordinate
    """
    #! Has to be updated as soon as @Mr.Hühnchen is done
    c1: float = ( (step_width**2) / (4-4*circle_multiplier**2) )**0.5
    c2: float = abs(_asin(circle_multiplier))
    block: float = (180*point - c2*(2*point-max_points)) / (max_points)

    x: float = -( c1 * _cos(angle) * _cos(block) )
    y: float = c1 * _sin(angle) * _cos(block)
    z: float = c1 * ( _sin(block) + config.number_a)

    return Coordinate(x, y, z)
