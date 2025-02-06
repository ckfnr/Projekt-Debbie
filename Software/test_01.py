from env.func.calculations import calc_coordinate

max_points: int = 50

for i in range(max_points+1):
    print(calc_coordinate(step_width=i, angle=0, max_points=50, point=10))
