import time
import threading
from adafruit_servokit import ServoKit, Servo  # type:ignore[import-untyped]
from typing import Any, Optional

# Config
from env.config import config

# Errors
from env.func.Errors import NoThreadError

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
    # Check all keys
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
    def __init__(self, *, servo_channel: int, min_angle: int, max_angle: int, deviation: int, mirrored: bool) -> None:
        # Check if all values are valid
        if not 0 <= servo_channel <= config.servo_channel_count - 1:
            raise ValueError(f"Servo channel must be between or equal to 0 and {config.servo_channel_count - 1}!")

        self.servo: Servo = servo_kit.servo[servo_channel]
        self.servo_channel: int = servo_channel
        self.min_angle: int = min_angle + (self.deviation if self.mirrored else -self.deviation)
        self.max_angle: int = max_angle + (self.deviation if self.mirrored else -self.deviation)
        self.deviation: int = deviation
        self.normal_position: int = config.servo_normal_position + deviation
        self.calculation_angle: float = self.normal_position
        self.mirrored: bool = mirrored
        self.lock: threading.Lock = threading.Lock()
        self.servo_thread: Optional[threading.Thread] = None

    def move(self, target_angle: int, duration: float, nm_action: bool = False) -> None:
        """
        Moves the servo to a target angle over a specified duration.

        :param target_angle (int): The target angle to move the servo to.
        :param duration (float): Time in seconds to complete the movement.
        :return (threading.Thread): The thread executing the movement.
        :raises ValueError: If the target angle is outside the valid range.
        """
        # Adjust target angle and calculate the step difference
        adjusted_target: int = ((2*self.normal_position - target_angle) if self.mirrored else (target_angle)) + (self.deviation if self.mirrored else -self.deviation)
        steps: int

        # Debug logging
        print(f"Target Angle: {target_angle}, Adjusted Target: {adjusted_target}, Min Angle: {self.min_angle}, Max Angle: {self.max_angle}")

        # Define steps
        if nm_action:
            steps = 50
        else:
            steps = abs(target_angle - self.servo.angle)

        step_difference: float = (adjusted_target - self.calculation_angle) / steps

        # Check if angle is valid
        if not self.min_angle <= adjusted_target <= self.max_angle:
            raise ValueError(f"Adjusted target angle {adjusted_target} is out of range [{self.min_angle} - {self.max_angle}]")

        def move_to_target() -> None:
            valid_angle: bool = True
            with self.lock:
                while abs(adjusted_target - self.calculation_angle) >= config.servo_stopping_treshhold:
                    if not self.min_angle <= self.calculation_angle + step_difference <= self.max_angle:
                        print(f"WARNING: Angle {self.calculation_angle + step_difference} not in range of [{self.min_angle} - {self.max_angle}]! Breaking out of loop...")
                        valid_angle = False
                        break
                    self.calculation_angle += step_difference
                    self.servo.angle = round(self.calculation_angle)
                    time.sleep(duration / steps)
                # Move to target angle
                if valid_angle:
                    self.calculation_angle = adjusted_target
                    self.servo.angle = self.calculation_angle
                valid_angle = True

        moving_thread: threading.Thread = threading.Thread(target=move_to_target, daemon=True)
        moving_thread.start()
        self.servo_thread = moving_thread

    def move_to_normal(self, duration_s: float) -> None:
        """
        Moves the servo to its normal (default) position.

        :return (threading.Thread): The thread executing the movement.
        """
        self.move(self.normal_position, duration_s, nm_action=True)

    def get_servo_angle(self) -> int:
        """
        Retrieves the current angle of the servo.

        :return (int): The current angle of the servo.
        """
        return self.servo.angle
    
    def join(self) -> None:
        """
        Joins the servo thread.
        """
        if not self.servo_thread:
            raise NoThreadError(f"There was no thread to join at servo with servo channel '{self.servo_channel}'!")

        self.servo_thread.join()

class Leg:
    """
    Manages a robotic leg composed of three servos: thigh, lower leg, and side axis.

    :param leg_configurations (dict[str, dict[str, Any]]): Configuration for the leg's channels, angle variations, and deviations.
    """
    def __init__(self, *, leg_configurations: dict[str, dict[str, Any]]) -> None:
        self.required_keys: dict[str, set[str]] = {
            "channels":   {"thigh", "lower_leg", "side_axis"},
            "angles":     {"min_thigh", "max_thigh", "min_lower_leg", "max_lower_leg", "min_side_axis", "max_side_axis"},
            "deviations": {"thigh", "lower_leg", "side_axis"},
            "mirrored":   {"thigh", "lower_leg", "side_axis"},
        }
        _validate_dict(self.required_keys, leg_configurations)

        self.thigh: ServoManager = ServoManager(
            servo_channel = leg_configurations["channels"]["thigh"],
            min_angle =     leg_configurations["angles"]["min_thigh"],
            max_angle =     leg_configurations["angles"]["max_thigh"],
            deviation =     leg_configurations["deviations"]["thigh"],
            mirrored=       leg_configurations["mirrored"]["thigh"],
        )
        self.lower_leg: ServoManager = ServoManager(
            servo_channel = leg_configurations["channels"]["lower_leg"],
            min_angle =     leg_configurations["angles"]["min_lower_leg"],
            max_angle =     leg_configurations["angles"]["max_lower_leg"],
            deviation =     leg_configurations["deviations"]["lower_leg"],
            mirrored=       leg_configurations["mirrored"]["lower_leg"],
        )
        self.side_axis: ServoManager = ServoManager(
            servo_channel = leg_configurations["channels"]["side_axis"],
            min_angle =     leg_configurations["angles"]["min_side_axis"],
            max_angle =     leg_configurations["angles"]["max_side_axis"],
            deviation =     leg_configurations["deviations"]["side_axis"],
            mirrored=       leg_configurations["mirrored"]["side_axis"],
        )

    def _move_to_nm_position(self, duration_s: float) -> None:
        self.thigh.move_to_normal(duration_s)
        self.lower_leg.move_to_normal(duration_s)
        self.side_axis.move_to_normal(duration_s)

    def move_to_normal_position(self, duration_s: float = config.servo_default_normalize_speed, wait: bool = False) -> None:
        """
        Moves all servos in the leg to their normal (default) positions. Waits until all servos have finished. (Default = servo_default_normalize_speed)

        :return (None): This function does not return a value.
        """
        self._move_to_nm_position(duration_s)

        if not wait:
            return

        for servo in [self.thigh, self.lower_leg, self.side_axis]:
            servo.join()

    def get_servos(self) -> tuple[ServoManager, ServoManager, ServoManager]:
        """Returns a tuple of the three ServoManagers in the leg."""
        return self.thigh, self.lower_leg, self.side_axis
