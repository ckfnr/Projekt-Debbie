from env.func.movement import Movement

m = Movement()

m.normalize_all_legs()

m.leg_right_front.thigh.set(target_angle=100, duration=0.5)
m.leg_right_front.thigh.start()
m.leg_right_front.thigh.join()