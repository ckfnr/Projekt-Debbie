from env.classes.movement import Movement
from env.classes.leg import Leg
from env.classes.servos import SServo

m = Movement()

for servo in m.all_servos:
    servo.servo_wrapper.angle = 90  # Set all servos to 90 degrees
