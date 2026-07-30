import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[4]

DATABASE_NAME = BASE_DIR / "bubble_tea.db"


def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
