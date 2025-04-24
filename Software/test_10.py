import time
from env.classes.movement import Movement
from env.classes.Classes import Coordinate
from env.func.calculations import calc_circle_coordinates

m = Movement()

coords: list[Coordinate] = calc_circle_coordinates(step_width=80.0, angle=0, max_points=20)
motion_time: float = 1 / 20

while True:
    for coord in coords:
        m.leg_left_front.set_to_coordinate(coordinate=coord+Coordinate(x=-40.0, y=0.0, z=0.0), duration_s=motion_time)  #? Why is there a little delay if the y < 2?
        m.leg_left_front.start()
        m.leg_left_front.join()

    # f1: float = time.time()
    m.leg_left_front.set_to_coordinate(coordinate=Coordinate(x=-40.0, y=0.0, z=0.0), duration_s=0.5)
    m.leg_left_front.start()
    m.leg_left_front.join()
    # print(f"Execution 1 took: {time.time() - f1} s")

    # f2: float = time.time()
    # m.leg_left_front.set_to_coordinate(coordinate=Coordinate(x=0.0, y=40.0, z=0.0), duration_s=0.3)
    # m.leg_left_front.start()
    # m.leg_left_front.join()
    # print(f"Execution 2 took: {time.time() - f2} s")
