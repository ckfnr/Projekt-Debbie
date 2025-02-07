from env.func.decorators import cached
from env.func.calculations import tan, _rad

@cached
def _tan(num: float) -> float: return tan(_rad(num))
