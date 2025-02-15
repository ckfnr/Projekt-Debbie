import time
from threading import Thread, Lock
from adafruit_servokit import ServoKit, Servo  # type:ignore[import-untyped]
from typing import Any, Optional

# Classes
from env.classes.Classes import Coordinate

# Decorators
from env.decr.decorators import cached

# Func
from env.func.DEBUG import dprint
from env.func.calculations import calc_servo_angles
from env.func.leg_helper import initialize_servos, adjust_angle, validate_dict

# Config
from env.config import config

# Errors
from env.err.Errors import NoThreadError

# Initialize servo kit
try:
    servo_kit: ServoKit = ServoKit(channels=config.servo_channel_count)
    initialize_servos(servo_kit=servo_kit)  # Safe initialization of servos
except Exception as e:
    raise RuntimeError(f"Failed to initialize ServoKit: {e}")

class SServo:
    """
    Manages a single servo's movement and state.

    :param servo_channel (int): The channel number of the servo on the ServoKit.
    :param min_angle (int): Minimum allowable angle for the servo.
    :param max_angle (int): Maximum allowable angle for the servo.
    :param deviation (int): Offset to apply to the servo's normal position.
    """
    def __init__(self, *, servo_channel: int, min_angle: int, max_angle: int, deviation: int, leg: str, mirrored: bool, servo_type: str) -> None:
        # raise ProgrammingError("There is still an issue in this code! Disabled functionality for savety!")

        # Check if all values are valid
        if not 0 <= servo_channel <= config.servo_channel_count - 1:
            raise ValueError(f"Servo channel must be between or equal to 0 and {config.servo_channel_count - 1}!")
        elif not servo_type in ["thigh", "lower_leg", "side_axis"]:
            raise ValueError(f"Servo type must be one of the following: 'thigh', 'lower_leg', 'side_axis'!")

        self.servo: Servo = servo_kit.servo[servo_channel]
        self.servo_channel: int = servo_channel
        self.deviation: int = deviation
        self.min_angle: int = min_angle + deviation
        self.max_angle: int = max_angle + deviation
        self.adjusted_normal_position: int = config.servo_normal_position + deviation
        self.calculation_angle: float = self.adjusted_normal_position
        self.mirrored: bool = mirrored
        self.lock: Lock = Lock()
        self.servo_thread: Optional[Thread] = None
        self.leg: str = leg
        self.servo_type: str = servo_type

    def set(self, target_angle: int, duration: float, nm_action: bool = False) -> None:
        """
        Moves the servo to a target angle over a specified duration.

        :param target_angle (int): The target angle to start the servo to.
        :param duration (float): Time in seconds to complete the movement.
        :param nm_action (bool): Flag indicating if this is a 'start to normal' action with fixed steps.
        :raises ValueError: If the target angle is outside the valid range.
        """
        #! This function has to be changed as soon as the controller is being used
        # Adjust target angle for mirroring and deviation
        adjusted_target = adjust_angle(is_mirrored=self.mirrored, max_angle=self.max_angle, min_angle=self.min_angle, angle=target_angle, deviation=self.deviation)

        # Check if the the servo has already reached its target
        if self.servo.angle == target_angle:
            time.sleep(duration)

        # Validate the adjusted target angle
        if not self.min_angle <= adjusted_target <= self.max_angle:
            raise ValueError(f"Adjusted target angle {adjusted_target} is out of range [{self.min_angle} - {self.max_angle}]")

        # Determine steps and step difference
        current_angle = self.servo.angle if self.servo.angle is not None else self.adjusted_normal_position
        steps = 50 if nm_action else max(1, abs(int(adjusted_target - current_angle)))
        step_difference = (adjusted_target - current_angle) / steps

        # Debug logging
        dprint(f"Leg: {self.leg}, Servo: {self.servo_type}, Target: {target_angle}, Adjusted Target: {adjusted_target}, Current Angle: {current_angle}, Steps: {steps}, Step Difference: {step_difference:.2f}")

        def move_to_target() -> None:
            nonlocal current_angle
            with self.lock:
                if duration == 0:
                    self.servo.angle = adjusted_target

                while abs(adjusted_target - current_angle) > config.servo_stopping_treshhold:
                    next_angle = current_angle + step_difference
                    if not self.min_angle <= round(next_angle, 0) <= self.max_angle:
                        dprint(f"WARNING: Next angle {next_angle} out of range [{self.min_angle} - {self.max_angle}]")
                        break

                    current_angle = next_angle
                    self.servo.angle = round(current_angle)
                    time.sleep(duration / steps)
                
                # Final adjustment to ensure we reach the exact target
                self.servo.angle = adjusted_target

        # Create and start the movement thread
        self.servo_thread = Thread(target=move_to_target, daemon=True)

    def start(self) -> None:
        if not self.servo_thread:
            raise NoThreadError(f"There was no thread to set servos ({self.leg = }, {self.servo_type = }) with servo channel '{self.servo_channel}'!")

        self.servo_thread.start()

    def join(self) -> None:
        """
        Joins the servo thread.
        """
        if not self.servo_thread:
            raise NoThreadError(f"There was no thread to join at servo ({self.leg = }, {self.servo_type = }) with servo channel '{self.servo_channel}'!")

        self.servo_thread.join()
        self.servo_thread = None

    def set_to_normal(self, duration_s: float) -> None: self.set((self.adjusted_normal_position - self.deviation), duration_s, nm_action=True)
    def get_servo_angle(self) -> int:                   return self.servo.angle

