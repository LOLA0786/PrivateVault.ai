import sqlite3

DB="intent_graph.db"

def init_db():
    conn=sqlite3.connect(DB)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS intent_graph(
        id INTEGER PRIMARY KEY,
        principal TEXT,
        action TEXT,
        normalized_action TEXT,
        ts DATETIME DEFAULT CURRENT_TIMESTAMP,
        risk INTEGER
    )
    """)

    conn.commit()
    conn.close()
