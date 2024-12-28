from mpu6050 import mpu6050  #type:ignore[import-untyped]

sensor = mpu6050(0x68)

accel_data: dict[str, float] = sensor.get_accel_data()
gyro_data: dict[str, float] = sensor.get_gyro_data()

print(f"{"  ".join(key + ": " + str(value) for key, value in accel_data.items())}")
print(f"{"  ".join(key + ": " + str(value) for key, value in gyro_data.items())}")
