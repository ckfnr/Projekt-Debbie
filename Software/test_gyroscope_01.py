import os
import time
from mpu6050 import mpu6050  #type:ignore[import-untyped]

sensor = mpu6050(0x68)

while True:
    accel_data: dict[str, float] = sensor.get_accel_data()
    gyro_data: dict[str, float] = sensor.get_gyro_data()

    # Print accelerometer data
    print("Accelerometer Data:")
    for key, value in accel_data.items():
        print(f"{key}: {value}")

    # Print gyroscope data
    print("Gyroscope Data:")
    for key, value in gyro_data.items():
        print(f"{key}: {value}")

    time.sleep(0.1)
    os.system("clear")
