from env.func.movement import Movement

m = Movement()
d: int = 1

def _get_value(input_string: str) -> int:
    """Get the value from the input string."""
    return int(input_string.split("=")[1].strip())

while True:
    servo_input: str = input("Enter a value (e.g. 'rf_s = 6') OR 'nm' to normalize all legs. > ").strip()

    # Move to normal position
    if servo_input == "nm":
        m.normalize_all_legs()
    # Right front
    elif servo_input.startswith("rf_t"):
        m.leg_right_front.thigh.move(target_angle=_get_value(servo_input), duration=d).join()
    elif servo_input.startswith("rf_l"):
        m.leg_right_front.lower_leg.move(target_angle=_get_value(servo_input), duration=d).join()
    elif servo_input.startswith("rf_s"):
        m.leg_left_front.side_axis.move(target_angle=_get_value(servo_input), duration=d).join()
    # Left front
    elif servo_input.startswith("lf_t"):
        m.leg_left_front.thigh.move(target_angle=_get_value(servo_input), duration=d).join()
    elif servo_input.startswith("lf_l"):
        m.leg_left_front.lower_leg.move(target_angle=_get_value(servo_input), duration=d).join()
    elif servo_input.startswith("lf_s"):
        m.leg_left_front.side_axis.move(target_angle=_get_value(servo_input), duration=d).join()
    # Right back
    elif servo_input.startswith("rb_t"):
        m.leg_right_back.thigh.move(target_angle=_get_value(servo_input), duration=d).join()
    elif servo_input.startswith("rb_l"):
        m.leg_right_back.lower_leg.move(target_angle=_get_value(servo_input), duration=d).join()
    elif servo_input.startswith("rb_s"):
        m.leg_right_back.side_axis.move(target_angle=_get_value(servo_input), duration=d).join()
    # Left back
    elif servo_input.startswith("lb_t"):
        m.leg_left_back.thigh.move(target_angle=_get_value(servo_input), duration=d).join()
    elif servo_input.startswith("lb_l"):
        m.leg_left_back.lower_leg.move(target_angle=_get_value(servo_input), duration=d).join()
    elif servo_input.startswith("lb_s"):
        m.leg_left_back.side_axis.move(target_angle=_get_value(servo_input), duration=d).join()
    # If input not valid
    else:
        print("Invalid input. Please enter a valid servo input (e.g. 'rf_s = 6')!")
