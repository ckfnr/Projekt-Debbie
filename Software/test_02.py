from pprint import pprint

# Func
from env.func.mmt_parser import parse_mmt

instructions = parse_mmt("TEST_movement.mmt")

pprint([i for i in instructions])
