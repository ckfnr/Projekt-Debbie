
# Func
from env.func.legs import Leg
from env.func.movement import Movement
from env.func.DEBUG import dprint

m = Movement()
d: float = 0.5

# Normalize all legs at startup
m.normalize_all_legs()

all_legs: list[Leg] = [m.leg_left_back, m.leg_left_front, m.leg_right_back, m.leg_right_front]

def main() -> None:
    while True:
        # Lie down
        for leg in all_legs:
            leg.thigh.set(target_angle=120, duration=d)
            leg.lower_leg.set(target_angle=80, duration=d)
        # Start threads
        for leg in all_legs:
            leg.thigh.start()
        # Join all threads
        for leg in all_legs:
            leg.thigh.join()

        # Stand up
        for leg in all_legs:
            leg.thigh.set(target_angle=90, duration=d)
            leg.lower_leg.set(target_angle=90, duration=d)
        # Start threads
        for leg in all_legs:
            leg.thigh.start()
        # Join all threads
        for leg in all_legs:
            leg.thigh.join()

        dprint("Done!")

if __name__ == "__main__": main()
