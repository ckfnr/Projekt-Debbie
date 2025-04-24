import math
import time
from env.classes.movement import Movement
from env.classes.Classes import Coordinate
from env.func.calculations import calc_servo_angles

m = Movement()

# Circle parameters
radius = 0.5  # Adjust as needed
center_x = 0.0
center_z = -2.0
steps = 36  # Number of points in the circle

duration_s = 1.0
step_duration = duration_s / steps

for i in range(steps + 1):
    angle = (2 * math.pi / steps) * i  # Angle in radians
    x = center_x + radius * math.cos(angle)
    z = center_z + radius * math.sin(angle)

    print(f"x={x}, y=0.0, z={z}")
    print(calc_servo_angles(coordinate=Coordinate(x=x, y=1.0, z=z)))
    
    m.leg_right_front.set_to_coordinate(coordinate=Coordinate(x=x, y=1.0, z=z), duration_s=step_duration)
    m.leg_right_front.start()
    m.leg_right_front.join()
    time.sleep(step_duration)
