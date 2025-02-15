from env.classes.movement import Movement

def main() -> None:
    m = Movement()

    m.leg_right_front.thigh.set_straight(angle=95)
    m.leg_right_front.thigh.start()
    m.leg_right_front.thigh.join()
