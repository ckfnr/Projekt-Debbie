import time
from env.func.movement import Movement

movement: Movement = Movement()

# Simple test (leg right front)
while True:
    rf_ll = movement.leg_right_front.lower_leg.move(target_angle=80, duration=2)   # Set the angle of the lower_leg servo to 50 degrees (duration = 2 seconds)
    rb_ll = movement.leg_right_back.lower_leg.move(target_angle=80, duration=2)
    lf_ll = movement.leg_left_front.lower_leg.move(target_angle=80, duration=2)
    lb_ll = movement.leg_left_back.lower_leg.move(target_angle=80, duration=2)

    for thread in [rf_ll, rb_ll, lf_ll, lb_ll]:
        thread.join()

    rf_ll = movement.leg_right_front.lower_leg.move(target_angle=130, duration=2)  # Set the angle of the lower_leg servo to 90 degrees (duration = 2 seconds)
    rb_ll = movement.leg_right_back.lower_leg.move(target_angle=130, duration=2)
    lf_ll = movement.leg_left_front.lower_leg.move(target_angle=130, duration=2)
    lb_ll = movement.leg_left_back.lower_leg.move(target_angle=130, duration=2)

    for thread in [rf_ll, rb_ll, lf_ll, rb_ll]:
        thread.join()

