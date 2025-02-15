# Func
from env.func.legs import Leg
from env.func.DEBUG import dprint

# Classes
from env.func.legs import SServo

# Config
from env.config import config

class Movement:
    def __init__(self) -> None:
        # Initialize all servos
        self.leg_right_front: Leg = Leg(leg_configurations=config.leg_configuration_rf, leg="rf")
        self.leg_right_back: Leg = Leg(leg_configurations=config.leg_configuration_rb,  leg="rb")
        self.leg_left_front: Leg = Leg(leg_configurations=config.leg_configuration_lf,  leg="lf")
        self.leg_left_back: Leg = Leg(leg_configurations=config.leg_configuration_lb,   leg="lb")

        # Define a tuple for easier access to all legs and servos at once
        self.all_legs: tuple[Leg, Leg, Leg, Leg] = (self.leg_right_front, self.leg_right_back, self.leg_left_front, self.leg_left_back)
        self.all_servos: tuple[SServo, ...] = tuple(servo for leg in self.all_legs for servo in leg.get_servos())

        dprint(f"{config.color_yellow}NOTE: All functions of the movement class will be created as soon as the coordinate system can be used.{config.color_reset}")

    def normalize_all_legs(self, duration_s: float = config.servo_default_normalize_speed) -> None:
        #! This function has to be updated as soon as the coordinate system can be used

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

    def walk_forward(self, *, distance_cm: float, duration_s: float) -> None:
        raise NotImplementedError("This function is not implemented yet!")

    def walk_sideways(self, *, distance_cm: float, duration_s: float) -> None:
        raise NotImplementedError("This function is not implemented yet!")

    def walk_backward(self, *, distance_cm: float, duration_s: float) -> None:
        raise NotImplementedError("This function is not implemented yet!")

    def turn_around(self, *, angle: float, duration_s: float) -> None:
        raise NotImplementedError("This function is not implemented yet!")

    def climb_stair(self, *, stair_height_cm: float, stair_width_cm: float, stair_count: int, duration_s: float) -> None:
        raise NotImplementedError("This function is not implemented yet!")

    def lift_body(self, *, floor_distance_cm: float, duration_s: float) -> None:
        raise NotImplementedError("This function is not implemented yet!")
