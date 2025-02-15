from time import sleep
from typing import Iterator, Literal, Any

# Config
from env.config import config

# Func
from env.func.DEBUG import dprint

# Decorators
from env.decr.decorators import validate_types

class Coordinate:
    @validate_types
    def __init__(self, x: float, y: float, z: float) -> None:
        """Initialize a 3D coordinate with x, y, and z values.\nUnit: mm"""
        self.x: float = float(x)
        self.y: float = float(y)
        self.z: float = float(z)

    def get_m(self) -> tuple[float, float, float]:   return self.x/1000, self.y/1000, self.z/1000
    def get_dm(self) -> tuple[float, float, float]:  return self.x/100, self.y/100, self.z/100
    def get_cm(self) -> tuple[float, float, float]:  return self.x*10, self.y*10, self.z*10
    def get_mm(self) -> tuple[float, float, float]:  return self.x, self.y, self.z
    def get_xyz(self) -> tuple[float, float, float]: return self.x, self.y, self.z

    def update(self, x: float, y: float, z: float) -> None: self.x, self.y, self.z = float(x), float(y), float(z)

    def __add__(self, other: 'Coordinate') -> 'Coordinate':     return Coordinate(self.x + other.x, self.y + other.y, self.z + other.z)
    def __sub__(self, other: 'Coordinate') -> 'Coordinate':     return Coordinate(self.x - other.x, self.y - other.y, self.z - other.y)
    def __mul__(self, other: 'Coordinate') -> 'Coordinate':     return Coordinate(self.x * other.x, self.y * other.y, self.z * other.z)
    def __truediv__(self, other: 'Coordinate') -> 'Coordinate': return Coordinate(self.x / other.x, self.y / other.y, self.z / other.z)
    def __iter__(self) -> Iterator:                             return iter([self.x, self.y, self.z])
    def __str__(self) -> str:                                   return f"x={round(self.x, 1)}, y={round(self.y, 1)}, z={round(self.z, 1)}"
    def __repr__(self) -> str:                                  return f"Coordinate(x={self.x}, y={self.y}, z={self.z})"

    # Equality check for comparing coordinates
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Coordinate): raise ValueError("Use a Coordinate instance!")
        return (self.x == other.x and self.y == other.y and self.z == other.z)

    # Hashing method for sets and dicts
    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))
