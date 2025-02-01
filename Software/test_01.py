dic: dict[str, dict[str, dict[str, float]]] = {
    'vectors':{
        'rf': {'x': 0.0, 'y': 0.0, 'z': -5.0},
        'rb': {'x': 0.0, 'y': 0.0, 'z': -5.0},
        'lf': {'x': 0.0, 'y': 0.0, 'z': -5.0},
        'lb': {'x': 0.0, 'y': 0.0, 'z': -5.0}
        }
    }

# print([i for i in dic["vectors"].values()])
# print([set(i) for i in dic["vectors"].values()])
# print(any({"x", "y", "z"} != set(i) for i in dic["vectors"].values()))
print(not all({"x", "y", "z"} == set(i.keys()) for i in dic["vectors"].values()))