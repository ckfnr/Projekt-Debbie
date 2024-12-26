import time
import threading
from adafruit_servokit import ServoKit, Servo  # type:ignore[import-untyped]

# Config
from env.config import config

servo_kit: ServoKit = ServoKit(channels=config.servo_channel_count)

class SingleServo:
    def __init__(self, servo_channel: int) -> None:
        if not 0 <= servo_channel <= config.servo_channel_count: raise ValueError(f"Servo channel must be between or equal to 0-{config.servo_channel_count}!")
        self.single_kit: Servo = servo_kit.servo[servo_channel]

    def move(self, actual_angle: int, target_angle: int, duration: float) -> None:
        def movement(actual_angle: int, target_angle: int, duration: float) -> None:
            # Calculate steps
            step_difference: int = (target_angle - actual_angle) // config.servo_default_steps
            while target_angle > actual_angle:
                actual_angle += step_difference
                self.single_kit.angle = actual_angle
                time.sleep(duration / config.servo_default_steps)

        threading.Thread(target=movement, args=(actual_angle, target_angle, duration), daemon=True).start()

class RightFront:
    def __init__(self) -> None:
        # Calculate the normal position for these servos
        self.thigh: int =     config.servo_normal_position + config.servo_deviation_thigh_rf
        self.lower_leg: int = config.servo_normal_position + config.servo_deviation_lower_leg_rf
        self.side_axis: int = config.servo_normal_position + config.servo_deviation_side_axis_rf

        # Create servo objects
        self.servo_thigh: SingleServo = SingleServo(config.servo_channel_RFT)
        self.servo_lower_leg: SingleServo = SingleServo(config.servo_channel_RFL)
        self.servo_side_axis: SingleServo = SingleServo(config.servo_channel_RFS)

    def move_to_normal_position(self) -> None:
        self.move_thigh(config.servo_normal_position, 10)
        self.move_lower_leg(config.servo_normal_position, 10)
        self.move_side_axis(config.servo_normal_position, 10)

    def move_thigh(self, value: int, duration: float) -> None:
        if not config.min_thigh_angle_rf <= value <= config.max_thigh_angle_rf: raise ValueError(f"Value must be between or equal to {config.min_thigh_angle_rf}-{config.max_thigh_angle_rf}!")
        new_angle: int = value + config.servo_deviation_thigh_rf  # Set the new servo value
        self.servo_thigh.move(self.thigh, new_angle, duration)
        self.thigh = new_angle
    
    def move_lower_leg(self, value: int, duration: float) -> None:
        if not config.min_lower_leg_angle_rf <= value <= config.max_lower_leg_angle_rf: raise ValueError(f"Value must be between or equal to {config.min_thigh_angle_rf}-{config.max_thigh_angle_rf}!")
        new_angle: int = value + config.servo_deviation_lower_leg_rf  # Set the new servo value
        self.servo_lower_leg.move(self.lower_leg, new_angle, duration)
        self.lower_leg = new_angle
    
    def move_side_axis(self, value: int, duration: float) -> None:
        if not config.min_side_axis_angle_rf <= value <= config.max_side_axis_angle_rf: raise ValueError(f"Value must be between or equal to {config.min_thigh_angle_rf}-{config.max_thigh_angle_rf}!")
        new_angle: int = value + config.servo_deviation_side_axis_rf  # Set the new servo value
        self.servo_side_axis.move(self.side_axis, new_angle, duration)
        self.side_axis = new_angle

