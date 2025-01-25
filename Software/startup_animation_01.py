from env.func.servos import Leg
from env.func.movement import Movement

m = Movement()
d: int = 2

# Normalize all legs at startup
m.normalize_all_legs()

all_legs: list[Leg] = [m.leg_left_back, m.leg_left_front, m.leg_right_back, m.leg_right_front]

def main() -> None:
    while True:
        # Lie down
        for leg in all_legs:
            leg.thigh.move(target_angle=120, duration=d)
            leg.lower_leg.move(target_angle=80, duration=d)
        # Join all threads
        for leg in all_legs:
            leg.thigh.join()

        # Stand up
        for leg in all_legs:
            leg.thigh.move(target_angle=40, duration=d)
            leg.lower_leg.move(target_angle=120, duration=d)
        # Join all threads
        for leg in all_legs:
            leg.thigh.join()

        print("Done!")

if __name__ == "__main__": main()
