from env.func.movement import Movement

def main() -> None:
    m = Movement()

    m.leg_right_front.thigh.set_straight(angle=95)
