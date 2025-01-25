import time
import threading
from env.func.servos import Leg

# Classes
from env.func.servos import ServoManager

# Config
from env.config import config

class Movement:
    def __init__(self) -> None:
        # Initialize all servos
        self.leg_right_front: Leg = Leg(leg_configurations=config.leg_configuration_rf, leg="rf")
        self.leg_right_back: Leg = Leg(leg_configurations=config.leg_configuration_rb,  leg="rb")
        self.leg_left_front: Leg = Leg(leg_configurations=config.leg_configuration_lf,  leg="lf")
        self.leg_left_back: Leg = Leg(leg_configurations=config.leg_configuration_lb,   leg="lb")

        # Define a tuple for easier access to all legs at once
        self.all_legs: tuple[Leg, Leg, Leg, Leg] = (self.leg_right_front, self.leg_right_back, self.leg_left_front, self.leg_left_back)

        # Auto normalize
        if config.auto_normalize_at_startup: self.normalize_all_legs()

    def normalize_all_legs(self, duration_s: float = config.servo_default_normalize_speed) -> None:
        # leg_threads: list[threading.Thread] = []
        all_servos: list[ServoManager] = []
        print("Moving servos to normal position...")

        # # Start moving all servos to their normal position
        # for leg in self.all_legs:
        #     leg_threads.extend(i for i in leg._move_to_nm_position(duration_s))

        # # Wait for all threads to finish
        # for thread in leg_threads:
        #     thread.join()

        for leg in self.all_legs:
            leg.move_to_normal_position(duration_s=duration_s)
            all_servos.extend(leg.get_servos())
        
        # Wait for all servos to finish
        for servo in all_servos:
            servo.join()

        print("Done!")

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
