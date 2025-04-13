from numpy import sin, cos, tan, arcsin, arccos, arctan, radians, degrees
from typing import Literal
from decimal import getcontext

# Set high precision for Decimal calculations
getcontext().prec = 28  

# Config
from env.config import config

# Classes
from env.classes.Classes import Coordinate

# Decorators
from env.decr.decorators import cached, validate_types

# Trigonometric functions
def _deg(num: float) -> float:  return degrees(num)
def _rad(num: float) -> float:  return radians(num)
def _sin(num: float) -> float:  return sin(_rad(num))
def _cos(num: float) -> float:  return cos(_rad(num))
# def _tan(num: float) -> float:  return tan(_rad(num))
def _asin(num: float) -> float: return _deg(arcsin(num))
def _acos(num: float) -> float: assert -1 <= num <= 1, f"Num {num} out of range in _acos!" ; return _deg(arccos(num))
def _atan(num: float) -> float: return _deg(arctan(num))
def _sqrt(num: float) -> float: return num ** 0.5



'<-- MOVEMENT CALCULATIONS -->'

@cached
@validate_types
def calc_circle_coordinates(step_width: float, angle: int, max_points: int = 50, circle_multiplier: float = config.number_a) -> list[Coordinate]:
    """
    Calculates the coordinates of a circle with a specified step width and coordinate count.<br>
    If max_points=50; it will return 51 points (0-50). 25 would be the very top of the movement<br>
    and it would be the exact half of the step width.
    
    :param circle_multiplier (float): The multiplier of how much the center of the circle will be moved down. (param 'a' in the maths-pdf)
    """
    return [_calc_circle_coordinate(
        step_width=step_width,
        angle=angle,
        max_points=max_points,
        point=point,
        circle_multiplier=circle_multiplier
    ) for point in range(max_points+1)]

@cached
@validate_types
def _get_radius(step_width: float, circle_multiplier: float) -> float: return _sqrt((step_width**2) / (4 - 4 * circle_multiplier**2))
@cached
@validate_types
def _get_pnr(point: int, c1: float, max_points: int) -> float: return (180 * point - c1 * (2 * point - max_points)) / (max_points)
@cached
@validate_types
def _get_c1(circle_multiplier: float) -> float: return abs(_asin(circle_multiplier))
@cached
@validate_types
def _get_c2(step_width: float) -> float: return step_width / 2
@cached
@validate_types
def _get_c3(r: float, pnr: float, c2: float) -> float: return r * _cos(pnr) - c2

