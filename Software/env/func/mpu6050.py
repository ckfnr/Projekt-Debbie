import smbus  #type:ignore

# Config
from env.config import config

class Gyro:
    def __init__(self) -> None:
        # MPU6050 Registers and their Address
        self.PWR_MGMT_1   = 0x6B
        self.SMPLRT_DIV   = 0x19
        self.CONFIG       = 0x1A
        self.GYRO_CONFIG  = 0x1B
        self.INT_ENABLE   = 0x38
        self.ACCEL_XOUT = 0x3B
        self.ACCEL_YOUT = 0x3D
        self.ACCEL_ZOUT = 0x3F

        # Initialize I2C bus
        self.bus = smbus.SMBus(1)
        self.Device_Address = 0x68  # MPU6050 device address

        # Deviations of each axis
        self.deviation_x: float = config.deviation_x
        self.deviation_y: float = config.deviation_y
        self.deviation_z: float = config.deviation_z

        self.mpu_init()

    def mpu_init(self) -> None:
        """Initializes the MPU6050 sensor."""
        self.bus.write_byte_data(self.Device_Address, self.PWR_MGMT_1, 1)  # Wake up MPU6050
        self.bus.write_byte_data(self.Device_Address, self.SMPLRT_DIV, 7)
        self.bus.write_byte_data(self.Device_Address, self.CONFIG, 0)
        self.bus.write_byte_data(self.Device_Address, self.GYRO_CONFIG, 24)
        self.bus.write_byte_data(self.Device_Address, self.INT_ENABLE, 1)
    
    def read_raw_data(self, addr: int) -> int:
        """Reads raw 16-bit data from the MPU6050 sensor."""
        high = self.bus.read_byte_data(self.Device_Address, addr)
        low = self.bus.read_byte_data(self.Device_Address, addr + 1)

        value = (high << 8) | low  # Combine high and low byte

        # Convert to signed value
        if value > 32768:
            value -= 65536
        return value

    def get_accel_data(self, axis: str) -> float:
        """Gets the acceleration data from the MPU6050 sensor."""
        if axis == 'x':
            return self.read_raw_data(self.ACCEL_XOUT) / 16384.0 * 90 + self.deviation_x
        elif axis == 'y':
            return self.read_raw_data(self.ACCEL_YOUT) / 16384.0 * 90 + self.deviation_y
        elif axis == 'z':
            return self.read_raw_data(self.ACCEL_ZOUT) / 16384.0 * 90 + self.deviation_z
        else:
            raise ValueError(f"Axis '{axis}' does not exist! Use 'x', 'y', or 'z' instead.")
