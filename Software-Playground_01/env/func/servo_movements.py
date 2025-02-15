import time
from threading import Lock, Thread
from typing import Optional
from adafruit_servokit import Servo, ServoKit  # type:ignore[import-untyped]

# Func
from env.func.DEBUG import dprint

# Config
from env.config import config

# Errors
from env.func.Errors import NoThreadError

# Classes
from env.func.Classes import AngleInt, AngleFloat

class ServoMaster:
    def __init__(
            self,
            mirrored: bool,
            deviation: int,
            max_angle: int,
            min_angle: int,
            leg: str,
            servo_type: str,
            lock: Lock,
            servo_channel: int,
            servo_kit: ServoKit,
            ) -> None:
        self.servo: Servo = servo_kit.servo[servo_channel]
        self.servo_channel: int = servo_channel
        self.deviation: int = deviation
        self.min_angle: AngleInt = AngleInt(angle=min_angle, deviation=deviation)
        self.max_angle: AngleInt = AngleInt(angle=max_angle, deviation=deviation)
        self.adjusted_normal_position: AngleInt = AngleInt(angle=config.servo_normal_position, deviation=deviation)
        self.calculation_angle: AngleFloat = self.adjusted_normal_position.conv_to_anglefloat()
        self.mirrored: bool = mirrored
        self.lock: Lock = lock
        self.servo_thread: Optional[Thread] = None
        self.leg: str = leg
        self.servo_type: str = servo_type
        self.range: tuple[int, int] = (0, self.servo.actuation_range)

class MStraightLine(ServoMaster):
    def __init__(
                self,
                mirrored: bool,
                deviation: int,
                max_angle: int,
                min_angle: int,
                leg: str,
                servo_type: str,
                lock: Lock,
                servo_channel: int,
                servo_kit: ServoKit,
            ) -> None:
        # Initialize master class
        super().__init__(mirrored=mirrored, deviation=deviation, max_angle=max_angle, min_angle=min_angle, leg=leg, servo_type=servo_type, lock=lock, servo_channel=servo_channel, servo_kit=servo_kit)

    def set(self, target_angle: int, duration: float, nm_action: bool = False) -> None:
        """
        Moves the servo to a target angle over a specified duration.

        :param target_angle (int): The target angle to start the servo to.
        :param duration (float): Time in seconds to complete the movement.
        :param nm_action (bool): Flag indicating if this is a 'start to normal' action with fixed steps.
        :raises ValueError: If the target angle is outside the valid range.
        """
        #! This function has to be changed as soon as the controller is being used
        #ToDo: Fix bugs
        with self.lock:
            self.target_angle: AngleInt = AngleInt(angle=target_angle, deviation=self.deviation)
            adjusted_target: AngleInt

            # Check if the the servo has already reached its target
            if self.servo.angle == target_angle:
                time.sleep(duration)

            # Adjust target angle for mirroring and deviation
            if self.mirrored:
                adjusted_target = self.max_angle - (self.target_angle - self.min_angle)  #? Why calc +deviation?
            else:
                # adjusted_target = target_angle + self.deviation
                adjusted_target = self.target_angle

            # Check if the adjusted target angle is in the range of the servo
            if not self.range[0] <= int(adjusted_target) <= self.range[1]:
                raise ValueError(f"Invalid angle: {int(adjusted_target)}. Servo supports angles between {self.range[0]} and {self.range[1]}.")

            # Validate the adjusted target angle
            if not self.min_angle <= adjusted_target <= self.max_angle:
                raise ValueError(f"Invalid angle: {adjusted_target}. Allowed range is from {self.min_angle} to {self.max_angle}.")

            # Determine steps and step difference
            current_angle = self.servo.angle if self.servo.angle is not None else self.adjusted_normal_position
            steps = 50 if nm_action else max(1, abs(int(adjusted_target - current_angle)))
            step_difference = int(adjusted_target - current_angle) / steps

            # Debug logging
            dprint(f"Leg: {self.leg}, Servo: {self.servo_type}, Target: {target_angle}, Adjusted Target: {adjusted_target}, Current AngleInt: {current_angle}, Steps: {steps}, Step Difference: {step_difference:.2f}")

            def move_to_target() -> None:
                nonlocal current_angle
                # next_angle: AngleFloat

                # If there is no duration, just set the final target angle
                if duration == 0:
                    self.servo.angle = adjusted_target
                    return

                # Move to the final target angle within the provided time
                while abs(int(adjusted_target - current_angle)) > config.servo_stopping_treshhold:
                    # next_angle = current_angle + step_difference
                    next_angle: AngleFloat = current_angle.add_float(step_difference)
                    if not self.min_angle <= next_angle.round(ndigits=0) <= self.max_angle:
                        dprint(f"WARNING: Next angle {next_angle} out of range [{self.min_angle} - {self.max_angle}]")
                        break

                    current_angle = next_angle
                    # self.servo.angle = round(current_angle)
                    self.servo.angle = current_angle.round(0)
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

class MCircle:
    def __init__(self) -> None:
        raise NotImplementedError("This function is not implemented yet!")

class MStair:
    def __init__(self) -> None:
        raise NotImplementedError("This function is not implemented yet!")