@cached
@validate_types
def _calc_circle_coordinate(step_width: float, angle: int, point: int, max_points: int, circle_multiplier: float) -> Coordinate:
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
    :param circle_multiplier: A multiplier affecting the curvature of the coordinate arrangement. Defaults to config.number_a.
    :type circle_multiplier: float
    :return: A Coordinate object containing the calculated (x, y, z) position.
    :rtype: Coordinate
    """
    r: float = _get_radius(step_width=step_width, circle_multiplier=circle_multiplier)
    c1: float = _get_c1(circle_multiplier=circle_multiplier)
    pnr: float = _get_pnr(point=point, max_points=max_points, c1=c1)
    c2: float = _get_c2(step_width=step_width)
    c3: float = _get_c3(r=r, pnr=pnr, c2=c2)

    x: float = -_cos(angle) * c3
    y: float = -_sin(angle) * c3
    z: float = r * (_sin(pnr) + circle_multiplier)

    return Coordinate(round(x, 6), round(y, 6), round(z, 6))



'<-- LEG CALCULATIONS -->'

@cached
@validate_types
def calc_epsilons(l_ds: float) -> dict[Literal["epsilon-alpha", "epsilon-beta"], float]:
    theta_2e      : float = _acos((config.z_def**2 + config.l_2**2 - config.l_1**2) / (2 * abs(config.z_def) * config.l_2))
    epsilon_alpha : float = 90 - theta_2e

    theta_3e      : float = _acos((config.l_1**2 + config.l_2**2 - config.z_def**2) / (2 * config.l_1 * config.l_2))
    theta_4e      : float = 180 - theta_3e

    l_2l3e        : float = _sqrt(config.l_2**2 + config.l_3**2 - 2 * config.l_2 * config.l_3 * _cos(theta_4e))
    theta_5e      : float = _acos((config.l_2**2 + l_2l3e**2 - config.l_3**2) / (2 * config.l_2 * l_2l3e))
    theta_6e      : float = _acos((l_2l3e**2 + config.l_5**2 - config.l_4**2) / (2 * l_2l3e * config.l_5))
    theta_7e      : float = theta_6e + theta_5e - epsilon_alpha

    theta_8e      : float = _acos((config.l_5**2 + config.l_7**2 - config.l_6**2) / (2 * config.l_5 * config.l_7))
    theta_9e      : float = 180 - theta_8e - theta_7e
    theta_10e     : float = theta_9e + 45

    l_8l9e        : float = _sqrt(config.l_7**2 + l_ds**2 - 2 * config.l_7 * l_ds * _cos(theta_10e))
    theta_11e     : float = _acos((l_8l9e**2 + l_ds**2 - config.l_7**2) / (2 * l_8l9e * l_ds))
    theta_12e     : float = _acos((l_8l9e**2 + config.l_9**2 - config.l_8**2) / (2 * l_8l9e * config.l_9))

    epsilon_beta  : float = 135 - theta_12e - theta_11e

    return {"epsilon-alpha": epsilon_alpha, "epsilon-beta": epsilon_beta}

@cached
@validate_types
def calc_servo_angles(coordinate: Coordinate, height_multiplier: float = config.height_multiplier) -> dict[Literal["thigh", "lower-leg", "side-axis"], int]:
    """Calculates the lower_leg, thigh and side_axis servo angles."""
    coordinate.add_xyz_tuple(config.coord_deviation)

    # Set up xyz
    x_sa: float = coordinate.x
    y_sa: float = coordinate.y
    z_sa: float = coordinate.z * height_multiplier

    # General calculations for servo angles
    l_ds  : float = _sqrt(2) * config.d_s
    z_sac : float = z_sa + config.z_def

    # Epsilon calculations
    epsilons: dict[str, float] = calc_epsilons(l_ds)
    epsilon_alpha: float = epsilons["epsilon-alpha"]
    epsilon_beta : float = epsilons["epsilon-beta"]

    # Servo angle formulas
    # <-- Start -->
    z_sa2D   : float = _sqrt(y_sa**2 + z_sac**2)
    l_1l2    : float = _sqrt(x_sa**2 + z_sa2D**2)
    theta_1X : float = _atan(x_sa / z_sa2D)

    theta_2  : float = _acos((l_1l2**2 + config.l_2**2 - config.l_1**2) / (2 * l_1l2 * config.l_2))
    theta_3  : float = _acos((config.l_1**2 + config.l_2**2 - l_1l2**2) / (2 * config.l_1 * config.l_2))
    theta_4  : float = 180 - theta_3

    l_2l3    : float = _sqrt(config.l_2**2 + config.l_3**2 - 2 * config.l_2 * config.l_3 * _cos(theta_4))
    theta_5  : float = _acos((config.l_2**2 + l_2l3**2 - config.l_3**2) / (2 * config.l_2 * l_2l3))
    theta_6  : float = _acos((l_2l3**2 + config.l_5**2 - config.l_4**2) / (2 * l_2l3 * config.l_5))

    alpha    : float = theta_2 - theta_1X + epsilon_alpha - 90
    theta_7  : float = theta_6 + theta_5 + alpha - epsilon_alpha

    theta_8  : float = _acos((config.l_5**2 + config.l_7**2 - config.l_6**2) / (2 * config.l_5 * config.l_7))
    theta_9  : float = 180 - theta_8 - theta_7
    theta_10 : float = theta_9 + 45

    l_8l9    : float = _sqrt(config.l_7**2 + l_ds**2 - 2 * config.l_7 * l_ds * _cos(theta_10))
    theta_11 : float = _acos((l_8l9**2 + l_ds**2 - config.l_7**2) / (2 * l_8l9 * l_ds))
    theta_12 : float = _acos((l_8l9**2 + config.l_9**2 - config.l_8**2) / (2 * l_8l9 * config.l_9))

    beta     : float = theta_12 + theta_11 + epsilon_beta - 135
    gamma    : float = _atan(y_sa / z_sac)
    # <-- End -->

    return {"thigh": int(round(alpha, 0)), "lower-leg": int(round(beta, 0)), "side-axis": int(round(gamma, 0))}
