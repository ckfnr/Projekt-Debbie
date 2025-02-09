import json
from sqlite3 import Connection, Cursor

# Classes
from env.func.Classes import Coordinate

def store_coordinates(target_coord: Coordinate, coords: list[Coordinate], cur: Cursor) -> None:
    """Store a list of coordinate tuples into the database."""
    # Serialize the list of coordinates to a JSON string
    coords_json = json.dumps([i.get_xyz() for i in coords])

    # Create a new table if it doesn't exist
    cur.execute('''CREATE TABLE IF NOT EXISTS coordinates
                (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_coord TEXT,
                coords TEXT
                )
                ''')

    # Insert the list of coordinates into the table
    cur.execute('''INSERT INTO coordinates (target_coord, coords) VALUES (?, ?)''', (str(target_coord.get_xyz()), coords_json))

def main() -> None:
    conn = Connection("movement.sqlite3")
    cur = conn.cursor()

    target_coord: Coordinate = Coordinate(10, 0, 0)
    # Test movement
    coords: list[Coordinate] = [
        Coordinate(1.0, 2.0, 3.0),
        Coordinate(4.0, 5.0, 6.0),
        Coordinate(7.0, 8.0, 9.0),
        Coordinate(10.0, 11.0, 12.0),
    ]

    store_coordinates(target_coord=target_coord, coords=coords, cur=cur)

    conn.commit()
    conn.close()

if __name__ == "__main__": main()
