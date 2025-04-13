from env.classes.movement import Movement
from env.classes.Classes import Coordinate

m = Movement()

for leg in m.all_legs:
    # for servo in leg.all_servos:
    #     print(f"Setting servo {servo.leg}:{servo.servo_type} to 90°")
    #     # servo.servo_wrapper.angle = 90
        
    leg.set_to_coordinate(coordinate=Coordinate(x=0.0, y=0.0, z=0.0), duration_s=1.0)

m.start_all_legs()

m.join_all_legs()