class Leg:
    """
    Manages a robotic leg composed of three servos: thigh, lower leg, and side axis.

    :param leg_configurations (dict[str, dict[str, Any]]): Configuration for the leg's channels, angle variations, and deviations.
    """
    def __init__(self, *, leg_configurations: dict[str, dict[str, Any]], leg: str) -> None:
        self.required_keys: dict[str, set[str]] = {
            "channels":   {"thigh", "lower_leg", "side_axis"},
            "angles":     {"min_thigh", "max_thigh", "min_lower_leg", "max_lower_leg", "min_side_axis", "max_side_axis"},
            "deviations": {"thigh", "lower_leg", "side_axis"},
            "mirrored":   {"thigh", "lower_leg", "side_axis"},
        }
        validate_dict(self.required_keys, leg_configurations)

        if not leg in ["rf", "lf", "rb", "lb"]:
            raise ValueError(f"Invalid leg: {leg}. Must be one of 'rf', 'lf', 'rb', 'lb'.")

        self.thigh: SServo = SServo(
            servo_channel = leg_configurations["channels"]["thigh"],
            min_angle =     leg_configurations["angles"]["min_thigh"],
            max_angle =     leg_configurations["angles"]["max_thigh"],
            deviation =     leg_configurations["deviations"]["thigh"],
            mirrored =      leg_configurations["mirrored"]["thigh"],
            leg =           leg,
            servo_type =    "thigh",
        )
        self.lower_leg: SServo = SServo(
            servo_channel = leg_configurations["channels"]["lower_leg"],
            min_angle =     leg_configurations["angles"]["min_lower_leg"],
            max_angle =     leg_configurations["angles"]["max_lower_leg"],
            deviation =     leg_configurations["deviations"]["lower_leg"],
            mirrored =      leg_configurations["mirrored"]["lower_leg"],
            leg =           leg,
            servo_type =    "lower_leg",
        )
        self.side_axis: SServo = SServo(
            servo_channel = leg_configurations["channels"]["side_axis"],
            min_angle =     leg_configurations["angles"]["min_side_axis"],
            max_angle =     leg_configurations["angles"]["max_side_axis"],
            deviation =     leg_configurations["deviations"]["side_axis"],
            mirrored =      leg_configurations["mirrored"]["side_axis"],
            leg =           leg,
            servo_type =    "side_axis",
        )
        self.current_position: Coordinate = Coordinate(0, 0, 0)  # Initialize current position to (0, 0, 0) --> Default position
        self.all_servos: tuple[SServo, SServo, SServo] = (self.thigh, self.lower_leg, self.side_axis)

    @cached
    def get_servos(self) -> tuple[SServo, SServo, SServo]:
        """Returns a tuple of the three ServoManagers in the leg."""
        return self.all_servos

    def get_current_position(self) -> Coordinate:
        return self.current_position

    def set_to_normal_position(self, duration_s: float = config.servo_default_normalize_speed) -> None:
        """
        Moves all servos in the leg to their normal (default) positions. Waits until all servos have finished. (Default = servo_default_normalize_speed)

        :return (None): This function does not return a value.
        """
        self.thigh.set_to_normal(duration_s)
        self.lower_leg.set_to_normal(duration_s)
        self.side_axis.set_to_normal(duration_s)

    def set_to_coordinate(self, coordinate: Coordinate, duration_s: float) -> None:
        """
        Moves all servos in the leg to the specified position. Waits until all servos have finished. (Default = servo_default_speed)
        
        :param coordinate: The position to move to.
        :return (None): This function does not return a value.
        """
        thigh_angle, lower_leg_angle, side_axis_angle = calc_servo_angles(coordinate=coordinate)
        self.thigh.set(target_angle=thigh_angle, duration=duration_s)
        self.lower_leg.set(target_angle=lower_leg_angle, duration=duration_s)
        self.side_axis.set(target_angle=side_axis_angle, duration=duration_s)

    def start(self) -> None:
        for servo in self.get_servos():
            servo.start()

    def join(self) -> None:
        for servo in self.get_servos():
            servo.join()
