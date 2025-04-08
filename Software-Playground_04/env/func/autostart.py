from time import sleep

# Classes
from env.classes.movement import Movement

# Config
from env.config import config

def startup_script(mvmnt: Movement) -> None:
    """Startup behavior."""
    d: float = 1
    # Sleep for a moment to ensure I2C devices are ready
    sleep(2) 

    # Autostart section
    if config.auto_parse_startup:
        mvmnt.parse_folder(config.mmt_default_path)

    # Set legs
    for leg in mvmnt.all_legs:
        leg.thigh.set_angle(target_angle=30, duration=d)
        leg.lower_leg.set_angle(target_angle=-10, duration=d)

    # Start legs
    mvmnt.start_all_legs()

    # Wait for all legs to finish their movement
    mvmnt.join_all_legs()

    mvmnt.normalize_all_legs()
