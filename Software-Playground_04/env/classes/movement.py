import os
import time
import threading
from typing import Callable

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
        self.leg_right_back: Leg =  Leg(leg_configurations=config.leg_configuration_rb, leg="rb", stop_event = self.stop_event)
        self.leg_left_front: Leg =  Leg(leg_configurations=config.leg_configuration_lf, leg="lf", stop_event = self.stop_event)
        self.leg_left_back: Leg =   Leg(leg_configurations=config.leg_configuration_lb, leg="lb", stop_event = self.stop_event)

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
            "step-forwards": self.walk_forward,
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

    @validate_types
    def normalize_all_legs(self, duration_s: float = config.servo_default_normalize_speed) -> None:
        """Normalize all legs to their normal position."""
        #! This function has to be updated as soon as the coordinate systems can be used

        all_servos: list[SServo] = []
        dprint("Moving servos to normal position...")

        # Set normalposition for all legs
        for leg in self.all_legs:
            leg.set_to_normal_position(duration_s=duration_s)
            all_servos.extend(leg.get_servos())

        # Move
        self.start_all_legs()

        # Wait for all servos to finish
        self.join_all_legs()

        dprint("Done!")

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

    #ToDo: Make function more efficient and implement controller!
    @validate_types
    def walk_forward(self) -> None:
        """Walk forward."""
        duration: float = 1.0
        circle_coordinates: list[Coordinate] = self.db.get_coordinates(step_width=5.0, angle=0)
        step_duration: float = duration / (len(circle_coordinates)/2)  # Duration between each coordinate

        def start_leg_movement(leg: Leg) -> None:
            for coordinate in circle_coordinates:
                leg.set_to_coordinate(coordinate=coordinate, duration_s=step_duration)
                leg.start()
                leg.join()
            
            leg.set_to_coordinate(coordinate=Coordinate(x=0.0, y=0.0, z=0.0), duration_s=duration/2)
            leg.start()
            leg.join()

        for leg in [self.leg_left_front, self.leg_left_back, self.leg_right_front, self.leg_right_back]:
            threading.Thread(target=lambda: start_leg_movement(leg), daemon=True).start()
            time.sleep(duration/4)

    @validate_types
    def walk_sideways(self, *, distance_cm: float, duration_s: float) -> None:
        raise NotImplementedError("This function is not implemented yet!")

    @validate_types
    def walk_backward(self, *, distance_cm: float, duration_s: float) -> None:
        raise NotImplementedError("This function is not implemented yet!")

    @validate_types
    def turn_clockwise(self, *, angle: float, duration_s: float) -> None:
        raise NotImplementedError("This function is not implemented yet!")

    #? Maybe remove this function
    @validate_types
    def climb_stair(self, *, stair_height_cm: float, stair_width_cm: float, stair_count: int, duration_s: float) -> None:
        raise NotImplementedError("This function is not implemented yet!")

    @validate_types
    def adjust_height_body(self, *, distance_mm: float, duration_s: float) -> None:
        for leg in self.all_legs:
            current_coordinate: Coordinate = leg.get_current_position()
            current_coordinate.add_z(value=distance_mm)
            leg.set_to_coordinate(coordinate=current_coordinate, duration_s=duration_s)
