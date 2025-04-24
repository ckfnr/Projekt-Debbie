from time import sleep

# Classes
from env.classes.movement import Movement

# Config
from env.config import config

def startup_script(mvmnt: Movement) -> None:
    """Startup behavior."""
    # Sleep for a moment to ensure I2C devices are ready
    sleep(2)

    mvmnt.normalize_all_legs()
