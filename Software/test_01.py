from timeit import timeit
from time import time
from env.func.calculations import calc_coordinate

num_tests: int = 100_000

start_time = time()
calc_coordinate(step_width=0, angle=0, max_points=50, point=10)
end_time = time()

print(f"First run took {end_time - start_time} seconds.")

# Wrap the call in a lambda to ensure it's treated as a callable
print(f"The others took {timeit(lambda: calc_coordinate(step_width=0, angle=0, max_points=50, point=10), number=num_tests)} seconds.")
