import time
from adafruit_servokit import ServoKit  # type:ignore[import-untyped]
from typing import Any

# Decorators
from env.decr.decorators import validate_types, cached

# Config
from env.config import config

@validate_types
def initialize_servos(servo_kit: ServoKit) -> None:
    for i in range(config.servo_channel_count):
        servo_kit.servo[i].angle = servo_kit.servo[i].angle
        time.sleep(0.1)  # Add a small delay to avoid abrupt movements

@cached
@validate_types
def adjust_angle(is_mirrored: bool, max_angle: int, angle: int, deviation: int, min_angle: int) -> int:
    """
    Adjusts the angle based on the mirror setting and deviation.
    """
    return max_angle - ((angle + deviation) - min_angle) if is_mirrored else angle + deviation

@cached
@validate_types
def validate_dict(required_keys: dict[str, set], dictionary: dict[str, Any]) -> None:
    """
    Validates whether a dictionary contains all required keys and subkeys.

    :param required_keys (dict[str, set]): Dictionary specifying required keys and their expected subkeys.
    :param dictionary (dict[str, Any]): The dictionary to validate.
    :raises ValueError: If any required key or subkey is missing.
    """
    # Check all keys
    for key, subkeys in required_keys.items():
        if key not in dictionary or not isinstance(dictionary[key], dict):
            raise ValueError(f"'{key}' must be a dictionary containing {subkeys}.")
        missing_keys = subkeys - dictionary[key].keys()
        if missing_keys:
            raise ValueError(f"'{key}' is missing required keys: {missing_keys}.")
