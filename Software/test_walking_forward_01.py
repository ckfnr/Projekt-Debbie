from env.classes.movement import Movement
from env.classes.Classes import Coordinate

m = Movement()

duration: float = 0.05
duration_single: float = duration / 2
step_width: float = 50.0
max_points: int = 10
angle: int = 0

while True:
    m.leg_right_front.set_to_coordinate(coordinate=Coordinate(x=-step_width/2, y=0.0, z=0.0), duration_s=duration_single)
    m.leg_left_back.set_to_coordinate(coordinate=Coordinate(x=-step_width/2, y=0.0, z=0.0), duration_s=duration_single)
    m.leg_right_front.start()
    m.leg_left_back.start()

    m.leg_left_front.set_circle(step_width=step_width, angle=angle, max_points=max_points, duration=duration_single)
    m.leg_right_back.set_circle(step_width=step_width, angle=angle, max_points=max_points, duration=duration_single)
    m.leg_left_front.start_circle()
    m.leg_right_back.start_circle()
    m.leg_left_front.join_circle()
    m.leg_right_back.join_circle()

    m.leg_right_front.join()
    m.leg_left_back.join()


    m.leg_left_front.set_to_coordinate(coordinate=Coordinate(x=-step_width/2, y=0.0, z=0.0), duration_s=duration_single)
    m.leg_right_back.set_to_coordinate(coordinate=Coordinate(x=-step_width/2, y=0.0, z=0.0), duration_s=duration_single)
    m.leg_left_front.start()
    m.leg_right_back.start()

    m.leg_right_front.set_circle(step_width=step_width, angle=angle, max_points=max_points, duration=duration_single)
    m.leg_left_back.set_circle(step_width=step_width, angle=angle, max_points=max_points, duration=duration_single)
    m.leg_right_front.start_circle()
    m.leg_left_back.start_circle()
    m.leg_right_front.join_circle()
    m.leg_left_back.join_circle()

    m.leg_left_front.join()
    m.leg_right_back.join()
