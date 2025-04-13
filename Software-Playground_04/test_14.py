from env.classes.movement import Movement
from env.classes.Classes import Coordinate

m = Movement()

while True:
    m.set_all_legs(coordinate=Coordinate(x=0.0, y=0.0, z=0.0), duration=0.5)
    m.start_all_legs()
    m.join_all_legs()

    m.set_all_legs(coordinate=Coordinate(x=40.0, y=0.0, z=0.0), duration=0.5)
    m.start_all_legs()
    m.join_all_legs()
