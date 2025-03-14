from time import sleep

# Classes
from env.classes.movement import Movement
from env.classes.controller import Controller

# Config
from env.config import config

def startup_script(mvmnt: Movement) -> None:
    """Startup behavior."""
    d: float = 1
    # Sleep for a moment to ensure I2C devices are ready
    sleep(2)  # Adjust this based on your system's boot time

    # Autostart section
    if config.auto_parse_startup:
        mvmnt.parse_folder(config.mmt_default_path)

    # Set legs
    for leg in mvmnt.all_legs:
        leg.thigh.set(target_angle=120, duration=d)
        leg.lower_leg.set(target_angle=80, duration=d)

    # Start legs
    for leg in mvmnt.all_legs:
        leg.thigh.start()
        leg.lower_leg.start()

    # Wait for all legs to finish their movement
    for leg in mvmnt.all_legs:
        leg.thigh.join()
        leg.lower_leg.join()

    mvmnt.normalize_all_legs()

def main() -> None:
    """Main function."""
    # Create a Movement and Controller objects
    mvmnt = Movement()
    ctrllr = Controller()

    # Execute startup script
    startup_script(mvmnt=mvmnt)

if __name__ == "__main__": main()
