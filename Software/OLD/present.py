from env.func.movement import Movement

movement = Movement()

d: float = 0.5

while True:
    thread_1 = movement.leg_right_front.thigh.move(target_angle=110, duration=d)
    thread_2 = movement.leg_left_front.thigh.move(target_angle=60, duration=d)
    thread_3 = movement.leg_right_back.thigh.move(target_angle=110, duration=d)
    thread_4 = movement.leg_left_back.thigh.move(target_angle=60, duration=d)

    for i in [thread_1, thread_2, thread_3, thread_4]:
        i.join()

    thread_1 = movement.leg_right_front.thigh.move(target_angle=60, duration=d)
    thread_2 = movement.leg_left_front.thigh.move(target_angle=110, duration=d)
    thread_3 = movement.leg_right_back.thigh.move(target_angle=60, duration=d)
    thread_4 = movement.leg_left_back.thigh.move(target_angle=110, duration=d)

    for i in [thread_1, thread_2, thread_3, thread_4]:
        i.join()

    # Move side axis of the right front leg
    movement.leg_right_front.side_axis.move(target_angle=100, duration=0.5)

