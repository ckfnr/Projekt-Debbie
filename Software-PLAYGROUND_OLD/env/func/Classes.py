import ctypes
from typing import Iterator

# Func
from env.func.DEBUG import dprint

class Coordinate:
    #ToDo: Add calculation for each axis (x, y, z)
    #ToDo: Add error handling
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
    def __sub__(self, other: 'Coordinate') -> 'Coordinate':     return Coordinate(self.x - other.x, self.y - other.y, self.z - other.z)
    def __mul__(self, other: 'Coordinate') -> 'Coordinate':     return Coordinate(self.x * other.x, self.y * other.y, self.z * other.z)
    def __truediv__(self, other: 'Coordinate') -> 'Coordinate': return Coordinate(self.x / other.x, self.y / other.y, self.z / other.z)
    def __iter__(self) -> Iterator[float]:                      return iter([self.x, self.y, self.z])
    def __str__(self) -> str:                                   return f"x={round(self.x, 1)}, y={round(self.y, 1)}, z={round(self.z, 1)}"
    def __repr__(self) -> str:                                  return f"Coordinate(x={self.x}, y={self.y}, z={self.z})"

    # Equality check for comparing coordinates
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Coordinate): return False
        return (self.x == other.x and self.y == other.y and self.z == other.z)

    # Hashing method for sets and dicts
    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))
    
class AngleInt:
    def __init__(self, angle: int, deviation: int) -> None:
        self.angle: int = angle
        self.adjusted_angle: int = angle + deviation
        self.deviation: int = deviation

    def conv_to_anglefloat(self) -> 'AngleFloat':             return AngleFloat(angle=float(self.angle), deviation=self.deviation)
    def add_int(self, num: int) -> 'AngleInt':                return AngleInt(angle=self.angle + num, deviation=self.deviation)
    def add_float(self, num: float) -> 'AngleFloat':          return AngleFloat(angle=self.angle + num, deviation=self.deviation)
    def get_original_angle(self) -> int:                      return self.angle
    
    def __str__(self) -> str:                                 return f"angle={self.angle}, adjusted_angle={self.adjusted_angle}, deviation={self.deviation}"
    def __repr__(self) -> str:                                return f"AngleInt(angle={self.angle}, deviation={self.deviation})"
    def __int__(self) -> int:                                 return self.adjusted_angle
    def __float__(self) -> float:                             return float(self.adjusted_angle)
    def __add__(self, other: 'AngleInt') -> 'AngleInt':       return AngleInt(angle=self.angle + other.angle, deviation=self.deviation)
    def __sub__(self, other: 'AngleInt') -> 'AngleInt':       return AngleInt(angle=self.angle - other.angle, deviation=self.deviation)
    def __mul__(self, other: 'AngleInt') -> 'AngleInt':       return AngleInt(angle=self.angle * other.angle, deviation=self.deviation)
    def __truediv__(self, other: 'AngleInt') -> 'AngleFloat': return AngleFloat(angle=self.angle / other.angle, deviation=self.deviation)
    def __le__(self, other: 'AngleInt') -> bool:              return self.adjusted_angle <= other.adjusted_angle
    def __ge__(self, other: 'AngleInt') -> bool:              return self.adjusted_angle >= other.adjusted_angle
    def __eq__(self, other: object) -> bool:                  return self.adjusted_angle == other.adjusted_angle if isinstance(other, type(self)) else False

class AngleFloat:
    def __init__(self, angle: float, deviation: int) -> None:
        self.angle: float = float(angle)
        self.adjusted_angle: float = float(angle + deviation)
        self.deviation: int = deviation

    def round(self, ndigits: int) -> 'AngleFloat':              return AngleFloat(angle=round(self.angle, ndigits), deviation=self.deviation)
    def add_float(self, num: float) -> 'AngleFloat':            return AngleFloat(angle=self.angle + num, deviation=self.deviation)
    
    def __str__(self) -> str:                                   return f"angle={self.angle}, adjusted_angle={self.adjusted_angle}, deviation={self.deviation}"
    def __repr__(self) -> str:                                  return f"AngleFloat(angle={self.angle}, deviation={self.deviation})"
    def __float__(self) -> float:                               return float(self.adjusted_angle)
    def __add__(self, other: 'AngleFloat') -> 'AngleFloat':     return AngleFloat(angle=self.angle + other.angle, deviation=self.deviation)
    def __sub__(self, other: 'AngleFloat') -> 'AngleFloat':     return AngleFloat(angle=self.angle - other.angle, deviation=self.deviation)
    def __mul__(self, other: 'AngleFloat') -> 'AngleFloat':     return AngleFloat(angle=self.angle * other.angle, deviation=self.deviation)
    def __truediv__(self, other: 'AngleFloat') -> 'AngleFloat': return AngleFloat(angle=self.angle / other.angle, deviation=self.deviation)
    def __le__(self, other: 'AngleInt') -> bool:                return self.adjusted_angle <= other.adjusted_angle
    def __ge__(self, other: 'AngleInt') -> bool:                return self.adjusted_angle >= other.adjusted_angle
    def __eq__(self, other: object) -> bool:                    return self.adjusted_angle == other.adjusted_angle if isinstance(other, type(self)) else False

# TEST
if __name__ == "__main__":
    dprint(" | ".join(str(i) for i in set([Coordinate(1, 2, 3), Coordinate(1, 2, 4), Coordinate(1, 2, 3)])))
    dprint(Coordinate(1, 2, 3) * Coordinate(1, 2, 3))
    dprint(Coordinate(1, 2, 3))
