import time
from env.func.movement import Movement

movement: Movement = Movement()

# Simple test (leg right front)
while True:
    movement.leg_right_front.lower_leg.move(target_angle=50, duration=2)  # Set the angle of the lower_leg servo to 50 degrees (duration = 2 seconds)
    time.sleep(2)
    movement.leg_right_front.lower_leg.move(target_angle=90, duration=2)  # Set the angle of the lower_leg servo to 90 degrees (duration = 2 seconds)
    time.sleep(2)
