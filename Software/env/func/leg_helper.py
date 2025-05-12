import time
from adafruit_servokit import ServoKit  # type:ignore[import-untyped, import-not-found]
from typing import cast

# Decorators
from env.decr.decorators import validate_types, cached

# Config
from env.config import config

@validate_types
def initialize_servos(servo_kit: ServoKit) -> None:
    """
    Initialize the servos on the servo kit.

    :param servo_kit: The servo kit to control the servos.
    :return: None
    """
    for i in range(config.servo_channel_count):
        servo_kit.servo[i].angle = servo_kit.servo[i].angle
        time.sleep(0.1)  # Add a small delay to avoid abrupt movements

@validate_types
def adjust_angle(is_mirrored: bool, max_angle: int, angle: int, deviation: int, min_angle: int) -> int:
    """
    Adjusts the angle based on mirroring and deviation.
    Assumes 90° is the neutral (internal 0°) position.
    Deviation is applied before mirroring to ensure symmetric movement.
    """
    adjusted = angle + 90 + deviation

    if is_mirrored:
        return 180 - adjusted  # It's a feature, not a bug! Even if the mirrored servos look like they have a skill issue.
    else:
        return adjusted

@validate_types
def adjust_min_max_angles(is_mirrored: bool, min_angle: int, max_angle: int, deviation: int) -> tuple[int, int]:
    """
    Adjusts the min and max angles based on the mirror setting and deviation.
    If mirrored, swaps the distances of min and max from the normal position,
    then applies the deviation.
    """
    adjusted_min = min_angle + deviation
    adjusted_max = max_angle + deviation

    if is_mirrored:
        return cast(tuple[int, int], tuple(sorted((180 - adjusted_max, 180 - adjusted_min))))  # Sort to ensure min is less than max; Use cast to avoid type error
    else:
        return (adjusted_min, adjusted_max)
