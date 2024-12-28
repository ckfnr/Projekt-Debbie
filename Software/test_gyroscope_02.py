import time
import math
import os

# Example raw data from your sensor
raw_accel_data = {'x': 0, 'y': 0, 'z': 0}
raw_gyro_data = {'x': 0, 'y': 0, 'z': 0}

# Conversion factors (adjust based on your MPU6050 configuration)
ACCEL_SCALE_FACTOR = 16384.0  # Assuming ±2g range
GYRO_SCALE_FACTOR = 131.0     # Assuming ±250 degrees/sec range
DT = 0.1                     # Sampling interval in seconds (adjust as needed)

# Initialize angles
angle_x = 0.0
angle_y = 0.0
angle_z = 0.0

def read_sensor_data():
    """
    Mock function to simulate reading data from the MPU6050.
    Replace this with actual I2C reads or your sensor library.
    """
    global raw_accel_data, raw_gyro_data
    # Simulate new data here
    raw_accel_data = {'x': 11.3, 'y': 0.0, 'z': 0.2}
    raw_gyro_data = {'x': -2.4, 'y': 0.1, 'z': 0.4}

def calculate_accel_angle(accel_data):
    """
    Calculate tilt angles from accelerometer data.
    Returns angles in degrees.
    """
    ax = accel_data['x'] / ACCEL_SCALE_FACTOR
    ay = accel_data['y'] / ACCEL_SCALE_FACTOR
    az = accel_data['z'] / ACCEL_SCALE_FACTOR

    angle_x = math.degrees(math.atan2(ay, math.sqrt(ax**2 + az**2)))
    angle_y = math.degrees(math.atan2(-ax, math.sqrt(ay**2 + az**2)))

    return angle_x, angle_y

def calculate_gyro_angle(gyro_data, dt):
    """
    Integrate gyroscope data to calculate angles.
    Returns angles in degrees.
    """
    global angle_x, angle_y, angle_z
    gx = gyro_data['x'] / GYRO_SCALE_FACTOR
    gy = gyro_data['y'] / GYRO_SCALE_FACTOR
    gz = gyro_data['z'] / GYRO_SCALE_FACTOR

    angle_x += gx * dt
    angle_y += gy * dt
    angle_z += gz * dt

    return angle_x, angle_y, angle_z

def complementary_filter(accel_angle, gyro_angle, alpha=0.98):
    """
    Fuse accelerometer and gyroscope data using a complementary filter.
    """
    filtered_angle_x = alpha * gyro_angle[0] + (1 - alpha) * accel_angle[0]
    filtered_angle_y = alpha * gyro_angle[1] + (1 - alpha) * accel_angle[1]

    return filtered_angle_x, filtered_angle_y

# Main loop
while True:
    read_sensor_data()

    accel_angle = calculate_accel_angle(raw_accel_data)
    gyro_angle = calculate_gyro_angle(raw_gyro_data, DT)
    fused_angle = complementary_filter(accel_angle, gyro_angle)

    print(f"Accel Angles: {accel_angle}")
    print(f"Gyro Angles: {gyro_angle}")
    print(f"Fused Angles: {fused_angle}")

    time.sleep(DT)

    os.system("clear")