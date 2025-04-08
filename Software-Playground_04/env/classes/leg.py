from typing import Any, Literal

# Classes
from env.classes.Classes import Coordinate
from env.classes.servos import SServo
from env.classes.events import StopEvent

# Decorators
from env.decr.decorators import cached, validate_types

# Func
from env.func.calculations import calc_servo_angles, calc_circle_coordinates
from env.func.DEBUG import dprint

# Config
from env.config import config

class Leg:
    """
    Manages a robotic leg composed of three servos: thigh, lower leg, and side axis.

    :param leg_configurations (dict[str, dict[str, Any]]): Configuration for the leg's channels, angle variations, and deviations.
    """
    # @validate_types
    def __init__(self, *, leg_configurations: dict[str, dict[str, Any]], leg: str, stop_event: StopEvent) -> None:
        self.required_keys: dict[str, set[str]] = {
            "channels":   {"thigh", "lower_leg", "side_axis"},
            "deviations": {"thigh", "lower_leg", "side_axis"},
            "mirrored":   {"thigh", "lower_leg", "side_axis"},
            "angles":     {"min_thigh", "max_thigh", "min_lower_leg", "max_lower_leg", "min_side_axis", "max_side_axis"},
        }
        self.leg: str = leg
        
        # Initialize stop event
        self._stop_event: StopEvent = stop_event

        # Check if the provided leg is valid
        if not leg in ["rf", "lf", "rb", "lb"]: raise ValueError(f"Invalid leg: {leg}. Must be one of 'rf', 'lf', 'rb', 'lb'.")

        # Initialize servos
        self.thigh: SServo = SServo(
            servo_channel = leg_configurations["channels"]["thigh"],
            min_angle =     leg_configurations["angles"]["min_thigh"],
            max_angle =     leg_configurations["angles"]["max_thigh"],
            deviation =     leg_configurations["deviations"]["thigh"],
            mirrored =      leg_configurations["mirrored"]["thigh"],
            leg =           leg,
            servo_type =    "thigh",
            stop_event =    self._stop_event,
        )
        self.lower_leg: SServo = SServo(
            servo_channel = leg_configurations["channels"]["lower_leg"],
            min_angle =     leg_configurations["angles"]["min_lower_leg"],
            max_angle =     leg_configurations["angles"]["max_lower_leg"],
            deviation =     leg_configurations["deviations"]["lower_leg"],
            mirrored =      leg_configurations["mirrored"]["lower_leg"],
            leg =           leg,
            servo_type =    "lower_leg",
            stop_event =    self._stop_event,
        )
        self.side_axis: SServo = SServo(
            servo_channel = leg_configurations["channels"]["side_axis"],
            min_angle =     leg_configurations["angles"]["min_side_axis"],
            max_angle =     leg_configurations["angles"]["max_side_axis"],
            deviation =     leg_configurations["deviations"]["side_axis"],
            mirrored =      leg_configurations["mirrored"]["side_axis"],
            leg =           leg,
            servo_type =    "side_axis",
            stop_event =    self._stop_event,
        )
        self.current_position: Coordinate = Coordinate(0.0, 0.0, 0.0)  # Initialize current position to (0, 0, 0) --> Default position
        self.all_servos: tuple[SServo, SServo, SServo] = (self.thigh, self.lower_leg, self.side_axis)

    @cached
    def get_servos(self) -> tuple[SServo, SServo, SServo]:
        """Returns a tuple of the three ServoManagers in the leg."""
        return self.all_servos

    def get_current_position(self) -> Coordinate: return self.current_position

    @validate_types
    def set_to_normal_position(self, duration_s: float = config.servo_default_normalize_speed) -> None:
        """
        Moves all servos in the leg to their normal positions (0°). Waits until all servos have finished. (Default = servo_default_normalize_speed)

        :return (None): This function does not return a value.
        """
        self.thigh.set_to_normal(duration_s)
        self.lower_leg.set_to_normal(duration_s)
        self.side_axis.set_to_normal(duration_s)

    @validate_types
    def set_to_coordinate(self, coordinate: Coordinate, duration_s: float) -> None:
        """
        Moves all servos in the leg to the specified position. Waits until all servos have finished. (Default = servo_default_speed)
        
        :param coordinate: The position to move to.
        :param duration_s: The duration of the movement in seconds.
        :return (None): This function does not return a value.
        """
        angles: dict[Literal['thigh', 'lower-leg', 'side-axis'], int] = calc_servo_angles(coordinate=coordinate)
        dprint(f"Leg {self}: Moving to position {coordinate} with angles {angles}")
        self.thigh.set_angle(target_angle=angles["thigh"], duration=duration_s)
        self.lower_leg.set_angle(target_angle=angles["lower-leg"], duration=duration_s)
        self.side_axis.set_angle(target_angle=angles["side-axis"], duration=duration_s)

    def start(self) -> None:
        for servo in self.all_servos:
            servo.start()

    def join(self) -> None:
        for servo in self.all_servos:
            servo.join()

    def interrupt(self) -> None:
        for servo in self.all_servos:
            servo.interrupt()
