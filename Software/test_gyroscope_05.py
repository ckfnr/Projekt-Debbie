import time
from env.func.mpu6050 import Gyro

g = Gyro()

while True:
    x: float = g.get_accel_data(axis="x")
    y: float = g.get_accel_data(axis="y")
    z: float = g.get_accel_data(axis="z")

    print(f"x = {x:.2f}  |  y = {y:.2f}  |  z = {z:.2f}", end="\r")
    time.sleep(0.1)
