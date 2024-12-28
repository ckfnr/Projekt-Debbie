import time
from mpu6050 import mpu6050  #type:ignore[import-untyped]

sensor = mpu6050(0x68)

accel_data = sensor.get_accel_data()
gyro_data = sensor.get_gyro_data()

print(f"{accel_data = }")
print(f"{gyro_data = }")