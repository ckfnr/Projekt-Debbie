import re
from typing import Any
from pprint import pprint

movement_file: str = "TEST_movement.mmt"

# Precompiled regex patterns
seconds_pattern = re.compile(r"seconds=(\d+(\.\d+)?)")
vector_pattern = re.compile(r"(\w+): ([\w=,\.\-\s]+)")

# Load and process data in a single loop
instructions: list[dict[str, Any]] = []
current_block: dict[str, Any] = {}

with open(movement_file, "r", encoding="UTF-8") as f:
    for idx, line in enumerate(f, start=1):
        line = line.strip()
        if not line or line.startswith("//"):
            continue  # Skip empty lines and comments

        if not line.endswith(";"):
            raise ValueError(f"Line {idx} must end with ';'! Offending line: {line}")

        line = line.rstrip(";")  # Remove semicolon

        if line == "MOVEMENT-START":
            current_block = {"type": "MOVEMENT", "duration": 0.0, "vectors": {}}

        elif line == "MOVEMENT-JOIN":
            if current_block:
                # Validation checks
                if not isinstance(current_block.get("type"), str) or current_block["type"] != "MOVEMENT":
                    raise ValueError(f"Invalid 'type' in movement block: {current_block}")
                if not isinstance(current_block.get("duration"), float) or current_block["duration"] <= 0:
                    raise ValueError(f"Invalid 'duration' in movement block: {current_block}")
                if not isinstance(current_block.get("vectors"), dict) or len(current_block["vectors"]) != 4 or not all({"x", "y", "z"} == set(i.keys()) for i in current_block["vectors"].values()):
                    raise ValueError(f"Invalid 'vectors' in movement block: {current_block}")
                if {"rf", "rb", "lf", "lb"} != set(current_block["vectors"].keys()):
                    raise ValueError(f"Missing required vector keys in movement block: {current_block['vectors']}")

                instructions.append(current_block)
                current_block = {}

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

            current_block["vectors"][part.strip()] = vector_data

# Final validation for unclosed blocks
if current_block:
    raise ValueError("The last instruction was not parsed successfully! Maybe forgot 'MOVEMENT-JOIN;'?")

print(f"{len(instructions)} instructions parsed")
# pprint(instructions)
