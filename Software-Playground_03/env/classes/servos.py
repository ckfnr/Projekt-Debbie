import time
from threading import Thread, Lock
from adafruit_servokit import ServoKit, Servo  # type:ignore[import-untyped]
from typing import Any, Optional

# Decorators
from env.decr.decorators import validate_types

# Func
from env.func.DEBUG import dprint
from env.func.leg_helper import initialize_servos, adjust_angle

# Config
from env.config import config

# Errors
from env.err.Errors import NoThreadError, ThreadAlreadySetError

# Initialize servo kit
try:
    servo_kit: ServoKit = ServoKit(channels=config.servo_channel_count)
    initialize_servos(servo_kit=servo_kit)  # Safe initialization of servos
except Exception as e:
    raise RuntimeError(f"Failed to initialize ServoKit: {e}")

class SServo:
    """
    Manages a single servo's movement and state.

    :param servo_channel (int): The channel number of the servo on the ServoKit.
    :param min_angle (int): Minimum allowable angle for the servo.
    :param max_angle (int): Maximum allowable angle for the servo.
    :param deviation (int): Offset to apply to the servo's normal position.
    """
    @validate_types
    def __init__(self, *, servo_channel: int, min_angle: int, max_angle: int, deviation: int, leg: str, mirrored: bool, servo_type: str) -> None:
        # raise ProgrammingError("There is still an issue in this code! Disabled functionality for savety!")

        # Check if all values are valid
        if not 0 <= servo_channel <= config.servo_channel_count - 1:
            raise ValueError(f"Servo channel must be between or equal to 0 and {config.servo_channel_count - 1}!")
        elif not servo_type in ["thigh", "lower_leg", "side_axis"]:
            raise ValueError(f"Servo type must be one of the following: 'thigh', 'lower_leg', 'side_axis'!")

        self.servo: Servo = servo_kit.servo[servo_channel]
        self.servo_channel: int = servo_channel
        self.deviation: int = deviation
        self.min_angle: int = min_angle + deviation
        self.max_angle: int = max_angle + deviation
        self.adjusted_normal_position: int = config.servo_normal_position + deviation
        self.calculation_angle: float = self.adjusted_normal_position
        self.mirrored: bool = mirrored
        self.lock: Lock = Lock()
        self.servo_thread: Optional[Thread] = None
        self.leg: str = leg
        self.servo_type: str = servo_type

    @validate_types
    def set(self, target_angle: int, duration: float, nm_action: bool = False) -> None:
        """
        Moves the servo to a target angle over a specified duration.

        :param target_angle (int): The target angle to start the servo to.
        :param duration (float): Time in seconds to complete the movement.
        :param nm_action (bool): Flag indicating if this is a 'start to normal' action with fixed steps.
        :raises ValueError: If the target angle is outside the valid range.
        """
        #ToDo: Change this function as soon as the controller is being used
        # Check if a task already exists
        if self.servo_thread:
            raise ThreadAlreadySetError(f"You have already called set for the servo '{self.leg} : {self.servo_type}'. Don't call it twice!")

        # Adjust target angle for mirroring and deviation
        adjusted_target = adjust_angle(is_mirrored=self.mirrored, max_angle=self.max_angle, min_angle=self.min_angle, angle=target_angle, deviation=self.deviation)

        # Check if the the servo has already reached its target
        if self.servo.angle == target_angle:
            time.sleep(duration)

        # Validate the adjusted target angle
        if not self.min_angle <= adjusted_target <= self.max_angle:
            raise ValueError(f"Adjusted target angle {adjusted_target} is out of range [{self.min_angle} - {self.max_angle}]")

        # Determine steps and step difference
        current_angle = self.servo.angle if self.servo.angle is not None else self.adjusted_normal_position
        steps = 50 if nm_action else max(1, abs(int(adjusted_target - current_angle)))
        step_difference = (adjusted_target - current_angle) / steps

        # Debug logging
        dprint(f"Leg: {self.leg}, Servo: {self.servo_type}, Target: {target_angle}, Adjusted Target: {adjusted_target}, Current Angle: {current_angle}, Steps: {steps}, Step Difference: {step_difference:.2f}")

        def move_to_target() -> None:
            nonlocal current_angle
            with self.lock:
                # If duration == 0, just set the servo angle to the adjusted angle
                if duration == 0:
                    self.servo.angle = adjusted_target
                    return

                while abs(adjusted_target - current_angle) > config.servo_stopping_treshhold:
                    next_angle = current_angle + step_difference
                    if not self.min_angle <= round(next_angle, 0) <= self.max_angle:
                        dprint(f"WARNING: Next angle {next_angle} out of range [{self.min_angle} - {self.max_angle}]")
                        break

                    current_angle = next_angle
                    self.servo.angle = round(current_angle)
                    time.sleep(duration / steps)
                
                # Final adjustment to ensure we reach the exact target
                self.servo.angle = adjusted_target

        # Create and start the movement thread
        self.servo_thread = Thread(target=move_to_target, daemon=True)

    def start(self) -> None:
        if not self.servo_thread:
            raise NoThreadError(f"There was no thread to set servos ({self.leg = }, {self.servo_type = }) with servo channel '{self.servo_channel}'!")

        self.servo_thread.start()

    def join(self) -> None:
        """
        Joins the servo thread.
        """
        if not self.servo_thread:
            raise NoThreadError(f"There was no thread to join at servo ({self.leg = }, {self.servo_type = }) with servo channel '{self.servo_channel}'!")

        self.servo_thread.join()
        self.servo_thread = None

    @validate_types
    def set_to_normal(self, duration_s: float) -> None: self.set((self.adjusted_normal_position - self.deviation), duration_s, nm_action=True)
    def get_servo_angle(self) -> int: return self.servo.angle
