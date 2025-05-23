from typing import Any


movement_file: str = "TEST_standup.mmt"

# Load data
with open(movement_file, "r", encoding="UTF-8") as f:
    data = f.read()

converted_data: list[str] = [i.strip() for i in data.split("\n") if i and not i.startswith("//")]

# Check if there are any errors in the file
for idx, line in enumerate(converted_data, start=1):
    if not line.endswith(";"):
        raise Exception(f"Line {idx} must end with ';'!")

# Convert to instructions
instructions: list[dict[str, Any]] = []
current_block: dict[str, str | float | dict[str, dict[str, float]]] = {}

for instruction in converted_data:
    instruction = instruction.rstrip(";")  # Remove the trailing semicolon for easier parsing

    if instruction == "MOVEMENT-START":
        current_block = {"type": "MOVEMENT", "duration": 0, "vectors": {}}

    elif instruction == "MOVEMENT-JOIN":
        if current_block:  # Only append if there is an active block
            # Check if any part of the instruction is not ok
            if not isinstance(current_block["type"], str):                  raise ValueError(f"Wrong type for 'type'! Got '{type(current_block["type"])}'; expected 'str'!")
            if not isinstance(current_block["duration"], float):            raise ValueError(f"Wrong type for 'duration'! Got '{type(current_block["duration"])}; expected 'float'!")
            if not isinstance(current_block["vectors"], dict):              raise ValueError(f"Wrong type for 'vectors'! Got '{type(current_block["vectors"])}; expected 'dict'!")
            if current_block["type"] != "MOVEMENT":                         raise ValueError(f"The value for 'type' is not 'MOVEMENT'! Got {current_block["type"]} instead.")
            if current_block["duration"] <= 0:                              raise ValueError(f"Wrong type for 'duration'! Got '{type(current_block["duration"])}; expected 'float'!")
            if len(current_block["vectors"]) != 4:                          raise ValueError(f"Too many values for 'vectors'! Got {len(current_block['vectors'])}; expected 4!")
            if ["rf", "rb", "lf", "lb"] - current_block["vectors"].keys():  raise ValueError(f"Wrong values for 'vectors'! Got '{current_block["vectors"]}'; expected ['rf', 'rb', 'lf', 'lb']!")

            instructions.append(current_block)
            current_block = {}

    elif instruction.startswith("seconds="):
        current_block["duration"] = float(instruction.split("=")[1])

    elif ":" in instruction:
        if not isinstance(current_block["vectors"], dict):
            raise ValueError("Vectors must be a dict!")

        part, coords = instruction.split(": ")
        coord_values = {k: float(v) for k, v in (pair.split("=") for pair in coords.split(", "))}
        current_block["vectors"][part] = coord_values

# Check if the last instruction was parsed successfully
if current_block:
    raise Exception("The last instruction was not parsed successfully! Maybe forgot 'MOVEMENT-JOIN;'?")

print(f"{len(instructions)} instructions parsed")
# for block in instructions:
#     pprint(block)
