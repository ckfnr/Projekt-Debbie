import time
import threading
from adafruit_servokit import ServoKit, Servo  # type:ignore[import-untyped]
from typing import Any

# Config
from env.config import config

# Initialize servo kit
try:
    servo_kit: ServoKit = ServoKit(channels=config.servo_channel_count)
except Exception as e:
    raise RuntimeError(f"Failed to initialize ServoKit: {e}")


def _validate_dict(required_keys: dict[str, set], dictionary: dict[str, Any]) -> None:
    """
    Validates whether a dictionary contains all required keys and subkeys.

    :param required_keys (dict[str, set]): Dictionary specifying required keys and their expected subkeys.
    :param dictionary (dict[str, Any]): The dictionary to validate.
    :raises ValueError: If any required key or subkey is missing.
    """
    for key, subkeys in required_keys.items():
        if key not in dictionary or not isinstance(dictionary[key], dict):
            raise ValueError(f"'{key}' must be a dictionary containing {subkeys}.")
        missing_keys = subkeys - dictionary[key].keys()
        if missing_keys:
            raise ValueError(f"'{key}' is missing required keys: {missing_keys}.")


class ServoManager:
    """
    Manages a single servo's movement and state.

    :param servo_channel (int): The channel number of the servo on the ServoKit.
    :param min_angle (int): Minimum allowable angle for the servo.
    :param max_angle (int): Maximum allowable angle for the servo.
    :param deviation (int): Offset to apply to the servo's normal position.
    """
    def __init__(self, servo_channel: int, min_angle: int, max_angle: int, deviation: int) -> None:
        if not 0 <= servo_channel <= config.servo_channel_count - 1:
            raise ValueError(f"Servo channel must be between 0 and {config.servo_channel_count - 1}!")
        if config.servo_default_steps <= 0:
            raise ValueError("config.servo_default_steps must be greater than zero!")

        self.servo: Servo = servo_kit[servo_channel]
        self.min_angle: int = min_angle
        self.max_angle: int = max_angle
        self.deviation: int = deviation
        self.normal_position: int = config.servo_normal_position + deviation
        self.calculation_angle: float = self.normal_position
        self.lock: threading.Lock = threading.Lock()

    def move(self, target_angle: int, duration: float) -> threading.Thread:
        """
        Moves the servo to a target angle over a specified duration.

        :param target_angle (int): The target angle to move the servo to.
        :param duration (float): Time in seconds to complete the movement.
        :return (threading.Thread): The thread executing the movement.
        :raises ValueError: If the target angle is outside the valid range.
        """
        if not self.min_angle <= target_angle <= self.max_angle:
            raise ValueError(f"Target angle {target_angle} is out of range [{self.min_angle}, {self.max_angle}]")
        
        adjusted_target: int = target_angle + self.deviation
        step_difference: float = (adjusted_target - self.calculation_angle) / config.servo_default_steps

        def move_to_target() -> None:
            with self.lock:
                while abs(adjusted_target - self.calculation_angle) >= config.servo_stopping_treshhold:
                    self.calculation_angle += step_difference
                    self.servo.angle = round(self.calculation_angle)
                    time.sleep(duration / config.servo_default_steps)
                self.calculation_angle = target_angle
                self.servo.angle = self.calculation_angle
        
        moving_thread: threading.Thread = threading.Thread(target=move_to_target, daemon=True)
        moving_thread.start()
        return moving_thread

    def move_to_normal(self, duration_s: float) -> threading.Thread:
        """
        Moves the servo to its normal (default) position.

        :return (threading.Thread): The thread executing the movement.
        """
        return self.move(config.servo_normal_position, duration_s)

    def get_servo_angle(self) -> int:
        """
        Retrieves the current angle of the servo.

        :return (int): The current angle of the servo.
        """
        return self.servo.angle


class Leg:
    """
    Manages a robotic leg composed of three servos: thigh, lower leg, and side axis.

    :param leg_configurations (dict[str, dict[str, Any]]): Configuration for the leg's channels, angles, and deviations.
    """
    def __init__(self, leg_configurations: dict[str, dict[str, Any]]) -> None:
        self.required_keys: dict[str, set[str]] = {
            "channels":   {"thigh", "lower_leg", "side_axis"},
            "angles":     {"min_thigh", "max_thigh", "min_lower_leg", "max_lower_leg", "min_side_axis", "max_side_axis"},
            "deviations": {"thigh", "lower_leg", "side_axis"},
        }
        _validate_dict(self.required_keys, leg_configurations)

        self.thigh: ServoManager = ServoManager(
            servo_channel=leg_configurations["channels"]["thigh"],
            min_angle=leg_configurations["angles"]["min_thigh"],
            max_angle=leg_configurations["angles"]["max_thigh"],
            deviation=leg_configurations["deviations"]["thigh"],
        )
        self.lower_leg: ServoManager = ServoManager(
            servo_channel=leg_configurations["channels"]["lower_leg"],
            min_angle=leg_configurations["angles"]["min_lower_leg"],
            max_angle=leg_configurations["angles"]["max_lower_leg"],
            deviation=leg_configurations["deviations"]["lower_leg"],
        )
        self.side_axis: ServoManager = ServoManager(
            servo_channel=leg_configurations["channels"]["side_axis"],
            min_angle=leg_configurations["angles"]["min_side_axis"],
            max_angle=leg_configurations["angles"]["max_side_axis"],
            deviation=leg_configurations["deviations"]["side_axis"],
        )

    def move_to_normal_position(self, duration_s: float = config.servo_default_normalize_speed) -> None:
        """
        Moves all servos in the leg to their normal (default) positions. (Default = servo_default_normalize_speed)

        :return (None): This function does not return a value.
        """
        thigh_thread: threading.Thread = self.thigh.move_to_normal(duration_s)
        lower_leg_thread: threading.Thread = self.lower_leg.move_to_normal(duration_s)
        side_axis_thread: threading.Thread = self.side_axis.move_to_normal(duration_s)

        for thread in [thigh_thread, lower_leg_thread, side_axis_thread]:
            try:
                thread.join()
            except Exception as e:
                print(f"Error in thread: {e}")
