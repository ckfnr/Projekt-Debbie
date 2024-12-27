# Do not use this script! It will be changed within the next 24 hours

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

    def move(self, *, actual_angle: int, target_angle: int, duration_s: float) -> None:
        def movement(actual_angle: int, target_angle: int, duration_s: float) -> None:
            # Calculate steps
            step_difference: int = (target_angle - actual_angle) // config.servo_default_steps

            # Move to target angle in steps
            if target_angle > actual_angle:
                while target_angle > actual_angle:
                    actual_angle += step_difference                      # Calculate new angle
                    self.single_kit.angle = actual_angle                 # Move to angle
                    time.sleep(duration_s / config.servo_default_steps)  # Sleep
            elif target_angle < actual_angle:
                while target_angle < actual_angle:
                    actual_angle -= step_difference                      # Calculate new angle
                    self.single_kit.angle = actual_angle                 # Move to angle
                    time.sleep(duration_s / config.servo_default_steps)  # Sleep

            # Finally move to target angle
            self.single_kit.angle = target_angle

        # Start movement in a new thread that DEBBIE is able to move multiple servos at a time
        threading.Thread(target=movement, args=(actual_angle, target_angle, duration_s), daemon=True).start()

class ServoRightFront:
    def __init__(self) -> None:
        # Calculate the normal position for these servos
        self.thigh_angle: int =     config.servo_normal_position + config.servo_deviation_thigh_rf
        self.lower_leg_angle: int = config.servo_normal_position + config.servo_deviation_lower_leg_rf
        self.side_axis_angle: int = config.servo_normal_position + config.servo_deviation_side_axis_rf

        # Create servo objects
        self.servo_thigh: SingleServo = SingleServo(config.servo_channel_RFT)
        self.servo_lower_leg: SingleServo = SingleServo(config.servo_channel_RFL)
        self.servo_side_axis: SingleServo = SingleServo(config.servo_channel_RFS)

    def move_to_normal_position(self, duration_s: float) -> None:
        self.move_thigh(value=config.servo_normal_position, duration_s=duration_s)
        self.move_lower_leg(value=config.servo_normal_position, duration_s=duration_s)
        self.move_side_axis(value=config.servo_normal_position, duration_s=duration_s)

    def move_thigh(self, value: int, duration_s: float) -> None:
        if not config.min_thigh_angle_rf <= value <= config.max_thigh_angle_rf: raise ValueError(f"Value must be between or equal to {config.min_thigh_angle_rf}-{config.max_thigh_angle_rf}!")
        new_angle: int = value + config.servo_deviation_thigh_rf  # Set the new servo value
        self.servo_thigh.move(actual_angle=self.thigh_angle, target_angle=new_angle, duration_s=duration_s)
        self.thigh_angle = new_angle
    
    def move_lower_leg(self, value: int, duration_s: float) -> None:
        if not config.min_lower_leg_angle_rf <= value <= config.max_lower_leg_angle_rf: raise ValueError(f"Value must be between or equal to {config.min_thigh_angle_rf}-{config.max_thigh_angle_rf}!")
        new_angle: int = value + config.servo_deviation_lower_leg_rf  # Set the new servo value
        self.servo_lower_leg.move(actual_angle=self.lower_leg_angle, target_angle=new_angle, duration_s=duration_s)
        self.lower_leg_angle = new_angle
    
    def move_side_axis(self, value: int, duration_s: float) -> None:
        if not config.min_side_axis_angle_rf <= value <= config.max_side_axis_angle_rf: raise ValueError(f"Value must be between or equal to {config.min_thigh_angle_rf}-{config.max_thigh_angle_rf}!")
        new_angle: int = value + config.servo_deviation_side_axis_rf  # Set the new servo value
        self.servo_side_axis.move(actual_angle=self.side_axis_angle, target_angle=new_angle, duration_s=duration_s)
        self.side_axis_angle = new_angle

