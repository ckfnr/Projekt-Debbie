import os

# Func
from env.classes.leg import Leg
from env.func.DEBUG import dprint

# Classes
from env.classes.leg import SServo
from env.classes.mmt_parser import Parser

# Decorators
from env.decr.decorators import validate_types_class, validate_types

# Config
from env.config import config

class Movement:
    @validate_types
    def __init__(self) -> None:
        # Initialize parser
        self.parser = Parser()

        # Initialize all servos
        self.leg_right_front: Leg = Leg(leg_configurations=config.leg_configuration_rf, leg="rf")
        self.leg_right_back: Leg =  Leg(leg_configurations=config.leg_configuration_rb, leg="rb")
        self.leg_left_front: Leg =  Leg(leg_configurations=config.leg_configuration_lf, leg="lf")
        self.leg_left_back: Leg =   Leg(leg_configurations=config.leg_configuration_lb, leg="lb")

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

        dprint(f"{config.color_yellow}[ NOTE ] All functions of the movement class will be created as soon as the coordinate systems can be used.{config.color_reset}")

    @validate_types
    def normalize_all_legs(self, duration_s: float = config.servo_default_normalize_speed) -> None:
        #! This function has to be updated as soon as the coordinate systems can be used

        all_servos: list[SServo] = []
        dprint("Moving servos to normal position...")

        # Set normalposition for all legs
        for leg in self.all_legs:
            leg.set_to_normal_position(duration_s=duration_s)
            all_servos.extend(leg.get_servos())

        # Move
        for servo in all_servos:
            servo.start()

        # Wait for all servos to finish
        for servo in self.all_servos:
            servo.join()

        dprint("Done!")

    @validate_types
    def execute(self, mmt: str) -> None:
        #! Has to be changed
        for instruction in self.parser.get_instructions(os.path.join(config.mmt_default_path, f"{mmt}.mmt")):
            for leg, coord in instruction.keys():
                # Pass duration
                if leg == "duration": continue

                # Move to coordinate
                self.parser_legs[leg].set_to_coordinate(coordinate=coord, duration_s=instruction["duration"])

    @validate_types
    def parse_folder(self, folder_path: str) -> None:
        mmt_files: list[str] = [file for file in os.listdir(folder_path) if file.endswith(".mmt") and os.path.isfile(file) and not "test" in file.lower() and not file.startswith(".")]
        self.parser.parse_files(file_paths=mmt_files)

    @validate_types
    def walk_forward(self, *, distance_cm: float, duration_s: float) -> None:
        raise NotImplementedError("This function is not implemented yet!")

    @validate_types
    def walk_sideways(self, *, distance_cm: float, duration_s: float) -> None:
        raise NotImplementedError("This function is not implemented yet!")

    @validate_types
    def walk_backward(self, *, distance_cm: float, duration_s: float) -> None:
        raise NotImplementedError("This function is not implemented yet!")

    @validate_types
    def turn_around(self, *, angle: float, duration_s: float) -> None:
        raise NotImplementedError("This function is not implemented yet!")

    @validate_types
    def climb_stair(self, *, stair_height_cm: float, stair_width_cm: float, stair_count: int, duration_s: float) -> None:
        raise NotImplementedError("This function is not implemented yet!")

    @validate_types
    def lift_body(self, *, floor_distance_cm: float, duration_s: float) -> None:
        raise NotImplementedError("This function is not implemented yet!")
