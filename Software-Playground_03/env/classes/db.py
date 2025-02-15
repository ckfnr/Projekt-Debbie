import sqlite3

# Classes
from env.classes.Classes import Coordinate

# Config
from env.config import config

class DB:
    def __init__(self) -> None:
        # Connect to the SQLite database
        self.conn = sqlite3.connect(config.db_file)
        self.cur = self.conn.cursor()

    def get_movement(self, step_width: float) -> list[Coordinate]:
        return [Coordinate(coord[0], coord[1], coord[2]) for coord in self.cur.execute("SELECT coords FROM circle WHERE step_width = ?", (step_width,)).fetchone()]
