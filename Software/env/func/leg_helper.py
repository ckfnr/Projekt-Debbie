import time
from adafruit_servokit import ServoKit  # type:ignore[import-untyped, import-not-found]

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

@cached
@validate_types
def adjust_angle(is_mirrored: bool, max_angle: int, angle: int, deviation: int, min_angle: int) -> int:
    """
    Adjusts the angle based on the mirror setting and deviation.<br>
    90° will be added --> (normal position = 0°).
    """
    # return max_angle - ((angle+90 + deviation) - min_angle) if is_mirrored else angle+90 + deviation  #? Maybe remove the part to add 90° to the angle?

    if is_mirrored:
        return max_angle - ((angle + 90 + deviation) - min_angle)
    else:
        return angle + 90 + deviation

@cached
@validate_types
def adjust_min_max_angles(is_mirrored: bool, min_angle: int, max_angle: int, deviation: int) -> tuple[int, int]:
    """
    Adjusts the min and max angles based on the mirror setting and deviation.
    If mirrored, swaps the distances of min and max from the normal position,
    then applies the deviation.
    """
    normal = config.servo_normal_position

    if is_mirrored:
        # return (180 - max_angle + deviation, 180 - min_angle + deviation)
        return (180 - max_angle - deviation, 180 - min_angle - deviation)
    else:
        return (min_angle + deviation, max_angle + deviation)
