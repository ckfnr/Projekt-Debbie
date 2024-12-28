import smbus 
from time import sleep

# MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT = 0x3B
ACCEL_YOUT = 0x3D
ACCEL_ZOUT = 0x3F

# Initialize I2C bus
bus = smbus.SMBus(1)
Device_Address = 0x68  # MPU6050 device address

def MPU_Init() -> None:
    """Initializes the MPU6050 sensor."""
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)  # Wake up MPU6050
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
    bus.write_byte_data(Device_Address, CONFIG, 0)
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr: int) -> int:
    """Reads raw 16-bit data from the MPU6050 sensor."""
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr + 1)
    
    value = (high << 8) | low  # Combine high and low byte
    
    # Convert to signed value
    if value > 32768:
        value -= 65536
    return value

MPU_Init()

while True:
    # Read raw accelerometer data
    acc_x = read_raw_data(ACCEL_XOUT)
    acc_y = read_raw_data(ACCEL_YOUT)
    acc_z = read_raw_data(ACCEL_ZOUT)

    # Convert to G values
    Ax: float = acc_x / 16384.0
    Ay: float = acc_y / 16384.0
    Az: float = acc_z / 16384.0

    # Calculate the angle (in degrees) using the accelerometer's Y-axis data
    angle_y: float = Ay * 90  # The accelerometer value on the Y-axis corresponds to an angle (e.g., -90 to 90 degrees)
    angle_x: float = Ax * 90  # The accelerometer value on the Y-axis corresponds to an angle (e.g., -90 to 90 degrees)
    angle_z: float = Az * 90  # The accelerometer value on the Y-axis corresponds to an angle (e.g., -90 to 90 degrees)

    # Print the calculated angle
    print(f"Angle-Y: {angle_y:.2f}  Angle-X: {angle_x:.2f}  Angle-Z: {angle_z:.2f}")
    
    sleep(0.1)  # Delay to make the output readable
