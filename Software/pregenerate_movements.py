import numpy

# Classes
from env.classes.db import DB
from env.classes.calculator import Calculator
from env.classes.Classes import Coordinate

def main() -> None:
    db = DB()
    clctr = Calculator()

    clctr.pregenerate_coordinates(frm = 1.0, to=20.0, step=0.1)

    for step_width in numpy.arange(1.0, 20.1, 0.1):
        print(f"Saving coordinates for step width {step_width:.1f}...")
        for angle in range(360):
            coords: list[Coordinate] = clctr.get_coordinates(step_width=round(step_width, 1), angle=angle)
            for coord in coords:
                db.store_coordinates(step_width=round(step_width, 1), angle=angle, coord=coord)
    db.save()

    print("Done!")

if __name__ == "__main__": main()