class RightBack:
    def __init__(self) -> None:
        # Calculate the normal position for these servos
        self.thigh: int =     config.servo_normal_position + config.servo_deviation_thigh_rb
        self.lower_leg: int = config.servo_normal_position + config.servo_deviation_lower_leg_rb
        self.side_axis: int = config.servo_normal_position + config.servo_deviation_side_axis_rb

        # Create servo objects
        self.servo_thigh: SingleServo = SingleServo(config.servo_channel_RBT)
        self.servo_lower_leg: SingleServo = SingleServo(config.servo_channel_RBL)
        self.servo_side_axis: SingleServo = SingleServo(config.servo_channel_RBS)

    def move_to_normal_position(self) -> None:
        self.move_thigh(config.servo_normal_position, 10)
        self.move_lower_leg(config.servo_normal_position, 10)
        self.move_side_axis(config.servo_normal_position, 10)

    def move_thigh(self, value: int, duration: float) -> None:
        if not config.min_thigh_angle_rb <= value <= config.max_thigh_angle_rb: raise ValueError(f"Value must be between or equal to {config.min_thigh_angle_rb}-{config.max_thigh_angle_rb}!")
        new_angle: int = value + config.servo_deviation_thigh_rb  # Set the new servo value
        self.servo_thigh.move(self.thigh, new_angle, duration)
        self.thigh = new_angle
    
    def move_lower_leg(self, value: int, duration: float) -> None:
        if not config.min_lower_leg_angle_rb <= value <= config.max_lower_leg_angle_rb: raise ValueError(f"Value must be between or equal to {config.min_thigh_angle_rb}-{config.max_thigh_angle_rb}!")
        new_angle: int = value + config.servo_deviation_lower_leg_rb  # Set the new servo value
        self.servo_lower_leg.move(self.lower_leg, new_angle, duration)
        self.lower_leg = new_angle
    
    def move_side_axis(self, value: int, duration: float) -> None:
        if not config.min_side_axis_angle_rb <= value <= config.max_side_axis_angle_rb: raise ValueError(f"Value must be between or equal to {config.min_thigh_angle_rb}-{config.max_thigh_angle_rb}!")
        new_angle: int = value + config.servo_deviation_side_axis_rb  # Set the new servo value
        self.servo_side_axis.move(self.side_axis, new_angle, duration)
        self.side_axis = new_angle

class LeftFront:
    def __init__(self) -> None:
        # Calculate the normal position for these servos
        self.thigh: int =     config.servo_normal_position + config.servo_deviation_thigh_lf
        self.lower_leg: int = config.servo_normal_position + config.servo_deviation_lower_leg_lf
        self.side_axis: int = config.servo_normal_position + config.servo_deviation_side_axis_lf

        # Create servo objects
        self.servo_thigh: SingleServo = SingleServo(config.servo_channel_LFT)
        self.servo_lower_leg: SingleServo = SingleServo(config.servo_channel_LFL)
        self.servo_side_axis: SingleServo = SingleServo(config.servo_channel_LFS)

    def move_to_normal_position(self) -> None:
        self.move_thigh(config.servo_normal_position, 10)
        self.move_lower_leg(config.servo_normal_position, 10)
        self.move_side_axis(config.servo_normal_position, 10)

    def move_thigh(self, value: int, duration: float) -> None:
        if not config.min_thigh_angle_lf <= value <= config.max_thigh_angle_lf: raise ValueError(f"Value must be between or equal to {config.min_thigh_angle_lf}-{config.max_thigh_angle_lf}!")
        new_angle: int = value + config.servo_deviation_thigh_lf  # Set the new servo value
        self.servo_thigh.move(self.thigh, new_angle, duration)
        self.thigh = new_angle
    
    def move_lower_leg(self, value: int, duration: float) -> None:
        if not config.min_lower_leg_angle_lf <= value <= config.max_lower_leg_angle_lf: raise ValueError(f"Value must be between or equal to {config.min_thigh_angle_lf}-{config.max_thigh_angle_lf}!")
        new_angle: int = value + config.servo_deviation_lower_leg_lf  # Set the new servo value
        self.servo_lower_leg.move(self.lower_leg, new_angle, duration)
        self.lower_leg = new_angle
    
    def move_side_axis(self, value: int, duration: float) -> None:
        if not config.min_side_axis_angle_lf <= value <= config.max_side_axis_angle_lf: raise ValueError(f"Value must be between or equal to {config.min_thigh_angle_lf}-{config.max_thigh_angle_lf}!")
        new_angle: int = value + config.servo_deviation_side_axis_lf  # Set the new servo value
        self.servo_side_axis.move(self.side_axis, new_angle, duration)
        self.side_axis = new_angle

