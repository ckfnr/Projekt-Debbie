# Classes
from env.classes.Classes import Coordinate
from env.classes.leg import Leg

# Func
from env.func.DEBUG import dprint
from env.func.calculations import calc_circle_coordinates
from env.func.iterator import iterate_with_offset
from env.types.typing import ITER

class Step:
    def __init__(self, angle: int, step_width: float) -> None:
        self._angle: int = angle
        self._step_width: float = step_width
        self._max_points: int = 10
        self._duration: float = 0.05
        self._duration_single: float = self._duration / 2
        
        # Calculate the coordinates for the step
        self._step_coordinates: list[Coordinate] = calc_circle_coordinates(step_width=self._step_width, angle=self._angle, max_points=self._max_points)
        self._coordinate_offset: Coordinate = Coordinate(x=-self._step_width / 2, y=0.0, z=0.0)
        self._step_coordinates = [coord + self._coordinate_offset for coord in self._step_coordinates]
        dprint(f"Step coordinates: {self._step_coordinates}")
    
    def get_step_coordinates(self) -> list[Coordinate]: return self._step_coordinates

    def start_at_nearest_point(self, leg: Leg) -> None:
        """Start the leg at the nearest point."""
        while True:
            for coord in iterate_with_offset(self._step_coordinates, offset=0):
                leg.set_to_coordinate(coordinate=coord, duration_s=self._duration_single)
                leg.start()
                leg.join()