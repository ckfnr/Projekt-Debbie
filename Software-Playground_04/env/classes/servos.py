import time
from threading import Thread, Lock, Event
from adafruit_servokit import ServoKit, Servo  # type:ignore[import-untyped]
from typing import Optional
import board  # type:ignore[import-untyped]
import busio  # type:ignore[import-untyped]

# Decorators
from env.decr.decorators import validate_types

# Func
from env.func.DEBUG import dprint
from env.func.leg_helper import initialize_servos, adjust_angle
from env.func.servos_helper import add_until_limit

# Classes
from env.classes.events import StopEvent
from env.classes.Classes import ServoWrapper

# Config
from env.config import config

# Errors
from env.err.Errors import NoThreadError

# Initialize servo kit
try:
    # Create an I2C instance
    i2c = busio.I2C(board.SCL, board.SDA)
    servo_kit: ServoKit = ServoKit(channels=config.servo_channel_count)

    # Initialize the ServoKit with the I2C bus
    kit = ServoKit(channels=16, i2c=i2c)
    
    initialize_servos(servo_kit=servo_kit)  # Safe initialization of servos
except Exception as e:
    dprint(f"Failed to initialize ServoKit. Returing to default position. Error: {e}")

class SServo:
    """
    Manages a single servo's movement and state.

    :param servo_channel (int): The channel number of the servo on the ServoKit.
    :param min_angle (int): Minimum allowable angle for the servo.
    :param max_angle (int): Maximum allowable angle for the servo.
    :param deviation (int): Offset to apply to the servo's normal position.
    """
    @validate_types
    def __init__(self,
                 *,
                 servo_channel: int,
                 min_angle: int,
                 max_angle: int,
                 deviation: int,
                 leg: str,
                 mirrored: bool,
                 servo_type: str,
                 stop_event: StopEvent
        ) -> None:
        # raise ProgrammingError("There is still an issue in this code! Disabled functionality for savety!")

        # Check if all values are valid
        if not 0 <= servo_channel <= config.servo_channel_count - 1: raise ValueError(f"Servo channel must be between or equal to 0 and {config.servo_channel_count - 1}!")
        elif not servo_type in ["thigh", "lower_leg", "side_axis"]:  raise ValueError(f"Servo type must be one of the following: 'thigh', 'lower_leg', 'side_axis'!")

        # Initialize threading
        self.lock: Lock = Lock()
        self._stop_event: StopEvent = stop_event

        # Initialize servo
        self.servo: Servo =                   servo_kit.servo[servo_channel]
        self.servo_wrapper: ServoWrapper =    ServoWrapper(servo=self.servo)  # Create a ServoWrapper instance to fix the bug that servo.angle is None sometimes (hardware issue); We call it "Pfusch"
        self.servo_channel: int =             servo_channel
        self.deviation: int =                 deviation
        self.min_angle: int =                 min_angle + deviation
        self.max_angle: int =                 max_angle + deviation
        self.adjusted_normal_position: int =  config.servo_normal_position + deviation
        self.calculation_angle: float =       self.adjusted_normal_position
        self.mirrored: bool =                 mirrored
        self.servo_thread: Optional[Thread] = None
        self.leg: str =                       leg
        self.servo_type: str =                servo_type
        self.start_time: Optional[float] =    None

    @validate_types
    def set_angle(self, target_angle: int, duration: float, nm_action: bool = False) -> None:
        """
        Moves the servo to a target angle over a specified duration.

        :param target_angle (int): The target angle to start the servo to.
        :param duration (float): Time in seconds to complete the movement.
        :param nm_action (bool): Flag indicating if this is a 'start to normal' action with fixed steps.
        :raises ValueError: If the target angle is outside the valid range.
        """
        #ToDo: Change this function as soon as the controller is being used

        # Adjust target angle for mirroring and deviation
        adjusted_target: int = adjust_angle(is_mirrored=self.mirrored, max_angle=self.max_angle, min_angle=self.min_angle, angle=target_angle, deviation=self.deviation)

        # Validate the adjusted target angle
        if not (self.min_angle <= adjusted_target <= self.max_angle): raise ValueError(f"Servo ({self.leg}:{self.servo_type}): Adjusted target angle {adjusted_target} is out of range [{self.min_angle} - {self.max_angle}]")

        # Determine steps and step difference
        current_angle =   self.servo_wrapper.angle if self.servo_wrapper.angle is not None else self.adjusted_normal_position
        steps =           50 if nm_action else max(1, abs(int(adjusted_target - current_angle)))
        step_difference = (adjusted_target - current_angle) // steps  # Calculate the step difference

        # Debug logging
        dprint(f"Leg: {self.leg}, Servo: {self.servo_type}, Target: {target_angle}, Adjusted Target: {adjusted_target}, Current Angle: {current_angle}, Steps: {steps}, Step Difference: {step_difference:.2f}")

        def move_to_target() -> None:
            nonlocal current_angle

            # Check if the the servo has already reached its target; If so, just wait
            if current_angle == adjusted_target:
                time.sleep(duration)
                return

            with self.lock:
                # If duration == 0, just set the servo angle to the adjusted angle
                if duration == 0:
                    self.servo_wrapper.angle = adjusted_target
                    return

                start_time = time.time()
                for step in range(steps):
                    # Break out of the loop if the stop event has been set
                    if self._stop_event.is_set(): return

                    # Calculate the exact time this step *should* occur
                    target_time = start_time + (step + 1) * (duration / steps)

                    # Get new angle and validate it
                    next_angle = max(self.min_angle, min(self.max_angle, add_until_limit(start=current_angle, increment=step_difference, limit=adjusted_target)))
                    if not self.min_angle <= round(next_angle, 0) <= self.max_angle:
                        dprint(f"WARNING: Current servo angle at servo ({self.leg}:{self.servo_type}): {self.servo_wrapper.angle}; next angle {next_angle} out of range [{self.min_angle} - {self.max_angle}]")
                        break

                    # Set servo to new angle and wait
                    current_angle = next_angle
                    self.servo_wrapper.angle = round(current_angle)

                    # Wait until the exact time for the next step
                    time.sleep(max(0, target_time - time.time()))

                # Final adjustment if the servo movement hasn't been interrupted to ensure we reach the exact target
                self.servo_wrapper.angle = adjusted_target

        # Interrupt running threads
        self.interrupt()
        self._stop_event.reset()

        # Create the new movement thread
        self.start_time = time.time()
        self.servo_thread = Thread(target=move_to_target, daemon=True)
        dprint(f"Created servo thread for leg {self.leg} and servo {self.servo_type}")

    def start(self) -> None:
        """Starts the servo movement."""
        if not self.servo_thread:
            raise NoThreadError(f"There was no thread to set_angle servos (leg={self.leg}, servo_type={self.servo_type}) with servo channel '{self.servo_channel}'!")

        self.servo_thread.start()

    def join(self) -> None:
        """Joins the servo thread."""
        # Check if there is an existing thread to join
        if not self.servo_thread: dprint(f"{config.color_yellow}[ WARNING ] There was no thread to join at servo ({self.leg = }, {self.servo_type = }) with servo channel '{self.servo_channel}'!{config.color_reset}"); return

        self.servo_thread.join()  # Wait for servo to finish its movement
        self.servo_thread = None  # Clear servo thread

        if not self.start_time: return  # No movement started
        dprint(f"✅ Finished movement of servo ({self.leg}:{self.servo_type}) with servo channel '{self.servo_channel}' took {(time.time() - self.start_time):.2f} seconds")
        self.start_time = None

    def clear_thread(self) -> None:
        """Clears the servo thread."""
        if self.servo_thread: self.servo_thread = None

    def interrupt(self) -> None:
        """Interrupts the servo movement if it is running."""
        # Check if a thread exists to interrupt
        if not self.servo_thread or not self.servo_thread.is_alive(): return

        dprint(f"Servo (leg={self.leg}, servo_type={self.servo_type}) has been interrupted!")
        self._stop_event.set()
        self.join()

    @validate_types
    def set_to_normal(self, duration_s: float) -> None: self.set_angle((self.adjusted_normal_position - self.deviation), duration_s, nm_action=True)
    def get_servo_angle(self) -> int: return self.servo_wrapper.angle
