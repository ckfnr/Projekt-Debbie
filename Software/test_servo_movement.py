import time
from env.func.movement import Movement

def test_servo_movement() -> None:
    m: Movement = Movement()
    # Test moving the right front thigh servo to various angles
    angles_to_test: list[int] = [90, 40, 120, 150]  # Including an out-of-range angle (150)
    for angle in angles_to_test:
        print(f"Moving servo to angle: {angle}")
        m.leg_right_front.thigh.move(target_angle=angle, duration=1.0)
        time.sleep(2)  # Wait for the movement to complete

if __name__ == "__main__":
    test_servo_movement()