class ServoRightBack:
    def __init__(self) -> None:
        # Calculate the normal position for these servos
        self.thigh_angle: int =     config.servo_normal_position + config.servo_deviation_thigh_rb
        self.lower_leg_angle: int = config.servo_normal_position + config.servo_deviation_lower_leg_rb
        self.side_axis_angle: int = config.servo_normal_position + config.servo_deviation_side_axis_rb

        # Create servo objects
        self.servo_thigh: SingleServo = SingleServo(config.servo_channel_RBT)
        self.servo_lower_leg: SingleServo = SingleServo(config.servo_channel_RBL)
        self.servo_side_axis: SingleServo = SingleServo(config.servo_channel_RBS)

    def move_to_normal_position(self, duration_s: float) -> None:
        self.move_thigh(value=config.servo_normal_position, duration_s=duration_s)
        self.move_lower_leg(value=config.servo_normal_position, duration_s=duration_s)
        self.move_side_axis(value=config.servo_normal_position, duration_s=duration_s)

    def move_thigh(self, value: int, duration_s: float) -> None:
        if not config.min_thigh_angle_rb <= value <= config.max_thigh_angle_rb: raise ValueError(f"Value must be between or equal to {config.min_thigh_angle_rb}-{config.max_thigh_angle_rb}!")
        new_angle: int = value + config.servo_deviation_thigh_rb  # Set the new servo value
        self.servo_thigh.move(actual_angle=self.thigh_angle, target_angle=new_angle, duration_s=duration_s)
        self.thigh_angle = new_angle
    
    def move_lower_leg(self, value: int, duration_s: float) -> None:
        if not config.min_lower_leg_angle_rb <= value <= config.max_lower_leg_angle_rb: raise ValueError(f"Value must be between or equal to {config.min_thigh_angle_rb}-{config.max_thigh_angle_rb}!")
        new_angle: int = value + config.servo_deviation_lower_leg_rb  # Set the new servo value
        self.servo_lower_leg.move(actual_angle=self.lower_leg_angle, target_angle=new_angle, duration_s=duration_s)
        self.lower_leg_angle = new_angle
    
    def move_side_axis(self, value: int, duration_s: float) -> None:
        if not config.min_side_axis_angle_rb <= value <= config.max_side_axis_angle_rb: raise ValueError(f"Value must be between or equal to {config.min_thigh_angle_rb}-{config.max_thigh_angle_rb}!")
        new_angle: int = value + config.servo_deviation_side_axis_rb  # Set the new servo value
        self.servo_side_axis.move(actual_angle=self.side_axis_angle, target_angle=new_angle, duration_s=duration_s)
        self.side_axis_angle = new_angle

class ServoLeftFront:
    def __init__(self) -> None:
        # Calculate the normal position for these servos
        self.thigh_angle: int =     config.servo_normal_position + config.servo_deviation_thigh_lf
        self.lower_leg_angle: int = config.servo_normal_position + config.servo_deviation_lower_leg_lf
        self.side_axis_angle: int = config.servo_normal_position + config.servo_deviation_side_axis_lf

        # Create servo objects
        self.servo_thigh: SingleServo = SingleServo(config.servo_channel_LFT)
        self.servo_lower_leg: SingleServo = SingleServo(config.servo_channel_LFL)
        self.servo_side_axis: SingleServo = SingleServo(config.servo_channel_LFS)

    def move_to_normal_position(self, duration_s: float) -> None:
        self.move_thigh(value=config.servo_normal_position, duration_s=duration_s)
        self.move_lower_leg(value=config.servo_normal_position, duration_s=duration_s)
        self.move_side_axis(value=config.servo_normal_position, duration_s=duration_s)

    def move_thigh(self, value: int, duration_s: float) -> None:
        if not config.min_thigh_angle_lf <= value <= config.max_thigh_angle_lf: raise ValueError(f"Value must be between or equal to {config.min_thigh_angle_lf}-{config.max_thigh_angle_lf}!")
        new_angle: int = value + config.servo_deviation_thigh_lf  # Set the new servo value
        self.servo_thigh.move(actual_angle=self.thigh_angle, target_angle=new_angle, duration_s=duration_s)
        self.thigh_angle = new_angle
    
    def move_lower_leg(self, value: int, duration_s: float) -> None:
        if not config.min_lower_leg_angle_lf <= value <= config.max_lower_leg_angle_lf: raise ValueError(f"Value must be between or equal to {config.min_thigh_angle_lf}-{config.max_thigh_angle_lf}!")
        new_angle: int = value + config.servo_deviation_lower_leg_lf  # Set the new servo value
        self.servo_lower_leg.move(actual_angle=self.lower_leg_angle, target_angle=new_angle, duration_s=duration_s)
        self.lower_leg_angle = new_angle
    
    def move_side_axis(self, value: int, duration_s: float) -> None:
        if not config.min_side_axis_angle_lf <= value <= config.max_side_axis_angle_lf: raise ValueError(f"Value must be between or equal to {config.min_thigh_angle_lf}-{config.max_thigh_angle_lf}!")
        new_angle: int = value + config.servo_deviation_side_axis_lf  # Set the new servo value
        self.servo_side_axis.move(actual_angle=self.side_axis_angle, target_angle=new_angle, duration_s=duration_s)
        self.side_axis_angle = new_angle

