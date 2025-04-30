from adafruit_servokit import Servo  # type:ignore[import-untyped, import-not-found]

# Decorators
from env.decr.decorators import validate_types

# Config
from env.config import config

class ServoWrapper:
    __slots__: tuple[str, str] = ("_servo", "_servo_angle")

    def __init__(self, servo: Servo) -> None:
        self._servo: Servo = servo
        self._servo_angle: int = int(self._servo.angle) if self._servo.angle is not None else config.servo_normal_position

    @property
    def angle(self) -> int:
        return self._servo_angle

    @angle.setter
    def angle(self, new_angle: int) -> None:
        if not isinstance(new_angle, int):
            raise TypeError(f"Angle must be an integer got {type(new_angle)}")
        if not 0 <= new_angle <= 180:
            raise ValueError("Angle must be between 0 and 180 degrees")

        self._servo_angle = new_angle
        self._servo.angle = new_angle

class Coordinate:
    """Coordinate object containing xyz of a coordinate."""
    __slots__: tuple[str, str, str, str] = ("_x", "_y", "_z", "_hash")

    @validate_types
    def __init__(self, x: float, y: float, z: float) -> None:
        """Initialize a 3D coordinate with x, y, and z values.\nUnit: mm"""
        self._x: float = x
        self._y: float = y
        self._z: float = z
        self.set_hash()  # Set the hash value based on the coordinates


    # Coordinate properties
    @property
    def x(self) -> float: return self._x
    @property
    def y(self) -> float: return self._y
    @property
    def z(self) -> float: return self._z

    def get_xyz(self) -> tuple[float, float, float]:        return self.x, self.y, self.z
    def get_avg(self) -> float:                             return round((self.x + self.y + self.z) / 3, 6)
    def get_difference(self, other: "Coordinate") -> float: return ((other.x - self.x)**2 + (other.y - self.y)**2 + (other.z - self.z)**2)


    # Hashing
    def set_hash(self) -> None:
        self._hash = hash((self.x, self.y, self.z))


    # Adding values to xyz
    def add_x(self, value: float) -> None:
        self._x += value
        self.set_hash()

    def add_y(self, value: float) -> None:
        self._y += value
        self.set_hash()
    
    def add_z(self, value: float) -> None:
        self._z += value
        self.set_hash()
    
    def add_xyz(self, x: float, y: float, z: float) -> None:
        self._x, self._y, self._z = self.x + x, self.y + y, self.z + z
        self.set_hash()

    def add_xyz_tuple(self, xyz: tuple[float, float, float]) -> None:
        self._x, self._y, self._z = self.x + xyz[0], self.y + xyz[1], self.z + xyz[2]
        self.set_hash()


    # Debug
    def __str__(self) -> str: 
        return f"x={self.x:.2f}, y={self.y:.2f}, z={self.z:.2f}"
    
    def __repr__(self) -> str:
        return f"Coordinate(x={self.x}, y={self.y}, z={self.z})"
    
    
    # Set and equality
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Coordinate):
            return False
        return (self.x, self.y, self.z) == (other.x, other.y, other.z)

    def __hash__(self) -> int:               
        return self._hash


    # Calculating
    def __add__(self, other: "Coordinate") -> 'Coordinate': return Coordinate(self.x +  other.x, self.y +  other.y, self.z +  other.z)
    def __sub__(self, other: "Coordinate") -> 'Coordinate': return Coordinate(self.x -  other.x, self.y -  other.y, self.z -  other.z)
    def __mul__(self, other: float)        -> 'Coordinate': return Coordinate(self.x *  other,   self.y *  other,   self.z *  other  )
    def __truediv__(self, other: float)    -> 'Coordinate': return Coordinate(self.x /  other,   self.y /  other,   self.z /  other  )
    def __floordiv__(self, other: float)   -> 'Coordinate': return Coordinate(self.x // other,   self.y // other,   self.z // other  )
