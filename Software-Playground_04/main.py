# Classes
from env.classes.movement import Movement
from env.classes.controller import Controller

# Func
from env.func.DEBUG import dprint
from env.func.autostart import startup_script

# Config
from env.config import config

def main() -> None:
    """Main function."""
    dprint(f"{config.color_yellow}Developer mode on!{config.color_reset}")

    # # Create a Movement and Controller objects
    # mvmnt = Movement()
    # ctrllr = Controller()  #ToDo: Implement controller

    # # Execute startup script
    # startup_script(mvmnt=mvmnt)

    ctrllr = Controller()
    mvmnt = Movement()

if __name__ == "__main__": main()
