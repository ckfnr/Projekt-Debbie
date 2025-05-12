from numpy import sin, cos, tan, arcsin, arccos, arctan, radians, degrees
from typing import Literal
from decimal import getcontext

# Set high precision for Decimal calculations
getcontext().prec = 28  

# Config
from env.config import config

# Func
from env.func.DEBUG import dprint

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


'<-- GENERAL CALCULATIONS -->'
@cached
@validate_types
def _add_or_subtract(value: float, add: bool, amount: float, target_value: float) -> float:
    """Adds or subtracts a value to/from the target value based on the add parameter."""
    if add:
        return min(value + amount, target_value)
    else:
        return max(value - amount, target_value)
    
def add_until_max(value: float, max_value: float) -> float:
    """Adds a value until it reaches the maximum value."""
    return _add_or_subtract(value, True, config.step_width, max_value)

def subtract_until_min(value: float, min_value: float) -> float:
    """Subtracts a value until it reaches the minimum value."""
    return _add_or_subtract(value, False, config.step_width, min_value)


'<-- MOVEMENT CALCULATIONS -->'

@cached
@validate_types
def calc_circle_coordinates(step_width: float, angle: int, max_points: int = config.max_points, smoothness: float = config.smoothness) -> list[Coordinate]:
    """
    Calculates the coordinates of a circle with a specified step width and coordinate count.<br>
    If max_points=10; it will return 11 points (0-10). 5 would be the very top of the movement<br>
    and it would be the exact half of the step width.
    
    :param smoothness (float): The multiplier of how much the center of the circle will be moved down. (param 'a' in the maths-pdf)
    """
    return [_calc_circle_coordinate(
        step_width=step_width,
        angle=angle,
        max_points=max_points,
        point=point,
        smoothness=smoothness
    ) for point in range(max_points+1)]

@cached
@validate_types
def _get_r(smoothness: float, step_width: float) -> float: return _sqrt((step_width**2) / (4 - 4 * smoothness**2))
@cached
@validate_types
def _get_h_m(r: float, smoothness: float) -> float: return (config.step_height) / (r * (1 + smoothness))

@cached
@validate_types
def _calc_circle_coordinate(step_width: float, angle: int, point: int, max_points: int, smoothness: float) -> Coordinate:
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
    :param smoothness: A multiplier affecting the curvature of the coordinate arrangement. Defaults to config.number_a.
    :type smoothness: float
    :return: A Coordinate object containing the calculated (x, y, z) position.
    :rtype: Coordinate
    """
    # Calculate the radius and height based on the step width and smoothness
    r: float = _get_r(smoothness=smoothness, step_width=step_width)
    h_m: float = _get_h_m(r=r, smoothness=smoothness)

    # Calculate the coordinates based on the given parameters
    c1: float = abs(_asin(smoothness))
    p_wm: float = (180 * point - c1 * (2 * point - max_points)) / (max_points)
    c2: float = step_width / 2
    c3: float = r * _cos(p_wm) - c2

    # Get xyz coordinates
    x: float = -_cos(angle) * c3
    y: float = _sin(angle) * c3
    z: float = h_m * r * (_sin(p_wm) + smoothness)

    dprint(f"calc_circle_coordinate(x={x}, y={y}, z={z}) with step_width={step_width}, r={r}, h_m={h_m}, c1={c1}, p_wm={p_wm}, c2={c2}, c3={c3}; smoothness={smoothness}")

    return Coordinate(round(x, 6), round(y, 6), round(z, 6))


'<-- LEG CALCULATIONS -->'

@cached
@validate_types
def calc_epsilons(l_ds: float) -> dict[Literal["epsilon-alpha", "epsilon-beta"], float]:
    """Calculates epsilon-alpha and epsilon-beta angles.

    Args:
        l_ds(float): Length of the last segment.

    Returns:
        dict[Literal["epsilon-alpha", "epsilon-beta"], float]: A dictionary containing the calculated epsilon-alpha and epsilon-beta angles.

    Raises:
        ValueError: If any of the intermediate calculations result in invalid values (e.g., taking the square root of a negative number or acos of a value outside the range [-1, 1]).
        TypeError: If input parameters are of incorrect type.
    """
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
def _get_l_ds() -> float: return _sqrt(2) * config.d_s
@cached
@validate_types
def _get_d_cpsum(y: float) -> float: return config.d_ys + config.d_cpm + (-(config.f_w / 2) if y > 0 else (config.f_w / 2))

@cached
@validate_types
def calc_servo_angles(coordinate: Coordinate) -> dict[Literal["thigh", "lower-leg", "side-axis"], int]:
    coordinate.add_xyz_tuple(config.coord_deviation)

    # General calculations for servo angles
    l_ds   : float = _get_l_ds()
    d_cpsum: float = _get_d_cpsum(y=coordinate.y)

    # Epsilon calculations
    epsilons     : dict[str, float] = calc_epsilons(l_ds)
    epsilon_alpha: float            = epsilons["epsilon-alpha"]
    epsilon_beta : float            = epsilons["epsilon-beta"]

    # Servo angle formulas
    # <-- Start -->
    z_sac    : float = coordinate.z + config.z_def  #ToDo: Use coordinate deviation instead
    l_cp     : float = _sqrt((coordinate.y + d_cpsum)**2 + z_sac**2)
    z_sa2D   : float = _sqrt(l_cp**2 - d_cpsum**2)
    l_1l2    : float = _sqrt(coordinate.x**2 + z_sa2D**2)
    theta_1X : float = _atan(coordinate.x / z_sa2D)

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
    gamma    : float = _atan((coordinate.y * abs(z_sac)) / (z_sac**2 + d_cpsum**2 + coordinate.y * d_cpsum))
    # <-- End -->

    return {"thigh": int(round(alpha, 0)), "lower-leg": int(round(beta, 0)), "side-axis": int(round(gamma, 0))}
