import time
from env.func.movement import Movement

m = Movement()

while True:
    while True:
        rf_t = m.leg_right_front.thigh.move(target_angle=120, duration=0.5)
        rf_l = m.leg_right_front.lower_leg.move(target_angle=80, duration=0.5)
        rf_t.join()
        m.leg_right_front.thigh.move(target_angle=80, duration=0.5).join()
        time.sleep(1)
        rf_l.join()
        m.leg_right_front.lower_leg.move(target_angle=110, duration=0.5).join()