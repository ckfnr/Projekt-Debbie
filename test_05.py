import time
from env.func.movement import Movement

m = Movement()

while True:
    while True:
        rf_t = m.leg_right_front.thigh.move(target_angle=120, duration=0.5)
        lb_t = m.leg_left_back.thigh.move(target_angle=80, duration=0.5)
        rf_l = m.leg_right_front.lower_leg.move(target_angle=80, duration=0.5)
        lb_l = m.leg_left_back.lower_leg.move(target_angle=120, duration=0.5)
        rf_t.join()
        lb_t.join()
        rf_l.join()
        lb_l.join()

        rf_t = m.leg_right_front.thigh.move(target_angle=80, duration=0.5)
        lb_t = m.leg_left_back.thigh.move(target_angle=120, duration=0.5)
        time.sleep(1)
        rf_t.join()
        lb_t.join()
        rf_l = m.leg_right_front.lower_leg.move(target_angle=110, duration=0.5)
        lb_l = m.leg_left_back.lower_leg.move(target_angle=80, duration=0.5)
        rf_l.join()
        lb_l.join()