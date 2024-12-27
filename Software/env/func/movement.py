import time
from env.func.servos import Leg

# Config
from env.config import config

class Movement:
    def __init__(self) -> None:
        # Initialize all servos
        self.leg_right_front: Leg = Leg(config.leg_configuration_rf)
        self.leg_right_back: Leg = Leg(config.leg_configuration_rb)
        self.leg_left_front: Leg = Leg(config.leg_configuration_lf)
        self.leg_left_back: Leg = Leg(config.leg_configuration_lb)

        # Define a tuple for easier access to all legs at once
        self.all_legs: tuple[Leg, Leg, Leg, Leg] = (self.leg_right_front, self.leg_right_back, self.leg_left_front, self.leg_left_back)

        # Auto normalize
        if config.auto_normalize_at_startup: self.normalize_legs()

    def normalize_legs(self, duration_s: float = config.servo_default_normalize_speed) -> None:
        print("Moving servos to normal position...")
        for leg in self.all_legs:
            leg.move_to_normal_position()
        time.sleep(duration_s)
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
