from env.classes.controller import Controller
from env.classes.movement import Movement
from env.classes.Classes import Coordinate

def main() -> None:
    c = Controller()
    m = Movement()
    c.get_input()

if __name__ == "__main__": main()
