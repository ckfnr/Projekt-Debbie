import time
from mpu6050 import mpu6050  #type:ignore[import-untyped]

# Set up the MPU6050 sensor
sensor = mpu6050(0x68)  # 0x68 is the I2C address of the MPU6050

while True:
    accel_data = sensor.get_accel_data()
    gyro_data = sensor.get_gyro_data()
    temp = sensor.get_temp()

    ax = round(accel_data['x'], 2)
    ay = round(accel_data['y'], 2)
    az = round(accel_data['z'], 2)
    gx = round(gyro_data['x'])
    gy = round(gyro_data['y'])
    gz = round(gyro_data['z'])
    tem = round(temp, 2)

    print(f"ax: {ax}\t ay: {ay}\t az: {az}\t gx: {gx}\t gy: {gy}\t gz: {gz}\t Temperature: {tem}°C", end="\r")
    time.sleep(0.2)
