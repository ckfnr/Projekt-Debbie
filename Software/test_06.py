from env.func.movement import Movement

m = Movement()

while True:
    t1 = m.leg_right_front.thigh.move(target_angle=120, duration=0.5)
    t2 = m.leg_right_front.lower_leg.move(target_angle=130, duration=0.5)
    t3 = m.leg_left_front.thigh.move(target_angle=40, duration=0.5)
    t4 = m.leg_left_front.lower_leg.move(target_angle=80, duration=0.5)
    t1.join()
    t2.join()
    t3.join()
    t4.join()

    t1 = m.leg_right_front.thigh.move(target_angle=40, duration=0.5)
    t2 = m.leg_right_front.lower_leg.move(target_angle=80, duration=0.5)
    t3 = m.leg_left_front.thigh.move(target_angle=120, duration=0.5)
    t4 = m.leg_left_front.lower_leg.move(target_angle=130, duration=0.5)
    t1.join()
    t2.join()
    t3.join()
    t4.join()