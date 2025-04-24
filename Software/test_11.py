from env.classes.movement import Movement
from env.classes.servos import SServo
from env.config import config

m = Movement()

# while True: m.leg_left_front.thigh.servo_wrapper._servo.angle = int(input("Enter the new servo value: "))

while True:
    args = input(">> ").split()

    leg: str = args[0]
    value: int = int(args[1])
    operator: str|None = args[2] if len(args) > 2 else None

    legs: dict[str, SServo] = {
        "l": m.leg_left_front.lower_leg,
        "t": m.leg_left_front.thigh,
        "s": m.leg_left_front.side_axis,
    }

    if leg not in legs: print("Invalid leg!")
    match operator:
        case "-f": legs[leg].servo_wrapper.angle = int(value)
        case None: legs[leg].servo_wrapper.angle = int(value) + config.leg_configuration_lf["deviations"]["lower_leg" if leg == "l" else "thigh" if leg == "t" else "side_axis"]
        case _: print("Invalid operator. Please use '-f' for lower leg")

    print(legs[leg].servo_wrapper._servo.angle)
