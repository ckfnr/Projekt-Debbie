from numpy import arange

class Coordinate:
    def __init__(self, x: float, y: float, z: float) -> None:
        """Initialize a 3D coordinate with x, y, and z values.\nUnit: mm"""
        self.x: float = x
        self.y: float = y
        self.z: float = z

    def get_m(self) -> tuple[float, float, float]:  return self.x/1000, self.y/1000, self.z/1000
    def get_dm(self) -> tuple[float, float, float]: return self.x/100, self.y/100, self.z/100
    def get_cm(self) -> tuple[float, float, float]: return self.x*10, self.y*10, self.z*10
    def get_mm(self) -> tuple[float, float, float]: return self.x, self.y, self.z
    
    def update(self, x: float, y: float, z: float) -> None: self.x, self.y, self.z = x, y, z
    def get_xyz(self) -> tuple[float, float, float]: return self.x, self.y, self.z

    def __add__(self, x: float, y: float, z: float) -> tuple[float, float, float]:     return self.x + x, self.y + y, self.z + z
    def __sub__(self, x: float, y: float, z: float) -> tuple[float, float, float]:     return self.x - x, self.y - y, self.z - z
    def __mul__(self, x: float, y: float, z: float) -> tuple[float, float, float]:     return self.x * x, self.y * y, self.z * z
    def __truediv__(self, x: float, y: float, z: float) -> tuple[float, float, float]:
        if x == 0 or y == 0 or z == 0: raise ZeroDivisionError("x, y or z equals 0!")
        return self.x / x, self.y / y, self.z / z

class StepMovement:
    def __init__(self, coordinate_distance: float, leg: int) -> None:
        self.coordinate_distance: float = coordinate_distance
        self.coordinates_x: list[Coordinate] = []
        self.leg: int = leg

    def generate_coordinates_x(self, start: float, end: float) -> None:
        self.coordinates_x = [Coordinate(float(x), 0, 0) for x in arange(start, end + 1, self.coordinate_distance)]
        if end % self.coordinate_distance != 0:
            self.coordinates_x.append(Coordinate(end, 0, 0))

        #ToDo: Add missing coordinates
        #ToDo: Don't forget about the leg index! Not all legs have the same movement!
    
    def __str__(self) -> str: return f"x-coordinates: {[coordinate.get_xyz() for coordinate in self.coordinates_x]}"

# TEST
if __name__ == "__main__":
    step_movement = StepMovement(coordinate_distance=2, leg=1)
    step_movement.generate_coordinates_x(0, 9)
    print(step_movement)