class ServoLeftBack:
    def __init__(self) -> None:
        # Calculate the normal position for these servos
        self.thigh_angle: int =     config.servo_normal_position + config.servo_deviation_thigh_lb
        self.lower_leg_angle: int = config.servo_normal_position + config.servo_deviation_lower_leg_lb
        self.side_axis_angle: int = config.servo_normal_position + config.servo_deviation_side_axis_lb

        # Create servo objects
        self.servo_thigh: SingleServo = SingleServo(config.servo_channel_LBT)
        self.servo_lower_leg: SingleServo = SingleServo(config.servo_channel_LBL)
        self.servo_side_axis: SingleServo = SingleServo(config.servo_channel_LBS)

    def move_to_normal_position(self, duration_s: float) -> None:
        self.move_thigh(value=config.servo_normal_position, duration_s=duration_s)
        self.move_lower_leg(value=config.servo_normal_position, duration_s=duration_s)
        self.move_side_axis(value=config.servo_normal_position, duration_s=duration_s)

    def move_thigh(self, value: int, duration_s: float) -> None:
        if not config.min_thigh_angle_lb <= value <= config.max_thigh_angle_lb: raise ValueError(f"Value must be between or equal to {config.min_thigh_angle_lb}-{config.max_thigh_angle_lb}!")
        new_angle: int = value + config.servo_deviation_thigh_lb  # Set the new servo value
        self.servo_thigh.move(actual_angle=self.thigh_angle, target_angle=new_angle, duration_s=duration_s)
        self.thigh_angle = new_angle
    
    def move_lower_leg(self, value: int, duration_s: float) -> None:
        if not config.min_lower_leg_angle_lb <= value <= config.max_lower_leg_angle_lb: raise ValueError(f"Value must be between or equal to {config.min_thigh_angle_lb}-{config.max_thigh_angle_lb}!")
        new_angle: int = value + config.servo_deviation_lower_leg_lb  # Set the new servo value
        self.servo_lower_leg.move(actual_angle=self.lower_leg_angle, target_angle=new_angle, duration_s=duration_s)
        self.lower_leg_angle = new_angle
    
    def move_side_axis(self, value: int, duration_s: float) -> None:
        if not config.min_side_axis_angle_lb <= value <= config.max_side_axis_angle_lb: raise ValueError(f"Value must be between or equal to {config.min_thigh_angle_lb}-{config.max_thigh_angle_lb}!")
        new_angle: int = value + config.servo_deviation_side_axis_lb  # Set the new servo value
        self.servo_side_axis.move(actual_angle=self.side_axis_angle, target_angle=new_angle, duration_s=duration_s)
        self.side_axis_angle = new_angle
