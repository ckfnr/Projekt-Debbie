from typing import Iterator

# Func
from env.func.DEBUG import dprint

# Decorators
from env.decr.decorators import validate_types

class Coordinate:
    """Coordinate object containing xyz of a coordinate."""
    # Prevent from making dynamic __dict__
    __slots__: tuple[str, str, str, str] = ("x", "y", "z", "_hash")

    @validate_types
    def __init__(self, x: float, y: float, z: float) -> None:
        """Initialize a 3D coordinate with x, y, and z values.\nUnit: mm"""
        self.x: float = x
        self.y: float = y
        self.z: float = z
        self._hash = hash((self.x, self.y, self.z))

    def get_m(self) -> tuple[float, float, float]:   return self.x/1000, self.y/1000, self.z/1000
    def get_dm(self) -> tuple[float, float, float]:  return self.x/100, self.y/100, self.z/100
    def get_cm(self) -> tuple[float, float, float]:  return self.x*10, self.y*10, self.z*10
    def get_mm(self) -> tuple[float, float, float]:  return self.x, self.y, self.z
    def get_xyz(self) -> tuple[float, float, float]: return self.x, self.y, self.z

    @validate_types
    def update(self, x: float, y: float, z: float) -> None: self.x, self.y, self.z, self._hash = x, y, z, hash((x, y, z))

    @validate_types
    def adjust_x(self, value: float) -> None: self.x += value
    @validate_types
    def adjust_y(self, value: float) -> None: self.y += value
    @validate_types
    def adjust_z(self, value: float) -> None: self.z += value

    def __eq__(self, other: object) -> bool: return (self.x == other.x and self.y == other.y and self.z == other.z) if isinstance(other, Coordinate) else False  # Equality check for comparing coordinates
    def __hash__(self) -> int:               return self._hash                                                                                                   # Hashing method for sets and dicts
