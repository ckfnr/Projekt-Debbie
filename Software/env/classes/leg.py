import threading
from typing import Any, Literal, Optional

# Classes
from env.classes.Classes import Coordinate
from env.classes.servos import SServo
from env.classes.events import StopEvent

# Decorators
from env.decr.decorators import cached, validate_types

# Func
from env.func.calculations import calc_servo_angles, calc_circle_coordinates
from env.func.DEBUG import dprint

# Errors
from env.err.Errors import NoThreadError

# Config
from env.config import config

# Typing
from env.types.typing import LegConfigDict

class Leg:
    """
    Manages a robotic leg composed of three servos: thigh, lower leg, and side axis.

    :param leg_configurations (dict[str, dict[str, Any]]): Configuration for the leg's channels, angle variations, and deviations.
    """
    # @validate_types
    def __init__(self, *, leg_configurations: LegConfigDict, leg: str, stop_event: StopEvent) -> None:
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
        self.circle_thread: Optional[threading.Thread] = None

    @cached
    def get_servos(self) -> tuple[SServo, SServo, SServo]:
        """Returns a tuple of the three ServoManagers in the leg."""
        return self.all_servos

    def get_current_position(self) -> Coordinate:
        return self.current_position

    @validate_types
    def set_to_normal_position(self, duration_s: float = config.servo_default_normalize_speed) -> None:
        """
        Moves all servos in the leg to their normal positions (0°). Waits until all servos have finished. (Default = servo_default_normalize_speed)

        :return (None): This function does not return a value.
        """
        self.set_to_coordinate(coordinate=Coordinate(x=0.0, y=0.0, z=0.0), duration_s=duration_s)

    @validate_types
    def set_to_coordinate(self, coordinate: Coordinate, duration_s: float) -> None:
        """
        Moves all servos in the leg to the specified position. Waits until all servos have finished. (Default = servo_default_speed)
        
        :param coordinate: The position to move to.
        :param duration_s: The duration of the movement in seconds.
        :return (None): This function does not return a value.
        """
        adjusted_coordinate: Coordinate = coordinate * config.coord_multiplier  # Adjust coordinate to the servo coordinate system
        angles: dict[Literal['thigh', 'lower-leg', 'side-axis'], int] = calc_servo_angles(coordinate=adjusted_coordinate)
        dprint(f"Leg {self}: Moving to position {coordinate} with angles {angles}")
        self.thigh.set_angle(target_angle=angles["thigh"], duration=duration_s)
        self.lower_leg.set_angle(target_angle=angles["lower-leg"], duration=duration_s)
        self.side_axis.set_angle(target_angle=angles["side-axis"], duration=duration_s)
        
        # Set current position to the new position
        self.current_position = coordinate

    @validate_types
    def set_circle(self, step_width: float, angle: int, max_points: int, duration: float) -> None:
        """Sets the leg to move in a circular path.

        Args:
            step_width(float): Step width for each coordinate calculation.
            angle(int): Angle of the circle in degrees.
            max_points(int): Maximum number of points to generate for the circle.
            duration(float): Total duration of the circular motion in seconds.

        Returns:
            None: No return value.

        Raises:
            ValueError: If any of the input parameters are invalid.
            Exception: If an error occurs during thread execution.
        """
        coords: list[Coordinate] = calc_circle_coordinates(step_width=step_width, angle=angle, max_points=max_points)
        motion_time: float = duration / max_points

        def execute() -> None:
            for coord in coords:
                # Break out of loop if the stop event has been set
                if self._stop_event.is_set(): break

                self.set_to_coordinate(coordinate=coord-Coordinate(x=coord.x/2, y=0.0, z=0.0), duration_s=motion_time)
                self.start()
                self.join()
                
                # Set current position to the new position
                self.current_position = coord

        self.circle_thread = threading.Thread(target=execute)

    def start_circle(self) -> None:
        """Starts the circle thread.

        Args:
            self(Circle): Instance of the Circle class.

        Returns:
            None: No return value.

        Raises:
            NoThreadError: Raised if no circle thread is set.
        """
        if self.circle_thread == None: raise NoThreadError("No circle thread set!")
        self.circle_thread.start()

    def join_circle(self) -> None:
        if self.circle_thread == None: raise NoThreadError("No circle thread set!")
        self.circle_thread.join()

    def start(self) -> None:
        for servo in self.all_servos:
            servo.start()

    def join(self) -> None:
        for servo in self.all_servos:
            servo.join()

    def interrupt(self) -> None:
        for servo in self.all_servos:
            servo.interrupt()
