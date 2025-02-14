from time import sleep
from env.func.movement import Movement

def main() -> None:
    m = Movement()
    d: float = 1

    # Sleep for a moment to ensure I2C devices are ready
    sleep(2)  # Adjust this based on your system's boot time

    # Set legs
    for leg in m.all_legs:
        leg.thigh.set(target_angle=120, duration=d)
        leg.lower_leg.set(target_angle=80, duration=d)

    # Start legs
    for leg in m.all_legs:
        leg.thigh.start()
        leg.lower_leg.start()

    # Join legs
    for leg in m.all_legs:
        leg.thigh.join()
        leg.lower_leg.join()

    m.normalize_all_legs()

if __name__ == "__main__": main()