class LeftBack:
    def __init__(self) -> None:
        # Calculate the normal position for these servos
        self.thigh: int =     config.servo_normal_position + config.servo_deviation_thigh_lb
        self.lower_leg: int = config.servo_normal_position + config.servo_deviation_lower_leg_lb
        self.side_axis: int = config.servo_normal_position + config.servo_deviation_side_axis_lb

        # Create servo objects
        self.servo_thigh: SingleServo = SingleServo(config.servo_channel_LBT)
        self.servo_lower_leg: SingleServo = SingleServo(config.servo_channel_LBL)
        self.servo_side_axis: SingleServo = SingleServo(config.servo_channel_LBS)

    def move_to_normal_position(self) -> None:
        self.move_thigh(config.servo_normal_position, 10)
        self.move_lower_leg(config.servo_normal_position, 10)
        self.move_side_axis(config.servo_normal_position, 10)

    def move_thigh(self, value: int, duration: float) -> None:
        if not config.min_thigh_angle_lb <= value <= config.max_thigh_angle_lb: raise ValueError(f"Value must be between or equal to {config.min_thigh_angle_lb}-{config.max_thigh_angle_lb}!")
        new_angle: int = value + config.servo_deviation_thigh_lb  # Set the new servo value
        self.servo_thigh.move(self.thigh, new_angle, duration)
        self.thigh = new_angle
    
    def move_lower_leg(self, value: int, duration: float) -> None:
        if not config.min_lower_leg_angle_lb <= value <= config.max_lower_leg_angle_lb: raise ValueError(f"Value must be between or equal to {config.min_thigh_angle_lb}-{config.max_thigh_angle_lb}!")
        new_angle: int = value + config.servo_deviation_lower_leg_lb  # Set the new servo value
        self.servo_lower_leg.move(self.lower_leg, new_angle, duration)
        self.lower_leg = new_angle
    
    def move_side_axis(self, value: int, duration: float) -> None:
        if not config.min_side_axis_angle_lb <= value <= config.max_side_axis_angle_lb: raise ValueError(f"Value must be between or equal to {config.min_thigh_angle_lb}-{config.max_thigh_angle_lb}!")
        new_angle: int = value + config.servo_deviation_side_axis_lb  # Set the new servo value
        self.servo_side_axis.move(self.side_axis, new_angle, duration)
        self.side_axis = new_angle

class Movement:
    def __init__(self) -> None:
        # Initialize all servos
        self.servo_right_front: RightFront = RightFront()
        self.servo_right_back: RightBack = RightBack()
        self.servo_left_front: LeftFront = LeftFront()
        self.servo_left_back: LeftBack = LeftBack()

        self.all_servos: tuple[RightFront, RightBack, LeftFront, LeftBack] = (self.servo_right_front, self.servo_right_back, self.servo_left_front, self.servo_left_back)
    
        # Move all servos to their normal position
        print("Moving servos to normal position...")
        for servo in self.all_servos:
            servo.move_to_normal_position()
        print("Done!")

    def walk_forward(self) -> None:
        raise NotImplementedError("This function is not implemented yet!")
    
    def walk_sideways(self) -> None:
        raise NotImplementedError("This function is not implemented yet!")
    
    def walk_back(self) -> None:
        raise NotImplementedError("This function is not implemented yet!")
    
    def turn_around(self) -> None:
        raise NotImplementedError("This function is not implemented yet!")
    
    def climb_stair(self) -> None:
        raise NotImplementedError("This function is not implemented yet!")
