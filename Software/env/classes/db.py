import sqlite3

# Classes
from env.classes.Classes import Coordinate

# Func
from env.func.DEBUG import dprint

# Config
from env.config import config

coord_table: str = """
CREATE TABLE IF NOT EXISTS coordinates(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    step_width REAL,
    angle INTEGER,
    x REAL,
    y REAL,
    z REAL
)
"""

class DB:
    def __init__(self) -> None:
        # Connect to the SQLite database
        self.conn = sqlite3.connect(config.db_file)
        self.cur = self.conn.cursor()

        # Performance optimizations
        self.cur.execute("PRAGMA journal_mode = WAL;")   # Speeds up concurrent access
        self.cur.execute("PRAGMA synchronous = NORMAL;") # Improves read/write speed

        # Initialize the table if it doesn't exist
        self.cur.execute(coord_table)

    def get_coordinates(self, step_width: float, angle: int) -> list[Coordinate]:
        """Get all coordinates for a given step width and angle."""
        dprint(f"Getting coordinates for step width {step_width} and angle {angle}")
        return [Coordinate(x=x, y=y, z=z) for x, y, z in self.cur.execute("SELECT x, y, z FROM coordinates WHERE step_width = ? AND angle = ? ORDER BY id", (step_width, angle)).fetchall()]

    def store_coordinates(self, step_width: float, angle: int, coord: Coordinate) -> None:
        self.cur.execute("INSERT OR IGNORE INTO coordinates (step_width, angle, x, y, z) VALUES (?, ?, ?, ?, ?)", (step_width, angle, round(coord.x, 7), round(coord.y, 7), round(coord.z, 7)))

    def save(self) -> None: self.conn.commit()
