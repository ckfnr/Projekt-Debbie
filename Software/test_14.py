from env.classes.movement import Movement
from env.classes.Classes import Coordinate

m = Movement()

while True:
    m.set_all_legs(coordinate=Coordinate(x=0.0, y=0.0, z=-20.0), duration=2.0)
    m.start_all_legs()
    m.join_all_legs()

    m.set_all_legs(coordinate=Coordinate(x=0.0, y=0.0, z=40.0), duration=2.0)
    m.start_all_legs()
    m.join_all_legs()
