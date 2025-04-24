import os

line_count: int = 0

for root, _, filenames in os.walk("./"):
    for filename in filenames:
        if not filename.lower().endswith(".py") or "test" in filename.lower(): continue

        with open(os.path.join(root, filename), "r") as file:
            line_count += len([line for line in file.readlines() if line != "\n" and not line.strip().startswith("#")])

print(f"Total lines of code: {line_count:,}")
