import time
from env.func.servos import ServoRightFront, ServoRightBack, ServoLeftFront, ServoLeftBack

# Config
from env.config import config

class Movement:
    def __init__(self) -> None:
        # Initialize all servos
        self.servo_right_front: ServoRightFront = ServoRightFront()
        self.servo_right_back: ServoRightBack = ServoRightBack()
        self.servo_left_front: ServoLeftFront = ServoLeftFront()
        self.servo_left_back: ServoLeftBack = ServoLeftBack()

        self.all_servos: tuple[ServoRightFront, ServoRightBack, ServoLeftFront, ServoLeftBack] = (self.servo_right_front, self.servo_right_back, self.servo_left_front, self.servo_left_back)
    
    def normalize_servos(self) -> None:
        print("Moving servos to normal position...")
        for servo in self.all_servos:
            servo.move_to_normal_position(duration_s=config.servo_normalize_speed)
        time.sleep(config.servo_normalize_speed)
        print("Done!")

    def walk_forward(self, *, distance_cm: float, duration_s: float) -> None:
        raise NotImplementedError("This function is not implemented yet!")
    
    def walk_sideways(self, *, distance_cm: float, duration_s: float) -> None:
        raise NotImplementedError("This function is not implemented yet!")
    
    def walk_back(self, *, distance_cm: float, duration_s: float) -> None:
        raise NotImplementedError("This function is not implemented yet!")
    
    def turn_around(self, *, angle: float, duration_s: float) -> None:
        raise NotImplementedError("This function is not implemented yet!")
    
    def climb_stair(self, *, stair_height_cm: float, stair_width_cm: float, stair_count: int, duration_s: float) -> None:
        raise NotImplementedError("This function is not implemented yet!")
