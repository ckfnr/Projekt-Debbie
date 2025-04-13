from env.classes.Classes import Coordinate
from env.classes.movement import Movement
from env.func.calculations import calc_servo_angles

m = Movement()

coords: list[Coordinate] = [
    Coordinate(x=-20.0, y=0.0, z=0.0),
    Coordinate(x=-20.0, y=0.0, z=20.0),
    Coordinate(x=20.0, y=0.0, z=20.0),
    Coordinate(x=20.0, y=0.0, z=0.0),
]

while True:
    for coord in coords:
        print(coord)

        print(calc_servo_angles(coordinate=coord))

        m.leg_left_front.set_to_coordinate(coord, 0.5)
        m.leg_left_front.start()
        m.leg_left_front.join()
