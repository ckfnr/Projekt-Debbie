from typing import Optional

# Classes
from env.classes.Classes import Coordinate

# Decorators
from env.decr.decorators import validate_types, cached

# Config
from env.config import config

class Parser:
    @validate_types
    def __init__(self) -> None:
        # self.file_path: str = file_path
        self.instructions: dict[str, list[dict[str, float|Optional[Coordinate]]]] = {}

    def parse_file(self, file_path: str) -> None:
        """Parses the MMT-File."""
        # Skip if file_path is already parsed
        if self.instructions.get(file_path, None): return

        # Reset instructions
        self.instructions[file_path] = []
        current_block: dict[str, float|Optional[Coordinate]] = {}

        # Iterate over all lines in the MMT-File
        with open(file_path, "r", encoding="UTF-8", buffering=1024) as f:
            for idx, line in enumerate(f, start=1):
                adjusted_line: str = line.strip()

                # Skip empty lines and comments
                if not adjusted_line or adjusted_line.startswith("//"): continue

                if adjusted_line == "MOVEMENT-START":  # Start of a new movement
                    current_block = {
                        "duration": 0.0,
                        "rf": None,
                        "rb": None,
                        "lf": None,
                        "lb": None,
                    }
                elif adjusted_line == "MOVEMENT-JOIN":  # End of the movement
                    if not current_block:
                        raise ValueError(f"Line {idx} is not part of a movement.")
                    if not isinstance(current_block["duration"], float) or current_block["duration"] <= 0:
                        raise ValueError(f"Invalid duration in movement, line {idx}! Got '{current_block.get('duration', None)}'; expected a positive number grater than 0.")
                    if not all(isinstance(current_block[leg], Coordinate) for leg in ["rf", "rb", "lf", "lb"]):
                        raise ValueError(f"Invalid leg in movement, line {idx}! Got 'None'; expected a Coordinate object.")
                    
                    # Append the movement to the list of instructions and reset the current block
                    self.instructions[file_path].append(current_block)
                    current_block = {}
                elif wait_match := config.wait_pattern.match(adjusted_line):
                    # Parse wait instruction
                    duration = float(wait_match.group(1))
                    
                    # Use the last movement's leg positions to maintain consistency
                    last_instr = self.instructions[file_path][-1]
                    
                    current_block.update({
                        "duration": duration,
                        "rf": last_instr["rf"],
                        "rb": last_instr["rb"],
                        "lf": last_instr["lf"],
                        "lb": last_instr["lb"],
                    })
                elif duration_match := config.duration_pattern.match(adjusted_line):
                    current_block["duration"] = float(duration_match.group(1))
                elif coords_match := config.coordinate_pattern.match(adjusted_line):
                    part, coords = coords_match.groups()
                    coord_data: dict[str, float] = {}

                    for pair in coords.split(", "):
                        if "=" not in pair:
                            raise ValueError(f"Invalid coordinate pair in line {idx}! Got '{pair}'; expected 'x=...', 'y=...' or 'z=...'.")
                        
                        # Extract the coordinate value and the axis
                        xyz, value = pair.split("=")

                        # Try to add the value to the corresponding coordinate
                        try:               coord_data[xyz.strip()] = float(value.strip())  # Strip spaces before conversion
                        except ValueError: raise ValueError(f"Invalid float value at line {idx}: '{value.strip()}'")

                    # Add the coordinates to the current block
                    current_block[part.strip()] = Coordinate(x=coord_data["x"], y=coord_data["y"], z=coord_data["z"])
        
        # Final validation for unclosed blocks
        if current_block:
            raise ValueError(f"Unclosed movement block at the end of the file. --> {current_block}")
        
    @validate_types
    def parse_files(self, file_paths: list[str]) -> None:
        """Parse all files in the given list of file paths."""
        for file_path in file_paths:
            self.parse_file(file_path)

    @cached
    def get_instructions(self, file_path: str) -> Optional[list[dict[str, float|Optional[Coordinate]]]]:
        return self.instructions.get(file_path, None)
