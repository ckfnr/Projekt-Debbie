from env.classes.movement import Movement
from env.classes.Classes import Coordinate
from env.func.calculations import calc_circle_coordinates, _calc_circle_coordinate

m = Movement()

# coords: list[Coordinate] = calc_circle_coordinates(step_width=80.0, angle=0, max_points=20)

coord: Coordinate = _calc_circle_coordinate(step_width=80.0, angle=0, point=10, max_points=10, smoothness=-0.5)

print(coord)