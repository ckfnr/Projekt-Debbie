import re

# Config
from env.config import config

# Classes
from env.func.Classes import Coordinate

def parse_mmt(file_path: str) -> list[dict[str, float | dict[str, Coordinate]]]:
    # Precompiled regex patterns
    seconds_pattern = re.compile(r"seconds=(\d+(\.\d+)?)")
    vector_pattern = re.compile(r"(\w+): ([\w=,\.\-\s]+)")

    # Load and process data in a single loop
    # instructions: list[list[float, dict[str, Coordinate]]] = []
    # current_block: list[float, dict[str, Coordinate]] = []
    instructions: list[dict[str, float | dict[str, Coordinate]]] = []
    current_block: dict[str, float | dict[str, Coordinate]] = {}
    

    with open(file_path, "r", encoding="UTF-8") as f:
        for idx, line in enumerate(f, start=1):
            line = line.strip()
            if not line or line.startswith("//"):
                continue  # Skip empty lines and comments

            if not line.endswith(";"):
                raise ValueError(f"Line {idx} must end with ';'! Offending line: {line}")

            line = line.rstrip(";")  # Remove semicolon

            if line == "MOVEMENT-START":
                # current_block = [0.0, {}]
                current_block = {"duration": 0.0, "coords": {}}

            elif line == "MOVEMENT-JOIN":
                if current_block:
                    # Validation checks
                    if not isinstance(current_block["duration"], float) or current_block["duration"] <= 0:
                        raise ValueError(f"Invalid 'duration' in movement block: {current_block}")
                    if not isinstance(current_block["coords"], dict) or len(current_block["coords"]) != 4:
                        raise ValueError(f"Invalid 'vectors' in movement block: {current_block}")

                    instructions.append(current_block)
                    # current_block = [0.0, {}]
                    current_block = {"duration": 0.0, "coords": {}}

            elif seconds_match := seconds_pattern.match(line):
                current_block["duration"] = float(seconds_match.group(1))

            elif vector_match := vector_pattern.match(line):
                part, coords = vector_match.groups()
                vector_data = {}

                for pair in coords.split(", "):
                    if "=" not in pair:
                        raise ValueError(f"Malformed vector entry at line {idx}: {pair}")

                    k, v = pair.split("=")
                    try:
                        vector_data[k.strip()] = float(v.strip())  # Strip spaces before conversion
                    except ValueError:
                        raise ValueError(f"Invalid float value at line {idx}: '{v.strip()}'")

                if not isinstance(current_block["coords"], dict):
                    raise ValueError(f"Instruction block of 'coords' has type '{type(current_block["coords"])}'; expected 'dict'!")

                current_block["coords"][part.strip()] = Coordinate(vector_data["x"], vector_data["y"], vector_data["z"])

    # Final validation for unclosed blocks
    if current_block != {"duration": 0.0, "coords": {}}:
        raise ValueError(f"The last instruction was not parsed successfully! Maybe forgot 'MOVEMENT-JOIN;'? Last block: {current_block}")

    # return [(instr["duration"], instr["coords"]) for instr in instructions]
    return instructions
