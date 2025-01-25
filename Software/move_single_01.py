from env.func.movement import Movement

m = Movement()
d: int = 1

def _get_value(input_string: str) -> int:
    """Extract the value from the input string."""
    return int(input_string.split("=")[1].strip())

# Map input prefixes to corresponding leg and servo attributes
servo_map = {
    "rf_t": m.leg_right_front.thigh,
    "rf_l": m.leg_right_front.lower_leg,
    "rf_s": m.leg_right_front.side_axis,
    "lf_t": m.leg_left_front.thigh,
    "lf_l": m.leg_left_front.lower_leg,
    "lf_s": m.leg_left_front.side_axis,
    "rb_t": m.leg_right_back.thigh,
    "rb_l": m.leg_right_back.lower_leg,
    "rb_s": m.leg_right_back.side_axis,
    "lb_t": m.leg_left_back.thigh,
    "lb_l": m.leg_left_back.lower_leg,
    "lb_s": m.leg_left_back.side_axis,
}

# Normalize all legs at startup
m.normalize_all_legs()

while True:
    servo_input: str = input("Enter a value (e.g. 'rf_s = 6') OR 'nm' to normalize all legs. > ").strip()

    if servo_input == "nm":
        m.normalize_all_legs()
    else:
        prefix = servo_input.split("=")[0].strip()  # Extract the prefix
        if prefix in servo_map:
            servo_map[prefix].move(target_angle=_get_value(servo_input), duration=d)
            servo_map[prefix].join()
        else:
            print("Invalid input. Please enter a valid servo input (e.g. 'rf_s = 6')!")
