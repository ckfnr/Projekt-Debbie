# from env.func.calculations import calc_coordinate

from math import sin, cos, tan, asin, acos, atan, degrees, radians

num1: float = 5
num2: float = 0.5

for cal in [sin, cos, tan]:
    print(f"{cal.__name__}({num1}) = {cal(radians(num1))}")  # These remain unchanged

for cal in [asin, acos, atan]:
    print(f"{cal.__name__}({num2}) = {degrees(cal(num2))}")  # Convert result to degrees
