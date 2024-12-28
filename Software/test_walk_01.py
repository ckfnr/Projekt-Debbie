from env.func.movement import Movement

m = Movement()

while True:
    m.leg_right_front.thigh.move(target_angle=50, duration=0.3)