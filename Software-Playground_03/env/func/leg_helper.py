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
