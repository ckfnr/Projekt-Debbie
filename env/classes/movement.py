import os
import time
import threading
from typing import Callable, Literal

# Func
from env.classes.leg import Leg
from env.func.DEBUG import dprint

# Classes
from env.classes.leg import SServo
from env.classes.mmt_parser import Parser
from env.classes.Classes import Coordinate
from env.classes.db import DB
from env.classes.events import StopEvent

# Decorators
from env.decr.decorators import validate_types

# Config
from env.config import config

#NOTE: Debbie has to be able to interrupted while doing it's step

class Movement:
    def __init__(self) -> None:
        # Initialize parser
        self.parser = Parser()
        
        # Initialize database
        self.db = DB()

        # Initialize stop event to stop leg movements if new key has been pressed
        self.stop_event = StopEvent()

        # Initialize all servos
        self.leg_right_front: Leg = Leg(leg_configurations=config.leg_configuration_rf, leg="rf", stop_event = self.stop_event)
        self.leg_right_back : Leg = Leg(leg_configurations=config.leg_configuration_rb, leg="rb", stop_event = self.stop_event)
        self.leg_left_front : Leg = Leg(leg_configurations=config.leg_configuration_lf, leg="lf", stop_event = self.stop_event)
        self.leg_left_back  : Leg = Leg(leg_configurations=config.leg_configuration_lb, leg="lb", stop_event = self.stop_event)

        # Define a tuple for easier access to all legs and servos at once
        self.all_legs: tuple[Leg, Leg, Leg, Leg] = (self.leg_right_front, self.leg_right_back, self.leg_left_front, self.leg_left_back)
        self.all_servos: tuple[SServo, ...] = tuple(servo for leg in self.all_legs for servo in leg.get_servos())

        # Define legs for parser
        self.parser_legs: dict[str, Leg] = {
            "rf": self.leg_right_front,
            "rb": self.leg_right_back,
            "lf": self.leg_left_front,
            "lb": self.leg_left_back
        }

        self.function_map: dict[str, Callable] = {
            # Steps
            "step-forwards" : lambda: self.make_step(direction="step-forward"),
            "step-backwards": lambda: self.make_step(direction="step-backward"),
            "sidestep-left" : lambda: self.make_step(direction="sidestep-left"),
            "sidestep-right": lambda: self.make_step(direction="sidestep-right"),

            # Normalize
            "normal"        : lambda: self.normalize_all_legs(duration_s=0.3),
            "turn-left"     : lambda: self.turn(direction="turn-left"),
            "turn-right"    : lambda: self.turn(direction="turn-right"),
        }

        dprint(f"{config.color_yellow}[ NOTE ] All functions of the movement class will be created as soon as the coordinate systems can be used.{config.color_reset}")

    @validate_types
    def set_all_legs(self, coordinate: Coordinate, duration: float) -> None:
        for leg in self.all_legs:
            leg.set_to_coordinate(coordinate=coordinate, duration_s=duration)

    def start_all_legs(self) -> None:
        """Starts all leg movements."""
        for leg in self.all_legs: leg.start()

    def join_all_legs(self) -> None:
        """Wait for all legs to finish."""
        for leg in self.all_legs: leg.join()

    def interrupt_movements(self) -> None:
        """Interrupts all movements."""
        self.stop_event.set()

        self.join_all_legs()
        self.stop_event.reset()

    #? Maybe remove this function (Doesn't make sense)
    @validate_types
    def normalize_all_legs(self, duration_s: float = config.servo_default_normalize_speed) -> None:
        """Normalize all legs to their normal position."""
        dprint("Moving servos to normal position...")

        # Set normalposition for all legs
        for leg in self.all_legs:
            leg.set_to_normal_position(duration_s=duration_s)

        self.start_all_legs()
        self.join_all_legs()

        dprint("Normalized all legs!")

    #? Maybe remove this function (Doesn't make sense)
    @validate_types
    def execute_mmt(self, mmt_name: str) -> None:
        """Execute a movement from the movement manager table (mmt)."""
        #! Has to be changed
        #? Why
        #? Maybe better parsing?
        for instruction in self.parser.get_instructions(os.path.join(config.mmt_default_path, f"{mmt_name}.mmt")):
            if not instruction: continue
            for leg, coord in instruction.items():
                # Pass duration
                if leg == "duration": continue

                # Move to coordinate
                self.parser_legs[leg].set_to_coordinate(coordinate=coord, duration_s=instruction["duration"])

    @validate_types
    def parse_folder(self, folder_path: str) -> None: self.parser.parse_files(file_paths=[file for file in os.listdir(folder_path) if file.endswith(".mmt") and os.path.isfile(file) and not "test" in file.lower() and not file.startswith(".")])


    # * Step functions
    @validate_types
    def _make_step(self, step_width: float, angles: dict[Literal["left-front", "left-back", "right-front", "right-back"], int], duration: float) -> None:
        duration_single: float = duration / 2

        self.leg_right_front.set_to_normal_position(duration_s=duration_single)
        self.leg_left_back.set_to_normal_position(duration_s=duration_single)
        self.leg_left_front.set_circle(step_width=step_width, angle=angles["left-front"], max_points=config.max_points, duration=duration_single)
        self.leg_right_back.set_circle(step_width=step_width, angle=angles["right-back"], max_points=config.max_points, duration=duration_single)

        self.leg_right_front.start()
        self.leg_left_back.start()
        self.leg_left_front.start_circle()
        self.leg_right_back.start_circle()

        self.leg_left_front.join_circle()
        self.leg_right_back.join_circle()
        self.leg_right_front.join()
        self.leg_left_back.join()


        self.leg_left_front.set_to_normal_position(duration_s=duration_single)
        self.leg_right_back.set_to_normal_position(duration_s=duration_single)
        self.leg_right_front.set_circle(step_width=step_width, angle=angles["right-front"], max_points=config.max_points, duration=duration_single)
        self.leg_left_back.set_circle(step_width=step_width, angle=angles["left-back"], max_points=config.max_points, duration=duration_single)

        self.leg_left_front.start()
        self.leg_right_back.start()
        self.leg_right_front.start_circle()
        self.leg_left_back.start_circle()

        self.leg_right_front.join_circle()
        self.leg_left_back.join_circle()
        self.leg_left_front.join()
        self.leg_right_back.join()

    def make_step(self, direction: Literal["step-forward", "step-backward", "sidestep-right", "sidestep-left"], step_width: float = config.step_width, duration: float = config.duration) -> None:
        """Make a step in the given direction."""
        assert direction in ["step-forward", "step-backward", "sidestep-right", "sidestep-left"], f"Direction {direction} is not valid. Use 'forward', 'backward', 'right' or 'left'."
        angles: dict[Literal["left-front", "left-back", "right-front", "right-back"], int] = config.step_map_angles[direction]
        self._make_step(step_width=step_width, angles=angles, duration=duration)

    def turn(self, direction: Literal["turn-left", "turn-right"], step_width: float = config.step_width, duration: float = config.duration) -> None:
        """Turns the robot in the given direction."""
        assert direction in ["turn-left", "turn-right"], f"Direction {direction} is not valid. Use 'left' or 'right'."
        angles: dict[Literal["left-front", "left-back", "right-front", "right-back"], int] = config.step_map_angles[direction]
        self._make_step(step_width=step_width, angles=angles, duration=duration)

    #? Maybe remove this function (Too complicated to implement)
    @validate_types
    def climb_stair(self, *, stair_height_cm: float, stair_width_cm: float, stair_count: int, duration_s: float) -> None:
        raise NotImplementedError("This function is not implemented yet!")

    @validate_types
    def adjust_height_body(self, *, distance_mm: float, duration_s: float) -> None:
        for leg in self.all_legs:
            current_coordinate: Coordinate = leg.get_current_position()
            current_coordinate.add_z(value=distance_mm)
            leg.set_to_coordinate(coordinate=current_coordinate, duration_s=duration_s)
