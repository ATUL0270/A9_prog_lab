"""Create (or reset) the SQLite database from schema.sql and seed.sql.

Usage:  python database/init_db.py
"""
import sqlite3
from pathlib import Path

BASE = Path(__file__).resolve().parent
DB_PATH = BASE / "shop.db"


def main():
    schema = (BASE / "schema.sql").read_text(encoding="utf-8")
    seed = (BASE / "seed.sql").read_text(encoding="utf-8")

    conn = sqlite3.connect(DB_PATH)
    try:
        conn.executescript(schema)
        conn.executescript(seed)
        conn.commit()
        count = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    finally:
        conn.close()

    print(f"Database created at {DB_PATH} with {count} products.")


if __name__ == "__main__":
    main()
