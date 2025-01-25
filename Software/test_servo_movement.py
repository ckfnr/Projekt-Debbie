import time
from env.func.movement import Movement

def test_servo_movement() -> None:
    m: Movement = Movement()
    angles_to_test: list[int] = [40, 120]  # Including an out-of-range angle (120)

    for servo in [m.leg_right_front.thigh,
                  m.leg_left_front.thigh,
                  m.leg_right_back.thigh,
                  m.leg_left_back.thigh]:
        for angle in angles_to_test:
            print(f"Moving servo to angle: {angle}")
            servo.move(target_angle=angle, duration=1.0)
            servo.join()

if __name__ == "__main__":
    test_servo_movement()
