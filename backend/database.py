import sqlite3
import datetime

DB = "events.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            label TEXT,
            score REAL,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_event(label, score):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute(
        "INSERT INTO events VALUES (NULL, ?, ?, ?)",
        (label, score, datetime.datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
