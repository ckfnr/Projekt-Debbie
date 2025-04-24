from env.classes.movement import Movement
from env.classes.Classes import Coordinate

m = Movement()

m.leg_left_front.set_to_coordinate(coordinate=Coordinate(x=-50.0, y=0.0, z=0.0), duration_s=5.0)
m.leg_left_front.start()
print("1. movement started")

m.interrupt_movements()
print("1. movement interrupted")

m.leg_left_front.set_to_coordinate(coordinate=Coordinate(x=50.0, y=0.0, z=0.0), duration_s=1.0)
m.leg_left_front.start()
print("2. movement started")

m.leg_left_front.join()
print("Movement finished")
