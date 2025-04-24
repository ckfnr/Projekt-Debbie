# from env.func.calculations import _calc_circle_coordinate

# print(_calc_circle_coordinate(step_width=1.0, angle=1, point=25, max_points=50, circle_multiplier=-0.5))

from env.classes.calculator import Calculator
from env.classes.Classes import Coordinate

clctr = Calculator()

clctr.pregenerate_coordinates(frm=1.0, to=2.0, step=0.1)

coords: list[Coordinate] = clctr.get_coordinates(step_width=1.0, angle=0)

print(coords[50])
