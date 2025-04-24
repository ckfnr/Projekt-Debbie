from numpy import arange

# Config
from env.config import config

# Classes
from env.classes.Classes import Coordinate
from env.decr.decorators import validate_types

# Func
from env.func.calculations import calc_circle_coordinates
from env.func.DEBUG import dprint

class Calculator:
    def __init__(self) -> None:
        # Dictionary of stored Coordinates
        # circle_multiplier -> step_width -> angle -> max_points -> list of Coordinates
        self.circle_coords: dict[float, dict[int, list[Coordinate]]] = {}
        self.circle_multiplier: float = config.number_a

    @validate_types
    def _pregenerate_coordinates_by_step_width(self, step_width: float) -> None:
        # Generate circle coordinates for each angle
        for angle in range(360):  # 0 to 359 degrees
            # Create missing keys
            self.circle_coords.setdefault(step_width, {}).setdefault(angle, [])

            circle_coords = calc_circle_coordinates(step_width=step_width, angle=angle)
            self.circle_coords[step_width][angle] = circle_coords
        
    @validate_types
    def pregenerate_coordinates(self, frm: float, to: float, step: float) -> None:
        # Generate circle coordinates for each step width
        for width in arange(frm, to+step, step):
            dprint(f"Pregenerating coordinates for step_width={width:.1f}...")
            self._pregenerate_coordinates_by_step_width(round(width, 1))

        dprint(f"Done! Pregenerated coords from {frm} to {to}.")

    @validate_types
    def get_coordinates(self, step_width: float, angle: int) -> list[Coordinate]:
        if step_width <= 0:       raise ValueError(f"Step width must be greater than 0; got {step_width}.")
        if not (0 <= angle <= 359): raise ValueError(f"Angle must be between 0 and 360 (both included); got {angle}.")
        
        try:
            return self.circle_coords[step_width][angle]
        except KeyError:
            raise KeyError(f"Coordinates for step_width {step_width} with angle {angle} are not pregenerated.")
