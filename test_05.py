from pprint import pprint
from env.classes.mmt_parser import Parser

mmt_file: str = "movements/TEST_movement.mmt"

parser = Parser()

parser.parse_file(file_path=mmt_file)

pprint(parser.get_instructions(file_path=mmt_file))
