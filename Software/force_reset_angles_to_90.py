from env.classes.movement import Movement

m = Movement()

for servo in m.all_servos:
    servo.servo_wrapper.angle = 90  # Set all servos to 90 degrees
